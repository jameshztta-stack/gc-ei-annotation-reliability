"""Frozen v2 EI-only library inference. Research evaluation matched first14 source labels.

This is NOT the public v1 engine: separate 8455 reference, float64 m^1 sqrt(I),
12 exact frozen search features and previously development-fit HGB classifier.
No v1 conformal/RI calibration is applied. The 5/10% acceptance *targets*
have FAILED independent certification; no future error guarantee is implied.
"""
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
from scipy import sparse

from .reference_builder import EXPECTED_SHA256, sha256

V2_REFERENCE_SHA256 = "2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01"
V2_HGB_SHA256 = "a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13"
V2_DEVELOPMENT_SHA256 = "67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce"
V2_MAX_MZ = 6420
V2_N_REFERENCE = 8455
V2_FEATURES = (
    "top_score", "top1_minus_top2", "top1_minus_top5",
    "log1p_near_0p01", "log1p_near_0p05", "top1_minus_top10",
    "mean_top5", "std_top10", "log1p_near_0p10", "log1p_query_peaks",
    "query_peak_overlap_with_top1_fraction",
    "query_intensity_share_matched_top1",
)

@dataclass
class V2Result:
    mode: str
    top1: dict
    top10: pd.DataFrame
    confidence: float
    margin: float
    accepted: bool
    decision: str
    risk_target: float
    risk_threshold: float
    warnings: list[str]
    ri_delta_top1: None = None
    conformal90_size: None = None
    conformal90: None = None


def bin_spectrum(peaks: Iterable[tuple[float, float]], max_mz: int = V2_MAX_MZ):
    """Exactly the reference benchmark's integer-mz, SUM positive counts.

    Input may contain decimal m/z; round using Python's original round() rule.
    Source-native MSP preprocessing already produces nominal mass values.
    """
    bins: dict[int, float] = {}
    ignored = 0
    for mz, intensity in peaks:
        try:
            mass = float(mz)
            value = float(intensity)
        except (TypeError, ValueError):
            continue
        if not np.isfinite(mass) or not np.isfinite(value) or value <= 0:
            continue
        mass = int(round(mass))
        if mass < 0 or mass > max_mz:
            ignored += 1
            continue
        bins[mass] = bins.get(mass, 0.0) + value
    if not bins:
        raise ValueError("No valid positive EI peaks within the fixed 0–6420 m/z range.")
    return bins, ignored


def weighted_matrix(raw_records, source_indices):
    """Research v2 exact float64 m^1 sqrt(I) L2 reference construction."""
    rr, cc, vv = [], [], []
    for i, source_row in enumerate(source_indices):
        bins, ignored = bin_spectrum(raw_records[int(source_row)]["peaks"])
        if ignored:
            raise ValueError(f"Frozen v2 source row {source_row} contains out-of-range m/z.")
        for mass, value in bins.items():
            rr.append(i)
            cc.append(mass)
            vv.append(value)
    A = sparse.csr_matrix(
        (np.asarray(vv, dtype=np.float64), (rr, cc)),
        shape=(len(source_indices), V2_MAX_MZ + 1),
        dtype=np.float64,
    )
    A.data = np.sqrt(A.data) * A.indices.astype(np.float64)
    norms = np.sqrt(np.asarray(A.multiply(A).sum(axis=1)).ravel())
    if np.any(norms == 0):
        raise ValueError("A frozen reference source spectrum has zero weighted norm.")
    return (sparse.diags(1.0 / norms) @ A).tocsr()


def query_vector(bins: dict[int, float]):
    mz = np.fromiter(bins.keys(), dtype=np.int32)
    v = np.fromiter(bins.values(), dtype=np.float64)
    vals = np.sqrt(v) * mz.astype(np.float64)
    norm = float(np.linalg.norm(vals))
    if not np.isfinite(norm) or norm <= 0:
        raise ValueError("The input became zero or nonfinite after frozen v2 EI weighting.")
    return sparse.csr_matrix(
        (vals / norm, (np.zeros(len(mz), dtype=np.int32), mz)),
        shape=(1, V2_MAX_MZ + 1),
        dtype=np.float64,
    )


