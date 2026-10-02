from gcei.engine import normalize_peaks, parse_peak_text


def test_parse_peak_text_accepts_csv_header():
    peaks = parse_peak_text("mz,intensity\n41,10\n43,20\n")
    assert peaks == [(41.0, 10.0), (43.0, 20.0)]


def test_normalize_merges_rounded_nominal_mass():
    masses, intensities = normalize_peaks([(41.1, 2.0), (41.2, 3.0), (43.0, 1.0)])
    assert list(masses) == [41, 43]
    assert list(intensities) == [5.0, 1.0]


def test_nonpositive_intensities_removed():
    masses, intensities = normalize_peaks([(41, -1), (43, 10)])
    assert list(masses) == [43]
    assert list(intensities) == [10.0]
