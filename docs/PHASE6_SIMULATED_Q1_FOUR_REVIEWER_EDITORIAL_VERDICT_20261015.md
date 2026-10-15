# Phase 6 — Simulated Q1 Elsevier editorial and four-reviewer gate, 15 October 2026

> **Explicit status: simulated, internal pre-submission critique, NOT actual external editor / journal reviewers, no endorsement, no real-world validation.** The article reviewed is `docs/PHASE6_COMPLETE_MANUSCRIPT_WORKING_DRAFT_20261015.md`, supplement `docs/PHASE6_SUPPLEMENTARY_DATA_AND_EXCEPTION_EVIDENCE_20261015.md`. Software v2.0.2 is unchanged. Review calibrated against existing historical archival evidence, source-pinned manifest, fixed Phase 3–5 workflows and the **24-point manuscript audit that PASSed**: [Actions run 38671295855](https://github.com/jameshztta-stack/gc-ei-annotation-reliability/actions/runs/38671295855). The audit checks *selected verifiable anchors*, not every interpretative claim.

## Simulated handling editor decision

**Verdict: MAJOR REVISION before journal submission; NOT YET suitable for a strong novel identification-methods research paper; CONDITIONAL candid path for a software-plus-retrospective GC–EI–MS study in a journal explicitly admitting original scientific software.** Crucial distinction: no requirement that this app beat every EI matching method in raw top1 accuracy; **there is a requirement to show a sufficiently distinctive practical and scholarly contribution**. A working Streamlit app is not intrinsically enough, especially when NIST and contemporary EI search ecosystems already offer rankings/probability/RI features.

### Editorial fit and potential title choice

**First legitimate Elsevier software-fit consideration:** *Chemometrics and Intelligent Laboratory Systems* (CILS); publisher's official current scope expressly includes **Original Software Publications**, but also rejects routine established-method applications and requires novel tools or genuine advancements in using chemometrics. Primary source: https://shop.elsevier.com/journals/chemometrics-and-intelligent-laboratory-systems/0169-7439 . We should NOT represent CILS as Q1 *analytical chemistry*; current publicly collated 2025 metrics treat its JCR math/statistics as Q1 but chemistry analytical as Q2. A qualifying JCR field definition must be verified via the user's institution's Clarivate JCR subscription. **DO NOT infer guaranteed acceptance from content fit.**

Alternative Q1-in-analytical-chemistry ambition: *Microchemical Journal*; its official scope explicitly permits mass spectrometry, chemometrics, ML and AI, but **requires significant method novelty/improvement and favors real sample applications**; this exact computational-only manuscript has a **higher desk-reject risk**. Official publisher source: https://shop.elsevier.com/journals/microchemical-journal/0026-265X . No physical experiments are added to the project on account of journal preference.

### Simulated editor cover memo (NOT a submitted cover letter)

The manuscript presents an auditable, open browser-facing GC–EI spectral annotation software workflow with source/chemical-key integrity checks, a frozen conventional retrieval function, retrospective source-label first-hit reliability screening and visibly bounded uncertainty interpretation. Software engineering has source-checksum and CI evidence; cases with non-confirming correctness and failed risk certificates are retained. This is coherent **scientific software engineering plus retrospective chemometric assessment**, but methodological novelty is incremental relative to existing probability, hit-list rank, score-gap and source-informed EI tools. Submission should be framed as a clearly specified reproducible software contribution with a tangible research utility demonstration, **not** a new structure-identification accuracy benchmark or fully calibrated universal GC–MS annotation model.

## Reviewer A — GC–EI–MS and analytical chemistry

| Reviewer item | Current assessment | Evidence / direct editorial action |
|---|---|---|
| A1. Identity label carefully defined | **PASS with limitation** | Article explicitly says publisher first14 source agreement and all 609 queries in reference, NOT confirmed authentic standard identity. Keep in abstract, figures and conclusion. |
| A2. Source independence | **MAJOR intrinsic limitation, disclosed** | Original 609 and reference share MS-DIAL archive; 466 source-selected SWGDRUG/RECETOX with no per-acquisition independent chain established. Do not term validation "independent experimental" or external laboratory transfer. |
| A3. Chemical metadata exceptions | **PASS to archive; manuscript SI detail essential** | 294 full-key-diverse groups, 373 name warnings, six advanced-key discrepant source rows (four labels), one raw fingerprint/label conflict. Audited SI reference paths are provided; preserve exact six-vs-four distinction. |
| A4. EI analytical realism | **MAJOR scope limitation, disclosed** | No measured unknown samples, coelution/deconvolution test, instrument transfer, absent-library trial or retention-index integration in v2. Absent labels not tested. No physical experiments necessary for the selected narrower software paper, but no claim of broad real-world chemical-ID performance. |
| A5. Source rights | **MAJOR unresolved compliance gate** | Original MSP `LICENSE` field missing in 1,119/13,111 retained records, nonempty fields varied CC BY-SA naming. Not evidence rights are denied, but **do not infer** that MIT code licence licenses the spectral data, nor redistribute raw or derived peaks without clearance. Research sample consumer may be noncommercial; check publisher and subsource terms. |

**Reviewer A simulated recommendation:** Major revisions for applied GC specificity, instrument/metadata source caveats and access-rights statement; not new method bench validation.

## Reviewer B — statistics, ML, and selective uncertainty

| Reviewer item | Current assessment | Evidence / action |
|---|---|---|
| B1. Correct denominators/reproducible archived rows | **PASS** | 609 top1 394; 466 334; 1410 dev earlier; numeric audit cross-computation passed. 609 is permanently spent. |
| B2. Honest paired same-task comparators | **PASS as retrospective** | 609 HGB/margin/cosine AUROC 0.8633/0.8127/0.7067. At K=198, margin selected 11 wrong vs HGB 12, so the manuscript discloses nonuniform HGB advantage. |
| B3. Probability and calibration | **PASS as source-label description with limitation** | HGB Brier 0.1406, 10-bin ECE 0.04494; heterogeneous 0.2–0.3 bin (67 total, 10 agreement). Source labels not chemical truth. |
| B4. Risk target certificates | **FAILED prospectively — retained honestly** | Historical 10%-target 198 accepted/12 wrong, 5%-target 38/0 wrong on 609; 185/12 and 25/0 on 466. No valid IID/exchangeability from source acquisitions; pre-fixed rules have no formal future coverage/risk guarantee. **Do not retune using spent outcomes.** |
| B5. Source groups, repeats and cross-collection selection | **UNRESOLVED for causal/inferential generalization** | Duplicate source spectra and possible library alias; 69 prior 466 overlap identities in 609; selected 466 includes 419 distinct first14 labels. Do not pool cohorts or infer IID p-values. |
| B6. Claim of novel HGB superiority | **NOT SUPPORTED** | Original 1410 nested OOF 12f logistic AUROC 0.85560 vs HGB 0.85528, HGB Brier 0.14416 vs logistic 0.14675, small difference. Avoid architectural innovation narrative. |

**Reviewer B simulated recommendation:** Minor manuscript corrections if performance is framed purely as retrospective source-label agreement; **major** if title/abstract continues to suggest risk-controlled identification.

## Reviewer C — mass-spectral software, prior art, and novelty

| Reviewer item | Current assessment | Evidence / direct action |
|---|---|---|
| C1. GC–MS vs LC–MS separation | **PASS** | Differentiate GC–EI identity-spectrum workflows from LC–MS/MS embedding/conformal papers. But GC–EI mass-weighted cosine/probability/margin are old, so GC rather than LC alone does not establish first use. |
| C2. Earlier GC–EI confidence tools | **MAJOR novelty pressure** | Stein & Scott (1994), Stein (1994), Kim & Zhang (2015), McGlynn et al. (2025) already report mass-weighted similarity, in-library probability, score difference and RI/uniqueness-based confidence. See DOI 10.1016/1044-0305(94)87009-8; 10.1016/1044-0305(94)85022-4; 10.1002/cem.2665; 10.1021/jasms.4c00451. NIST26 offers far larger EI/RI library, so relative competitiveness is NOT demonstrated. |
| C3. Distinct software deliverable | **PASS for implementation; CONDITIONAL as publishable innovation** | Public single/batch Streamlit, pinned reference/model, explicit uncertainty, source audit; 12 examples/120 engine candidate rows, 13 fault tests, 2 headless UI tests. Real batch UI downloads only one top1 row per spectrum, NOT 10-ranked per batch. Human adoption/usability/benefit versus current software not measured. |
| C4. Comparison to real existing GC–EI applications | **MAJOR open comparative positioning** | Top1-only mock is **author-constructed**; not NIST, AMDIS, FastEI or other real product. Claims like "uniquely user-friendly" or "first integrated" cannot be supported. An honest documentation-based feature map and manuscript framing is required; no need to rig unfair numeric comparisons. |
| C5. Prior art references | **PASS for anchor [1]–[7]; further literature review remains** | Original publisher metadata were verified for the core 1994/2015/2025 EI references, Huber et al. matchms (2020), Yang et al. million-scale EI matching (2023), and Xu et al. LLM4MS (2025). Additional related 2025/2026 publications still require citation completeness and final author DOI review. |
| C6. Extent of algorithmic novelty | **LIMITED** | HGB classifies correctness of **unchanged** top1, not candidate ranking; no novel spectral embedding, formula model, first-hit margin or general uncertainty technique demonstrated. |

**Reviewer C simulated recommendation:** Major revisions / high editorial desk risk for a Q1 "new algorithm" article; **plausible** software publication path if the complete workflow's verified utility is compelling and journal permits applied open research software without a new algorithm.

## Reviewer D — reproducible software and data governance

| Reviewer item | Current assessment | Evidence / direct action |
|---|---|---|
| D1. Frozen source, numerical reproduction and unit QA | **PASS** | Code and source hashes pinned, independent same-case analytical replay, 12-case engine regression, 13 synthetic fault tests and two app UI simulations. Phase 6 automated claim gate **24 checks passed** on original source chemistry and provenance JSON. |
| D2. Software license vs upstream data | **OPEN major compliance** | MIT source code licence and old public Zenodo software DOI do not confer spectrum redistribution rights. Original MSP per-record LICENSE coverage 11,992/13,111, 1,119 absent. Third-party data source use terms must be read and authors attest compliance. |
| D3. Figure/outputs archiving | **PARTIAL** | Phase 3 GitHub Actions plots generated and available in artifacts; main submission still needs immutable final figure exports, Figure 1 data lineage, error/reliability and rank taxonomy legends, archived original-data manifests. |
| D4. Interface truth scope | **PASS on inspected UI text, WITH correction** | Current UI caveats label outputs as tentative and uncertified. Actual batch CSV is first-hit summary only; row-per-spectrum batch top10 data were generated programmatically in regression, not exported by current live batch button. |
| D5. Human replication | **OUTSTANDING** | Automated independent program logic ≠ independently performed human scientific source review. Before external submission, arrange separate independent domain expert if possible. Do not assert that one has already performed it. |
| D6. Hosting/usability/effectiveness claims | **NOT TESTED beyond automated headless checks** | Public app address is known; source code CI does not guarantee current hosting uptime, digital accessibility, successful human operation, broad user adoption or researcher workflow efficiency. |

**Reviewer D simulated recommendation:** Core software source quality good, major concern for data licensing/access, incomplete final submission figures and no independently replicated human external review.

## Required final pre-submission actions — no laboratory experiments

1. **Complete journal selection accurately:** For CILS, obtain current Elsevier Guide for Authors and ask whether exact "Original Software Publication" requires special files/article length. Its publisher **scope** was verified; ScienceDirect Guide for Authors fetch was not accessible through our present browser, so do not invent a word limit/figure cap. Verify current JCR category quartile via actual Clarivate credentials if Q1 status materially matters. If strict analytical chemistry Q1 is essential, Microchemical Journal carries substantially higher desk risk for this nonexperimental study.
2. **Finalize full references:** Verify DOI bibliographic metadata for [5]–[7] and any new GC–EI studies; do not imply LC/MSMS advances were GC–EI-first. Explicitly acknowledge NIST probability/RI alternatives.
3. **Finalize data licence and software provenance:** Document exact original MSP record access rights, 1,119 missing license flags; distinguish original data-source license versus MIT code. Preserve source fetch and source SHA. Full repo and original archive links should be verifiable by a human reviewer.
4. **Complete submission figures, captions and SI pointers:** Existing verified Phase 3 figure files, risk–coverage plots, exact exception inventory/metadata-field table, current app outputs, workflow diagram and version separation. No invented real-world specimen or independent user case study.
5. **Author approval:** Confirm names, authentic contributions, funding, conflicts, AI/software usage declaration, corresponding author, affiliations and correct data availability.
6. **Second manual scholarly evaluation:** An uninvolved GC–EI–MS analytical chemist or software reviewer should check source/data roles and practical user interface if possible; this remains recommended but should never be falsely claimed complete.

### Explicitly NOT mandatory to solve for the narrowed manuscript

- Obtaining a new wet-laboratory authentic standard or other independent experimental validation **provided no physical-truth/transferability claims are made**. A particular journal may still demand real samples and reject under its own standards.
- Achieving the originally labelled 5%- and 10%-future-error certification. Keep the honest negative result, report observed count limits and never imply certification.
- Inventing another algorithm or outperforming NIST/FastEI/AMDIS on their distinct original task; require a clearly described original, research-relevant and auditable software contribution instead.
- Retraining/retuning on spent 609/466. This would damage the methodological integrity and does not create a new untouched test.

## Unbiased overall simulated judgment

| Evaluation | Result |
|---|---|
| Source/numerical reproducibility | **PASS for executed checks** |
| Chemical database-label integrity accounting | **PASS for source QC and source-encoding exceptions, not physical truth** |
| Existing frozen classifier correctness discrimination | **Useful retrospective evidence, not novel retrieval** |
| Web application functionality / 12-case demonstrations | **PASS engineering, unmeasured independent usability** |
| Clear novelty relative to actual GC–EI matching and confidence prior art | **CONDITIONAL / major editorial debate** |
| Authentic-standard external generalization and OOL | **NOT established; declared out of scope** |
| Formal future 5%/10% risk bound | **FAILED/not certified; must remain disclosed** |
| Complete journal-specific references, figure files and third-party source rights | **INCOMPLETE submission preparation** |
| **Ready for narrow scientific software peer review?** | **Nearly as a draft; after missing compliance/manuscript packaging gates** |
| **Guaranteed ready for a Q1 acceptance?** | **NO — never a guarantee** |

**Simulated editorial conclusion:** **MAJOR REVISION (internal only)**, principally for evidence-bound software novelty against existing EI tools, final reference/figure and licensing readiness, not for failing to invent a higher-performing identification algorithm. Continue manuscript and compliance preparation; do not claim source-independent physical truth or release a misleading newer production version.

**Evidence audit run**: 38671295855 (SUCCESS, 24 anchored claims). Earlier Phase 6 audit runs failed because of literal *wording checks* (`"six/four"` versus numeric counts and `"not yet"` versus explicit no-fabrication statement), with no source/model/results differences; these were repaired transparently. Both failed CI runs and successful final run remain in the GitHub Actions audit trail.
