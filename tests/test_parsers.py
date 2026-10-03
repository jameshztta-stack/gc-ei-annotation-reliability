from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv


def test_text_parser_accepts_csv_header():
    peaks = parse_single_spectrum_text("mz,intensity\n41,10\n43,20\n")
    assert peaks == [(41.0, 10.0), (43.0, 20.0)]


def test_csv_parser_accepts_abundance_alias():
    peaks = read_spectrum_csv(b"mz,abundance\n41,10\n93,100\n")
    assert peaks == [(41, 10), (93, 100)]


def test_normalize_merges_rounded_nominal_mass():
    merged, ignored = GCEIEngine._normalize_peaks([(41.1, 2.0), (41.2, 3.0), (43.0, 1.0)], max_mz=100)
    assert merged == {41: 5.0, 43: 1.0}
    assert ignored == 0


def test_nonpositive_intensities_removed():
    merged, ignored = GCEIEngine._normalize_peaks([(41, -1), (43, 10)], max_mz=100)
    assert merged == {43: 10.0}
    assert ignored == 0
