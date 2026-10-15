# Manuscript v0.3 — GC–EI–MS source-audited software and retrospective confidence analysis

**WORKING ARTICLE DRAFT — 15 October 2026 (not a submission or peer-reviewed manuscript).** The title, abstract, original source numbers and headings are drafted for a scientifically bounded Elsevier software/methods article. **Source-verified evidence and DOI literature are cited in-line by numbered bracket references; journal formatting and final bibliography must be checked by the authors before submission.** No model, reference, historical test role or deployment was changed for the text. Single-author credit is not pre-assigned here; the corresponding author must verify contributors and journal authorship criteria.

## Candidate title

**An auditable web-based GC–EI–MS library annotation workflow: reproducible source curation and retrospective evaluation of top-hit reliability**

Short title: **Auditable GC–EI–MS annotation and reliability**

### Abstract

Gas chromatography–electron ionization mass spectrometry (GC–EI–MS) library searching provides ranked candidate annotations, but the leading spectral match does not necessarily establish molecular identity. We developed a browser-accessible, source-audited computational workflow that preserves a conventional mass-weighted cosine candidate ranking while separately evaluating the likelihood that the first candidate agrees with a publisher-reported chemical-connectivity label. A public MS-DIAL source containing 28,220 records was curated to 13,111 distinct retained spectral fingerprints and a fixed reference of 8,455 InChIKey-first14 connectivity entries. A 12-feature histogram gradient boosting (HGB) classifier, fitted on 1,410 previously exposed development cases, evaluated the existing first-ranked retrieval without reranking candidates. Among 609 originally reserved but now permanently evaluated **within-MS-DIAL** cases whose source-labelled connectivities were represented in the reference, the correct publisher connectivity occupied rank 1 in 394 cases (64.70%). The HGB source-label correctness score had an area under the receiver operating characteristic curve (AUROC) of 0.8633, compared with 0.8127 for the first–second hit similarity margin and 0.7067 for first-hit cosine similarity. The original 10%-target acceptance rule selected 198/609 cases, including 12 source-label disagreements; the more restrictive 5%-target rule selected 38/609, with zero observed disagreements. **Neither rule carries a certified future error bound.** A separately published but preselected and previously exposed SWGDRUG/RECETOX panel (n=466) exhibited comparable descriptive ranking behavior; independent source acquisition ancestry was not verified. The Streamlit application accepts single and batch EI spectra, presents tentative ranked candidates, exports version-linked results and makes scientific limits explicit. Independent numerical reproduction, frozen-asset verification, twelve unlabelled example regressions and headless interface tests support software integrity—not authenticated chemical identification. The contribution is an auditable GC–EI–MS annotation **reporting and reliability-assessment workflow**, without claims of new retrieval principles, retention-index fusion or source-independent sample identification.

**Keywords:** Electron ionization; gas chromatography–mass spectrometry; chemometrics; mass spectral library; reliability assessment; selective prediction; source provenance; scientific software.

### Highlights (candidate, conform to exact journal format at submission)

1. Frozen spectral-library retrieval and top-hit reliability are reported separately.
2. Source audits retain full-key, naming, metadata and acquisition-lineage exceptions.
3. HGB correctness discrimination exceeds cosine alone on retrospective source labels.
4. Historical strict confidence screens have major coverage/review-workload tradeoffs.
5. Public GC–EI–MS web software provides tentative annotations and provenance exports.

## 1. Introduction

Library-based GC–EI–MS is widely used to prioritize potential chemical identities from EI fragment spectra. Search algorithms compare observed ion masses and abundances with reference collections and supply ranked hit lists. Their rankings, however, depend on the quality of experimental peak extraction, representation of the analyte in the reference, fragment sharing across compounds and the credibility of the publisher-supplied structural metadata. Spectral similarity by itself does not fully establish sample identity; manual consideration of retention indices, sample context and confirmatory evidence remains important [1,2,4].

Modified spectral cosine and mass/intensity weighting have a long methodological history [1]. Similarly, probabilistic indicators of library identification correctness were explicitly formulated decades ago, with an important distinction between correctness **conditional on the analyte being represented in a library** and the separate probability that it is present in that library at all [2]. GC–MS work has also investigated the difference between top-ranked and second-ranked similarity scores as a means of prioritizing potentially false library identifications [3]. More recent GC–EI–MS research has incorporated spectral uniqueness, compound ubiquity and retention-index information into confidence-related library workflows [4]. Other open spectral informatics projects, virtual EI libraries and learned representations [5–7] make clear that combining a familiar spectral similarity function with a machine-learning estimator cannot, by itself, establish algorithmic novelty.

