"""Public source checksum verification and MSP parsing."""
from __future__ import annotations
import hashlib
import re
from pathlib import Path

EXPECTED_SHA256 = "a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70"

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

