"""Parsing and validation of GC–EI mass-spectrum input files."""
from __future__ import annotations
import io
import re
import pandas as pd

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
