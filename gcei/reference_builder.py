from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


ARTIFACT_NAMES = {"AIR", "WATER", "SILOXANE", "COLUMN BLEED", "UNKNOWN"}
PUBLICATION_SEED = 20260925


def _parse_msp(path: Path) -> list[dict]:
    records: list[dict] = []
    current: dict = {}
    peaks: list[tuple[float, float]] = []

    with Path(path).open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                if current:
                    current["peaks"] = peaks
                    records.append(current)
                    current = {}
                    peaks = []
                continue

            if ":" in line and not re.match(r"^[+-]?(?:\d+\.?\d*|\.\d+)\s+", line):
                key, value = line.split(":", 1)
                current[key.strip().upper()] = value.strip()
                continue

            parts = line.replace(",", " ").split()
            if len(parts) >= 2:
                try:
                    peaks.append((float(parts[0]), float(parts[1])))
                except ValueError:
                    pass

    if current:
        current["peaks"] = peaks
        records.append(current)
    return records


def _positive_float(value) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return number if np.isfinite(number) and number > 0 else float("nan")


def _canonical_spectrum(peaks: list[tuple[float, float]]) -> tuple[tuple[int, float], ...]:
    merged: dict[int, float] = {}
    for raw_mz, raw_intensity in peaks:
        intensity = float(raw_intensity)
        if not np.isfinite(intensity) or intensity <= 0:
            continue
        mz = int(round(float(raw_mz)))
        merged[mz] = merged.get(mz, 0.0) + intensity
    return tuple((mz, round(float(merged[mz]), 8)) for mz in sorted(merged))


def _connectivity(record: dict) -> str:
    inchikey = record.get("INCHIKEY", "").strip()
    return inchikey[:14] if len(inchikey) >= 14 else ""


def _load_fixed_id_sets(root: Path) -> tuple[set[str], set[str]]:
    cal = {
        line.strip()
        for line in (root / "docs" / "calibration_connectivity_ids.txt").read_text().splitlines()
        if line.strip()
    }
    test = {
        line.strip()
        for line in (root / "docs" / "test_connectivity_ids.txt").read_text().splitlines()
        if line.strip()
    }
    return cal, test


def _select_reference_indices(rows: pd.DataFrame, calibration_ids: set[str], test_ids: set[str]) -> dict[str, int]:
    by_identity = rows.groupby("connectivity", sort=True)
    rng = np.random.RandomState(PUBLICATION_SEED)
    selected: dict[str, int] = {}

    for identity, group in by_identity:
        indices = group["record_index"].astype(int).to_numpy()
        if len(indices) == 1:
            selected[identity] = int(indices[0])
            continue

        if identity in calibration_ids or identity in test_ids:
            permuted = indices.copy()
            rng.shuffle(permuted)
            selected[identity] = int(permuted[0])
        else:
            selected[identity] = int(indices[0])

    return selected


def build_reference_assets(source_msp: Path, output_npz: Path, output_metadata_csv: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    calibration_ids, test_ids = _load_fixed_id_sets(root)

    parsed = _parse_msp(Path(source_msp))
    normalized = []
    exact_map: dict[tuple, set[str]] = {}

    for record_index, record in enumerate(parsed):
        name = record.get("NAME", "").strip()
        identity = _connectivity(record)
        if not identity:
            continue
        if name.upper().strip() in ARTIFACT_NAMES:
            continue

        canonical = _canonical_spectrum(record.get("peaks", []))
        if not canonical:
            continue
        exact_map.setdefault(canonical, set()).add(identity)
        normalized.append(
            {
                "record_index": record_index,
                "connectivity": identity,
                "inchikey": record.get("INCHIKEY", "").strip(),
                "name": name,
                "ri": _positive_float(record.get("RETENTIONINDEX")),
                "canonical": canonical,
            }
        )

    conflicting = {key for key, identities in exact_map.items() if len(identities) > 1}

    seen_same_identity_exact: set[tuple[str, tuple]] = set()
    clean = []
    for row in normalized:
        canonical = row["canonical"]
        if canonical in conflicting:
            continue
        token = (row["connectivity"], canonical)
        if token in seen_same_identity_exact:
            continue
        seen_same_identity_exact.add(token)
        clean.append(row)

    clean_df = pd.DataFrame(clean)
    selected = _select_reference_indices(clean_df, calibration_ids, test_ids)

    by_index = {int(row["record_index"]): row for row in clean}
    selected_rows = [by_index[index] for _, index in sorted(selected.items())]

    max_mz = max(mz for row in selected_rows for mz, _ in row["canonical"])
    X = np.zeros((len(selected_rows), max_mz + 1), dtype=np.float32)

    metadata = []
    for i, row in enumerate(selected_rows):
        masses = np.asarray([mz for mz, _ in row["canonical"]], dtype=int)
        intensities = np.asarray([value for _, value in row["canonical"]], dtype=float)
        transformed = masses.astype(float) * np.sqrt(intensities)
        X[i, masses] = transformed
        norm = float(np.linalg.norm(X[i]))
        if norm > 0:
            X[i] /= norm
        metadata.append(
            {
                "connectivity": row["connectivity"],
                "inchikey": row["inchikey"],
                "name": row["name"],
                "ri": row["ri"],
                "record_index": int(row["record_index"]),
            }
        )

    output_npz = Path(output_npz)
    output_metadata_csv = Path(output_metadata_csv)
    output_npz.parent.mkdir(parents=True, exist_ok=True)
    output_metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output_npz, X=X)
    pd.DataFrame(metadata).to_csv(output_metadata_csv, index=False)

    if len(metadata) != 8543:
        raise RuntimeError(f"Reference reconstruction produced {len(metadata)} identities; expected 8543.")