Reproducibility and interpretation nevertheless remain practical issues when small-source, in-library EI benchmarks are used to justify confidence scores on arbitrary query spectra. Distinct library records do not always correspond to independent laboratory acquisitions; formula and connectivity consistency may result partly from the original eligibility filters; and apparent calibration on publisher-provided structural labels does not establish authentic-standard chemical identification. Public scientific software also varies in the documentation and machine-readable provenance it provides. A narrower but testable contribution is to **make the data, software identity, candidate rank, model-derived correctness score and unresolved scientific limits separately inspectable in a single reproducible workflow**.

We therefore implemented and audited a GC–EI–MS library annotation web application with three objectives: (i) construct a fixed, source-verified connectivity reference and disclose chemical/provenance exceptions; (ii) contrast the same pre-existing top-hit correctness ranking signal from a frozen HGB classifier against simple spectral-score and score-margin baselines on archived publisher-labelled cases; and (iii) document end-to-end software integrity and the retrospective review-workload implications of the original fixed acceptance decisions. This is a **computational software and retrospective source-label study**, not a newly designed chemical structure elucidation algorithm or validation of a new physical laboratory method.

## 2. Materials and methods

### 2.1. Public EI source and chemical reference

The original MS-DIAL public GC–EI–MS/Kovats-RI MSP, deposited at Zenodo under DOI `10.5281/zenodo.21910638`, contains 28,220 records and was retrieved under an exact SHA-256 verification rule (**`a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70`**). Prespecified quality rules removed unsupported molecular representations and redundant nominal spectral fingerprints; 13,111 distinct fingerprints were retained and organized by 8,455 supported first14 InChIKey connectivity labels. One representative spectrum for each reference label was fixed in a source-index manifest (SHA-256 **`2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01`**). Original exact spectral identity was evaluated following nominal m/z rounding, summation of repeated nominal ions and stringent record-to-structure consistency rules. This step checks how the source was processed; it does not authenticate experimental molecular truth.

The 13,111 retained spectra included **294** first14 connectivity groups containing multiple regenerated full Standard InChIKeys, **373** spectra flagged for source-name semantic review and **six** original advanced-InChIKey-layer discrepancies involving **four** connectivity labels. One raw exact-spectrum fingerprint group mapped to conflicting original connectivity labels; the structurally supported representative was retained under the original curation rule without using model-prediction outcomes. The current paper therefore addresses **connectivity-level annotation only**; stereochemical and exact-molecular-form identity are not inferred from first14 agreement. Full frozen source indices, source flags, the four-identity exception audit and one conflicting fingerprint are indexed in Supplementary Information.

### 2.2. Spectral similarity and fixed retrieval

Peak masses were rounded to nominal integer m/z values (Python round-to-nearest-even convention); intensities had to be positive and finite and repeated nominal peaks were summed. The current model accepts m/z 0–6420 with positive raw intensity; unsupported nonnumeric or nonpositive inputs are filtered as specified by the code, and queries without usable weighted signal are rejected. Let `I_j(m)` denote the summed unnormalized ion abundance for spectrum `j` at nominal mass `m`. Its nonnegative weighted feature vector is `w_j(m) = m sqrt(I_j(m))`, normalized to unit Euclidean norm. Cosine similarity was the dot product between normalized weighted query and the corresponding fixed reference vector. Exactly the same reference index, preprocessing and stable reference-order tie resolution were used for all comparisons. **HGB did not change the retrieved top1 or rerank the hit list**.

### 2.3. Original development, source-labelled study panels and independence

An original set of **2,019** query-capable first14 identities was partitioned into **1,410** previously examined development cases and **609** initially reserved within-MS-DIAL queries. The development history included 201 similarity-exploration records, 383 fit-development records, 403 confidence/risk-stage records and 423 legacy candidate-set development records. These historical uses were exposed before the present Phase 3–6 retrospective reanalyses. A separate, source-selected collection of **466** EI spectra (370 SWGDRUG, 96 RECETOX) covered **419 unique** publisher-provided first14 labels; it had likewise already been examined. The 466 panel was not used to train the original HGB model; **69 of 609** within-source labels overlap it by first14 identity. The entire 609 original one-shot outcome evaluation has now occurred and **may never again be described as untouched validation following a method change**.

