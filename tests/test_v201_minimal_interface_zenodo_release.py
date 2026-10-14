"""Researcher-facing single-model UI and citation integrity without loading EI data."""
import ast
import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_single_model_streamlit_landing_first_render():
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=35)
    assert not app.exception, app.exception
    assert len(app.title) == 1
    assert app.title[0].value == "GC–EI–MS Annotation Tool"
    assert len(app.warning) == 0
    assert len(app.info) == 0
    # There is NO reference model picker: only one current user-facing engine.
    assert len(app.selectbox) == 1  # confidence screening only
    assert len(app.radio) == 2  # single/batch and paste/upload
    assert app.radio[0].value == "Single spectrum"
    assert len(app.text_area) == 1
    assert app.text_area[0].value == ""
    assert "What" not in app.title[0].value or app.title[0].value


def test_ui_onboarding_and_template_appear_before_input():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert 'APP_VERSION = "2.0.2"' in source
    assert source.index('st.title("GC–EI–MS Annotation Tool")') < source.index('st.subheader("1. Prepare your data")')
    assert source.index('st.subheader("1. Prepare your data")') < source.index('st.subheader("2. Analyze")')
    assert source.index('st.code(SINGLE_EXAMPLE') < source.index('with st.form("single_spectrum_form")')
    assert source.index('st.code(BATCH_EXAMPLE') < source.index('with st.form("batch_spectra_form")')
    assert 'Download single-spectrum template' in source
    assert 'Download batch template' in source
    assert "Use a CSV with two columns" in source
    assert "Each unique ID is analyzed separately" in source
    assert "Identify **possible compound matches**" in source


def test_only_current_research_model_and_all_numerical_rules_retained():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'return GCEIV2Engine(ensure_v2_assets(), V2_HGB)' in source
    assert 'GCEIEngine' not in source
    assert 'V1_MODE' not in source
    assert 'Legacy' not in source and 'legacy' not in source
    assert 'frozen' not in source.lower()  # no workflow terminology on site
    assert "original_source_sha256" in source and "V2_HGB_SHA256" in source
    assert 'risk_target = .10 if screening.startswith("Standard") else .05' in source
    assert "result.accepted" in source
    assert "not certified error guarantees" in source
    assert "394 publisher-provided connectivity labels" in source
    assert "st.success(" not in source
    assert 'with st.expander("How to cite")' in source
    assert "Dr. James H. Zothantluanga" in source
    assert "Research Director, Jazer Research Lab, Aizawl, Mizoram, India" in source
    assert "Research article:" in source
    assert "Original spectral library:" in source


def test_publication_metadata_represents_v202_only_not_old_doi():
    meta = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert meta["version"] == "2.0.2"
    assert meta["license"] == "MIT"
    assert meta["creators"][0]["name"] == "Zothantluanga, James H."
    assert "8,455" in meta["description"]
    assert "not" in meta["description"].lower()
    assert "version: 2.0.2" in cff
    assert "value: \"10.5281/zenodo.23372495\"" not in cff
    assert 'value: "10.5281/zenodo.23373447"' in cff
    assert "10.5281/zenodo.23373447" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert "10.5281/zenodo.23373447" in (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.0.2"' in (ROOT / "app.py").read_text(encoding="utf-8")
