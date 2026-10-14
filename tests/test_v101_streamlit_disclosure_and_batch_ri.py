"""Scientific and usability regression for Streamlit v1.0.1 release.

All synthetic input; no original publisher data or spectral model outcomes.
"""
from pathlib import Path
from types import MethodType
import ast
import pandas as pd
import pytest
from gcei.engine import GCEIEngine

ROOT = Path(__file__).resolve().parents[1]


def _batch_engine():
    obj=object.__new__(GCEIEngine)
    def analyze(_self, peaks, kovats_ri=None, risk_target=.10):
        list(peaks)
        class Result:
            mode="EI-only" if kovats_ri is None else "EI+RI"
            top1={"display_name":"synthetic","formula":"C2H6","connectivity_id":"SYNTHETIC"}
            confidence=.42
            conformal90_size=12
            risk_target=.10
            risk_threshold=.87
            ri_delta_top1=None
            decision="Synthetic tentative annotation"
        result=Result()
        result.risk_target=risk_target
        return result
    obj.analyze=MethodType(analyze,obj)
    return obj


def test_batch_rejects_contradictory_retention_indices_within_spectrum():
    frame=pd.DataFrame({
        "spectrum_id":["one","one"],
        "mz":[41,43],"intensity":[10,20],"ri":[900.,1200.]})
    with pytest.raises(ValueError,match="conflicting retention indices"):
        _batch_engine().analyze_batch(frame)


@pytest.mark.parametrize("ri",[-1.0, 0.0,float("inf"),"not_a_number"])
def test_batch_rejects_invalid_supplied_ri(ri):
    frame=pd.DataFrame({"spectrum_id":["case"],"mz":[41],
                        "intensity":[10],"ri":[ri]})
    with pytest.raises(ValueError,match="retention indices|Kovats RI"):
        _batch_engine().analyze_batch(frame)


def test_batch_repeated_consistent_ri_is_accepted():
    frame=pd.DataFrame({"spectrum_id":["A","A","B"],"mz":[41,43,57],
       "intensity":[10,20,30],"ri":[902,902,None]})
    result=_batch_engine().analyze_batch(frame)
    assert list(result["mode"])==["EI+RI","EI-only"]
    assert len(result)==2


def test_public_app_retains_only_current_ei_model_without_legacy_option():
    source=(ROOT/"app.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert 'APP_VERSION = "2.0.2"' in source
    assert "GCEIV2Engine" in source
    assert "V2_REFERENCE_SHA256" in source and "V2_HGB_SHA256" in source
    assert "GCEIEngine" not in source
    assert "V1_MODE" not in source
    assert "frozen" not in source.lower()
    assert "not certified error guarantees" in source
    assert "394 publisher-provided connectivity labels" in source
    assert "result.accepted" in source
    assert "historical_rule_met" in source
    assert "st.success(" not in source
    assert 'st.subheader("1. Prepare your data")' in source
    assert 'st.subheader("2. Analyze")' in source
    assert 'with st.expander("How to cite")' in source
    assert "Dr. James H. Zothantluanga" in source


def test_engine_threshold_math_and_scoring_untouched():
    source=(ROOT/"gcei/engine.py").read_text(encoding="utf-8")
    assert 'if risk_target not in (0.10, 0.05):' in source
    assert 'threshold = float(model["empirical_risk_thresholds"][f"{risk_target:.2f}"])' in source
    assert "np.argsort(-score, kind=\"stable\")" in source
    assert "score >= top_score - q90 - 1e-8" in source
    assert "historical" in source.lower()
