"""Chemical-name and molecular-structure consistency rules for the EI reference source."""
from __future__ import annotations
from collections import Counter
import csv,hashlib,re
from pathlib import Path
from rdkit import Chem
from reproducibility.chemical_selection import structure,sha_of_path

# These regexes explicitly encode *screening* logic; they are not exhaustive
# chemical-name resolvers. If an indicated substituent is missing from the
# computed structure, the EI spectrum is quarantined from molecular-truth use.
DERIVATIVE_RULES = [
    ("TMS_without_Si", re.compile(
        r"(?i)(?<![A-Z0-9])(?:[1-9][0-9]*)?\s*(?:TMS|TRIMETHYLSILYL)\b"),"Si"),
    ("other_silyl_without_Si", re.compile(
        r"(?i)\b(?:TBDMS|TBS-deriv(?:ative)?|TBDPS|TRIETHYLSILYL|"
        r"TERT[- ]?BUTYLDIMETHYLSILYL|SILYLATED|SILYLATION)\b"),"Si"),
    ("methoxime_without_N", re.compile(
        r"(?i)\b(?:METHOXIME|METHOXYIMINO|MEOX|MOX)\b"),"N"),
    ("pentafluorobenzyl_without_F", re.compile(
        r"(?i)\b(?:PENTAFLUOROBENZYL|PFB[- ]?DERIV)\b"),"F"),
]

ESTER_CLAIMS = [
    ("methyl_ester_name_but_no_methyl_ester_structure",
     re.compile(r"\bmethyl\s+ester\b", re.I),
     Chem.MolFromSmarts("[CX3](=[OX1])[OX2][CH3]")),
    ("ethyl_ester_name_but_no_ethyl_ester_structure",
     re.compile(r"\bethyl\s+ester\b", re.I),
     Chem.MolFromSmarts("[CX3](=[OX1])[OX2][CH2][CH3]")),
]

REVIEW_ONLY = {
    "name_mentions_deriv_without_formula_test":
        re.compile(r"(?i)\b(?:derivative|derivatized|derivatisation|derivatization|"
                   r"acetylated|methyl ester|ethyl ester|methoxylated)\b"),
    "name_qualifier_not_identity":
        re.compile(r"(?i)(?:\bminor\b|\bsimilar to\b|\bsim to\b|"
                   r"\bputative\b|\btentative\b|\bisomer\b)"),
}
def derivation_flags(record):
    name=record.get("NAME","").split(";")[0].strip()
    struct=structure(record.get("SMILES",""))
    if not struct: return [],[]
    formula=struct["formula"]
    hard=[rule for rule,regex,element in DERIVATIVE_RULES
          if regex.search(name) and element not in formula]
    # Validate carboxylate methyl/ethyl ester naming at substructure level.
    try:
        mol=Chem.MolFromSmiles(record.get("SMILES","").strip())
    except Exception:
        mol=None
    if mol is not None:
        for label,claim_regex,smarts in ESTER_CLAIMS:
            if claim_regex.search(name) and not mol.HasSubstructMatch(smarts):
                hard.append(label)
    soft=[rule for rule,regex in REVIEW_ONLY.items() if regex.search(name)]
    return hard,soft

def save_csv(path,items,columns):
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        writer.writerows(items)

def fingerprint(path):
    return sha_of_path(Path(path))

def calc_semantic_pool(raw, strict_annot):
    rawflags=Counter()
    softflags=Counter()
    exclusions=[]
    warning_rows=[]
    # *Before* deduplication so a valid record is never overwritten by a
    # chemically suspect exact-spectrum duplicate.
    for i,rec in enumerate(raw):
        hard,soft=derivation_flags(rec)
        if hard:
            for k in hard:rawflags[k]+=1
            if strict_annot[i]["strict_eligible"]:
                strict_annot[i]["strict_eligible"]=False
                exclusions.append({"source_index":i,
                                   "name":rec.get("NAME","").split(";")[0],
                                   "structure_connectivity":strict_annot[i]["derived_conn"],
                                   "flags":";".join(hard),
                                   "source_inchikey":rec.get("INCHIKEY","")})
        if soft:
            for k in soft:softflags[k]+=1
            warning_rows.append({"source_index":i,
                                 "name":rec.get("NAME","").split(";")[0],
                                 "flags":";".join(soft),
                                 "source_inchikey":rec.get("INCHIKEY","")})
    return rawflags,softflags,exclusions,warning_rows

def cp_upper(k,n,alpha=.05):
    return float(beta.ppf(1-alpha,k+1,n-k)) if k<n else 1.0

def data_invariants(chosen,pair_rows,refs,nall):
    ids={x["connectivity"] for x in chosen}
    refmap={x["connectivity"]:x for x in refs}
    qpids={x["connectivity"] for x in pair_rows}
    roles=Counter(x["role"] for x in pair_rows)
    assert len(ids)==len(refs)
    assert len(refmap)==len(refs)
    assert len(qpids)==len(pair_rows)
    assert qpids.issubset(ids)
    assert all(x["reference_source_index"]!=x["query_source_index"] for x in pair_rows)
    assert all(x["reference_spectrum_sha256"]!=x["query_spectrum_sha256"] for x in pair_rows)
    assert all(refmap[x["connectivity"]]["reference_source_index"]==x["reference_source_index"]
               for x in pair_rows)
    assert len({x["spectrum_sha256"] for x in chosen})==len(chosen)
    assert len({x["source_index"] for x in chosen})==len(chosen)
    assert all(0 <= int(x["source_index"])<nall for x in chosen)
    assert len({x["reference_source_index"] for x in pair_rows}
               |{x["query_source_index"] for x in pair_rows})==2*len(pair_rows)
    # Any reference/ query occurrence must correspond to an eligible chosen spectrum.
    byid_idx={(x["connectivity"],x["source_index"]):x["spectrum_sha256"] for x in chosen}
    for x in pair_rows:
        assert byid_idx[(x["connectivity"],x["reference_source_index"])]==x["reference_spectrum_sha256"]
        assert byid_idx[(x["connectivity"],x["query_source_index"])]==x["query_spectrum_sha256"]
    return {
        "unique_candidate_identities":len(ids),
        "unique_query_identities":len(qpids),
        "total_spectral_rows":len(chosen),
        "roles":dict(roles),
        "all_independent_invariants_passed":True,
    }
