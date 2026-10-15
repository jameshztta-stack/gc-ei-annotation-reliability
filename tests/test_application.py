"""Checks for the current GC–EI–MS web application."""
import hashlib
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_application_single_and_batch_screens():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=35).run()
    assert not app.exception
    assert app.title[0].value == "GC–EI–MS Annotation Tool"
    assert app.radio[0].value == "Single spectrum"
    assert len(app.selectbox) == 1
    assert app.text_area
    app.radio[0].set_value("Batch spectra").run()
    assert not app.exception
    assert app.radio[0].value == "Batch spectra"


def test_current_model_and_version_files():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.0.2"' in text
    assert "GCEIV2Engine(ensure_v2_assets(), V2_HGB)" in text
    assert "not certified error guarantees" in text
    assert "GC–EI–MS Annotation Tool" in text
    assert "Research article:" not in text
    expected = {
        "models/v2/reference_index.csv": "2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01",
        "models/v2/hgb_model.joblib": "a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13",
    }
    for path, sha in expected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
