# Phase 4 — GC–EI–MS Prior-Art and Novelty Audit (14 October 2026)

**Status:** literature-scoped scientific positioning audit, NOT proof of novelty, not systematic/full-bibliographic search, not a new validation. **No model/reference/threshold changes.** All DOI links were cross-checked against publisher or PubMed/NLM evidence. In the matrix, "not demonstrated" is not equivalent to "cannot be done by prior software".

## Scientific question and demonstrated evidence

**Our fixed v2 task:** ranked retrieval of a publisher-reported InChIKey first14 *connectivity label* when the label is **already present** among 8,455 MS-DIAL source-matched reference identities. Weighted cosine `m/z^1 * sqrt(intensity)` fixes top-1; the 12-feature HGB predicts whether that existing top-1 label will agree with the source label, and **does not change its rank**. Original single-use, now-SPENT 609: 394/609 top-1 first14 agreement, HGB AUROC 0.8633, Brier 0.1406; fixed original 10%-target accepts 198 (12 errors), 5%-target accepts 38 (0 errors), BOTH **uncertified**. 466 retrospectively source-selected SWGDRUG/RECETOX: 334/466 top1, selected overlaps, 419 first14 chemical labels, source-lab acquisition lineage NOT authenticated. Original 1,410 exposed development: nested-CV HGB Brier 0.1442 vs 12-feature logistic 0.1467; no decisive model superiority.

## Verified prior work with *overlapping conceptual contribution*

