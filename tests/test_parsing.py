"""Spectrum CSV and ion-peak parsing tests."""
import pytest
from gcei.engine import parse_single_spectrum_text, read_spectrum_csv
from gcei.v2_engine import bin_spectrum


def test_text_and_csv_input():
    assert parse_single_spectrum_text("mz,intensity\n41,10\n43,20") == [(41.0,10.0),(43.0,20.0)]
    assert parse_single_spectrum_text("# note\n41 10\n43;20\n93\t100") == [(41.,10.),(43.,20.),(93.,100.)]
    assert read_spectrum_csv(b"mz,abundance\n41,10\n93,100") == [(41,10),(93,100)]


def test_invalid_input():
    with pytest.raises(ValueError,match="No numeric"):
        parse_single_spectrum_text("mz,intensity\na,b")
    with pytest.raises(ValueError,match="must contain mz"):
        read_spectrum_csv(b"mass,signal\n41,10")


def test_nominal_mass_and_nonpositive_peaks():
    peaks, invalid = bin_spectrum([(41.1,2.),(41.2,3.),(43.,1.),(44.,-1.),(42.,0.)])
    assert peaks == {41:5.,43:1.}
    assert invalid == 0


def test_mass_range_and_empty_spectrum():
    peaks, invalid = bin_spectrum([(41.,10.),(-1.,20.),(6421.,4.)])
    assert peaks == {41:10.} and invalid == 2
    with pytest.raises(ValueError,match="No valid positive"):
        bin_spectrum([(43,0),(-1,10)])
