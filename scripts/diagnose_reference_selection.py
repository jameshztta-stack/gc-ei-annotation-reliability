from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from gcei.bootstrap import _download_source, _verify_source
from gcei.reference_builder import (
    ARTIFACT_NAMES,
    PUBLICATION_SEED,
    _canonical_spectrum,
    _connectivity,
    _load_fixed_id_sets,
    _parse_msp,
    _positive_float,
)

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RECORD_INDEX_SHA256 = "e0760a2a68554fd94f6c64a7a6da45560214926e42e05f1cd26a84ba21cf55b8"


def sha256_indices(selected: dict[str, int]) -> str:
    values = np.asarray([selected[k] for k in sorted(selected)], dtype=np.int64)
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def prepare_clean(source_msp: Path) -> pd.DataFrame:
    parsed = _parse_msp(source_msp)
    normalized = []
    exact_map: dict[tuple, set[str]] = {}
    for record_index, record in enumerate(parsed):
        name = record.get("NAME", "").strip()
        identity = _connectivity(record)
        if not identity or name.upper().strip() in ARTIFACT_NAMES:
            continue
        canonical = _canonical_spectrum(record.get("peaks", []))
        if not canonical:
            continue
        exact_map.setdefault(canonical, set()).add(identity)
        normalized.append({
            "record_index": record_index,
            "connectivity": identity,
            "ri": _positive_float(record.get("RETENTIONINDEX")),
            "canonical": canonical,
        })
    conflicting = {key for key, identities in exact_map.items() if len(identities) > 1}
    seen: set[tuple[str, tuple]] = set()
    clean = []
    for row in normalized:
        canonical = row["canonical"]
        if canonical in conflicting:
            continue
        token = (row["connectivity"], canonical)
        if token in seen:
            continue
        seen.add(token)
        clean.append(row)
    return pd.DataFrame(clean)


def split_candidates(ids_sorted: np.ndarray, ids_seen: np.ndarray):
    out = []
    for label, base in (("sorted", ids_sorted), ("seen", ids_seen)):
        # One RandomState permutation/shuffle, then 40/60 split.
        rng = np.random.RandomState(PUBLICATION_SEED)
        perm = np.asarray(base).copy()
        rng.shuffle(perm)
        out.append((f"{label}:shuffle:cal_first", set(perm[:818]), set(perm[818:]), rng))

        rng = np.random.RandomState(PUBLICATION_SEED)
        perm = rng.permutation(np.asarray(base))
        out.append((f"{label}:permutation:cal_first", set(perm[:818]), set(perm[818:]), rng))

        # Some scripts may have taken 60% test first.
        rng = np.random.RandomState(PUBLICATION_SEED)
        perm = np.asarray(base).copy()
        rng.shuffle(perm)
        out.append((f"{label}:shuffle:test_first", set(perm[1229:]), set(perm[:1229]), rng))
    return out


def build_selected(
    clean_df: pd.DataFrame,
    eligible_order: list[str],
    cal_ids: set[str],
    test_ids: set[str],
    rng: np.random.RandomState,
    iteration: str,
    method: str,
) -> dict[str, int]:
    groups = {k: g["record_index"].astype(int).to_numpy() for k, g in clean_df.groupby("connectivity", sort=False)}
    all_ids_sorted = sorted(groups)
    selected: dict[str, int] = {}
    for identity in all_ids_sorted:
        idx = groups[identity]
        if len(idx) == 1:
            selected[identity] = int(idx[0])

    if iteration == "eligible_order":
        ids = list(eligible_order)
    elif iteration == "sorted":
        ids = sorted(cal_ids | test_ids)
    elif iteration == "seen":
        ids = [x for x in pd.unique(clean_df["connectivity"]) if x in cal_ids or x in test_ids]
    elif iteration == "cal_then_test_sorted":
        ids = sorted(cal_ids) + sorted(test_ids)
    elif iteration == "test_then_cal_sorted":
        ids = sorted(test_ids) + sorted(cal_ids)
    else:
        raise ValueError(iteration)

    for identity in ids:
        idx = groups[identity].copy()
        if method == "shuffle_first":
            rng.shuffle(idx)
            chosen = idx[0]
        elif method == "choice2_first":
            chosen = rng.choice(idx, size=2, replace=False)[0]
        elif method == "choice1":
            chosen = rng.choice(idx, size=1, replace=False)[0]
        elif method == "permutation_first":
            chosen = rng.permutation(idx)[0]
        else:
            raise ValueError(method)
        selected[identity] = int(chosen)
    return selected


