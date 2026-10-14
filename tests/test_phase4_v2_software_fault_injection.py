"""Predeclared synthetic-only software fault injection; no chemical case labels.

These tests verify code behavior on fabricated numbers and damaged LOCAL COPIES
of exact model/index bytes. They are NOT evidence of EI identification accuracy,
calibration or any certified selective-risk guarantee.
"""
import shutil

import numpy as np
import pandas as pd
import pytest

from gcei import v2_bootstrap
from gcei.v2_engine import (
    GCEIV2Engine, V2_N_REFERENCE, V2_FEATURES,
    bin_spectrum, frozen_features, query_vector,
)


def test_nominal_round_even_and_duplicate_bin_intensity_sum():
    bins, ignored = bin_spectrum([
        (50.4, 4.0), (50.49, 6.0), (50.5, 20.0), (51.0, 1.5)
    ])
    assert bins == {50: 30.0, 51: 1.5}
    assert ignored == 0


def test_invalid_peaks_skipped_out_of_range_counted():
    bins, ignored = bin_spectrum([
        (93, 100), (-1, 5), (6421, 6),
        (float("nan"), 2), (42, -100), ("invalid", 1), (40, 0)
    ])
    assert bins == {93: 100.0}
    assert ignored == 2


@pytest.mark.parametrize("peaks", [
    [], [(42, 0)], [(40, -2)], [(float("nan"), 4)],
    [(999999, 4)], [("invalid", "number")]
])
def test_no_usable_peaks_fail_without_confidence(peaks):
    with pytest.raises(ValueError, match="No valid positive EI peaks"):
        bin_spectrum(peaks)


def test_only_mz_zero_has_invalid_weighted_norm():
    bins, _ = bin_spectrum([(0, 100.0)])
    with pytest.raises(ValueError, match="zero or nonfinite"):
        query_vector(bins)


def test_exact_frozen_feature_count_deterministic_and_shape_guard():
    scores = np.zeros(V2_N_REFERENCE, dtype=np.float64)
    scores[0] = 1.0
    scores[1] = 0.9
    bins = {40: 10.0, 55: 30.0}
    ref = {55: 35.0, 80: 1.0}
    features = frozen_features(scores, bins, ref)
    assert features.shape == (len(V2_FEATURES),) == (12,)
    assert np.isfinite(features).all()
    assert np.array_equal(features, frozen_features(scores, bins, ref))
    assert features[0] == 1.0
    assert abs(features[1] - 0.1) < 1e-12
    assert features[10] == 0.5
    assert features[11] == 0.75
    with pytest.raises(ValueError, match="Invalid v2 similarity vector"):
        frozen_features(scores[:-1], bins, ref)


def test_current_v2_rejects_wrong_risk_target_and_ri_before_inference():
    # A blank uninitialized engine is safe here: invalid requests must reject
    # before touching any fitted estimator, reference or real spectrum.
    engine = GCEIV2Engine.__new__(GCEIV2Engine)
    with pytest.raises(ValueError, match="exact original"):
        engine.analyze([], risk_target=0.11)
    with pytest.raises(ValueError, match="RI fusion"):
        engine.analyze([(40, 100)], kovats_ri=1042.0, risk_target=0.10)


def test_current_v2_batch_required_columns_and_ri_rejected():
    engine = GCEIV2Engine.__new__(GCEIV2Engine)
    with pytest.raises(ValueError, match="spectrum_id,mz,intensity"):
        engine.analyze_batch(pd.DataFrame({"mz": [40], "intensity": [50]}))
    with pytest.raises(ValueError, match="nonempty batch"):
        engine.analyze_batch(pd.DataFrame(columns=["spectrum_id", "mz", "intensity"]))
    with pytest.raises(ValueError, match="cannot be integrated"):
        engine.analyze_batch(pd.DataFrame({
            "spectrum_id": ["synthetic"], "mz": [40],
            "intensity": [50], "ri": [1025.0]
        }))


def test_frozen_index_and_hgb_local_copy_corruption_are_rejected(tmp_path, monkeypatch):
    # Production model remains untouched; corrupt only temporary self-contained
    # copies and verify pre-run checksum rejection independently for EACH file.
    original_index = v2_bootstrap.V2_INDEX
    original_model = v2_bootstrap.V2_HGB
    assert original_index.is_file() and original_model.is_file()
    local_index = tmp_path / "reference_index.csv"
    local_model = tmp_path / "hgb_model.joblib"
    shutil.copyfile(original_index, local_index)
    shutil.copyfile(original_model, local_model)
    monkeypatch.setattr(v2_bootstrap, "V2_INDEX", local_index)
    monkeypatch.setattr(v2_bootstrap, "V2_HGB", local_model)
    v2_bootstrap._verify_v2_pins()
    model_bytes = bytearray(local_model.read_bytes())
    model_bytes[-1] ^= 1
    local_model.write_bytes(model_bytes)
    with pytest.raises(RuntimeError, match="HGB model SHA-256 mismatch"):
        v2_bootstrap._verify_v2_pins()
    shutil.copyfile(original_model, local_model)
    index_bytes = bytearray(local_index.read_bytes())
    index_bytes[-1] ^= 1
    local_index.write_bytes(index_bytes)
    with pytest.raises(RuntimeError, match="reference index SHA-256 mismatch"):
        v2_bootstrap._verify_v2_pins()