The endpoint was binary agreement between a fixed ranked top1 first14 and a publisher's archived first14 connectivity label. Every original 609 query was intentionally **in reference**. Neither a different source-record index nor a distinct EI peak-list fingerprint demonstrates a distinct standard, vial, instrument run, laboratory or independently verified truth label. The curated source contained instrument-type annotations for only **211/13,111** retained spectra and no independently authenticated run- or standard-lot identifier in the examined metadata fields. The 466 publisher-separate panel was preselected for reference-included compatible labels and may overlap in original measurement provenance. No independent authentic-standard accuracy or absent-library rejection performance was tested.

### 2.4. Frozen top-hit reliability and historical selection rules

The twelve fixed features computed for the unchanged first-ranked m/z¹×sqrt(I) retrieval were: top similarity; top1 minus top2, top5 and top10 similarities; logarithms of candidate counts within 0.01, 0.05 and 0.10 of the winner; mean top-five similarity; standard deviation of top-ten similarity; logarithm of query-peak count; raw ion-set overlap fraction with the winning reference; and summed query intensity share of matched peaks. The original development-fitted `HistGradientBoostingClassifier` binary artifact was SHA-256 **`a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13`**; original trained settings and dependency versions are preserved in `models/v2/release_manifest.json`.

The original nominal **10%-target** acceptance screen required HGB score `>= 0.87`. The original nominal **5%-target** screen required HGB `>= 0.94` **and** top1–top2 similarity gap `>= 0.20`. These names are inherited from the development research and are retained for transparent historical comparison. They are **not** certification claims; no independent future conditional error control or conformal coverage is established.

### 2.5. Descriptive statistical comparisons and software demonstration

We compared the original first-hit cosine score, first–second cosine margin and frozen HGB correctness score on the **same, permanently spent** source-labelled cases, assessing AUROC and observed error among the top K highest-scored examples with identical acceptance counts. Only the HGB probability-like output was evaluated by the Brier score and fixed-bin reliability analysis: raw similarity and margin were **not** erroneously treated as calibrated probabilities. Any row-resampling sensitivity summaries were descriptive and did not assume verified lab-independent source groups. Exact differences among accepted-case masks were retained. In the original development set, nested out-of-fold logistic and HGB comparators were evaluated descriptively rather than promoted to a new tuned model.

Software utility was defined in advance as a reproducible report-contract test, not an external EI-engine benchmark. The author-constructed top1-only reporting mock retained **exactly the frozen model's own leading candidate and similarity** while omitting other report fields. The complete software also includes a top-ten list, top-two margin, source-label correctness score, historical rule flag, explicit limitations and SHA-pinned source/model/reference identity. We verified these output invariants on **12 existing unlabelled botanical example peak lists**, each processed individually and in a batch. The ten ranked candidates per spectrum (**120 rows**) were exported programmatically during regression; the public app's **batch download currently reports one top-hit summary row per input spectrum**, while single-spectrum use offers an independent candidate-top-ten download. We additionally ran **13** synthetic software failure/input-integrity tests and **two** headless tests of the actual Streamlit single- and batch-input screens. These are software engineering tests; neither human usability nor authentic chemical identity was assessed.

### 2.6. Reproducibility, licensing and study-role controls

Exact SHA-256 checks apply to the original MSP, reference manifest and HGB model. Original already-exposed 609/466 per-case ledgers were checked against immutable file fingerprints before retrospective recomputation. Numerical parity was audited independently using archived source parsing and a separate matched-case Python implementation; all numerical and UI tests are reproducible through versioned GitHub Actions. The public application is v2.0.2 (`https://gc-ei-annotation.streamlit.app/`), with archival software DOI `10.5281/zenodo.23373447`. This MIT-licensed software **does not transfer** reuse rights in third-party source spectra. Original publisher peak arrays are not redistributed through the open GitHub research repository; source access/licence obligations remain source-specific. Supplementary Information enumerates **1,119 retained source MSP records lacking an explicit original LICENSE field**, so the source corpus is **not** presumed unrestricted or public domain.

