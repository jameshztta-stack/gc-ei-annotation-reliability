from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gcei.bootstrap import ensure_reference_assets
from gcei.engine import AnnotationEngine


def sha256_array(values: np.ndarray) -> str:
    arr = np.ascontiguousarray(values)
    return hashlib.sha256(arr.tobytes()).hexdigest()


def sha256_text(values) -> str:
    return hashlib.sha256("\n".join(map(str, values)).encode()).hexdigest()


EXPECTED_FINGERPRINTS = {
    "n_reference_identities": 8543,
    "matrix_shape": [8543, 588],
    "connectivity_sha256": "6e04de3b1087171241fbc08ec728c14a034ee5a5c32834363164296853f8f559",
    "record_index_sha256": "e0760a2a68554fd94f6c64a7a6da45560214926e42e05f1cd26a84ba21cf55b8",
    "ri_sha256": "d102cfaa41ea6460e46bf8c8d8b541b8b0826615907c15b2ab36603b4c9e2ca4",
    "matrix_sha256": "b298613bef2612d113952a9983ed40b15f736aa0889ca1dd7235dbfb7e5a0f31",
}


def validate_fingerprints(engine: AnnotationEngine) -> list[str]:
    checks = []
    checks.append(f"reference identities = {len(engine.connectivity)}")
    assert len(engine.connectivity) == EXPECTED_FINGERPRINTS["n_reference_identities"]
    assert list(engine.reference_matrix.shape) == EXPECTED_FINGERPRINTS["matrix_shape"]
    assert sha256_text(engine.connectivity) == EXPECTED_FINGERPRINTS["connectivity_sha256"]
    assert sha256_array(engine.record_index.astype(np.int64)) == EXPECTED_FINGERPRINTS["record_index_sha256"]
    assert sha256_array(engine.reference_ri.astype(np.float64)) == EXPECTED_FINGERPRINTS["ri_sha256"]
    assert sha256_array(engine.reference_matrix.astype(np.float32)) == EXPECTED_FINGERPRINTS["matrix_sha256"]
    checks.append("reference fingerprints = PASS")
    return checks


def validate_botanical(engine: AnnotationEngine) -> list[str]:
    input_df = pd.read_csv(ROOT / "examples" / "example_batch_12_botanical.csv")
    expected = pd.read_csv(ROOT / "tests" / "botanical_expected.csv")
    expected_map = expected.set_index("spectrum_id")

    rows = []
    for spectrum_id, group in input_df.groupby("spectrum_id", sort=False):
        peaks = list(zip(group["mz"].astype(float), group["intensity"].astype(float)))
        result = engine.annotate(peaks)
        exp = expected_map.loc[spectrum_id]
        assert result["top_candidate_name"] == exp["top_candidate_name"]
        assert result["top_candidate_connectivity"] == exp["top_candidate_connectivity"]
        assert int(result["candidate_set_size_90"]) == int(exp["candidate_set_size_90"])
        assert abs(result["top_similarity"] - float(exp["top_similarity"])) <= 1e-6
        assert abs(result["predicted_top1_correctness"] - float(exp["predicted_top1_correctness"])) <= 1e-6
        rows.append(spectrum_id)
    return [f"botanical regression = PASS ({len(rows)}/12)"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the public reference assets and validate the frozen publication outputs.")
    parser.add_argument("--msp", type=Path, default=None, help="Exact local publication MSP. If omitted, obtained from the original Zenodo record.")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="gcei_release_validation_") as temp_dir:
        assets = ensure_reference_assets(Path(temp_dir), source_msp=args.msp)
        engine = AnnotationEngine.from_files(
            assets.reference_npz,
            assets.metadata_csv,
            ROOT / "models" / "model_ei.json",
            ROOT / "models" / "model_ri.json",
            ROOT / "models" / "calibration.json",
        )

        messages = []
        messages.extend(validate_fingerprints(engine))
        messages.extend(validate_botanical(engine))
        for message in messages:
            print(message)
        print("FULL RELEASE VALIDATION: PASS")


if __name__ == "__main__":
    main()
