#!/usr/bin/env python3
"""End-to-end v2 software DEMONSTRATION on already published in-repo example peaks.
No authentic reference standard, no accuracy claim, no HGB refit or threshold change.
This is not an independently sourced validation cohort.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from gcei.v2_bootstrap import ensure_v2_assets, V2_HGB
from gcei.v2_engine import GCEIV2Engine, V2_HGB_SHA256, V2_REFERENCE_SHA256
from gcei.reference_builder import EXPECTED_SHA256

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/".cache/phase3_v2_example_demo"

def main():
    out=OUT;out.mkdir(parents=True,exist_ok=True)
    engine=GCEIV2Engine(ensure_v2_assets(),V2_HGB)
    batch=pd.read_csv(ROOT/"examples/example_batch_12_botanical.csv")
    assert batch.spectrum_id.nunique()==12 and not batch.empty
    assert {"spectrum_id","mz","intensity"}.issubset(batch.columns)
    assert "ri" not in batch or batch.ri.isna().all()
    results10=engine.analyze_batch(batch,risk_target=.10)
    results05=engine.analyze_batch(batch,risk_target=.05)
    assert len(results10)==len(results05)==12
    assert results10.spectrum_id.tolist()==results05.spectrum_id.tolist()
    assert results10.top1_connectivity_id.tolist()==results05.top1_connectivity_id.tolist()
    assert results10.source_independent_risk_certified.eq(False).all()
    assert results05.source_independent_risk_certified.eq(False).all()
    assert results10.source_msp_sha256.eq(EXPECTED_SHA256).all()
    assert results10.reference_index_sha256.eq(V2_REFERENCE_SHA256).all()
    assert results10.model_sha256.eq(V2_HGB_SHA256).all()

    single=pd.read_csv(ROOT/"examples/example_single_CdeL_P02.csv")
    r=engine.analyze(zip(single.mz,single.intensity),risk_target=.10)
    row=results10.loc[results10.spectrum_id=="CdeL_P02"].iloc[0]
    assert r.top1["connectivity_id"]==row.top1_connectivity_id
    assert np.isclose(r.confidence,row.historical_HGB_score,rtol=0,atol=1e-12)
    assert np.isclose(r.margin,row.top1_top2_cosine_margin,rtol=0,atol=1e-12)

    top10=[];cases=[]
    for sid,peaks in batch.groupby("spectrum_id",sort=False):
        res=engine.analyze(zip(peaks.mz,peaks.intensity),risk_target=.10)
        strict=engine.analyze(zip(peaks.mz,peaks.intensity),risk_target=.05)
        assert res.top1["connectivity_id"]==strict.top1["connectivity_id"]
        assert res.top10.shape[0]==10
        assert res.top10.connectivity_id.nunique()==10
        for _,cand in res.top10.iterrows():
            top10.append({"spectrum_id":sid,"rank":int(cand["rank"]),
                          "candidate_first14":str(cand["connectivity_id"]),
                          "candidate_name":str(cand["display_name"]),
                          "formula":str(cand["formula"]),
                          "EI_similarity":float(cand["similarity"])})
        cases.append({"spectrum_id":sid,"top1_first14":res.top1["connectivity_id"],
                      "top1_name":res.top1["display_name"],
                      "top1_similarity":float(res.top1["similarity"]),
                      "margin_top1_top2":float(res.margin),
                      "frozen_HGB_score":float(res.confidence),
                      "passes_historical_10_rule_UNCERTIFIED":bool(res.accepted),
                      "passes_historical_5_rule_UNCERTIFIED":bool(strict.accepted),
                      "top1_TENTATIVE_only":True,
                      "unknown_true_chemical_identity":True})
    one=pd.DataFrame(cases)
    assert len(one)==12
    assert one.top1_first14.notna().all()
    one.to_csv(out/"12_case_v2_demo_summary.csv",index=False)
    pd.DataFrame(top10).to_csv(out/"12_case_v2_top10_ranked_candidates.csv",index=False)
    manifest={
     "study_role":"EXISTING botanical peak examples; SOFTWARE OUTPUT DEMO ONLY; not externally authenticated truth",
     "n_peaks_spectra":12,"n_candidate_rows":len(top10),"RI_fusion_used":False,
     "conformal_v1_used":False,"confidence_model_fitted":False,
     "frozen_reference_size":8455,
     "source_SHA256":EXPECTED_SHA256,"reference_SHA256":V2_REFERENCE_SHA256,
     "HGB_model_SHA256":V2_HGB_SHA256,
     "single_batch_exact_case_parity":True,
     "10pct_and_5pct_certified":False,
     "10_rule_pass_n":int(one.passes_historical_10_rule_UNCERTIFIED.sum()),
     "5_rule_pass_n":int(one.passes_historical_5_rule_UNCERTIFIED.sum()),
     "v1_legacy_expected_results_not_reused":True,
     "accuracy_denominator_not_defined_without_authenticated_truth":True,
    }
    (out/"12_case_v2_software_provenance_manifest.json").write_text(json.dumps(manifest,indent=2)+"\\n")
    print(json.dumps(manifest,indent=2))
if __name__=="__main__":main()