## 3. Results

### 3.1. Frozen library and chemical-source quality

The source-controlled curation retained **13,111** distinct nominal EI spectral fingerprints representing **8,455** connectivity reference identities. Audits reconstructed the original inclusion and chemical-identifier checks and catalogued the **294** within-connectivity full-key-diverse groups, **373** retained source-name warnings and **six** source-row advanced-layer discrepancies. These are a record of known metadata limitations, not evidence of six chemically misidentified standards. The source acquisition census lacked sufficient raw-run and standard-lot information to establish independence of spectra recorded within the original MS-DIAL compilation.

### 3.2. Retrospective within-source and selected cross-collection retrieval

For the **609** originally reserved but now one-time evaluated within-MS-DIAL queries, the original source first14 label was first-ranked in **394/609 (64.70%)**, among the first five candidates in **489/609 (80.30%)** and among the first ten in **509/609 (83.58%)**. The remaining label-rank groupings were **95** at ranks 2–5, **20** at ranks 6–10 and **100** below rank 10. The original fixed m/z²×sqrt(I) weight yielded **385/609** first-ranked agreements compared with **394/609** for m/z¹×sqrt(I); the nine-case net difference is descriptive and does not prove superiority across all settings.

In the previously exposed and source-selected **466** SWGDRUG/RECETOX cases, **334/466 (71.67%)** publisher connectivity labels were first-ranked. The analogous rank groups were **67** at ranks 2–5, **6** at ranks 6–10 and **59** below rank 10. Of **132** top-ranked labels disagreeing with publisher first14 identities, **50** first hits had the same molecular formula as the publisher-matched entry, indicating a potential formula-preserving structural ambiguity; this does not establish that any pair are confirmed experimentally identified constitutional isomers. The selected 466 results were not pooled with the 609 as independent measured experiments.

### 3.3. Same-case correctness discrimination and calibration

Across the 609 cases, frozen HGB AUROC was **0.86330**, versus **0.81268** for the first–second similarity gap and **0.70668** for the top EI cosine. Its source-label Brier score was **0.140645**, and fixed ten-bin expected calibration error (ECE) was **0.04494**. Nevertheless, local calibration was not uniform: among **67** cases scoring between 0.2 and 0.3, only **10** first-hit publisher labels agreed (14.93%), whereas their mean HGB score was approximately 0.2477. Good overall discrimination therefore should not be equated with uniformly calibrated new-source identification confidence.

At matched **K=198** selected cases, the HGB score selected **12** publisher-label disagreements, whereas margin-only selected **11** and cosine-only **45**. At **K=305**, the respective counts were **31**, **41** and **68**; HGB did not dominate the simple margin at every acceptance level. On the previously exposed 466 panel, HGB AUROC was **0.87009**, margin **0.83107** and cosine **0.69876**, with HGB Brier **0.124997**. Original 1,410-case development out-of-fold comparison gave HGB Brier **0.14416**, versus **0.14675** for the 12-feature logistic comparator, a modest difference insufficient to demonstrate architectural superiority.

### 3.4. Historical screening performance and review burden

| Archived panel | Original non-certified rule | Accepted/N | Accepted first14-agreeing | Accepted first14-disagreeing | Flagged disagreeing | Flagged agreeing |
|---|---|---:|---:|---:|---:|---:|
| 609 MS-DIAL within-source | 10%-target | **198/609** | **186** | **12** | **203** | **208** |
| 609 MS-DIAL within-source | 5%-target | **38/609** | **38** | **0** | **215** | **356** |
| 466 SWGDRUG/RECETOX selected | 10%-target | **185/466** | **173** | **12** | **120** | **161** |
| 466 SWGDRUG/RECETOX selected | 5%-target | **25/466** | **25** | **0** | **132** | **309** |

The historical 10%-target screen flagged **203/215 (94.42%)** top-hit publisher-label disagreements for further review within MS-DIAL but also flagged **208/394 (52.79%)** first-hit label agreements. The nominal 5%-target screen flagged all **215** disagreements but also **356/394 (90.36%)** agreements and accepted only **6.24%** of evaluated cases. Both original 5%/10% *prospective error target certifications remain failed/unestablished*; observed zero mismatches among 38 or 25 cases does not establish future zero or sub-5% error. These are source-label screen outcomes, **not actual recovered or prevented chemical misidentifications**.

