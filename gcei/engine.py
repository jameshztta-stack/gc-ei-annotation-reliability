from __future__ import annotations

import io
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import sparse


@dataclass
class AnalysisResult:
    mode: str
    top1: dict
    confidence: float
    conformal90_size: int
    conformal90: pd.DataFrame
    top10: pd.DataFrame
    decision: str
    risk_target: float
    risk_threshold: float
    ri_delta_top1: float | None
    warnings: list[str]


class GCEIEngine:
    """Frozen inference engine derived from the publication v1.1 workflow."""

    @staticmethod
    def _display_name(name: str) -> str:
        return str(name).split(";")[0].strip()

    def __init__(self, asset_dir: str | Path):
        self.asset_dir = Path(asset_dir)
        self.cal = json.loads((self.asset_dir / "calibration.json").read_text())
        self.R = sparse.load_npz(self.asset_dir / "reference_matrix.npz").tocsr()
        self.meta = pd.read_csv(self.asset_dir / "reference_metadata.csv").fillna("")
        self.ref_ri = np.load(self.asset_dir / "reference_ri.npy")
        self.model_ei = json.loads((self.asset_dir / "model_ei.json").read_text())
        self.model_ri = json.loads((self.asset_dir / "model_ri.json").read_text())
        self.max_mz = int(self.cal["max_mz"])
        if len(self.meta) != self.R.shape[0]:
            raise ValueError("Reference metadata and matrix row counts do not match.")
        if self.R.shape != (8543, self.max_mz + 1):
            raise ValueError(f"Unexpected reference-matrix shape: {self.R.shape}.")

    @staticmethod
    def _normalize_peaks(peaks: Iterable[tuple[float, float]], max_mz: int):
        accum: dict[int, float] = {}
        ignored = 0
        for mz, intensity in peaks:
            try:
                mz = float(mz)
                intensity = float(intensity)
            except (TypeError, ValueError):
                continue
            if not np.isfinite(mz) or not np.isfinite(intensity) or intensity <= 0:
                continue
            m = int(round(mz))
            if m < 0 or m > max_mz:
                ignored += 1
                continue
            accum[m] = accum.get(m, 0.0) + intensity
        if not accum:
            raise ValueError("No valid positive m/z-intensity peaks were found.")
        return accum, ignored

    def _query_vector(self, peaks):
        d, ignored = self._normalize_peaks(peaks, self.max_mz)
        cols = np.fromiter(d.keys(), dtype=int)
        vals = np.fromiter(d.values(), dtype=np.float32)
        M = sparse.csr_matrix((vals, (np.zeros(len(cols), dtype=int), cols)), shape=(1, self.max_mz + 1))
        X = M.astype(np.float32)
        X.data = np.power(X.data, float(self.cal["intensity_power"]), dtype=np.float32)
        mass = np.arange(X.shape[1], dtype=np.float32)
        X.data *= np.power(mass[X.indices], float(self.cal["mass_power"]), dtype=np.float32)
        norm = float(np.sqrt(X.multiply(X).sum()))
        if norm == 0:
            raise ValueError("Spectrum became zero after transformation.")
        return (X / norm).tocsr(), ignored

    @staticmethod
    def _features(S: np.ndarray) -> np.ndarray:
        p = np.partition(S, -5, axis=1)[:, -5:]
        s = np.sort(p, axis=1)[:, ::-1]
        top = s[:, 0]
        return np.c_[
            top,
            top - s[:, 1],
            top - s[:, 4],
            np.log1p(np.sum(S >= top[:, None] - 0.01, axis=1)),
            np.log1p(np.sum(S >= top[:, None] - 0.05, axis=1)),
        ]

    @staticmethod
    def _predict_probability(X: np.ndarray, model: dict) -> float:
        mean = np.asarray(model["scaler_mean"], dtype=float)
        scale = np.asarray(model["scaler_scale"], dtype=float)
        coef = np.asarray(model["logistic_coef"], dtype=float)
        intercept = float(model["logistic_intercept"])
        z = ((X[0] - mean) / scale) @ coef + intercept
        if z >= 0:
            p = 1.0 / (1.0 + math.exp(-float(z)))
        else:
            ez = math.exp(float(z))
            p = ez / (1.0 + ez)
        return float(p)

    def analyze(self, peaks, kovats_ri: float | None = None, risk_target: float = 0.10, top_n: int = 10) -> AnalysisResult:
        if risk_target not in (0.10, 0.05):
            raise ValueError("risk_target must be 0.10 or 0.05")
        X, ignored = self._query_vector(peaks)
        ei = (X @ self.R.T).toarray().astype(np.float32)
        ei_order = np.argsort(-ei[0], kind="stable")
        ei_top_idx = int(ei_order[0])
        warnings = []
        if ignored:
            warnings.append(f"{ignored} peak(s) outside the reference m/z range were ignored.")

        use_ri = kovats_ri is not None and np.isfinite(float(kovats_ri)) and float(kovats_ri) > 0
        if use_ri:
            qri = float(kovats_ri)
            ri_term = np.zeros_like(ei, dtype=np.float32)
            valid = np.isfinite(self.ref_ri) & (self.ref_ri > 0)
            d = qri - self.ref_ri[valid]
            ri_term[:, valid] = np.exp(-0.5 * (d / float(self.cal["ri_sigma"])) ** 2).astype(np.float32)
            S = (1 - float(self.cal["ri_weight"])) * ei + float(self.cal["ri_weight"]) * ri_term
            q90 = float(self.cal["ri_conformal_margin_90_ideal"])
            model = self.model_ri
            mode = "EI+RI"
            warnings.append("RI-assisted output uses the study's ideal same-database RI calibration. Interpret only when the experimental Kovats RI is chromatographically compatible with the reference system.")
        else:
            S = ei
            q90 = float(self.cal["ei_conformal_margin_90"])
            model = self.model_ei
            mode = "EI-only"

        score = S[0]
        order = np.argsort(-score, kind="stable")
        top_idx = int(order[0])
        top_score = float(score[top_idx])
        prob = self._predict_probability(self._features(S), model)
        threshold = float(model["empirical_risk_thresholds"][f"{risk_target:.2f}"])

        mask = score >= top_score - q90 - 1e-8
        set_idx = np.flatnonzero(mask)
        set_idx = set_idx[np.argsort(-score[set_idx], kind="stable")]

        def frame(indices):
            df = self.meta.iloc[list(map(int, indices))].copy()
            df.insert(0, "rank", np.arange(1, len(df) + 1))
            df["display_name"] = df["name"].map(self._display_name)
            df["similarity"] = [float(score[int(i)]) for i in indices]
            cols = ["rank", "connectivity_id", "display_name", "name", "formula", "similarity", "ri", "inchi_key", "smiles"]
            return df[cols].reset_index(drop=True)

        top10 = frame(order[: max(1, int(top_n))])
        cset = frame(set_idx)
        top = self.meta.iloc[top_idx].to_dict()
        top["display_name"] = self._display_name(top.get("name", ""))
        top["similarity"] = top_score

        ri_delta = None
        if use_ri:
            if top_idx != ei_top_idx:
                ei_name = self._display_name(self.meta.iloc[ei_top_idx].get("name", ""))
                ri_name = self._display_name(self.meta.iloc[top_idx].get("name", ""))
                warnings.append(
                    f"RI-assisted ranking changed the EI-only top candidate from {ei_name} to {ri_name}. "
                    "RI evidence materially changed the ranking; verify chromatographic comparability before relying on the RI-assisted top hit."
                )
                try:
                    ei_rr = float(self.ref_ri[ei_top_idx])
                    if np.isfinite(ei_rr) and ei_rr > 0:
                        ei_delta = abs(float(kovats_ri) - ei_rr)
                        if ei_delta > 50:
                            warnings.append(
                                f"The EI-only top candidate ({ei_name}) has ΔRI > 50 relative to the supplied RI. "
                                "In the study, large RI disagreement could reduce retrieval accuracy."
                            )
                        elif ei_delta > 20:
                            warnings.append(
                                f"The EI-only top candidate ({ei_name}) has ΔRI > 20 relative to the supplied RI. "
                                "The study showed that RI benefit diminished around this level of disagreement."
                            )
                except Exception:
                    pass
            try:
                rr = float(self.ref_ri[top_idx])
                if np.isfinite(rr) and rr > 0:
                    ri_delta = abs(float(kovats_ri) - rr)
                    if ri_delta > 50:
                        warnings.append("Top candidate has ΔRI > 50. In the study, large RI disagreement could reduce retrieval accuracy.")
                    elif ri_delta > 20:
                        warnings.append("Top candidate has ΔRI > 20. The study showed that RI benefit diminished around this level of disagreement.")
            except Exception:
                pass

        if prob >= threshold:
            decision = f"Top candidate passes the empirical {int(risk_target*100)}% target-error operating point for {mode}. Report only as a library-based tentative annotation unless stronger orthogonal confirmation is available."
        else:
            decision = f"Do not accept the top hit as a single-candidate annotation under the empirical {int(risk_target*100)}% target-error operating point. Review/report the calibrated candidate set or obtain additional evidence."

        return AnalysisResult(
            mode=mode,
            top1=top,
            confidence=prob,
            conformal90_size=int(mask.sum()),
            conformal90=cset,
            top10=top10,
            decision=decision,
            risk_target=risk_target,
            risk_threshold=threshold,
            ri_delta_top1=ri_delta,
            warnings=warnings,
        )

    def analyze_batch(self, df: pd.DataFrame, risk_target: float = 0.10) -> pd.DataFrame:
        required = {"spectrum_id", "mz", "intensity"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Batch file is missing columns: {', '.join(sorted(missing))}")
        out = []
        for sid, g in df.groupby("spectrum_id", sort=False):
            ri = None
            if "ri" in g.columns:
                vals = pd.to_numeric(g["ri"], errors="coerce").dropna()
                if len(vals):
                    ri = float(vals.iloc[0])
            r = self.analyze(zip(g["mz"], g["intensity"]), kovats_ri=ri, risk_target=risk_target)
            out.append({
                "spectrum_id": sid,
                "mode": r.mode,
                "top1_name": r.top1.get("display_name", r.top1.get("name", "")),
                "top1_formula": r.top1.get("formula", ""),
                "top1_connectivity_id": r.top1.get("connectivity_id", ""),
                "top_similarity": r.top1.get("similarity", np.nan),
                "predicted_top1_correctness": r.confidence,
                "conformal90_set_size": r.conformal90_size,
                "risk_target": r.risk_target,
                "passes_empirical_operating_point": bool(r.confidence >= r.risk_threshold),
                "ri_delta_top1": r.ri_delta_top1,
                "decision": r.decision,
            })
        return pd.DataFrame(out)


def parse_single_spectrum_text(text: str) -> list[tuple[float, float]]:
    peaks = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p for p in re.split(r"[,;\t ]+", line) if p]
        if len(parts) < 2:
            continue
        try:
            peaks.append((float(parts[0]), float(parts[1])))
        except ValueError:
            continue
    if not peaks:
        raise ValueError("No numeric m/z-intensity pairs could be parsed.")
    return peaks


def read_spectrum_csv(data: bytes | str) -> list[tuple[float, float]]:
    if isinstance(data, bytes):
        data = data.decode("utf-8-sig", errors="replace")
    df = pd.read_csv(io.StringIO(data))
    cols = {c.lower().strip(): c for c in df.columns}
    mz_col = cols.get("mz") or cols.get("m/z")
    i_col = cols.get("intensity") or cols.get("abundance") or cols.get("abund")
    if mz_col is None or i_col is None:
        raise ValueError("Single-spectrum CSV must contain mz (or m/z) and intensity (or abundance) columns.")
    return list(zip(df[mz_col], df[i_col]))
