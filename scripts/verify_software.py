"""Verify the published model and reference, and optionally reproduce example analysis.

Run "python scripts/verify_software.py" to verify the repository assets.
Run "python scripts/verify_software.py --examples" to obtain the MS-DIAL
source and test the twelve supplied example spectra with the current model.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

INDEX_SHA = "2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01"
MODEL_SHA = "a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13"


def verify_assets():
    for filename, expected in [
        ("models/v2/reference_index.csv", INDEX_SHA),
        ("models/v2/hgb_model.joblib", MODEL_SHA),
    ]:
        observed=hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
        if observed!=expected:
            raise RuntimeError(f"Checksum mismatch: {filename}")
        print(f"Verified: {filename}")


def verify_examples():
    import pandas as pd
    from gcei.v2_bootstrap import ensure_v2_assets,V2_HGB
    from gcei.v2_engine import GCEIV2Engine
    e=GCEIV2Engine(ensure_v2_assets(),V2_HGB)
    examples=pd.read_csv(ROOT / "examples/example_batch_12_botanical.csv")
    out=e.analyze_batch(examples)
    assert len(out)==12 and out.spectrum_id.nunique()==12
    for sid,group in examples.groupby("spectrum_id",sort=False):
        r=e.analyze(zip(group.mz,group.intensity))
        row=out.set_index("spectrum_id").loc[sid]
        assert row.top1_connectivity_id == r.top1["connectivity_id"]
        assert abs(float(row.top_similarity)-float(r.top1["similarity"])) < 1e-12
        assert len(r.top10)==10
    print("Verified 12 example spectra, single/batch result consistency and ten candidates each.")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--examples",action="store_true",help="Rebuild source-dependent assets and check twelve examples.")
    args=parser.parse_args()
    verify_assets()
    if args.examples:
        verify_examples()
