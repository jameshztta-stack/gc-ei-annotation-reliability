from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import sparse

EXPECTED_SHA256 = "a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70"
SPLIT_SEED = 20260925
MASS_POWER = 1.0
INTENSITY_POWER = 0.5


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_msp(path: Path):
    records = []
    rec, peaks, in_peaks = {}, [], False

    def flush():
        nonlocal rec, peaks, in_peaks
        if rec:
            rec["peaks"] = peaks
            rec["_idx"] = len(records)
            records.append(rec)
        rec, peaks, in_peaks = {}, [], False

    with path.open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                if rec:
                    flush()
                continue
            if in_peaks and "\t" in line and not re.match(r"^[A-Za-z][^:]*:", line):
                p = line.split()
                if len(p) >= 2:
                    try:
                        peaks.append((int(round(float(p[0]))), float(p[1])))
                        continue
                    except ValueError:
                        pass
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip().upper()
                rec[k] = v.strip()
                if k == "NUM PEAKS":
                    in_peaks = True
        if rec:
            flush()
    return records


def exact_key(peaks):
    d = defaultdict(float)
    for m, i in peaks:
        d[m] += i
    return tuple(sorted((m, round(i, 8)) for m, i in d.items() if i > 0))


def prepare_library(path: Path):
    raw = parse_msp(path)
    for r in raw:
        r["conn"] = r.get("INCHIKEY", "")[:14]
        try:
            r["ri"] = float(r.get("RETENTIONINDEX", "nan"))
        except ValueError:
            r["ri"] = float("nan")
        r["skey"] = exact_key(r["peaks"])

    groups = defaultdict(list)
    for i, r in enumerate(raw):
        groups[r["skey"]].append(i)
    bad = {k for k, ids in groups.items() if len({raw[i]["conn"] for i in ids}) > 1}
    unique = [raw[ids[0]].copy() for k, ids in groups.items() if k not in bad]
    clean = [r for r in unique if r.get("INCHIKEY") not in ("NA", "Z artifact")]

    by = defaultdict(list)
    for i, r in enumerate(clean):
        by[r["conn"]].append(i)
    conns = list(by.keys())
    return clean, by, conns


def select_reference_spectra(by, conns):
    rng = np.random.default_rng(SPLIT_SEED)
    ref = {}
    for c in conns:
        ids = by[c]
        if len(ids) >= 2:
            p = rng.permutation(ids)[:2]
            ref[c] = int(p[0])
        else:
            ref[c] = ids[0]
    return ref


def raw_matrix(clean, indices, max_mz):
    data, rr, cc = [], [], []
    for row, idx in enumerate(indices):
        d = defaultdict(float)
        for m, i in clean[int(idx)]["peaks"]:
            if i > 0 and 0 <= m <= max_mz:
                d[m] += float(i)
        for m, v in d.items():
            rr.append(row)
            cc.append(m)
            data.append(v)
    return sparse.csr_matrix(
        (np.asarray(data, np.float32), (rr, cc)),
        shape=(len(indices), max_mz + 1),
    )


def transform(M):
    X = M.copy().astype(np.float32)
    X.data = np.power(X.data, INTENSITY_POWER, dtype=np.float32)
    mass = np.arange(X.shape[1], dtype=np.float32)
    X.data *= np.power(mass[X.indices], MASS_POWER, dtype=np.float32)
    n = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
    n[n == 0] = 1
    return (sparse.diags((1 / n).astype(np.float32)) @ X).tocsr()


def build_reference_assets(msp_path: str | Path, out_dir: str | Path):
    msp_path = Path(msp_path)
    out_dir = Path(out_dir)
    if sha256(msp_path) != EXPECTED_SHA256:
        raise ValueError("MSP SHA-256 mismatch. Refusing to build from a different library.")
    out_dir.mkdir(parents=True, exist_ok=True)

    clean, by, conns = prepare_library(msp_path)
    ref = select_reference_spectra(by, conns)
    max_mz = max(m for r in clean for m, i in r["peaks"])
    R = transform(raw_matrix(clean, [ref[c] for c in conns], max_mz))
    refri = np.asarray([clean[ref[c]]["ri"] for c in conns], dtype=float)

    sparse.save_npz(out_dir / "reference_matrix.npz", R, compressed=True)
    np.save(out_dir / "reference_ri.npy", refri)

    fields = ["row", "connectivity_id", "name", "formula", "inchi_key", "smiles", "ri"]
    with (out_dir / "reference_metadata.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row, c in enumerate(conns):
            r = clean[ref[c]]
            w.writerow({
                "row": row,
                "connectivity_id": c,
                "name": r.get("NAME", ""),
                "formula": r.get("FORMULA", ""),
                "inchi_key": r.get("INCHIKEY", ""),
                "smiles": r.get("SMILES", ""),
                "ri": r.get("ri", float("nan")),
            })

    if len(conns) != 8543:
        raise RuntimeError(f"Reference reconstruction produced {len(conns)} identities; expected 8543.")
    if R.shape != (8543, 6421):
        raise RuntimeError(f"Reference reconstruction produced matrix shape {R.shape}; expected (8543, 6421).")

    return {
        "source_sha256": EXPECTED_SHA256,
        "n_reference_identities": len(conns),
        "max_mz": int(max_mz),
        "matrix_shape": tuple(R.shape),
        "matrix_nnz": int(R.nnz),
    }