### 3.5. Verified software reporting and headless interface checks

The original **12** example input spectra generated **120** unique ranked engine candidate rows with top-one numerical identity and similarity invariant across original 10% and 5% screen choices, individual/batch execution and repeated fixed-environment inference. Their true experimental chemical identity was unknown and no example-set percentage correct was estimated. The original frozen model, 8,455 reference index and original source hashes were preserved through the run. The **13 synthetic failure-injection software cases** and the **two actual-application headless Streamlit interface tests** passed. This evidence supports software reproducibility and disclosure integrity; it is not a user survey, cross-laboratory measurement study, online uptime audit or demonstrated superiority over third-party application features.

## 4. Discussion

### 4.1. Distinctive scope and limits of the integrated contribution

This work does not introduce weighted cosine, first–second score margins, uncertainty estimation, or a newly designed ML classifier. Those ideas have established GC–EI–MS precedent [1–4]. Its specific contribution is a **public browser-delivered, immutable and independently audited workflow** that unifies source-level chemical identifier screening, conventional EI retrieval, publisher-label first-hit correctness estimation, complete candidate-rank review and explicit interpretation limits. This is a distinctive software research implementation but it should not be marketed as the first GC–EI confidence tool or as an experimentally proven advance over modern NIST software, recent EI probabilistic methods or learned EI rankers. Existing NIST/EI software also provides hit lists, probabilities and retention-index comparison [4]. The tool's smaller source-dependent reference and absent RI fusion are functional limitations relative to that wider ecosystem, not competitive strengths.

### 4.2. Value of evidence-bound review selection and the rejected risk certificate

The review-routing results quantify a plausible information-management use case: highlighting potentially ambiguous top-hit annotations before researchers interpret them as resolved compounds. The value is balanced by the large proportion of source-agreeing hits also flagged, especially under the stricter rule. Consequently, selected-source disagreement metrics should not be recast as net error reduction, faster research decisions or real user outcomes. More importantly, source-record dependence, deliberately in-reference labels and absence of authentic standard validation preclude an inference of certified prospective 5% or 10% chemical identification error. This negative finding should be retained as a scientifically informative limitation rather than concealed through further threshold tuning.

### 4.3. Chemistry and data-source uncertainties

First14 labels omit layers distinguishing some stereochemical and molecular representation features. Source name qualifiers, chemical derivative records and full-key inconsistencies deserve explicit treatment, and the inclusion filter's enforced structural agreement cannot function as independent evidence of chemical truth. The presence of an original source fingerprint under two nominal source labels further illustrates why source data governance and chemically sensible eligibility rules matter. The 609 within-MS-DIAL benchmark reflects a compiled database's related spectrum families, and the selected 466 publisher panel was not independently authenticated as separate acquisition ancestry. Results cannot be generalized automatically to unidentified field specimens, trace coelution, deconvolution artifacts, genuinely absent library compounds or direct sample-based identification decisions.

### 4.4. Software access, methodological novelty, and reproducibility tradeoffs

A free-to-access browser workflow makes the implementation directly usable without requiring investigators to install an external programming stack; this is **a design property**, not a formally measured user accessibility or adoption effect. Source and result exports let researchers recognize the frozen software/library configuration used for a result. Nevertheless, reproducing the computations still depends on third-party source accessibility and permissible data use, and an open-source software licence does not transfer database rights. In addition, the current batch UI exposes first-hit summary outputs rather than the top-ten list for every batch entry, which is available via single-spectrum mode and direct engine calls. A scientific software report should describe this nuance precisely rather than claim nonexistent user-interface functionality.

### 4.5. Appropriate next scientific use

The workflow can be used as a **tentative EI-library annotation assistant** for spectra sufficiently comparable to the library's representation, followed by researcher-led interpretation and independent confirmation where chemical identity is consequential. Work on formal absent-reference recognition, acquisition-verified external transfer, additional RI and chromatographic evidence, and rigorously controlled prospective risk may be pursued separately; none is demonstrated by the frozen current v2.0.2 model. This scope is sufficient to present an open software-and-retrospective-evidence paper, but cannot ensure that a specific journal will deem its advance substantial enough for acceptance.

## 5. Conclusions

