# Phase 5 — Verified Software Utility and Source-Label Review-Routing Results
**Date:** 15 October 2026 (Asia/Kolkata). **Status: computational verification PASSED; novelty/reviewer acceptability NOT certified.**

**Primary evidence:** Phase 5 GitHub Actions [38618746013](https://github.com/jameshztta-stack/gc-ei-annotation-reliability/actions/runs/38618746013) completed SUCCESS, pinned historical ledgers and actual frozen v2 example engine. [UI headless simulation 38619103980](https://github.com/jameshztta-stack/gc-ei-annotation-reliability/actions/runs/38619103980) completed SUCCESS (**2 tests passed**). Phase 4 13 synthetic input-integrity checks previously PASSED; Phase 3 numerical dual implementation and 12 existing-example CI PASSED. Production app, model, reference, original cohorts and installed package versions are untouched.

**Do not misinterpret:** the 609 original within-MS-DIAL benchmark is **permanently spent**, and the selected 466 SWGDRUG/RECETOX rows are **already exposed**. Publisher-provided first14 connectivity labels are NOT authenticated chemical truth. All tested truth identities were intentionally present in the retrieval reference for the 609 test. No unmeasured experimental performances, real-world users, human usability scores or new prospective validations were obtained.

## A. Reconstructed utility: review routing of HISTORICAL top-1 publisher labels

Each cohort independently recomputed from exact original archived CSV, SHA-verified; original fixed rules **not retuned**.

| Already used source panel | Historical screen | Accepted / N | Accepted source-label agrees / wrong | Flagged for further review: source-label wrong / correct | Proportion of wrong source labels flagged | Correct top-1 labels also flagged |
|---|---|---|---|---|---|---|
| Within-source MS-DIAL | no automatic flag (author-created mock) | 609/609 hypothetical accept-all | 394 / 215 | 0 / 0 | 0% by design | 0% by design |
| Within-source MS-DIAL | original 10% target | **198/609 (32.51%)** | **186 / 12** | **203 / 208** | **203/215 (94.42%)** | **208/394 (52.79%)** |
| Within-source MS-DIAL | original 5% target | **38/609 (6.24%)** | **38 / 0** | **215 / 356** | **215/215 (100%)** | **356/394 (90.36%)** |
| Selected SWGDRUG/RECETOX | no automatic flag (author-created mock) | 466/466 hypothetical accept-all | 334 / 132 | 0 / 0 | 0% by design | 0% by design |
| Selected SWGDRUG/RECETOX | original 10% target | **185/466 (39.70%)** | **173 / 12** | **120 / 161** | **120/132 (90.91%)** | **161/334 (48.20%)** |
| Selected SWGDRUG/RECETOX | original 5% target | **25/466 (5.36%)** | **25 / 0** | **132 / 309** | **132/132 (100%)** | **309/334 (92.51%)** |

**The mock is a reporting format, not NIST/AMDIS/FastEI.** It presents exactly the same fixed top-1 hit and similarity as our app but no automatic study-specific review flag. The accept-all interpretation is **hypothetical**, NOT an assertion that other programs automatically confirm all their high-scoring hits or encourage poor analytical interpretation.

These are source-database *disagreements among existing archived observations*, not chemical errors verified by authentic standards, not recorded human review outcomes, not genuine prevented misidentifications. The 10%/5% labels are **historical names, with no valid future error guarantees**; the strict screen has very low acceptance. Flagging correct labels is consequential and **must be reported together with error flags**. Neither target passed formal risk certification. The 466 selected source family has 419 unique first14 reference labels; acquisition-lab independence was not authenticated. Do not combine 609/466 as IID trials, report a p-value implying two independent external laboratories or adjust rules using these outputs.

## B. Audited software feature / output-contract benchmark (no chemistry truth)

The real frozen 8,455-identity v2 engine was rerun on **12 pre-existing botanical-spectrum examples** from the repo, in batch and individually, with the original 10% and 5% historical screening choices. **All 12 example checks passed** and generated **120 ranked candidate rows**, exactly 10 unique connectivity candidates per original example, with deterministic stable descending similarity.

The 12-case checks verify:
- all 12 preserve the exact top1 and similarity in the author-constructed top1-only report and the full report, in the 10% versus 5% modes and single versus batch analysis; **HGB does not rerank/alter chemical retrieval**;
- finite frozen HGB score and top-two margin, rule flags, 10 unique ranked candidates per original example;
- original model / reference-index / MS-DIAL source SHA-256 embedded in export, no missing row, explicit `source_independent_risk_certified=False` and `chemical_identity_independently_confirmed=False`;
- plain-language scope warnings for uncertified risk and unresolved chemical stereochemistry, and no RI/conformal v1 transfer;
- exact numerical parity of two repeated analyses of each input with fixed dependency versions.

The 12 examples are not independent physical sample annotations with known outcomes; **NO identification accuracy/percentage is defined** for them. Software-feature completeness can be 12/12 by design and **does not establish meaningful human adoption, usefulness versus commercial tools, or new algorithmic novelty**.

## C. Headless test of the **actual** Streamlit interface

Independent of the engine-level example check, `streamlit.testing.v1.AppTest` executed `app.py` without render exceptions in both single-spectrum and batch screens. **Two automated UI tests PASSED**, verifying selected input mode, text area / batch template, original 10%-rule UI selection, 8,455 library text and scientifically cautious caveats (tentative connectivity; not guaranteed risk). This checks actual application script and basic programmatic UI interactions, **not live network availability, actual human usability, accessible design compliance or measured user satisfaction**.

Streamlit headless testing is a documented official interface simulation: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest

## D. Externally appropriate software contribution statement

> We implemented a public, browser-accessible, frozen and source-audited GC–EI–MS research application that reports ten connectivity-level reference candidates, quantitative similarity and top-two ambiguity, an estimated publisher-label top-hit correctness score, non-certified review-screening signals, explicit limitations, and machine-readable version provenance. Automated engineering tests verify software integrity and consistent single-/batch-spectrum presentation. Previously published source-label evaluations reveal how different retrospective confidence thresholds route both incorrect and correct library labels for further review; these findings are not external authenticated chemical-identification accuracy or prospective error guarantees.

**Avoid:** "First-ever GI/GC EI reliability tool", "guaranteed correction of 94% of misidentifications", "clinically/analytically validated for all GC–MS", "98% user satisfaction", "validated independent laboratories", "greater performance than NIST/AMDIS/FastEI", "full end-to-end experimental source independence", "error guarantees".

## E. Simulated reviewer verdict after this stage

**Software correctness and traceable functionality: PASS** for actual tested script, 12 example contracts, version-linked exports, source SHA and 2 UI-simulation tests.

**Distinct integrated workflow: defensible as an application-specific engineering deliverable**, but merely adding metadata/checksum/flag fields is *not* a fundamentally new EI algorithm, and other modern library tools also supply top-N candidates, RI and uncertainty-related functions. No actual head-to-head feature review of all major current GC–EI programs was implemented here; do not claim uniqueness or comparative superiority.

**Novel research benefit: CONDITIONAL.** Retrospective review prioritization describes a useful tradeoff in two selected cohorts, but the original confidence margins and correctness probability are established concepts, and the 609/466 are spent. A Q1 software editor may still reject for incremental advancement. To maximize fit, emphasize documented open-source ease of access, data integrity, reporting boundaries, honest comparative descriptive analysis and practical source verification rather than "first novel confidence model".

**Source-independent authentic standard identification: NOT ESTABLISHED**, and not required to *write* a scoped computational paper, though journal editors might require it for strong analytical-accuracy assertions.

**Formal prospective 10%/5% error certification: FAILED/NOT PROVEN**. Not mandatory to fix for a *descriptive* software methods publication; must not imply certification in title/abstract or interface.

**Submission:** safe to progress to complete manuscript + supplement + actual external human scientific review; **not yet a Q1 acceptance-ready guarantee**.

## Files and reproducibility

- Design frozen before Phase 5 execution: `docs/PHASE5_UTILITY_BENCHMARK_PREDECLARED_20261015.md`.
- Source-pinned evaluator: `scripts/phase5_quantitative_software_utility.py`; GitHub workflow: `.github/workflows/phase5-quantitative-software-utility.yml`.
- Generated downloadable GH Actions evidence: `retrospective_review_routing.csv`, `summary.json`, `12_preexisting_cases_full_vs_top1_mock.csv`, `120_ranked_existing_demo_candidates.csv`, plus no-live-demo count mirror in GitHub Action artifacts (run 38618746013).
- UI-specific predeclaration: `docs/PHASE5_STREAMLIT_UI_SMOKE_PREDECLARED_20261015.md`; `tests/test_phase5_app_ui_smoke.py`, `.github/workflows/phase5-streamlit-ui-smoke.yml`, run 38619103980.
- Prior original fixed-case outcome SHA-256: MS-DIAL 609 `62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7`; 466 `09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b`.
- Original frozen source `a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70`; reference `2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01`; HGB `a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13`.
