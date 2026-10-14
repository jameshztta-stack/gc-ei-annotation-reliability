"""Compile source-locked v2 deployable reference index and HGB model.

Development-only original 1410 label training was frozen BEFORE the 609 final
evaluation. This script recreates exactly that old model binary; it MUST NOT
learn from the now-spent 609, selected 466 or incoming users' samples.
"""
from pathlib import Path
import csv,hashlib,json
import joblib
import numpy as np
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"models/v2/reference_index.csv"
DEV=ROOT/".cache/v2_original_1410_development_predictions.csv"
MODEL=ROOT/"models/v2/hgb_model.joblib"
OUTPUT=ROOT/"models/v2/release_manifest.json"
INDEX_SHA="2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01"
DEV_SHA="67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce"
MODEL_SHA="a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13"
SOURCE_SHA="a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70"
FEATURES=("top_score","top1_minus_top2","top1_minus_top5",
    "log1p_near_0p01","log1p_near_0p05","top1_minus_top10",
    "mean_top5","std_top10","log1p_near_0p10","log1p_query_peaks",
    "query_peak_overlap_with_top1_fraction",
    "query_intensity_share_matched_top1")
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rows(path):
 with Path(path).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def main():
 assert sklearn.__version__=="1.8.0" and np.__version__=="2.3.5"
 assert sha(INDEX)==INDEX_SHA and sha(DEV)==DEV_SHA
 ref=rows(INDEX)
 dev=rows(DEV)
 assert len(ref)==8455 and len(dev)==1410
 assert len({r["connectivity"] for r in ref})==8455
 assert len({r["reference_source_index"] for r in ref})==8455
 assert len({r["source_connectivity"] for r in dev})==1410
 X=np.array([[float(r["feature_"+z]) for z in FEATURES] for r in dev],dtype=np.float64)
 y=np.array([int(r["top1_correct_source_database_label"]) for r in dev],dtype=int)
 assert X.shape==(1410,12) and y.sum()==901 and set(y)=={0,1}
 clf=HistGradientBoostingClassifier(
   max_leaf_nodes=5,max_iter=100,learning_rate=.05,
   min_samples_leaf=25,l2_regularization=10.,random_state=20261013)
 clf.fit(X,y)
 MODEL.parent.mkdir(parents=True,exist_ok=True)
 joblib.dump(clf,MODEL,compress=3)
 actual=sha(MODEL)
 assert actual==MODEL_SHA,(actual,"v2 model hash drift: FAIL CLOSED")
 output={
 "research_model_status":"source-locked development fitted HGB; 5/10 targets not certified",
 "original_MS_DIAL_SHA256":SOURCE_SHA,
 "research_v2_reference_index_SHA256":INDEX_SHA,
 "reference_first14_n":8455,
 "development_original_1410_SHA256":DEV_SHA,
 "development_n":1410,
 "exact_model_sha256":actual,
 "model_object_type":"HistGradientBoostingClassifier",
 "library_versions":{"numpy":np.__version__,"sklearn":sklearn.__version__},
 "features":list(FEATURES),
 "algorithm":"nominal EI m/z^1 sqrt(I), float64 weighted cosine",
 "10pct_rule":{"HGB_min_probability":.87,"certified":False},
 "5pct_rule":{"HGB_min_probability":.94,"top1_minus_top2_min":.20,"certified":False},
 "v1_conformal_or_RI_reused":False,
 "609_final_test_data_used_for_training":False,
 "466_external_source_used_for_training":False,
 "model_fitted_from_original_1410_exposed_development_only":True,
 "research_609_test_status":"permanently spent as heldout; within-source 394/609",
 "deployment_scope":"experimental source-dependent connectivity library annotation only",
 }
 OUTPUT.write_text(json.dumps(output,indent=2)+"\n")
 print(json.dumps({"status":"PASS EXACT HGB AND FIRST14 REFERENCE","model_sha256":actual,
                   "references":len(ref),"train_dev":len(dev)},indent=2))
if __name__=="__main__":main()