We report a transparent, source-audited GC–EI–MS annotation workflow in which traditional mass-weighted cosine determines the candidate rank and a separate frozen classifier estimates retrospective publisher-connectivity label agreement. Source chemistry, a 609-case within-library evaluation, a selected 466-case second publisher panel, descriptive uncertainty screening and verifiable web-software behavior are documented without conflating database agreement with authentic chemical identification. The tool supplies accessible ranked evidence and explicit uncertainty disclosures, while **no prospective 5% or 10% error certificate, laboratory-source generalization or chemical authentication** has been demonstrated. Its primary result is an auditable software reporting practice and a clear evaluation of its limits, rather than a new EI retrieval algorithm.

## Data and code availability (to retain in final submission)

The original MS-DIAL public source is available from DOI **10.5281/zenodo.21910638** subject to its original reuse conditions. Research scripts, exact HGB/index/source checksums, prior exposed source-label prediction ledgers and audit workflow logs reside in the version-controlled repository `https://github.com/jameshztta-stack/gc-ei-annotation-reliability`, with the manuscript research changes in draft PR #8. The publicly accessible Streamlit application is `https://gc-ei-annotation.streamlit.app/`; software v2.0.2 is archived at **10.5281/zenodo.23373447**. The original source MS peak-array archive is **not mirrored** within the software repository. Source licensing must be checked with publishers independently from the MIT software licence. The exact archival research commit, prespecified historical file hashes, source exception audit and GitHub Actions run identifiers are listed in the phase-6 supplementary evidentiary map.

## Competing interests, contributions and acknowledgement

**AUTHOR APPROVAL REQUIRED:** Corresponding author and collaborator names, affiliation, individual author contributions, funding acknowledgements, conflicts of interest and software/LLM assistance statements **have not been fabricated**. Provide only documented declarations once approved by the actual contributors. Publication and authorship roles remain subject to applicable journal policy.

## References — source-verified anchor list (format and completeness to be finalized)

[1] Stein SE, Scott DR. Optimization and testing of mass spectral library search algorithms for compound identification. *J Am Soc Mass Spectrom.* 1994;5:859–866. https://doi.org/10.1016/1044-0305(94)87009-8

[2] Stein SE. Estimating probabilities of correct identification from results of mass spectral library searches. *J Am Soc Mass Spectrom.* 1994;5:316–323. https://doi.org/10.1016/1044-0305(94)85022-4

[3] Kim S, Zhang X. Discovery of False Identification Using Similarity Difference in GC-MS based Metabolomics. *J Chemom.* 2015;29:80–86. https://doi.org/10.1002/cem.2665

[4] McGlynn DF et al. New Library-Based Methods for Nontargeted Compound Identification by GC-EI-MS. *J Am Soc Mass Spectrom.* 2025;36:389–399. https://doi.org/10.1021/jasms.4c00451

[5] Huber F, Verhoeven S, Meijer C, et al. matchms – processing and similarity evaluation of mass spectrometry data. *J Open Source Softw.* 2020;5(52):2411. https://doi.org/10.21105/joss.02411

[6] Yang Q, Ji H, Xu Z, et al. Ultra-fast and accurate electron ionization mass spectrum matching for compound identification with million-scale in-silico library. *Nat Commun.* 2023;14:3722. https://doi.org/10.1038/s41467-023-39279-7

[7] Xu Y, Ma Y, Xu W, et al. A large language model for deriving spectral embeddings for accurate compound identification in mass spectrometry. *Commun Chem.* 2025;8:326. https://doi.org/10.1038/s42004-025-01708-7

**Further contextual EI studies identified but not exhaustively integrated:** https://doi.org/10.1038/s42004-025-01706-9; https://doi.org/10.1016/j.aca.2025.343858; https://doi.org/10.1002/cem.70174. Must verify metadata/full-text before using to establish a first-or-only novelty claim. The final reference list will require journal-specific formatting and primary verification.

---

**Internal author note (REMOVE before real submission):** This article is a scientifically bounded draft, not an independent external reviewer report. Every value is grounded in archived original data and audited Phase 3–5 source artefacts; no new physical experiments are implied. Selected historical data and absent acquisition lineage constrain generalization. Complete a human full-text reference metadata check, journal Original Software Publication length and submission policy check, primary data licence permissions review, and authorship sign-off.