| Work (verifiable link) | What was already established | Manuscript consequence / fair contrast |
|---|---|---|
| Stein & Scott, 1994, [JASMS DOI](https://doi.org/10.1016/1044-0305(94)87009-8) | EI cosine/dot product and tuning mass/intensity exponents including sqrt intensity | We **did not invent** EI weighted cosine or sqrt intensity. Our m1 choice is reference-specific and does not guarantee superiority in other sources. |
| Stein, 1994, [JASMS DOI](https://doi.org/10.1016/1044-0305(94)85022-4) | Probabilistic indicators of correct identification and important separation of probability **given in-library** from probability of library membership | We **did not invent** probabilistic interpretation of EI hits. Crucially, our v2 HGB is only a score for correctness **conditional on an in-library, publisher-labelled closed-reference task**; out-of-library membership was not modeled. |
| Kim & Zhang, 2015, [J Chemom DOI](https://doi.org/10.1002/cem.2665) | False identification control and first-versus-second similarity-score difference | We **did not invent** margin screening, screening-based abstention, or a score-margin threshold. Our matched-acceptance curves are a retrospectively reproduced comparison, not new certified risk control. |
| McGlynn et al., 2025, [JASMS DOI](https://doi.org/10.1021/jasms.4c00451) | Automated GC–EI confidence-related context: spectral uniqueness, ubiquity, RI adjustment, noise reduction | Do **not** claim first integrated EI identification reliability tool. Our current v2 **does not use RI**, unlike capabilities in this work. The data/reference task differs; do not compare reported headline numbers directly. |
| Huber et al., 2020, [matchms JOSS DOI](https://doi.org/10.21105/joss.02411) | Open-source spectral processing and similarity evaluation | A Python user-facing MS comparison program alone is not novel. Stress immutable source verification, exact replicability, clearly bounded tentative connectivity outputs. |
| Yang et al., 2023, [FastEI Nat Commun DOI](https://doi.org/10.1038/s41467-023-39279-7) | Large in-silico EI library, Word2Vec spectral representations, fast HNSW retrieval and standalone interface | Our 8,455-entry **source-data** library has no demonstrated advantage over FastEI in retrieval size/speed/accuracy. NO numeric cross-paper comparison. |
| Xu et al., 2025, [LLM4MS Commun Chem DOI](https://doi.org/10.1038/s42004-025-01708-7) | EI spectral embeddings from fine-tuned language model, million-scale library, standalone graphical software | Our HGB **does not create embeddings** or rerank candidates; no competing retrieval-speed or matching-performance claim. |
| Ashyrmamatov et al., 2025, [Commun Chem DOI](https://doi.org/10.1038/s42004-025-01706-9) | Atomic-environment modeling to rerank EI library results | Our model does **not** use atomic-environment constraints or move a correct candidate upward; separate top-1 correctness prediction is the actual contribution. |
| Son et al., 2026, [J Chemom DOI](https://doi.org/10.1002/cem.70174) | EI spectral clustering and model-based flagging for spectra insufficiently represented in reference libraries, including out-of-library experiments | Our project does not verify true absent-reference detection; absence of an accepted hit can **never** be reported as confirmed out-of-library evidence. |
| Krishnaswamy-Usha, Capistran & Kearsley, 2026, [Chemometr Intell Lab Syst DOI](https://doi.org/10.1016/j.chemolab.2026.105773) | Replicate-derived peak likelihood scoring for drug-isomer EI discrimination; investigates acquisition concentration and preprocessing | We cannot claim novel improved stereoisomer discrimination. Their authenticated replicate study is a different endpoint; our first14 representation collapses stereochemical differences. |

### Adjacent methods to distinguish carefully

- *Conformal prediction for MS/MS molecular retrieval* now has specific prior art: [Reliable Molecular Retrieval from Mass Spectra Using Conformal Prediction](https://doi.org/10.1021/acs.jcim.6c00727) (2026), on MassSpecGym **LC–MS/MS**, **not EI**. The old v1 conformal margins do **not** transfer to v2; no v2 conformal candidate-set coverage claim.
- NIST's publicly documented [2026 EI/RI database](https://www.nist.gov/programs-projects/electron-ionization-library-component-nistepanih-mass-spectral-library-and-nist-gc) is far larger than our research 8,455-label subset. Its advanced library/database search and retention-index functionality cannot be presented as an omission or inferior tool without a documented comparison. Our open small-source software has a different distribution and reproducibility purpose.
- Prior 2025 [Novel probabilistic similarity scores for sets of replicate EI mass spectra](https://doi.org/10.1016/j.aca.2025.343858) is directly relevant prior art identified via the 2026 chemolab article; examine full paper before claiming no existing EI replicate-score uncertainty methods. We do not claim to reproduce it.

## Four possible contributions, ranked by strength (based on CURRENT evidence)

1. **Strongest: end-to-end reproducible provenance-aware research tool.** Frozen source, 8,455 reference index and fitted HGB checksum gate; identical 609-case numerical/Streamlit parity; exportable top10 candidate ranks, uncertainty score and explicit uncertified acceptance rules; source bytes not redistributed.
2. **Strong: transparent retrospective analysis of how confidence screens alter *acceptance*, not raw retrieval.** Same-case HGB vs cosine vs margin AUROCs (609: 0.8633 / 0.7067 / 0.8127), curves through every denominator, reliability bins. Margin is slightly better than HGB at 198 selected (11 vs 12 errors). This negative nuance increases trustworthiness.
3. **Moderate: connection between original-source chemical audit and practical ranked ambiguity.** Rank taxonomy 609 394/95/20/100; 466 retrospective 334/67/6/59; chemical exceptions and full-key discrepancies disclosed rather than silently relabeled as specimen-truth errors.
4. **Moderate/weak: a familiar 12-feature HGB fitted to top-hit correctness.** Development OOF Brier improves only 0.00258 over 12-feature logistic and bootstrap interval includes zero. No compelling learner-specific breakthrough.

## Explicitly barred claims

- First GC–EI mass weighted cosine / first margin / first correctness probability / first software with ranked candidates.
- Novel HGB architecture; new EI spectral embedding; improved retrieval top-1 accuracy *because of HGB*.
- Faster or more accurate than NIST26, FastEI, LLM4MS, atomic re-rankers, probabilistic isomer scorers, or out-of-library detection methods.
- Statistically guaranteed 5%/10% prospective error, generic 90/95% conformal coverage for current v2, authentic molecule or stereoisomer identification.
- Verified independent sample-acquisition lineage for 609 or 466, prospective external generalization, or uniform chemical sample-lab transfer.

## Honest novelty conclusion

**No identifiable new general-purpose EI identification algorithm is established.** The reportable contribution is a **carefully audited open scientific software implementation + transparent comparison of reliability screening and its failure boundaries**. This is potentially useful but may not satisfy a Q1 journal's substantive novelty threshold, even after perfect computational reproducibility. It is not sufficient to advertise that previously known components are integrated. The practical user task is to expose provenance and ambiguity for closed-reference EI source spectra without fabricating risk guarantees.

**Best next purely computational improvement:** preregister and implement end-to-end **software fault-injection / usability-relevant quality checks** (checksum mismatch, malformed input, ambiguous scores, wrong-scope RI, repeated binning, batch/single consistency, deterministic report regeneration), then report pass/fail evidence as software engineering performance, not chemical identification accuracy. Avoid tuning on 609/466 spent outcomes. Do not claim empirical user benefit until a real usage comparator exists.

## Reviewer pass/fail gate

- Literature novelty: **PASS for non-first-claim boundary and targeted prior-art check; FAIL for high-novelty algorithm claim.**
- Same-case basic confidence screening comparison: **PASS, retrospective only**.
- Source/label scope: **PASS when explicitly identified as source first14 agreement; authentic chemical truth not established**.
- Statistical risk guarantee: **FAIL; keep negative results**.
- Strong new practical utility over established software: **NOT YET demonstrated in matched independent use**; targeted fault-injection tests can strengthen auditability only.
- Novel state-of-the-art chemical identification: **NOT SUPPORTED**.

This is an evidence-bounded targeted search through 14 October 2026, not exhaustive prior-art clearance.
