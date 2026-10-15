#!/usr/bin/env python3
"""Reproduce the current EI classifier and previously reported source-label results.

Input records were generated from publicly described spectral sources. They
contain derived feature vectors, source-label outcomes and numerical predictions,
not publisher MSP peak arrays. Original test outcomes are reused *only* for
retrospective verification; no additional tuning or performance certification.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import tempfile
from pathlib import Path
import numpy as np
import joblib
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, brier_score_loss

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"reproducibility"/"records"
ORIGINAL_HASHES={
"development_features.csv":"67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce",
"within_source_evaluation.csv":"62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7",
"cross_collection_evaluation.csv":"09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b",
}
EXPECTED_MODEL="a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13"
FEATURES=["top_score","top1_minus_top2","top1_minus_top5","log1p_near_0p01",
"log1p_near_0p05","top1_minus_top10","mean_top5","std_top10",
"log1p_near_0p10","log1p_query_peaks",
"query_peak_overlap_with_top1_fraction","query_intensity_share_matched_top1"]


def check_files():
    for name,expected in ORIGINAL_HASHES.items():
        actual=hashlib.sha256((D/name).read_bytes()).hexdigest()
        if actual!=expected:
            raise AssertionError(f"{name}: source outcome/feature ledger checksum differs from recorded study: {actual}")
    assert hashlib.sha256((ROOT/"models/v2/hgb_model.joblib").read_bytes()).hexdigest()==EXPECTED_MODEL


def read(name):
    with (D/name).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classifier():
    return HistGradientBoostingClassifier(max_leaf_nodes=5,max_iter=100,
        learning_rate=.05,min_samples_leaf=25,l2_regularization=10.,
        random_state=20261013)


def model_training():
    rows=read("development_features.csv")
    x=np.asarray([[float(row["feature_"+z]) for z in FEATURES] for row in rows],dtype=np.float64)
    y=np.asarray([int(row["top1_correct_source_database_label"]) for row in rows],dtype=int)
    assert x.shape==(1410,12) and int(y.sum())==901
    assert np.isfinite(x).all()
    assert sklearn.__version__=="1.8.0" and np.__version__=="2.3.5", "Use the numerical versions in requirements.txt"
    m=classifier().fit(x,y)
    # Persist in the same joblib encoding as the published software.
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"replicated.joblib"
        joblib.dump(m,p,compress=3)
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        assert sha==EXPECTED_MODEL, f"Model bytes could not be reproduced: {sha}"
    winner=np.array([float(row["feature_top_score"]) for row in rows])
    assert winner.size==1410
    return m,{"development_n":len(y),"development_publisher_label_agreement_n":int(y.sum()),
              "exact_model_sha256":sha}


def original_selected_counts(rows,label,score,ranks,accepted):
    y=np.asarray([int(z[label]) for z in rows])
    p=np.asarray([float(z[score]) for z in rows])
    rank=np.asarray([int(z[ranks]) for z in rows])
    assert np.array_equal(rank==1,y.astype(bool))
    result={"n":int(len(y)),"top1_source_agreed":int(y.sum()),
      "top5_source_agreed":int((rank<=5).sum()),
      "top10_source_agreed":int((rank<=10).sum()),
      "HGB_AUROC":float(roc_auc_score(y,p)),
      "HGB_Brier":float(brier_score_loss(y,p)),
      "screening":{}}
    for threshold,column in accepted:
        a=np.asarray([int(z[column]) for z in rows],dtype=bool)
        n=int(a.sum());wrong=int(((y==0)&a).sum())
        result["screening"][threshold]={"accepted":n,"publisher_disagreements":wrong,
                                        "certified_for_future_samples":False}
    return result


def evaluate(model):
    w=read("within_source_evaluation.csv")
    e=read("cross_collection_evaluation.csv")
    assert len(w)==609 and len(e)==466
    # The stored first-hit classifier outputs must be recreated by the exact trained binary.
    for rows,score in [(w,"HGB_probability"),(e,"HGB_probability_devfit")]:
        xx=np.asarray([[float(z["feature_"+k]) for k in FEATURES] for z in rows])
        pp=model.predict_proba(xx)[:,1]
        previously=np.asarray([float(z[score]) for z in rows])
        assert np.max(np.abs(pp-previously))<1e-12, "Model prediction differs from archived original outcomes"
    inside=original_selected_counts(w,"m1_top1_correct","HGB_probability","m1_correct_rank",
        [("standard","accept_10pct"),("strict","accept_5pct")])
    external=original_selected_counts(e,"m1_top1_correct","HGB_probability_devfit","m1_correct_label_rank",
        [("standard","accept_10pct_rule"),("strict","accept_5pct_rule")])
    assert inside["n"]==609 and inside["top1_source_agreed"]==394
    assert inside["top5_source_agreed"]==489 and inside["top10_source_agreed"]==509
    assert inside["screening"]["standard"]=={"accepted":198,"publisher_disagreements":12,"certified_for_future_samples":False}
    assert inside["screening"]["strict"]=={"accepted":38,"publisher_disagreements":0,"certified_for_future_samples":False}
    assert external["n"]==466 and external["top1_source_agreed"]==334
    assert external["screening"]["standard"]["accepted"]==185
    assert external["screening"]["strict"]["accepted"]==25
    return {"within_MSDIAL_source_labels":inside,"selected_SWGDRUG_RECETOX_source_labels":external,
      "source_independent_chemical_identity_confirmed":False,
      "note":"Published source first14 label agreement only; selected in-reference cases, previously analyzed; no future error-rate certification."}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=None,help="Write verified summary JSON to this local path")
    args=p.parse_args()
    check_files()
    m,training=model_training()
    report={"training":training,"retrospective_evaluation":evaluate(m)}
    if args.output:
        path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
