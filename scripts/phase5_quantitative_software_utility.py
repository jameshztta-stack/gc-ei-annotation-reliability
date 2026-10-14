#!/usr/bin/env python3
"""Phase 5: predeclared software-reporting utility & retrospective review routing.

NO new chemical ID accuracy, new dataset, retraining, prospective risk guarantee,
matched head-to-head vs third-party software, or independent usability study.
Original 609 and 466 source labels are SPENT; botanical examples are unlabelled.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

LEDGERS = {
    "609": "62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7",
    "466": "09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b",
}

CONFIG = {
    "609": {
        "correct": "m1_top1_correct", "truth": "source_database_first14_label",
        "pred": "m1_top1_predicted_first14", "prob": "HGB_probability",
        "gap": "feature_top1_minus_top2", "rule10": "accept_10pct", "rule5": "accept_5pct",
        "expected_correct": 394, "expected_10": (198, 12), "expected_5": (38, 0),
        "label": "Original spent within-MS-DIAL publisher first14 labels",
    },
    "466": {
        "correct": "m1_top1_correct", "truth": "true_publisher_first14",
        "pred": "m1_top1_predicted_first14", "prob": "HGB_probability_devfit",
        "gap": "m1_top1_minus_top2", "rule10": "accept_10pct_rule",
        "rule5": "accept_5pct_rule", "expected_correct": 334,
        "expected_10": (185, 12), "expected_5": (25, 0),
        "label": "Previously exposed selected SWGDRUG/RECETOX publisher first14 labels",
    },
}

ROOT = Path(__file__).resolve().parents[1]


def input_ledger(path: Path, role: str) -> pd.DataFrame:
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == LEDGERS[role], "Archived ledger SHA mismatch"
    d = pd.read_csv(path)
    assert len(d) == int(role), "Archived denominator changed"
    cfg = CONFIG[role]
    assert all(x in d.columns for x in (
        "m1_top1_cosine", cfg["truth"], cfg["pred"], cfg["correct"],
        cfg["prob"], cfg["gap"], cfg["rule10"], cfg["rule5"]
    )), "Missing predeclared columns"
    y = d[cfg["correct"]].to_numpy(dtype=int)
    assert set(y) == {0, 1}
    assert int(y.sum()) == cfg["expected_correct"]
    assert (d[cfg["truth"]].astype(str) == d[cfg["pred"]].astype(str)).to_numpy().astype(int).tolist() == y.tolist()
    p = d[cfg["prob"]].to_numpy(dtype=float)
    gap = d[cfg["gap"]].to_numpy(dtype=float)
    assert np.isfinite(p).all() and np.isfinite(gap).all()
    assert ((p >= 0) & (p <= 1)).all()
    assert (d[cfg["rule10"]].to_numpy(dtype=int) == (p >= 0.87).astype(int)).all()
    assert (d[cfg["rule5"]].to_numpy(dtype=int) ==
            ((p >= 0.94) & (gap >= 0.20)).astype(int)).all()
    for label, rule in [("10", cfg["rule10"]), ("5", cfg["rule5"])]:
        accepted = d[rule].to_numpy(dtype=int)
        assert set(accepted).issubset({0, 1})
        counts = (int(accepted.sum()), int(((accepted == 1) & (y == 0)).sum()))
        assert counts == cfg[f"expected_{label}"], (role, label, counts)
    return d


def routing(d: pd.DataFrame, role: str):
    cfg = CONFIG[role]
    y = d[cfg["correct"]].to_numpy(dtype=int)
    n = len(y)
    total_true = int(y.sum())
    total_false = n - total_true
    details = []
    for setting, col in [("10%-target historic", cfg["rule10"]),
                         ("5%-target historic", cfg["rule5"])]:
        accepted = d[col].to_numpy(dtype=int).astype(bool)
        ac = int((accepted & (y == 1)).sum())
        aw = int((accepted & (y == 0)).sum())
        rc = int((~accepted & (y == 1)).sum())
        rw = int((~accepted & (y == 0)).sum())
        assert ac + aw + rc + rw == n
        assert ac + rc == total_true and aw + rw == total_false
        details.append({
            "role": role, "rule": setting, "n": n,
            "original_top1_label_correct": total_true,
            "original_top1_label_wrong": total_false,
            "accepted_n": ac + aw, "accepted_correct_n": ac,
            "accepted_wrong_n": aw, "sent_to_review_n": rc + rw,
            "sent_to_review_but_label_correct_n": rc,
            "sent_to_review_and_label_wrong_n": rw,
            "review_fraction_of_wrong_labels": rw / total_false,
            "review_fraction_of_correct_labels": rc / total_true,
            "accepted_label_disagreement_fraction": aw / (ac+aw),
            "coverage": (ac+aw) / n,
            "certified_prospective_risk": False,
            "source_independent_chemical_truth": False,
            "interpretation": "Historical source-label review routing only; not realized prevented misidentifications",
        })
    return details


def twelve_examples(out: Path):
    """Actual frozen v2, not the original v1 model and no real-sample truth."""
    from gcei.v2_bootstrap import ensure_v2_assets, V2_HGB
    from gcei.v2_engine import (
        GCEIV2Engine, V2_N_REFERENCE, V2_HGB_SHA256, V2_REFERENCE_SHA256
    )
    from gcei.reference_builder import EXPECTED_SHA256
    engine = GCEIV2Engine(ensure_v2_assets(), V2_HGB)
    batch = pd.read_csv(ROOT / "examples/example_batch_12_botanical.csv")
    assert len(batch) > 12 and batch.spectrum_id.nunique() == 12
    assert not batch.spectrum_id.isna().any()
    batch10 = engine.analyze_batch(batch, risk_target=0.10)
    batch05 = engine.analyze_batch(batch, risk_target=0.05)
    assert len(batch10) == len(batch05) == 12
    assert batch10.spectrum_id.tolist() == batch05.spectrum_id.tolist()
    out_rows, top10 = [], []
    for sid, group in batch.groupby("spectrum_id", sort=False):
        peaks = list(zip(group.mz, group.intensity))
        result = engine.analyze(peaks, risk_target=.10)
        strict = engine.analyze(peaks, risk_target=.05)
        rerun = engine.analyze(peaks, risk_target=.10)
        assert result.top10.equals(rerun.top10)
        assert result.confidence == rerun.confidence and result.margin == rerun.margin
        assert result.accepted == rerun.accepted
        assert result.top1["connectivity_id"] == strict.top1["connectivity_id"]
        assert result.top1["similarity"] == strict.top1["similarity"]
        assert result.confidence == strict.confidence and result.margin == strict.margin
        assert len(result.top10) == 10
        assert result.top10.connectivity_id.nunique() == 10
        assert result.top10["rank"].astype(int).tolist() == list(range(1, 11))
        s = result.top10.similarity.to_numpy(dtype=float)
        assert np.isfinite(s).all() and np.all(np.diff(s) <= 1e-12)
        assert (0 <= result.confidence <= 1 and np.isfinite(result.margin))
        assert result.top1["connectivity_id"] == str(result.top10.iloc[0].connectivity_id)
        assert result.accepted == (result.confidence >= 0.87)
        assert strict.accepted == ((result.confidence >= 0.94) and (result.margin >= 0.20))
        assert result.warnings and all(isinstance(w, str) for w in result.warnings)
        assert any("not certified" in w.lower() for w in result.warnings)
        assert any("stereochemistry" in w.lower() for w in result.warnings)
        assert not result.ri_delta_top1 and result.conformal90_size is None
        b10 = batch10.loc[batch10.spectrum_id == sid].iloc[0]
        b05 = batch05.loc[batch05.spectrum_id == sid].iloc[0]
        assert b10.top1_connectivity_id == result.top1["connectivity_id"] == b05.top1_connectivity_id
        assert np.isclose(b10.historical_HGB_score, result.confidence, atol=1e-12, rtol=0)
        assert np.isclose(b10.top1_top2_cosine_margin, result.margin, atol=1e-12, rtol=0)
        assert b10.historical_acceptance_rule_met == result.accepted
        assert b05.historical_acceptance_rule_met == strict.accepted
        assert b10.source_independent_risk_certified == False
        assert b05.source_independent_risk_certified == False
        assert b10.source_msp_sha256 == EXPECTED_SHA256
        assert b10.reference_index_sha256 == V2_REFERENCE_SHA256
        assert b10.model_sha256 == V2_HGB_SHA256
        assert int(b10.reference_first14_n) == V2_N_REFERENCE == 8455

        # Top1-only baseline uses the *same* fixed frozen result, stripped to
        # fields; NOT a benchmarking claim about any external EI software.
        baseline = {
            "top1_first14": str(result.top1["connectivity_id"]),
            "top1_name": str(result.top1["display_name"]),
            "top1_similarity": float(result.top1["similarity"])
        }
        enhanced = dict(baseline, frozen_HGB_score=result.confidence,
            top1_top2_margin=result.margin,
            historical_rule_10_met_UNCERTIFIED=bool(result.accepted),
            historical_rule_5_met_UNCERTIFIED=bool(strict.accepted),
            n_ranked_candidates=10,
            publisher_identity_label_authenticated=False,
            chemical_identity_independently_confirmed=False,
            future_risk_guaranteed=False,
            has_plain_language_uncertainty_warnings=True,
            source_msp_sha256=EXPECTED_SHA256,
            reference_index_sha256=V2_REFERENCE_SHA256,
            model_sha256=V2_HGB_SHA256,
            previous_609_cases_newly_tested=False)
        assert all(baseline[x] == enhanced[x] for x in baseline)
        out_rows.append({"spectrum_id":sid, **enhanced})
        for rec in result.top10.to_dict(orient="records"):
            top10.append({
                "spectrum_id":sid, "rank":int(rec["rank"]),
                "candidate_first14":str(rec["connectivity_id"]),
                "display_name":str(rec["display_name"]),
                "formula":str(rec["formula"]),
                "EI_similarity":float(rec["similarity"]),
            })
    examples = pd.DataFrame(out_rows)
    rankings = pd.DataFrame(top10)
    assert len(examples) == 12 and len(rankings) == 120
    assert rankings.groupby("spectrum_id")["rank"].nunique().eq(10).all()
    assert examples.spectrum_id.is_unique
    assert examples.future_risk_guaranteed.eq(False).all()
    assert examples.chemical_identity_independently_confirmed.eq(False).all()
    assert examples.has_plain_language_uncertainty_warnings.eq(True).all()
    examples.to_csv(out / "12_preexisting_cases_full_vs_top1_mock.csv", index=False, float_format="%.17g")
    rankings.to_csv(out / "120_ranked_existing_demo_candidates.csv", index=False, float_format="%.17g")
    return {
        "n_preexisting_unlabelled_examples":12,
        "n_ranked_candidates":120,
        "source_SHA256":EXPECTED_SHA256,
        "reference_SHA256":V2_REFERENCE_SHA256,
        "model_SHA256":V2_HGB_SHA256,
        "all_12_have_10_unique_ranked_candidates":True,
        "all_12_have_provenance_warnings_and_uncertified_flags":True,
        "all_12_preserve_top1_in_top1_only_mock":True,
        "all_12_preserve_top1_across_rules":True,
        "all_12_preserve_top1_single_vs_batch":True,
        "all_12_pass_numerically_identical_repeat_inference":True,
        "10_historical_rule_met_n":int(examples.historical_rule_10_met_UNCERTIFIED.sum()),
        "5_historical_rule_met_n":int(examples.historical_rule_5_met_UNCERTIFIED.sum()),
        "not_a_human_usability_study":True,
        "not_a_prospective_identity_accuracy_study":True,
    }


def main():
    pa = argparse.ArgumentParser()
    pa.add_argument("--source-609", type=Path, required=True)
    pa.add_argument("--source-466", type=Path, required=True)
    pa.add_argument("--out", type=Path, default=Path(".cache/phase5_utility"))
    pa.add_argument("--skip-live-demo", action="store_true")
    a=pa.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    allmetrics=[]
    for role,source in [("609",a.source_609),("466",a.source_466)]:
        allmetrics += routing(input_ledger(source,role),role)
    df=pd.DataFrame(allmetrics)
    assert len(df)==4 and df.n.tolist()==[609,609,466,466]
    df.to_csv(a.out/"retrospective_review_routing.csv", index=False)
    summary={
        "scope":"ALREADY_SPENT_SOURCE_LABELS; descriptive software reporting, not novel chemical validation",
        "original_ledger_SHA256":LEDGERS,
        "n_role_609":609, "n_role_466":466,
        "risk5_risk10_certified":False,
        "source_acquisition_independence_proven":False,
        "top1_only_baseline":"AUTHOR-CONSTRUCTED reporting mock, NOT benchmark against other MS software",
        "routing":allmetrics,
    }
    if not a.skip_live_demo:
        summary["existing_example_software_checks"]=twelve_examples(a.out)
    (a.out/"summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    print(json.dumps(summary,indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
