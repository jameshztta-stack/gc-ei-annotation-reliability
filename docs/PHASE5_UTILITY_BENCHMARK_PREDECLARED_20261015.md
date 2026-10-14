# Phase 5 — Predeclared Computational Software-Utility Comparator (2026-10-15)

**Designed prior to implementation of the new Phase 5 outputs.** This is a descriptive engineering and previously-SPENT data reuse study; no new independent experimental cases, truth labels, users, survey, model fitting, model selection, or prospective 5%/10% risk guarantee. Existing 609/466 values have already been seen. Data are fixed to source commit `9d5c57a44e57d3eed94c82930c2868e451573676`, the exact archival SHA checks below. **Primary scientific task is still first14 *publisher label* agreement when identity is in the search reference.**

## Motivation and pre-specified comparator

A transparent **author-constructed top1-only reporting mock**, NOT NIST, MS-DIAL, AMDIS, FastEI or another external benchmarked system, displays only an already-computed top candidate name/connectivity ID and its EI similarity. It does **not** certify identity, nor does it imply responsible users would uncritically accept the match. It lacks an *automated* study-specific first-hit correctness score, the frozen study's two rule flags, the top10 evidence table and frozen source/provenance fields.

Compare with the REAL frozen v2.0.2 end-to-end engine on the repository's 12 **pre-existing** botanical example input spectra; the app reports top1, top10, margin, HGB, historical acceptance rule, source/model/index SHA and explicit warnings. These botanical inputs are **NOT authenticated chemical truth** and **cannot be used to estimate identification accuracy**. All observations are software facts, not a human usability result.

## Prespecified endpoints

1. **Feature-contract completeness** for every one of 12 example spectra (binary yes/no per case, not a new chemical-performance score):
   - 10 unique ranked first14 candidate rows, ranks exactly 1…10, rank-one equals baseline top1; descending nonincreasing EI cosine.
   - original top1 name, connectivity first14 and similarity exactly preserved across historical .10/.05 decision choice and batch/single modes; no top1 change from HGB.
   - finite [0,1] HGB score, finite top1-top2 margin, old 10% and 5% rule booleans, explicit uncertified warning, original SHA-pinned source/index/model outputs, `chemical_identity_independently_confirmed=False`.
   - source and model pins not modified, no v1 RI/conformal/registration claim.
   - output JSON+CSV; one CSV row per query and 10 candidate rows per query; exact 12-case denominators. Export schema must be deterministic across two sequential runs (byte-identical CSV for same frozen environment); do not claim this across arbitrary Python versions.

2. **Retrospective decision *review-routing* accounting** using ONLY originally fixed historical rules, no tuning:
   - For 609 MS-DIAL spent within-source cases and 466 source-selected spent cross-collection cases **separately**, calculate all four cells of (source first14 agreement yes/no) × (accept historical rule yes/no).
   - Report accepted total, accepted correct, accepted wrong, rejected correct, rejected wrong, fraction of previously incorrect first14 hits flagged for extra review, fraction of previously correct first14 hits also flagged. Do NOT say chemical misidentifications prevented, errors reduced in a real deployment, or "sensitivity" of true chemical detection.
   - The **top1-only mock** has NO automatic review flag. For illustration ONLY, a hypothetical `accept-all` automation would pass every existing rank-one candidate and thus all source mismatches, but this is not an assertion about established software or user behavior.
   - Evaluate original fixed `HGB >= 0.87` (.10) and `HGB >= 0.94 AND margin >= 0.20` (.05), no posthoc operating point selection. Report raw label mismatch counts and uncertainty/independence limits. First14 counts checked against known values.
   - Paired comparison with margin or cosine already exists in Phase 3; reference Phase 3 rather than claiming first-time algorithm superiority.

3. **Machine-checkable audit/disclosure fields**: each app output has at least the three immutable SHA identifiers and explicit non-certification fields. Report coverage `12/12` if true (engineering check), not enhanced identification accuracy. Check exact schema, not merely written descriptions.

## Source and data protection
- 609 original one-shot ledger SHA `62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7` (now SPENT).
- 466 source-selected retrospective ledger SHA `09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b` (now SPENT).
- 12 **already-shared** example spectra in `examples/example_batch_12_botanical.csv`. Source chemical origin and specimen identity unverified.
- Build is pinned original 28,220 MSP + HGB model + reference. Source EI archives NOT redistributed; only summaries and example-derived outputs are archived.

## Predeclared internal auditor tests
- Hard fail on missing columns, wrong SHA, incorrect denominators, missing flags, apparent changed top1, duplicated candidate identities/ranks, nonfinite numbers, false future-risk certification, inconsistency of rule outcomes with stored confidence/margin.
- Hard fail on a false "100% independent identification" or "improved HGB retrieval" claim in any generated metadata. Reports must identify all 609+466 as historical and botanical example as unlabelled.
- Confirm exposure/audit against already published Phase 3 counts; any discrepancy is disclosed rather than disguised as novel testing.

## Interpretation gate
**Permissible:** An auditable browser-based software workflow supports top10 candidate review, reproducible file-based output, traceable reference/model versions and flags for further verification. In two source-labelled retrospective cohorts, report actual tradeoffs in which first-hit source matches would be flagged.
**Not permissible:** Enhanced real-world patient/food safety, improved chemical authentication, experimentally proven accessibility, user study success, formal prospective selective error, state-of-the-art head-to-head, unique confidence science. Merely supplying more report fields is not strong algorithmic novelty. Human workflow superiority is untested.

**Success means software-specific use-case evidence, NOT proof that Q1 innovation threshold is met.** The code and journal manuscript must retain this distinction.
