"""Prepare and verify the defined EI reference library and reliability model.

The reference identifiers, model parameters and source checksum are specified
by the published software archive. No training occurs during analysis.
"""
from __future__ import annotations
import csv
import json
import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
from scipy import sparse

from .bootstrap import _download_source
from .reference_builder import EXPECTED_SHA256, parse_msp, sha256
from .v2_engine import (
    V2_N_REFERENCE,V2_MAX_MZ,V2_HGB_SHA256,V2_REFERENCE_SHA256,
    weighted_matrix,bin_spectrum,
)

ROOT=Path(__file__).resolve().parent.parent
MODEL_ASSETS=ROOT/"models/v2"
V2_INDEX=MODEL_ASSETS/"reference_index.csv"
V2_HGB=MODEL_ASSETS/"hgb_model.joblib"
V2_RUNTIME=ROOT/".runtime_assets_v2"
REQUIRED=("reference_matrix.npz","raw_reference_bins.npz",
          "reference_metadata.csv","build_integrity.json")


def _verify_v2_pins():
    if not V2_INDEX.exists() or not V2_HGB.exists():
        raise RuntimeError(
            "The specified v2 index/model artifacts are missing from the deployment. "
            "A different reference or model cannot be substituted."
        )
    if sha256(V2_INDEX)!=V2_REFERENCE_SHA256:
        raise RuntimeError("specified v2 reference index SHA-256 mismatch.")
    if sha256(V2_HGB)!=V2_HGB_SHA256:
        raise RuntimeError("specified v2 HGB model SHA-256 mismatch.")


def _complete(out: Path):
    if not all((out/z).is_file() for z in REQUIRED):
        return False
    try:
        m=json.loads((out/"build_integrity.json").read_text())
        return (
            m["source_sha256"]==EXPECTED_SHA256 and
            m["reference_index_sha256"]==V2_REFERENCE_SHA256 and
            m["model_sha256"]==V2_HGB_SHA256 and
            m["reference_n"]==V2_N_REFERENCE and
            m["max_mz"]==V2_MAX_MZ and
            all(sha256(out/name)==checksum for name,checksum in m["asset_hashes"].items())
        )
    except (OSError,KeyError,ValueError,TypeError,AssertionError):
        return False


def build_v2_reference(msp_path: str | Path,out_dir: str | Path):
    _verify_v2_pins()
    msp_path=Path(msp_path)
    out_dir=Path(out_dir)
    if sha256(msp_path)!=EXPECTED_SHA256:
        raise RuntimeError("Source MS-DIAL MSP SHA-256 mismatch; reject v2 build.")
    with V2_INDEX.open(newline="",encoding="utf-8") as f:
        selected=list(csv.DictReader(f))
    if len(selected)!=V2_N_REFERENCE or \
       len({x["connectivity"] for x in selected})!=V2_N_REFERENCE:
        raise RuntimeError("The reference index is not unique or complete.")
    raw=parse_msp(msp_path)
    if len(raw)!=28220:
        raise RuntimeError("Not the original 28,220 source-spectrum MS-DIAL archive.")
    source_rows=[]
    metadata=[]
    for i,row in enumerate(selected):
        src=int(row["reference_source_index"])
        if src<0 or src>=len(raw):
            raise RuntimeError("specified reference source index out of bounds.")
        conn=row["connectivity"]
        if len(conn)!=14 or not conn.isalpha() or not conn.isupper():
            raise RuntimeError("Invalid specified first14 connectivity label.")
        specimen=raw[src]
        source_rows.append(src)
        metadata.append({
          "row":i,"connectivity_id":conn,
          "reference_source_index":src,
          "name":specimen.get("NAME",""),
          "formula":specimen.get("FORMULA",""),
          "inchi_key":specimen.get("INCHIKEY",""),
          "smiles":specimen.get("SMILES",""),
        })
    if len(set(source_rows))!=V2_N_REFERENCE:
        raise RuntimeError("Duplicate specified v2 reference spectrum source index.")
    R=weighted_matrix(raw,source_rows)

    ii=[];jj=[];vv=[]
    for i,source_index in enumerate(source_rows):
        bins,invalid=bin_spectrum(raw[source_index]["peaks"])
        if invalid:
            raise RuntimeError("specified v2 source spectrum includes out-of-range peaks.")
        for mz,intensity in bins.items():
            ii.append(i);jj.append(mz);vv.append(intensity)
    rawbins=sparse.csr_matrix(
        (np.array(vv,dtype=np.float64),(ii,jj)),
        shape=(V2_N_REFERENCE,V2_MAX_MZ+1),dtype=np.float64)
    if R.shape != rawbins.shape:
        raise RuntimeError("Weighted and raw specified v2 matrix dimensions do not match.")
    if not np.isfinite(R.data).all() or not np.isfinite(rawbins.data).all():
        raise RuntimeError("Nonfinite source matrix data.")
    if np.any(np.sqrt(np.asarray(R.multiply(R).sum(axis=1)).ravel())<=0):
        raise RuntimeError("Nonpositive v2 reference normalized row.")
    out_dir.mkdir(parents=True,exist_ok=True)
    sparse.save_npz(out_dir/"reference_matrix.npz",R,compressed=True)
    sparse.save_npz(out_dir/"raw_reference_bins.npz",rawbins,compressed=True)
    with (out_dir/"reference_metadata.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(metadata[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(metadata)
    assets={name:sha256(out_dir/name) for name in REQUIRED[:-1]}
    build={
      "source_sha256":EXPECTED_SHA256,
      "reference_index_sha256":V2_REFERENCE_SHA256,
      "model_sha256":V2_HGB_SHA256,
      "reference_n":V2_N_REFERENCE,
      "max_mz":V2_MAX_MZ,
      "algorithm":"float64 EI m/z^1 sqrt(I) L2 cosine, stable first-index tie",
      "ri_fusion_supported":False,
      "experimental_source_independence_validated":False,
      "5pct_and_10pct_certified":False,
      "asset_hashes":assets,
    }
    (out_dir/"build_integrity.json").write_text(json.dumps(build,indent=2)+"\n")
    return build


def ensure_v2_assets(dest: str | Path | None=None):
    _verify_v2_pins()
    dest=Path(dest or os.environ.get("GCEI_V2_ASSET_DIR",V2_RUNTIME))
    if _complete(dest):
        return dest
    dest.parent.mkdir(parents=True,exist_ok=True)
    # Build in a sibling and publish only when every hash is valid.
    with tempfile.TemporaryDirectory(prefix=".gcei_v2_build_",dir=dest.parent) as td:
        temp=Path(td)
        provided=os.environ.get("GCEI_MSP_PATH")
        if provided:
            msp=Path(provided).expanduser().resolve()
            if not msp.is_file():
                raise FileNotFoundError("Configured GCEI_MSP_PATH source is missing.")
        else:
            msp=temp/"original_frozen_source.msp"
            _download_source(msp)
        build_v2_reference(msp,temp)
        if not _complete(temp):
            raise RuntimeError("v2 reference builder failed source/hash self-test.")
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True,exist_ok=True)
        for name in REQUIRED:
            shutil.copy2(temp/name,dest/name)
    if not _complete(dest):
        raise RuntimeError("specified v2 deployment assets failed integrity re-check.")
    return dest
