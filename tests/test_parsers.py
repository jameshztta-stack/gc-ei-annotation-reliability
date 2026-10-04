import pandas as pd
import pytest

from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv


def test_text_parser_accepts_csv_header():
    peaks = parse_single_spectrum_text("mz,intensity\n41,10\n43,20\n")
    assert peaks == [(41.0, 10.0), (43.0, 20.0)]


def test_text_parser_accepts_common_delimiters_and_comments():
    peaks = parse_single_spectrum_text("# comment\n41 10\n43;20\n93\t100\n")
    assert peaks == [(41.0, 10.0), (43.0, 20.0), (93.0, 100.0)]


def test_text_parser_rejects_empty_or_nonnumeric_input():
    with pytest.raises(ValueError, match="No numeric m/z-intensity pairs"):
        parse_single_spectrum_text("mz,intensity\nfoo,bar\n")


def test_csv_parser_accepts_abundance_alias():
    peaks = read_spectrum_csv(b"mz,abundance\n41,10\n93,100\n")
    assert peaks == [(41, 10), (93, 100)]


def test_csv_parser_rejects_missing_required_columns():
    with pytest.raises(ValueError, match="must contain mz"):
        read_spectrum_csv(b"mass,value\n41,10\n93,100\n")


def test_normalize_merges_rounded_nominal_mass():
    merged, ignored = GCEIEngine._normalize_peaks([(41.1, 2.0), (41.2, 3.0), (43.0, 1.0)], max_mz=100)
    assert merged == {41: 5.0, 43: 1.0}
    assert ignored == 0


def test_nonpositive_and_nonnumeric_intensities_removed():
    merged, ignored = GCEIEngine._normalize_peaks(
        [(41, -1), (42, 0), (43, 10), (44, "bad")],
        max_mz=100,
    )
    assert merged == {43: 10.0}
    assert ignored == 0


def test_normalize_rejects_when_no_valid_positive_peaks_remain():
    with pytest.raises(ValueError, match="No valid positive"):
        GCEIEngine._normalize_peaks([(41, 0), (43, -2), (44, float("nan"))], max_mz=100)


def test_out_of_range_peaks_are_counted_and_valid_peaks_retained():
    merged, ignored = GCEIEngine._normalize_peaks([(41, 10), (101, 20), (-1, 5)], max_mz=100)
    assert merged == {41: 10.0}
    assert ignored == 2


def test_all_out_of_range_peaks_are_rejected():
    with pytest.raises(ValueError, match="No valid positive"):
        GCEIEngine._normalize_peaks([(101, 20), (-1, 5)], max_mz=100)


def test_batch_rejects_missing_required_columns_without_loading_assets():
    engine = object.__new__(GCEIEngine)
    bad = pd.DataFrame({"spectrum_id": ["x"], "mz": [41.0]})
    with pytest.raises(ValueError, match="Batch file is missing columns: intensity"):
        engine.analyze_batch(bad)


def test_invalid_risk_target_is_rejected_before_scoring():
    engine = object.__new__(GCEIEngine)
    with pytest.raises(ValueError, match="risk_target must be 0.10 or 0.05"):
        engine.analyze([(41, 10)], risk_target=0.20)
