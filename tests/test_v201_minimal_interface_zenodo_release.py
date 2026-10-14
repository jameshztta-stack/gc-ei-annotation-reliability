"""Minimal UI, scientific-claim and provenance tests.

These checks do not load any original MSP, frozen HGB or actual 609 outcomes.
The v2 mathematical model is unchanged and protected by separate pinned tests.
"""
import ast
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]


def test_minimal_app_structure_and_source_free_first_render():
    at=AppTest.from_file(str(ROOT/"app.py")).run(timeout=35)
    assert not at.exception, at.exception
    assert len(at.title)==1
    assert "GC–EI–MS Annotation" in at.title[0].value
    assert len(at.warning)==0
    assert len(at.info)==0
    assert len(at.expander)==2
    assert at.expander[0].label=="Input examples"
    assert at.expander[1].label=="Methods, limitations & provenance"
    assert len(at.radio)>=2
    assert len(at.selectbox)>=2
    assert "v2 · EI + HGB" in at.selectbox[0].options
    assert at.selectbox[0].value=="v2 · EI + HGB"
    assert len(at.text_area)==1
    assert at.text_area[0].value==""


def test_ui_does_not_rewrite_frozen_scoring_or_overclaim():
    source=(ROOT/"app.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert 'APP_VERSION = "2.0.1"' in source
    assert "GCEIV2Engine(ensure_v2_assets(), V2_HGB)" in source
    assert "GCEIEngine(ensure_runtime_assets())" in source
    assert 'with st.expander("Methods, limitations & provenance")' in source
    assert "not certified future-error guarantees" in source
    assert "389/609" not in source
    assert "394/609" in source
    assert "198/609" in source
    assert "38/609" in source
    assert "Historical decision rule" in source
    assert "st.success" not in source
    assert "st.success" not in source
    # Loading the original MSP must be initiated only from a submitted action.
    assert "load_engine(model_name).analyze(" in source
    assert "load_engine(model_name).analyze_batch(" in source
    assert "with st.form(" in source
    assert "request_fingerprint(" in source


def test_zenodo_metadata_matches_source_version_and_is_not_old_v1_doi():
    m=json.loads((ROOT/".zenodo.json").read_text(encoding="utf-8"))
    cff=(ROOT/"CITATION.cff").read_text(encoding="utf-8")
    assert m["version"]=="2.0.1"
    assert m["upload_type"]=="software"
    assert m["license"]=="MIT"
    assert m["creators"][0]["name"]=="Zothantluanga, James H."
    assert "5%/10%" in m["description"] and "not" in m["description"].lower()
    assert "version: 2.0.1" in cff
    assert "10.5281/zenodo.23143113" in cff
    assert "identifiers:" in cff
    assert 'value: "10.5281/zenodo.23372495"' in cff
    assert 'value: "10.5281/zenodo.23143113"' not in cff  # old v1 version stays separate
    assert "10.5281/zenodo.23372495" in (ROOT/"README.md").read_text(encoding="utf-8")
    assert "10.5281/zenodo.23372495" in (ROOT/"app.py").read_text(encoding="utf-8")
    release=(ROOT/"docs/RELEASE_V2_0_1_ZENODO_NOTES.md").read_text(encoding="utf-8")
    assert "v2.0.1" in release
    assert "394/609" in release
    assert "a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13" in release
