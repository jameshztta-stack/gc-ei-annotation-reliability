"""Reconstruct source-level chemical eligibility and reference selection.

Runs from original publisher MSP with its expected SHA-256. Generated reference
index must match the installed software's exact reference-index bytes.
The exercise checks database labels, not independently authenticated identities.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,tempfile
from collections import Counter
from pathlib import Path
from rdkit import rdBase
from gcei.bootstrap import _download_source
from gcei.reference_builder import EXPECTED_SHA256,parse_msp
from reproducibility.chemical_selection import audit_record,choose_valid_exact_spectra,plan_partitions,sha_of_path
from reproducibility.chemical_policy import calc_semantic_pool
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"models/v2/reference_index.csv"
INDEX_SHA="2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01"


def reconstruct(source):
    assert sha_of_path(source)==EXPECTED_SHA256,"Original source checksum mismatch"
    raw=parse_msp(source)
    assert len(raw)==28220
    checks=[audit_record(i,s) for i,s in enumerate(raw)]
    _,_,excluded,review=calc_semantic_pool(raw,checks)
    chosen,rejected,conflicts,npatterns,mixed=choose_valid_exact_spectra(raw,checks)
    assert len(chosen)==13111 and not conflicts and npatterns==14146
    assert len(excluded)==150
    plan=plan_partitions(chosen)
    refs=plan["candidate_reference_rows"]
    assert len(refs)==8455 and plan["query_eligible_groups"]==2019
    roles=plan["identities_in_partitions"]
    assert roles=={"similarity_development":201,"confidence_fit":383,
                   "risk_threshold_calibration":403,"conformal_calibration":423,
                   "untouched_independent_test":609}
    output=io.StringIO(newline="")
    writer=csv.DictWriter(output,fieldnames=["connectivity","reference_source_index"],lineterminator="\r\n")
    writer.writeheader();writer.writerows(refs)
    generated=output.getvalue().encode("utf-8")
    actual=hashlib.sha256(generated).hexdigest()
    # Some CSV archive writers use platform-specific newlines; compare row identities first.
    with INDEX.open(newline="",encoding="utf-8") as f: original=list(csv.DictReader(f))
    assert refs==[{"connectivity":z["connectivity"],"reference_source_index":int(z["reference_source_index"])} for z in original]
    assert hashlib.sha256(INDEX.read_bytes()).hexdigest()==INDEX_SHA
    return {"original_source_spectra":28220,"retained_unique_spectral_fingerprints":len(chosen),
      "reference_connectivity_identities":len(refs),"distinct_query_connectivities":2019,
      "designated_development_connectivities":1410,"retrospective_within_source_queries":609,
      "source_name_warnings":len(review),"source_structure_quarantine":len(excluded),
      "source_chemical_truth_independently_verified":False,"source_data_sha256":EXPECTED_SHA256,
      "reference_index_sha256":INDEX_SHA,"rdkit_version":rdBase.rdkitVersion}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--msp",type=Path,help="Exact local copy of MS-DIAL MSP; otherwise fetch original")
    p.add_argument("--output",type=Path,help="Write summary JSON locally")
    a=p.parse_args()
    if a.msp: res=reconstruct(a.msp)
    else:
      with tempfile.TemporaryDirectory() as td:
        source=Path(td)/"MSDIAL.msp"
        _download_source(source)
        res=reconstruct(source)
    if a.output:
      a.output.parent.mkdir(parents=True,exist_ok=True)
      a.output.write_text(json.dumps(res,indent=2)+"\n")
    print(json.dumps(res,indent=2))
if __name__=="__main__":main()
