"""Molecular-structure checks, spectral deduplication and deterministic source partitioning."""
from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
import csv
import hashlib
import json
import re
import tempfile
import numpy as np
from rdkit import Chem, RDLogger, rdBase
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

from gcei.bootstrap import _download_source
from gcei.reference_builder import EXPECTED_SHA256, parse_msp

RDLogger.DisableLog("rdApp.*")

def exact_key(peaks):
    from collections import defaultdict
    d=defaultdict(float)
    for mass,intensity in peaks: d[mass]+=intensity
    return tuple(sorted((m,round(i,8)) for m,i in d.items() if i>0))
VALID_KEY = re.compile(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$")
BAD_SMILES = {
    "", "n/a", "na", "none", "null", "unknown", "-", "?",
    "like tag compound", "labeled compound", "contaminated compound",
    "not available",
}
HALOGEN = {"F", "Cl", "Br", "I"}
SALT_NAME = re.compile(
    r"(?:ammonium|phosphonium|pyridinium|imidazolium|sulfonium)",
    flags=re.IGNORECASE,
)
ISOTOPE_NAME = re.compile(r"\b(?:13c|15n|d[0-9]+|deuterated|isotope.label|isotopic.label)\b",
                          flags=re.IGNORECASE)
ALLOCATION = [("similarity_development", 0.10),
              ("confidence_fit", 0.19),
              ("risk_threshold_calibration", 0.20),
              ("conformal_calibration", 0.21),
              ("untouched_independent_test", 0.30)]
SEED = 20261013

@lru_cache(maxsize=65000)
def structure(smiles):
    s=(smiles or "").strip()
    if s.lower() in BAD_SMILES:
        return None
    try:
        m=Chem.MolFromSmiles(s)
        if m is None or m.GetNumAtoms()==0: return None
        return {
            "key":Chem.MolToInchiKey(m),
            "formula":CalcMolFormula(m),
            "nheavy":m.GetNumHeavyAtoms(),
            "only_monatomic_halide":(
                m.GetNumAtoms()==1 and m.GetAtomWithIdx(0).GetSymbol() in HALOGEN),
            "has_isotope":any(a.GetIsotope() > 0 for a in m.GetAtoms()),
        }
    except Exception:
        return None

def audit_record(index, rec):
    ik=rec.get("INCHIKEY","").strip()
    name=rec.get("NAME","").split(";")[0].strip()
    smiles=rec.get("SMILES","").strip()
    formula=rec.get("FORMULA","").strip()
    s=structure(smiles)
    flags=[]
    if s is None: flags.append("unverifiable_smiles")
    if not VALID_KEY.fullmatch(ik): flags.append("noncanonical_full_inchikey")
    if not formula: flags.append("formula_missing")
    if s is not None:
        if ik[:14] != s["key"][:14]: flags.append("structure_connectivity_disagreement")
        if formula and formula != s["formula"]: flags.append("formula_disagreement")
        if s["only_monatomic_halide"] and SALT_NAME.search(name):
            flags.append("compound_name_but_structure_is_counterion")
        if ISOTOPE_NAME.search(name) and not s["has_isotope"]:
            flags.append("name_mentions_isotope_but_structure_not_isotopic")
    strict = not flags
    return {
        "original_index": index,
        "source_key":ik,
        "name": name,
        "smiles": smiles,
        "formula": formula,
        "derived_key": s["key"] if s else "",
        "derived_conn": s["key"][:14] if s else "",
        "derived_formula":s["formula"] if s else "",
        "source_firstblock":ik[:14],
        "flags":flags,
        "strict_eligible":strict,
    }

def sha_of_path(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def stable_spectral_fingerprint(peaks):
    return hashlib.sha256(repr(exact_key(peaks)).encode("utf-8")).hexdigest()

def choose_valid_exact_spectra(raw, records):
    # Deduplication is performed *after* chemical adjudication.
    by_spectrum=defaultdict(list)
    for i,r in enumerate(raw):
        by_spectrum[stable_spectral_fingerprint(r.get("peaks",[]))].append(i)
    chosen=[]
    rejected=Counter()
    conflicts=[]
    duplicate_source_conflicts=0
    for sp, source_indices in by_spectrum.items():
        ids=[i for i in source_indices if records[i]["strict_eligible"]]
        if not ids:
            rejected["spectra_without_strict_structure_supported_record"]+=1
            continue
        derived={records[i]["derived_conn"] for i in ids}
        if len(derived) > 1:
            rejected["exact_spectrum_shared_by_multiple_supported_connectivities"]+=1
            conflicts.append({"spectrum_sha256":sp, "source_record_indices":ids[:20],
                              "different_derived_connectivities":sorted(derived)})
            continue
        mixed_source=len({records[i]["source_firstblock"] for i in source_indices})>1
        if mixed_source:duplicate_source_conflicts+=1
        chosen_id=min(ids)
        chosen.append({"source_index":chosen_id,
                       "connectivity":records[chosen_id]["derived_conn"],
                       "spectrum_sha256":sp,
                       "duplicate_raw_records":len(source_indices),
                       "raw_source_identifier_conflict":mixed_source})
    return chosen, dict(rejected), conflicts, len(by_spectrum), duplicate_source_conflicts

def plan_partitions(chosen):
    by_id=defaultdict(list)
    for row in chosen:by_id[row["connectivity"]].append(row)
    singletons={k:v for k,v in by_id.items() if len(v)==1}
    eligible={k:v for k,v in by_id.items() if len(v)>=2}
    # Identity labels are assigned exactly once to one of the five partitions.
    rng=np.random.default_rng(SEED)
    keys=np.asarray(sorted(eligible))
    perm=list(map(str,rng.permutation(keys)))
    n=len(perm)
    counts=[int(n*p) for label,p in ALLOCATION[:-1]]
    counts.append(n-sum(counts))
    splits={}
    start=0
    for (name,_), count in zip(ALLOCATION,counts):
        members=sorted(perm[start:start+count]);start+=count
        splits[name]=members
    assert start==n and len(set(perm))==n
    assert set().union(*(set(v) for v in splits.values()))==set(eligible)
    for i,(a,vs) in enumerate(splits.items()):
        for b,ws in list(splits.items())[i+1:]:
            assert not (set(vs)&set(ws)), (a,b)
    pair_rows=[]
    for group in sorted(eligible):
        candidate=sorted(by_id[group],key=lambda d:d["source_index"])
        pick=rng.permutation(len(candidate))[:2]
        ref=candidate[int(pick[0])]
        query=candidate[int(pick[1])]
        assert ref["source_index"] != query["source_index"]
        assert ref["spectrum_sha256"] != query["spectrum_sha256"]
        partition=next(k for k,members in splits.items() if group in members)
        pair_rows.append({
            "connectivity":group,
            "role":partition,
            "reference_source_index":ref["source_index"],
            "query_source_index":query["source_index"],
            "reference_spectrum_sha256":ref["spectrum_sha256"],
            "query_spectrum_sha256":query["spectrum_sha256"],
        })
    assert len(pair_rows)==n
    assert all(r["connectivity"] in by_id for r in pair_rows)
    assert all(k not in eligible for k in singletons)
    return {
        "identity_pool_total":len(by_id),
        "query_eligible_groups":n,
        "singleton_candidate_only_groups":len(singletons),
        "distinct_spectra":len(chosen),
        "identities_in_partitions":{k:len(v) for k,v in splits.items()},
        "pair_rows":pair_rows,
        "singleton_rows":[{"connectivity":k, "reference_source_index":v[0]["source_index"],
                           "reference_spectrum_sha256":v[0]["spectrum_sha256"]}
                          for k,v in sorted(singletons.items())],
        "candidate_reference_rows": [
             {"connectivity":k,"reference_source_index":next(
                 (row["reference_source_index"] for row in pair_rows
                  if row["connectivity"]==k),v[0]["source_index"])}
             for k,v in sorted(by_id.items())],
    }

def write_csv(path, rows, keys):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