def frozen_features(scores: np.ndarray, bins: dict[int, float], candidate_bins: dict[int, float]):
    """Reconstruct frozen 12 features in the *exact* original fit order.

    Should numerically agree to 1e-11 with source-baseline test vectors.
    Only scores and user-input ion bins are used; no target label is supplied.
    """
    scores = np.asarray(scores, dtype=np.float64)
    if scores.shape != (V2_N_REFERENCE,) or not np.isfinite(scores).all():
        raise ValueError("Invalid v2 similarity vector; no score issued.")
    top = np.sort(np.partition(scores, -10)[-10:])[::-1]
    peak = top[0]
    overlap = set(bins) & set(candidate_bins)
    intensity_total = sum(bins.values())
    features = np.asarray([
        peak,
        peak - top[1],
        peak - top[4],
        np.log1p(np.sum(scores >= peak - 0.01)),
        np.log1p(np.sum(scores >= peak - 0.05)),
        peak - top[9],
        top[:5].mean(),
        top.std(),
        np.log1p(np.sum(scores >= peak - 0.10)),
        np.log1p(len(bins)),
        len(overlap) / len(bins),
        sum(bins[z] for z in overlap) / intensity_total,
    ], dtype=np.float64)
    if features.shape != (12,) or not np.isfinite(features).all():
        raise ValueError("Invalid frozen 12-feature score vector.")
    return features


