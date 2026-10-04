from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
from scipy import sparse

from gcei.bootstrap import MODELS, ensure_runtime_assets
from gcei.engine import GCEIEngine
from gcei.reference_builder import build_reference_assets

EXPECTED = ROOT / "tests" / "botanical_expected.csv"
BATCH = ROOT / "examples" / "example_batch_12_botanical.csv"

EXPECTED_MATRIX_SCI_HASH = "be75298636574bed4534788fabfc8647566fa27f10377ffe265ebc47a28de976"
EXPECTED_RI_HASH = "01c2017a781362a4354e9e7c94c87caf8e86bf04c972a53ca8279675637f332b"
EXPECTED_METADATA_HASH = "66c1ae7dac23e6dc08ab2a5e07418c9c2de0981e96101574ab6f3eb8ba646068"


def hbytes(*parts: bytes) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.hexdigest()


def matrix_scientific_hash(path: Path) -> str:
    x = sparse.load_npz(path).tocsr()
    return hbytes(
        np.asarray(x.shape, dtype=np.int64).tobytes(),
        x.data.tobytes(),
        x.indices.tobytes(),
        x.indptr.tobytes(),
    )


def canonical_metadata_hash(path: Path) -> str:
    df = pd.read_csv(path, keep_default_na=False)
    payload = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def ri_hash(path: Path) -> str:
    a = np.load(path)
    return hbytes(np.asarray(a.shape, dtype=np.int64).tobytes(), a.tobytes())


def prepare_assets(msp: Path | None, work: Path) -> Path:
    if msp is None:
        return ensure_runtime_assets(work)
    build_reference_assets(msp, work)
    for name in ("calibration.json", "model_ei.json", "model_ri.json"):
        shutil.copy2(MODELS / name, work / name)
    return work


def validate_fingerprints(asset_dir: Path):
    got = {
        "matrix": matrix_scientific_hash(asset_dir / "reference_matrix.npz"),
        "ri": ri_hash(asset_dir / "reference_ri.npy"),
        "metadata": canonical_metadata_hash(asset_dir / "reference_metadata.csv"),
    }
    exp = {
        "matrix": EXPECTED_MATRIX_SCI_HASH,
        "ri": EXPECTED_RI_HASH,
        "metadata": EXPECTED_METADATA_HASH,
    }
    bad = {k: (exp[k], got[k]) for k in exp if exp[k] != got[k]}
    if bad:
        raise AssertionError(f"Reference-asset fingerprint mismatch: {json.dumps(bad, indent=2)}")
    return got


def validate_botanical(asset_dir: Path):
    eng = GCEIEngine(asset_dir)
    batch = pd.read_csv(BATCH)
    observed = eng.analyze_batch(batch, risk_target=0.10).set_index("spectrum_id")
    expected = pd.read_csv(EXPECTED).set_index("spectrum_id")

    failures = []
    for sid, e in expected.iterrows():
        o = observed.loc[sid]
        if str(o["top1_name"]).upper() != str(e["top1_name"]).split(";")[0].strip().upper():
            failures.append(f"{sid}: top1 {o['top1_name']} != {e['top1_name']}")
        if abs(float(o["top_similarity"]) - float(e["top_similarity"])) > 5e-7:
            failures.append(f"{sid}: top similarity mismatch")
        if int(o["conformal90_set_size"]) != int(e["conformal90_set_size"]):
            failures.append(f"{sid}: conformal set size mismatch")
        if abs(float(o["predicted_top1_correctness"]) - float(e["predicted_top1_correctness"])) > 2e-6:
            failures.append(f"{sid}: confidence mismatch")
    if failures:
        raise AssertionError("Botanical regression failed:\n" + "\n".join(failures))
    return len(expected)


def validate_ri_warning_behavior(asset_dir: Path):
    eng = GCEIEngine(asset_dir)
    batch = pd.read_csv(BATCH)
    g = batch.loc[batch["spectrum_id"] == "CdeL_P02"]
    r = eng.analyze(zip(g["mz"], g["intensity"]), kovats_ri=1200.0, risk_target=0.10)
    warnings = "\n".join(r.warnings)
    if r.top1.get("display_name", "").strip().lower() != "sabinene hydrate acetate (cis-)":
        raise AssertionError(f"Unexpected RI-assisted top candidate in warning regression: {r.top1.get('display_name')}")
    if "RI-assisted ranking changed the EI-only top candidate from ALPHA-PINENE" not in warnings:
        raise AssertionError("Missing warning that RI changed the EI-only top candidate.")
    if "EI-only top candidate (ALPHA-PINENE) has ΔRI > 50" not in warnings:
        raise AssertionError("Missing large-ΔRI warning for the EI-only top candidate.")
    if abs(float(r.ri_delta_top1) - 6.0) > 1e-9:
        raise AssertionError(f"Unexpected RI-assisted top-candidate ΔRI: {r.ri_delta_top1}")
    return {
        "ri_test_top1": r.top1.get("display_name", ""),
        "ri_test_top1_delta": r.ri_delta_top1,
        "warning_count": len(r.warnings),
    }


def main():
    p = argparse.ArgumentParser(description="Rebuild the publication reference library and validate frozen v1.1 outputs.")
    p.add_argument("--msp", type=Path, help="Optional exact local publication MSP. If omitted, use official Zenodo runtime bootstrap.")
    p.add_argument("--keep-assets", type=Path, help="Optional directory in which to keep built runtime assets.")
    a = p.parse_args()

    if a.keep_assets:
        a.keep_assets.mkdir(parents=True, exist_ok=True)
        asset_dir = prepare_assets(a.msp, a.keep_assets)
        fingerprints = validate_fingerprints(asset_dir)
        n = validate_botanical(asset_dir)
        ri_warning = validate_ri_warning_behavior(asset_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="gcei_release_validation_") as td:
            asset_dir = prepare_assets(a.msp, Path(td))
            fingerprints = validate_fingerprints(asset_dir)
            n = validate_botanical(asset_dir)
            ri_warning = validate_ri_warning_behavior(asset_dir)

    print("PASS: v1.1 scientific reproducibility validation")
    print(json.dumps({
        "reference_fingerprints": fingerprints,
        "botanical_spectra_checked": n,
        "ri_warning_regression": ri_warning,
    }, indent=2))


if __name__ == "__main__":
    main()
