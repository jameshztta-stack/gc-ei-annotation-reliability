#!/usr/bin/env python3
"""Evidence-audited manuscript integrity gate; NOT a peer review or truth validation.

Reconciles locked manuscript text against verified historical numeric ledgers,
publisher metadata summaries, frozen-v2 app features, and restriction language.
No model fit, original spectra download, new chemical identity labels, or
threshold search takes place.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TITLE = "PHASE6_COMPLETE_MANUSCRIPT_WORKING_DRAFT_20261015.md"
SI = "PHASE6_SUPPLEMENTARY_DATA_AND_EXCEPTION_EVIDENCE_20261015.md"
NUMERIC = "phase3_paired_summary.json"


def ensure(statement, msg):
    if not statement:
        raise AssertionError(msg)


def has(s, target):
    ensure(target in s, f"Required text absent: {target}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit-source", type=Path, required=True)
    p.add_argument("--provenance-source", type=Path, required=True)
    p.add_argument("--numeric-source", type=Path,
                   default=ROOT/"audits/phase3_retrospective_confidence_20261014"/NUMERIC)
    p.add_argument("--out", type=Path, default=ROOT/".cache/phase6_manuscript_gate.json")
    a = p.parse_args()

    art=(ROOT/"docs"/TITLE).read_text(encoding="utf-8")
    si=(ROOT/"docs"/SI).read_text(encoding="utf-8")
    app=(ROOT/"app.py").read_text(encoding="utf-8")
    engine=(ROOT/"gcei/v2_engine.py").read_text(encoding="utf-8")
    frozen=json.loads((ROOT/"models/v2/release_manifest.json").read_text(encoding="utf-8"))
    n=json.loads(a.numeric_source.read_text(encoding="utf-8"))
    ch=json.loads(a.audit_source.read_text(encoding="utf-8"))
    prov=json.loads(a.provenance_source.read_text(encoding="utf-8"))

    checks=[]
    def pass_(msg,cond):
        ensure(cond,msg);checks.append(msg)

    pass_("main manuscript and SI contain appropriately scoped EI software article",
          "GC–EI–MS" in art and "Streamlit" in art and "source" in si)
    pass_("frozen 8455 not mislabeled as old v1 8543",
          frozen["reference_first14_n"]==8455
          and "**8,455**" in art and "**8,543**" in si
          and "older v1" in si)
    pass_("current v2 model and original source/index exact hashes",
          all(z in art and z in si for z in [
           frozen["original_MS_DIAL_SHA256"],frozen["research_v2_reference_index_SHA256"],
           frozen["exact_model_sha256"]]))
    pass_("original reference source statistics and reference manifest",
          "**13,111**" in art and "**8,455**" in art and "28,220" in art)

    pass_("original development and heldout denominators",
          n["n"]["dev1410"]==1410 and n["n"]["test609"]==609
          and n["n"]["retrospective466"]==466
          and "1,410" in art and "609" in art and "466" in art)
    pass_("all original 609 marked spent & in-library",
          "permanently" in art.lower() and "in reference" in art.lower()
          and "within-MS-DIAL" in art)
    pass_("466 origins and first14 unique numbers correct",
          n["n"]["distinct_466_first14"]==419 and n["n"]["prior466overlap_in_609"]==69
          and "370 SWGDRUG" in art and "96 RECETOX" in art
          and "419 unique" in art and "69 of 609" in art)
    pass_("MSDIAL source-label top1/top5/top10 counts unchanged",
          n["correct"]["test609"]==394 and all(x in art for x in
          ["394/609", "489/609", "509/609"]))
    pass_("retrospective 466 source label top1 count unchanged",
          n["correct"]["retrospective466"]==334 and "334/466" in art)
    pass_("AUROC exact source archive numerical concordance",
          abs(n["comparison"]["test609"]["HGB"]["AUROC"]-.8633042143784677)<1e-12
          and abs(n["comparison"]["test609"]["margin"]["AUROC"]-.812678550348247)<1e-12
          and abs(n["comparison"]["test609"]["similarity"]["AUROC"]-.7066816196434895)<1e-12
          and all(x in art for x in ["0.86330","0.81268","0.70668"]))
    pass_("probability Brier and calibration use HGB, not raw cosine",
          abs(n["comparison"]["test609"]["HGB"]["Brier"]-.14064475004139237)<1e-12
          and abs(n["calibration"]["test609"]["ECE10"]-.04493789489416912)<1e-12
          and "0.140645" in art and "0.04494" in art)
    pass_("609 matched K198 nuance HGB not universal winner",
          n["matched_coverage"]["test609"]["198"]["HGB"]["wrong"]==12
          and n["matched_coverage"]["test609"]["198"]["margin"]["wrong"]==11
          and "margin-only" in art and "12" in art and "11" in art)
    pass_("historical acceptance/scope fixed and not certified",
          "10%-target" in art and "5%-target" in art
          and "certified future error bound" in art and "prospective" in art
          and bool(frozen["10pct_rule"]["certified"]) is False
          and bool(frozen["5pct_rule"]["certified"]) is False)
    pass_("4 historical review routing cells reported",
          all(z in art for z in ["203", "208", "215", "356", "120", "161", "132", "309"]))
    pass_("chemistry exception counts from source-forensics JSON",
          ch["within_14char_connectivity_full_advanced_identity_diversity_groups"]==294
          and ch["retained_name_review_only_rows"]==373
          and ch["retained_advanced_molecular_identifier_mismatch_count"]==6
          and len({x["connectivity"] for x in ch["six_advanced_molecular_identifier_exception_cases"]})==4
          and all(z in si for z in ["**294**","**373**","**six**","**four**"]))
    pass_("raw-source fingerprint collision exact 4 original rows",
          ch["exact_retained_original_source_identifier_conflict_group_count"]==1
          and len(ch["exact_spectral_group_source_rows"])==4
          and ch["retained_representative_in_collision"]==1799
          and "1799" in si and "1073" in si and "15077" in si and "15803" in si)
    pass_("source provenance ledger instrument type and license coverage",
          prov["retained_spectra"]==13111
          and prov["field_coverage"]["INSTRUMENTTYPE"]["nonempty"]==211
          and prov["field_coverage"]["LICENSE"]["nonempty"]==11992
          and 13111-11992==1119
          and "**1,119**" in si and "211/13,111" in si)
    pass_("non-independence of original lab acquisitions clearly disclosed",
          prov["verified_disjoint_original_acquisitions"]==0
          and "independent" in si.lower() and
          "not" in art.lower() and "authentic" in art.lower())
    pass_("same current EI-only v2 feature no-RI/no conformal mixing",
          frozen["v1_conformal_or_RI_reused"]==False
          and "absent RI fusion" in art
          and "no RI" in si
          and "RI fusion" in engine)
    pass_("current batch UI exports only top1 per input, single top10",
          "result.top10.to_csv" in app
          and "results.to_csv" in app
          and "one top-hit summary row" in art
          and "12×10" not in art)
    pass_("12 unlabelled demo + 120 engine top10 and human-study limitations",
          "120" in art and "12" in art and "human usability" in art
          and "authentic" in art.lower())
    pass_("specified software release and data DOIs anchored",
          "10.5281/zenodo.21910638" in art
          and "10.5281/zenodo.23373447" in art
          and "10.5281/zenodo.23373447" in si)
    pass_("published source prior-art citations use exact DOI anchors",
          all(z in art for z in ["10.1016/1044-0305(94)87009-8",
          "10.1016/1044-0305(94)85022-4", "10.1002/cem.2665",
          "10.1021/jasms.4c00451"]))
    pass_("unresolved final author and rights approval are not fabricated",
          "AUTHOR APPROVAL REQUIRED" in art and
          "licensing" in si.lower() and
          "not yet" in art.lower())

    out={"status":"PASS","checks":checks,"checks_n":len(checks),
         "scope":"MANUSCRIPT-CHECK, NOT PEER REVIEW / PHYSICAL ID TRUTH",
         "source":{"chemical":str(a.audit_source),"provenance":str(a.provenance_source),
                   "numeric":str(a.numeric_source)},
         "manuscript":str(ROOT/"docs"/TITLE)}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":out["status"],"checks_n":len(checks),"check_names":checks},indent=2))


if __name__ == "__main__":
    main()