class GCEIV2Engine:
    """Separate research-v2 model, without borrowing public-v1 calibration."""

    def __init__(self, asset_dir: str | Path, model_path: str | Path):
        asset_dir = Path(asset_dir)
        model_path = Path(model_path)
        if sha256(model_path) != V2_HGB_SHA256:
            raise RuntimeError("Frozen v2 HGB SHA-256 mismatch: refusing unverified model.")
        self.meta = pd.read_csv(asset_dir / "reference_metadata.csv").fillna("")
        self.R = sparse.load_npz(asset_dir / "reference_matrix.npz").tocsr()
        if self.R.shape != (V2_N_REFERENCE, V2_MAX_MZ + 1):
            raise ValueError("Frozen v2 reference matrix has the wrong dimensions.")
        if len(self.meta) != V2_N_REFERENCE:
            raise ValueError("Frozen v2 reference metadata row mismatch.")
        if self.meta["connectivity_id"].nunique() != V2_N_REFERENCE:
            raise ValueError("Frozen v2 reference IDs are not unique.")
        if str(self.R.dtype) != "float64":
            raise ValueError("Frozen v2 numerical matrix must be float64.")
        # This is a trusted release-owned pickle-like object, never a user upload.
        self.model = joblib.load(model_path)
        if type(self.model).__name__ != "HistGradientBoostingClassifier":
            raise ValueError("Unexpected model class.")
        self.original_source_SHA256 = EXPECTED_SHA256

    def analyze(self, peaks, kovats_ri=None, risk_target=0.10, top_n=10):
        if risk_target not in (0.10, 0.05):
            raise ValueError("Use the exact original historical 10% or 5% rule.")
        if kovats_ri is not None:
            raise ValueError(
                "RI fusion was not evaluated/calibrated for frozen research v2. "
                "Choose v1 legacy mode to explore RI with its separate historical model."
            )
        bins, ignored = bin_spectrum(peaks)
        S = np.asarray((query_vector(bins) @ self.R.T).toarray(), dtype=np.float64).ravel()
        if S.shape != (V2_N_REFERENCE,) or not np.isfinite(S).all():
            raise ValueError("Frozen v2 query score computation failed.")
        order = np.argsort(-S, kind="stable")
        winner = int(order[0])
        # Reconstruct original raw ion fractions from the frozen normalized
        # reference only. For overlap proportions, support is invariant to EI
        # mass/sqrt-intensity; zero-mass bins are omitted after m^1 weighting.
        # The original study *includes* nominal m/z=0 as a positive raw bin;
        # store frozen unweighted reference bins in a second NPZ instead.
        if not hasattr(self, "raw_reference"):
            raise RuntimeError("v2 raw source-bin matrix is unavailable; cannot compute audited features.")
        refrow = self.raw_reference.getrow(winner)
        rawbin = {int(i):float(v) for i,v in zip(refrow.indices,refrow.data)}
        features = frozen_features(S, bins, rawbin)
        confidence = float(self.model.predict_proba(features.reshape(1,-1))[0,1])
        if not (0 <= confidence <= 1 and np.isfinite(confidence)):
            raise ValueError("Invalid frozen-HGB confidence.")
        margin = float(features[1])
        threshold = .87 if risk_target == .10 else .94
        accepted = confidence >= threshold and (risk_target == .10 or margin >= .20)

        def make_frame(indices):
            df = self.meta.iloc[list(map(int, indices))].copy()
            df.insert(0, "rank", np.arange(1, len(df)+1))
            df["display_name"] = df["name"].astype(str).map(lambda z:z.split(";")[0].strip())
            df["similarity"] = [float(S[int(k)]) for k in indices]
            return df[["rank","connectivity_id","display_name","name","formula",
                       "similarity","inchi_key","smiles","reference_source_index"]].reset_index(drop=True)

        top = self.meta.iloc[winner].to_dict()
        top["display_name"] = str(top.get("name","")).split(";")[0].strip()
        top["similarity"] = float(S[winner])
        top["reference_source_index"] = int(top["reference_source_index"])
        warnings = [
            "Experimental authentic-standard identity, source acquisition independence and out-of-library "
            "performance are not established.",
            "The v2 HGB score is a historical classifier output; neither 5% nor 10% risk target is certified.",
            "Only database connectivity (InChIKey first14) is represented; stereochemistry and exact analyte "
            "identity require additional evidence.",
        ]
        if ignored:
            warnings.append(f"{ignored} peak(s) outside original m/z 0–6420 were excluded.")

        decision = (
            f"Passes the historical {risk_target:.0%}-target acceptance rule "
            "(NOT a certified error guarantee)."
            if accepted else
            f"Does not pass the historical {risk_target:.0%}-target rule; "
            "report candidates as ambiguous, not as a confirmed identification."
        )
        return V2Result(
            mode="v2 EI-only",top1=top,top10=make_frame(order[:max(1,int(top_n))]),
            confidence=confidence,margin=margin,accepted=bool(accepted),
            decision=decision,risk_target=risk_target,risk_threshold=threshold,
            warnings=warnings
        )

    def set_raw_reference(self, asset_dir):
        self.raw_reference = sparse.load_npz(
            Path(asset_dir) / "raw_reference_bins.npz").tocsr()
        if self.raw_reference.shape != (V2_N_REFERENCE, V2_MAX_MZ + 1):
            raise ValueError("v2 raw reference bin matrix dimensions mismatch.")
        if str(self.raw_reference.dtype) != "float64":
            raise ValueError("v2 raw reference bins must retain float64 intensities.")
        if (self.raw_reference.data <= 0).any():
            raise ValueError("v2 reference contains nonpositive original raw source intensities.")

    def analyze_batch(self, df: pd.DataFrame, risk_target=0.10):
        required={"spectrum_id","mz","intensity"}
        if not required.issubset(df.columns):
            raise ValueError("Batch v2 CSV must include spectrum_id,mz,intensity.")
        if df.empty or df["spectrum_id"].isna().any():
            raise ValueError("Supply a nonempty batch and every spectrum_id.")
        if "ri" in df.columns and df["ri"].notna().any():
            nonempty=df["ri"].dropna().astype(str).str.strip()
            if nonempty.ne("").any():
                raise ValueError(
                    "Kovats RI cannot be integrated with the frozen v2 EI-only model. "
                    "Remove the supplied RI or select historical v1 mode."
                )
        output=[]
        for sid, group in df.groupby("spectrum_id",sort=False):
            r=self.analyze(zip(group["mz"],group["intensity"]),risk_target=risk_target)
            output.append({
              "spectrum_id":sid,"mode":r.mode,
              "top1_name":r.top1.get("display_name",""),
              "top1_formula":r.top1.get("formula",""),
              "top1_connectivity_id":r.top1.get("connectivity_id",""),
              "top_similarity":r.top1.get("similarity",np.nan),
              "historical_HGB_score":r.confidence,
              "top1_top2_cosine_margin":r.margin,
              "target_risk_rule":r.risk_target,
              "historical_acceptance_rule_met":r.accepted,
              "source_independent_risk_certified":False,
              "reference_first14_n":V2_N_REFERENCE,
              "source_msp_sha256":EXPECTED_SHA256,
              "reference_index_sha256":V2_REFERENCE_SHA256,
              "model_sha256":V2_HGB_SHA256,
              "decision":r.decision,
            })
        return pd.DataFrame(output)
