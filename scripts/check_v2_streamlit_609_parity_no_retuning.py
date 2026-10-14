#!/usr/bin/env python3
"""Exact software parity of NEW deployed v2 application with SPENT original 609.

Uses archived original SHA-pinned per-case outcomes ONLY as fixed software
regression fixtures: NOT untouched testing, NOT model selection and NOT
experimental source-independent external validation. No new model training.
"""
from __future__ import annotations
import csv,hashlib,json,os
from pathlib import Path
import numpy as np
from gcei.reference_builder import EXPECTED_SHA256,parse_msp,sha256
from gcei.v2_bootstrap import build_v2_reference,V2_FROZEN,V2_HGB,V2_INDEX
from gcei.v2_engine import (
 GCEIV2Engine,V2_FEATURES,V2_HGB_SHA256,V2_REFERENCE_SHA256,
 frozen_features,query_vector,bin_spectrum,
)
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/".cache/v2_original_sha_locked_msdial.msp"
FIX=ROOT/".cache/v2_locked_609_predictions.csv"
OUT=ROOT/"audits/v2_streamlit_frozen_parity_20261014/v2_standalone_app_exact_609_software_parity.json"
FIX_SHA="62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7"
SOURCE_SHA="a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70"
def rows(p):
 with Path(p).open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def main():
 assert os.environ.get("GCEI_V2_609_SOFTWARE_PARITY_ONLY")=="YES_SPENT_609_NO_MODEL_SELECTION"
 assert sha256(SOURCE)==SOURCE_SHA==EXPECTED_SHA256
 assert sha256(FIX)==FIX_SHA
 assert sha256(V2_INDEX)==V2_REFERENCE_SHA256
 assert sha256(V2_HGB)==V2_HGB_SHA256
 source=parse_msp(SOURCE)
 reference=rows(V2_INDEX)
 fixtures=rows(FIX)
 assert len(source)==28220 and len(reference)==8455 and len(fixtures)==609
 assert len({r["source_database_first14_label"] for r in fixtures})==609
 output_dir=ROOT/".cache/v2_app_parity_build"
 build=build_v2_reference(SOURCE,output_dir)
 engine=GCEIV2Engine(output_dir,V2_HGB)
 reference_col={r["connectivity"]:i for i,r in enumerate(reference)}
 assert len(reference_col)==8455
 assert engine.meta["connectivity_id"].tolist()==[x["connectivity"] for x in reference]
 sums={"m1_top1":0,"m1_top5":0,"m1_top10":0,
       "accept_10":0,"error_10":0,"accept_05":0,"error_05":0,
       "first14_external_exposed":0}
 max_delta={"similarity":0.,"confidence":0.,"twelve_features":0.}
 for j,r in enumerate(fixtures):
  index=int(r["original_query_source_index"])
  assert 0<=index<28220
  query=source[index]["peaks"]
  result10=engine.analyze(query,risk_target=.10)
  result05=engine.analyze(query,risk_target=.05)
  first14=r["source_database_first14_label"]
  assert first14 in reference_col
  correctref=reference_col[first14]
  predicted=reference_col[result10.top1["connectivity_id"]]
  assert predicted==int(r["m1_top1_reference_index"]),("top1 rank differs",j)
  assert result10.top1["connectivity_id"]==r["m1_top1_predicted_first14"]
  assert result10.top1["reference_source_index"]==int(reference[predicted]["reference_source_index"])
  rawbins,_=bin_spectrum(query)
  score=np.asarray((query_vector(rawbins)@engine.R.T).toarray(),dtype=np.float64).ravel()
  true_score=score[correctref]
  rank=1+int(np.sum(score>true_score)) + int(np.sum(
     (score==true_score)&(np.arange(len(score))<correctref)))
  assert rank==int(r["m1_correct_rank"]),(j,rank,r["m1_correct_rank"])
  recorded=np.array([float(r["feature_"+name]) for name in V2_FEATURES])
  wraw=engine.raw_reference.getrow(predicted)
  rr={int(m):float(v) for m,v in zip(wraw.indices,wraw.data)}
  actual=frozen_features(score,rawbins,rr)
  deviation=float(np.max(np.abs(actual-recorded)))
  max_delta["twelve_features"]=max(max_delta["twelve_features"],deviation)
  assert np.allclose(actual,recorded,atol=1e-11,rtol=0),(j,"12 original HGB features differ",deviation)
  dscore=abs(result10.top1["similarity"]-float(r["m1_top1_cosine"]))
  max_delta["similarity"]=max(max_delta["similarity"],dscore)
  assert dscore<=1e-11,(j,"similarity",dscore)
  dp=abs(result10.confidence-float(r["HGB_probability"]))
  max_delta["confidence"]=max(max_delta["confidence"],dp)
  assert dp<=1e-12,(j,"HGB correctness probability",dp)
  assert abs(result10.margin-float(r["feature_top1_minus_top2"]))<=1e-11
  assert result10.accepted==bool(int(r["accept_10pct"])),(j,"10% rule")
  assert result05.accepted==bool(int(r["accept_5pct"])),(j,"5% rule")
  assert result10.risk_threshold==.87 and result05.risk_threshold==.94
  assert result05.top1["connectivity_id"]==result10.top1["connectivity_id"]
  assert result10.top1["connectivity_id"]==result10.top10.iloc[0]["connectivity_id"]
  top10=result10.top10["connectivity_id"].tolist()
  assert len(top10)==10
  assert len(set(top10))==10
  assert (rank==1)==(int(r["m1_top1_correct"])==1)
  sums["m1_top1"]+=int(rank==1)
  sums["m1_top5"]+=int(rank<=5)
  sums["m1_top10"]+=int(rank<=10)
  sums["accept_10"]+=int(result10.accepted)
  sums["accept_05"]+=int(result05.accepted)
  sums["error_10"]+=int(result10.accepted and rank!=1)
  sums["error_05"]+=int(result05.accepted and rank!=1)
  sums["first14_external_exposed"]+=int(r["source_first14_also_in_prior_466"])
 assert sums=={"m1_top1":394,"m1_top5":489,"m1_top10":509,
                "accept_10":198,"error_10":12,"accept_05":38,
                "error_05":0,"first14_external_exposed":69},sums
 OUTPUT={
   "status":"PASS_ALL_609_SPENT_TEST_CASES_EXACT_APP_INFERENCE_PARITY_NO_RETUNING",
   "original_609_test_status":"ALREADY SPENT; NOT independent new validation",
   "source_and_frozen_reference_SHA256":[sha256(SOURCE),sha256(V2_INDEX)],
   "pretrained_original_HGB_SHA256":sha256(V2_HGB),
   "archived_once_scored_row_ledger_SHA256":sha256(FIX),
   "total_609_app_cases_replayed":len(fixtures),
   "reference_rows":len(reference),
   "m1_margin_and_exact_12_features_reproduced":True,
   "HGB_binary_refitted_on_609":False,
   "neither_5pct_nor_10pct_risk_certified":True,
   "RI_and_v1_conformal_margins_not_used":True,
   "check_counts":sums,
   "max_absolute_difference":max_delta,
   "scientific_limit":"Full software parity with source-dependent previously exposed 609 cases, not new experimental truth or certified selected risk."
 }
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(OUTPUT,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(OUTPUT,indent=2))
if __name__=="__main__":main()
