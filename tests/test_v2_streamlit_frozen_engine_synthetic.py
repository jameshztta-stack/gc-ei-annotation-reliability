"""Adversarial v2-only inference tests using SYNTHETIC peaks and false candidates.

No frozen 609 outcomes, no real EI spectra, no fitting. Verify critical
confidence/abstention/RI separation and safe model source checks.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from scipy import sparse
from gcei.v2_engine import (
    GCEIV2Engine, V2_N_REFERENCE, V2_MAX_MZ,
    bin_spectrum,query_vector,frozen_features,weighted_matrix,
)

class StubProbability:
    def predict_proba(self, X):
        assert X.shape==(1,12) and np.isfinite(X).all()
        return np.array([[.04,.96]])


def toy_engine():
    e=object.__new__(GCEIV2Engine)
    e.model=StubProbability()
    e.meta=pd.DataFrame({
        "connectivity_id":[f"TEST{x:010d}" for x in range(V2_N_REFERENCE)],
        "reference_source_index":np.arange(V2_N_REFERENCE),
        "name":[f"Synthetic test compound {i}" for i in range(V2_N_REFERENCE)],
        "formula":["C2H6"]*V2_N_REFERENCE,
        "inchi_key":["TEST_ONLY"]*V2_N_REFERENCE,
        "smiles":["CC"]*V2_N_REFERENCE,
    })
    raw=[{"peaks":[(41,100.),(43,100.)]},
         {"peaks":[(41,99.),(43,101.)]}]
    raw.extend({"peaks":[(57,10.)]} for _ in range(V2_N_REFERENCE-2))
    e.R=weighted_matrix(raw,range(V2_N_REFERENCE))
    rr,cc,vv=[],[],[]
    for i,record in enumerate(raw):
        for mass,intensity in record["peaks"]:
            rr.append(i);cc.append(mass);vv.append(intensity)
    e.raw_reference=sparse.csr_matrix((vv,(rr,cc)),shape=(V2_N_REFERENCE,V2_MAX_MZ+1),dtype=float)
    return e


def test_source_native_nominal_bins_and_precise_features_do_not_drop_zero_mz():
    raw={0:100.,41:25.,43:100.}
    candidate={0:60.,41:7.}
    score=np.zeros(V2_N_REFERENCE)
    score[0]=.89;score[1]=.86
    feat=frozen_features(score,raw,candidate)
    assert len(feat)==12
    assert feat[10]==pytest.approx(2/3)
    assert feat[11]==pytest.approx(125/225)
    assert feat[1]==pytest.approx(.03)
    assert feat[9]==pytest.approx(np.log1p(3))
    bins,ignored=bin_spectrum([(41.49,10),(41.51,20),(41.,5),(43,3)])
    assert bins=={41:15.,42:20.,43:3.} and ignored==0


def test_v2_frozen_hgb_probability_is_not_sufficient_without_m1_margin_for_5pct():
    e=toy_engine()
    raw=[(41,100.),(43,100.)]
    a=e.analyze(raw,risk_target=.10)
    b=e.analyze(raw,risk_target=.05)
    assert a.top1["reference_source_index"]==0
    assert a.top10.iloc[0]["reference_source_index"]==0
    assert a.confidence==pytest.approx(.96)
    assert b.confidence==pytest.approx(.96)
    assert a.accepted is True
    assert b.accepted is False
    assert a.margin<.20
    assert b.risk_threshold==.94
    assert "NOT a certified error guarantee" in a.decision
    assert "not pass" in b.decision


def test_v2_rejects_legacy_ri_and_batch_instead_of_improperly_reusing_v1():
    e=toy_engine()
    with pytest.raises(ValueError,match="RI fusion"):
        e.analyze([(41,100.)],kovats_ri=927.)
    frame=pd.DataFrame({"spectrum_id":["X"],"mz":[41],"intensity":[10],"ri":[923.]})
    with pytest.raises(ValueError,match="Kovats RI cannot be integrated"):
        e.analyze_batch(frame)
    clean=frame.drop(columns=["ri"])
    out=e.analyze_batch(clean,risk_target=.10)
    assert len(out)==1
    assert not out["source_independent_risk_certified"].any()
    assert out.iloc[0]["model_sha256"]
    assert out.iloc[0]["reference_index_sha256"]


def test_untrusted_external_hgb_cannot_be_loaded(tmp_path):
    corrupt=tmp_path/"untrusted_model.joblib"
    corrupt.write_bytes(b"pickle-like bytes are untrusted")
    with pytest.raises(RuntimeError,match="SHA-256 mismatch"):
        GCEIV2Engine(tmp_path,corrupt)