def main() -> None:
    cal_fixed, test_fixed = _load_fixed_id_sets(ROOT)
    with tempfile.TemporaryDirectory(prefix="gcei_diag_") as td:
        msp = Path(td) / "source.msp"
        _download_source(msp)
        _verify_source(msp)
        clean_df = prepare_clean(msp)

        counts = clean_df["connectivity"].value_counts()
        eligible = set(counts[counts >= 2].index)
        ids_sorted = np.asarray(sorted(eligible), dtype=object)
        ids_seen = np.asarray([x for x in pd.unique(clean_df["connectivity"]) if x in eligible], dtype=object)

        print(f"clean spectra={len(clean_df)} identities={clean_df['connectivity'].nunique()} eligible={len(eligible)}")
        print(f"fixed split: cal={len(cal_fixed)} test={len(test_fixed)}")

        matching_splits = []
        for label, cal, test, rng_after in split_candidates(ids_sorted, ids_seen):
            ok = cal == cal_fixed and test == test_fixed
            print(f"SPLIT {label}: {'MATCH' if ok else 'no'} cal_overlap={len(cal & cal_fixed)}/818 test_overlap={len(test & test_fixed)}/1229")
            if ok:
                matching_splits.append((label, cal, test, rng_after))

        # Even if no reconstructed split matches, the fixed manifests are authoritative.
        # Test plausible reference-selection RNG states/orderings against the frozen hash.
        split_states = []
        for base_label, base in (("sorted", ids_sorted), ("seen", ids_seen)):
            r = np.random.RandomState(PUBLICATION_SEED)
            shuffled = np.asarray(base).copy(); r.shuffle(shuffled)
            split_states.append((f"after_{base_label}_shuffle", r, list(shuffled)))
            split_states.append((f"fresh_after_{base_label}_shuffle", np.random.RandomState(PUBLICATION_SEED), list(shuffled)))
        split_states.append(("fresh_no_split", np.random.RandomState(PUBLICATION_SEED), list(ids_sorted)))

        found = False
        for state_label, base_rng, eligible_order in split_states:
            for iteration in ("eligible_order", "sorted", "seen", "cal_then_test_sorted", "test_then_cal_sorted"):
                for method in ("shuffle_first", "choice2_first", "choice1", "permutation_first"):
                    rng = np.random.RandomState()
                    rng.set_state(base_rng.get_state())
                    selected = build_selected(clean_df, eligible_order, cal_fixed, test_fixed, rng, iteration, method)
                    digest = sha256_indices(selected)
                    if digest == EXPECTED_RECORD_INDEX_SHA256:
                        print(f"REFERENCE_SELECTION_MATCH state={state_label} iteration={iteration} method={method} sha={digest}")
                        found = True
        if not found:
            print("REFERENCE_SELECTION_MATCH none among enumerated strategies")
            # Print current implementation fingerprint for direct comparison.
            from gcei.reference_builder import _select_reference_indices
            current = _select_reference_indices(clean_df, cal_fixed, test_fixed)
            print(f"CURRENT_SHA256={sha256_indices(current)}")
            print(f"EXPECTED_SHA256={EXPECTED_RECORD_INDEX_SHA256}")
            raise SystemExit(2)


if __name__ == "__main__":
    main()
