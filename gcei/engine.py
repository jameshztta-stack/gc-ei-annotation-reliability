from __future__ import annotations

import csv
import io
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd


@dataclass
class LinearLogisticModel:
    mean: np.ndarray
    scale: np.ndarray
    coef: np.ndarray
    intercept: float

    @classmethod
    def from_json(cls, path: str | Path) -> "LinearLogisticModel":
        obj = json.loads(Path(path).read_text())
        return cls(
            mean=np.asarray(obj["mean"], dtype=float),
            scale=np.asarray(obj["scale"], dtype=float),
            coef=np.asarray(obj["coef"], dtype=float),
            intercept=float(obj["intercept"]),
        )

    def predict_probability(self, features: Sequence[float]) -> float:
        x = np.asarray(features, dtype=float)
        z = (x - self.mean) / self.scale
        eta = float(np.dot(z, self.coef) + self.intercept)
        if eta >= 0:
            return 1.0 / (1.0 + math.exp(-eta))
        e = math.exp(eta)
        return e / (1.0 + e)


def _python_round_mass(value: float) -> int:
    return int(round(float(value)))


def normalize_peaks(peaks: Iterable[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray]:
    merged: dict[int, float] = {}
    for raw_mz, raw_intensity in peaks:
        mz = _python_round_mass(raw_mz)
        intensity = float(raw_intensity)
        if not np.isfinite(intensity) or intensity <= 0:
            continue
        merged[mz] = merged.get(mz, 0.0) + intensity

    if not merged:
        raise ValueError("The spectrum does not contain any positive finite intensity values.")

    masses = np.fromiter(sorted(merged), dtype=int)
    intensities = np.asarray([merged[int(m)] for m in masses], dtype=float)
    return masses, intensities


def vectorize_query(peaks: Iterable[tuple[float, float]], max_mz: int) -> np.ndarray:
    masses, intensities = normalize_peaks(peaks)
    valid = (masses >= 0) & (masses <= max_mz)
    masses = masses[valid]
    intensities = intensities[valid]
    if len(masses) == 0:
        raise ValueError(f"No positive peaks fall inside the publication reference m/z range 0–{max_mz}.")

    vec = np.zeros(max_mz + 1, dtype=float)
    vec[masses] = np.power(masses.astype(float), 1.0) * np.sqrt(intensities)
    norm = float(np.linalg.norm(vec))
    if norm <= 0:
        raise ValueError("The transformed spectrum has zero norm.")
    return vec / norm


def _count_within(scores: np.ndarray, top: float, margin: float) -> int:
    return int(np.sum(scores >= top - margin - 1e-15))


def confidence_features(scores: np.ndarray) -> list[float]:
    if scores.ndim != 1 or len(scores) < 5:
        raise ValueError("At least five candidate scores are required.")
    order = np.argsort(-scores, kind="mergesort")
    top_scores = scores[order[:5]]
    top1 = float(top_scores[0])
    return [
        top1,
        float(top_scores[0] - top_scores[1]),
        float(top_scores[0] - top_scores[4]),
        math.log1p(_count_within(scores, top1, 0.01)),
        math.log1p(_count_within(scores, top1, 0.05)),
    ]


class AnnotationEngine:
    def __init__(
        self,
        reference_matrix: np.ndarray,
        connectivity: np.ndarray,
        names: np.ndarray,
        full_inchikey: np.ndarray,
        reference_ri: np.ndarray,
        record_index: np.ndarray,
        model_ei: LinearLogisticModel,
        model_ri: LinearLogisticModel,
        calibration: dict,
    ) -> None:
        self.reference_matrix = np.asarray(reference_matrix, dtype=float)
        self.connectivity = np.asarray(connectivity).astype(str)
        self.names = np.asarray(names).astype(str)
        self.full_inchikey = np.asarray(full_inchikey).astype(str)
        self.reference_ri = np.asarray(reference_ri, dtype=float)
        self.record_index = np.asarray(record_index, dtype=int)
        self.model_ei = model_ei
        self.model_ri = model_ri
        self.calibration = calibration
        self.max_mz = self.reference_matrix.shape[1] - 1

        if self.reference_matrix.shape[0] != len(self.connectivity):
            raise ValueError("Reference matrix and metadata length do not match.")

    @classmethod
    def from_files(
        cls,
        reference_npz: str | Path,
        metadata_csv: str | Path,
        model_ei_json: str | Path,
        model_ri_json: str | Path,
        calibration_json: str | Path,
    ) -> "AnnotationEngine":
        arrays = np.load(reference_npz, allow_pickle=False)
        meta = pd.read_csv(metadata_csv)
        return cls(
            reference_matrix=arrays["X"],
            connectivity=meta["connectivity"].astype(str).to_numpy(),
            names=meta["name"].fillna("").astype(str).to_numpy(),
            full_inchikey=meta["inchikey"].fillna("").astype(str).to_numpy(),
            reference_ri=pd.to_numeric(meta["ri"], errors="coerce").to_numpy(float),
            record_index=meta["record_index"].astype(int).to_numpy(),
            model_ei=LinearLogisticModel.from_json(model_ei_json),
            model_ri=LinearLogisticModel.from_json(model_ri_json),
            calibration=json.loads(Path(calibration_json).read_text()),
        )

    def _rank(self, scores: np.ndarray, top_n: int | None = None) -> np.ndarray:
        order = np.argsort(-scores, kind="mergesort")
        return order if top_n is None else order[:top_n]

    def annotate(self, peaks: Iterable[tuple[float, float]], query_ri: float | None = None) -> dict:
        query = vectorize_query(peaks, self.max_mz)
        ei_scores = self.reference_matrix @ query

        use_ri = query_ri is not None and np.isfinite(float(query_ri)) and float(query_ri) > 0
        if use_ri:
            delta = np.abs(self.reference_ri - float(query_ri))
            ri_component = np.exp(-0.5 * np.square(delta / 10.0))
            ri_component[~np.isfinite(self.reference_ri) | (self.reference_ri <= 0)] = 0.0
            scores = 0.8 * ei_scores + 0.2 * ri_component
            model = self.model_ri
            margin = float(self.calibration["ri"]["conformal_q90"])
            risk = self.calibration["ri"]["risk_thresholds"]
        else:
            delta = None
            scores = ei_scores
            model = self.model_ei
            margin = float(self.calibration["ei"]["conformal_q90"])
            risk = self.calibration["ei"]["risk_thresholds"]

        order = self._rank(scores)
        top_index = int(order[0])
        top_score = float(scores[top_index])
        features = confidence_features(scores)
        probability = float(model.predict_probability(features))

        candidate_mask = scores >= top_score - margin - 1e-15
        candidate_order = order[candidate_mask[order]]

        def record(idx: int, rank: int) -> dict:
            item = {
                "rank": rank,
                "name": self.names[idx],
                "connectivity": self.connectivity[idx],
                "inchikey": self.full_inchikey[idx],
                "score": float(scores[idx]),
                "ei_similarity": float(ei_scores[idx]),
                "reference_ri": None if not np.isfinite(self.reference_ri[idx]) else float(self.reference_ri[idx]),
            }
            if use_ri and delta is not None:
                item["delta_ri"] = None if not np.isfinite(self.reference_ri[idx]) else float(delta[idx])
            return item

        top10 = [record(int(idx), rank + 1) for rank, idx in enumerate(order[:10])]
        candidate_set = [record(int(idx), rank + 1) for rank, idx in enumerate(candidate_order)]

        threshold_10 = float(risk["target_error_10pct"])
        threshold_05 = float(risk["target_error_05pct"])
        if probability >= threshold_05:
            decision = "Empirically accepted at the 5% target-error operating point"
        elif probability >= threshold_10:
            decision = "Empirically accepted at the 10% target-error operating point"
        else:
            decision = "Review / candidate set / abstain from exact single-candidate annotation"

        top_delta = None
        if use_ri and delta is not None and np.isfinite(delta[top_index]):
            top_delta = float(delta[top_index])

        summary = {
            "mode": "EI+RI" if use_ri else "EI-only",
            "top_candidate_name": self.names[top_index],
            "top_candidate_connectivity": self.connectivity[top_index],
            "top_candidate_inchikey": self.full_inchikey[top_index],
            "top_similarity": top_score,
            "predicted_top1_correctness": probability,
            "candidate_set_size_90": int(len(candidate_order)),
            "decision": decision,
            "query_ri": None if not use_ri else float(query_ri),
            "top_candidate_reference_ri": None if not np.isfinite(self.reference_ri[top_index]) else float(self.reference_ri[top_index]),
            "top_candidate_delta_ri": top_delta,
        }

        return {
            **summary,
            "used_ri": use_ri,
            "top10": top10,
            "candidate_set_90": candidate_set,
            "summary_row": summary,
        }


def parse_peak_text(text: str) -> list[tuple[float, float]]:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise ValueError("No spectrum was supplied.")

    rows = []
    for line in lines:
        normalized = line.replace(";", ",").replace("\t", ",")
        parts = [p.strip() for p in normalized.split(",") if p.strip()]
        if len(parts) < 2:
            parts = line.split()
        if len(parts) < 2:
            continue
        try:
            mz = float(parts[0])
            intensity = float(parts[1])
        except ValueError:
            continue
        rows.append((mz, intensity))

    if not rows:
        raise ValueError("No numeric m/z–intensity pairs could be parsed.")
    return rows


def parse_peak_csv(content: bytes | str) -> list[tuple[float, float]]:
    if isinstance(content, bytes):
        content = content.decode("utf-8-sig")
    df = pd.read_csv(io.StringIO(content))
    lower = {str(c).strip().lower(): c for c in df.columns}
    mz_key = next((lower[k] for k in ("mz", "m/z", "mass") if k in lower), None)
    int_key = next((lower[k] for k in ("intensity", "abundance", "relative_intensity") if k in lower), None)
    if mz_key is None or int_key is None:
        raise ValueError("CSV must contain m/z (or mz/mass) and intensity (or abundance) columns.")
    return list(zip(pd.to_numeric(df[mz_key], errors="coerce"), pd.to_numeric(df[int_key], errors="coerce")))
