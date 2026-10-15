"""Phase 5: actual app.py Streamlit headless presentation smoke.

Only verifies UI script execution, controls and scientifically cautious
disclosures. No physical browser, user-study, published deployment or GC–EI
chemical truth. No live inference, no downloads of experimental MSP files.
"""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1] / "app.py"


def _render_text(app):
    return " ".join(
        str(element.value) for collection in (
            app.title, app.subheader, app.markdown, app.caption
        ) for element in collection
    )


def test_actual_app_single_input_with_scientific_disclosures():
    at=AppTest.from_file(str(APP), default_timeout=30).run()
    assert not at.exception, [x.message for x in at.exception]
    assert at.title and at.title[0].value == "GC–EI–MS Annotation Tool"
    assert at.radio[0].value == "Single spectrum"
    assert at.radio[1].value == "Paste peaks"
    assert at.selectbox[0].value == "Standard (score ≥0.87)"
    assert at.text_area
    text=_render_text(at)
    assert "8,455" in text
    assert "tentative" in text.lower()
    assert "not guaranteed" in text.lower() or "not certified" in text.lower()
    assert "source" in text.lower()
    assert "spectrum" in text.lower()


def test_actual_app_switch_to_batch_mode_with_required_columns():
    at=AppTest.from_file(str(APP), default_timeout=30).run()
    assert not at.exception
    at.radio[0].set_value("Batch spectra").run()
    assert not at.exception, [x.message for x in at.exception]
    assert at.radio[0].value == "Batch spectra"
    text=_render_text(at)
    assert "spectrum_id" in text
    assert "intensity" in text
    assert "retention-index" in text.lower() or "retention" in text.lower()
    assert "tentative" in text.lower()
