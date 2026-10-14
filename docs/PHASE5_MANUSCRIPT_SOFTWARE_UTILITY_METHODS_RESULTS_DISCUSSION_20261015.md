# Phase 5 publication-ready Methods, Results and discussion insert

**Scope:** constrained GC–EI–MS **software-and-data reliability** manuscript, not new independent chemical identification evaluation. Prepared after passing GitHub Actions benchmarks on 15 October 2026; all 609 and 466 source labels previously exposed. Integrate into the existing Phase 4 manuscript draft after cross-referencing figures, supplement and citations. No prospective risk guarantee or human usability finding.

## Methods — software utility validation and descriptive review routing

We evaluated the implemented software as a scientific reporting workflow rather than as a newly designed spectral-retrieval algorithm. A deliberately minimal, investigator-defined reporting baseline was constructed by retaining only the frozen engine's first-ranked connectivity candidate, candidate name and spectral cosine similarity. This baseline is an output-format control **and does not represent any external mass-spectral search product**. In comparison, the complete workflow retains the original ranking and additionally provides ten candidate identities, top-two similarity separation, the frozen histogram gradient boosting (HGB) correctness score, historical screening-rule decisions, explicit evidence limitations and original-source, reference-index and model SHA-256 identifiers. For 12 pre-existing, unlabelled botanical EI peak examples distributed with the research software, we evaluated required-field completeness, 10-candidate rank invariants, numerical repeatability, identical first-hit retrieval across the historical 10% and 5% decisions, single-spectrum versus batch parity, and appropriate uncertified-risk disclosure. We did not interpret the botanical candidates as experimentally authenticated identifications.

The actual Streamlit interface was separately subjected to two headless `st.testing.v1.AppTest` scenarios: render the single-spectrum screen with reference/scope descriptions and switch to the batch CSV workflow without exception. These tests verify execution and presentation controls in the source code but do not measure user satisfaction, independent laboratory usage, hosting uptime or subjective usability.

To describe possible additional-review workload, we also tabulated the already published, retrospectively observed source-first14 agreement against each of the original frozen screening decisions in the 609 within-MS-DIAL and 466 SWGDRUG/RECETOX source-selected panels. At each original operating point, we reported four joint counts: accepted correct-source-label, accepted incorrect-source-label, flagged correct-source-label and flagged incorrect-source-label. The original rules were not adjusted after exposure to the 609 or 466 data. All denominators and input CSV checksums were independently verified. No case was withheld from this descriptive reuse and no inferential independence of physical sample acquisition was assumed.

## Results — software reproducibility, output utility and screening tradeoffs

The source-verified v2 engine returned exactly ten distinct connectivity-level reference candidates for each of the **12 pre-existing example spectra**, generating **120 ranked rows**. The top-ranked candidate and its similarity were numerically unchanged between single and batch processing, between historical screening rules, and between the original top-hit-only mock and complete reporting. All 12 cases contained the specified model/source/reference provenance and explicit scientific-limitations fields, and repeated fixed-environment inference yielded identical ranking and numerical scores. The headless actual-application checks also completed successfully (**two tests passed**). These results demonstrate implementation fidelity; none of the 12 cases had an experimentally authenticated truth label for measuring chemical accuracy.

For the **609 previously evaluated within-MS-DIAL source queries**, a top-hit-only hypothetical accept-all report retained **215** first14 disagreements out of 609. Under the historical 10%-target screen, **198/609** would have remained accepted, including **12** source-label disagreements, while **411** would have been directed to further review, including **203** source-label disagreements and **208** source-label agreements. Thus, **203/215 (94.42%)** of historically disagreeing first hits were flagged, at the cost of also flagging **208/394 (52.79%)** agreeing first hits. The stricter historical 5%-target screen accepted only **38/609**, all historically label-agreeing, and flagged **215/215** disagreements **and 356/394** agreements. These are descriptive outcomes under selection using existing stored scores; neither operating point passed certification as a future risk control.

In the **466 previously exposed, retrospectively selected SWGDRUG/RECETOX** source observations, the historical 10%-target screen accepted **185/466**, comprising **173** first14 agreements and **12** disagreements, and flagged **120/132 (90.91%)** source disagreements together with **161/334 (48.20%)** agreeing top hits. The strict screen accepted **25/466** cases with zero observed source disagreements but flagged all **132** disagreements and **309** agreements. Because source acquisition lineage was not independently authenticated, this source-selected panel should not be described as a prospective laboratory-transfer test or pooled with the 609 observations.

### Table — historical review routing (publisher connectivity label endpoint)

| Retrospective panel | Preexisting rule | Accepted | Accepted label disagreements | Flagged label disagreements | Flagged label agreements |
|---|---|---:|---:|---:|---:|
| MS-DIAL 609 | 10% original (uncertified) | 198 | 12 | 203 | 208 |
| MS-DIAL 609 | 5% original (uncertified) | 38 | 0 | 215 | 356 |
| Source-selected 466 | 10% original (uncertified) | 185 | 12 | 120 | 161 |
| Source-selected 466 | 5% original (uncertified) | 25 | 0 | 132 | 309 |

Footnote: Previously observed source first14 identity agreement is neither authentic-standard identity nor independent instrument-source truth. The fixed rules act on the same search top1 but do not rerank that candidate. Acceptance is a historical software flag rather than a certified prediction-set or true error probability. The minimal top1-only mock is **not an existing competing EI software product**.

## Discussion — scientifically defensible utility argument

The complete, browser-accessible workflow provides an operational means for presenting candidate uncertainty and source-auditable reporting to researchers without requiring them to execute the underlying Python engine. This is a practical software delivery contribution, not a claim of formally measured ease of use; availability of a web address and passing headless tests alone do not establish adoption, accessibility compliance or independent performance across user laboratories. Historical review-routing results indicate that additional annotation skepticism can target many source-disagreeing top hits while imposing a substantial verification burden on agreeing hits. Selective screens do not remove erroneous chemical identifications, and our study did not observe user follow-up decisions. Increased output-field completeness is not equivalent to improved chemical inference.

These findings support an **auditable EI annotation reporting** contribution with transparent limitations; established prior methods already cover weighted cosine, score gaps and hit-confidence estimation. Comparisons to programs such as NIST, AMDIS, FastEI or LLM4MS must be framed as literature-dependent contextual capabilities unless a genuine matched-comparator test is performed. The present source-selected retrospective panels and software simulations cannot show state-of-the-art retrieval, chemical truth outside the fixed 8,455-reference library, or certified prospective 5% or 10% mistake rates.

## Figure and supplement integration

- Provide a reproducible workflow diagram showing original source SHA => reference SHA => existing EI top1 => HGB top-hit **scoring only** => tentative annotation plus rank10/metadata/warnings, with data-label provenance and no asserted authentic standards.
- Use Phase 3 AUROC/reliability/risk–coverage plots for mathematical justification, with no risk certificates.
- Use the Phase 5 four-cell routing table as **main text** or supplement, depending on word limits; both flagged-correct and flagged-incorrect numbers must be visible.
- Include **12 pre-existing unlabelled** output CSV and 120 ranked-candidate records as supplement, plus 2 headless UI tests and full CI artifact, software DOI and exact original source licence, without purporting to validate accuracy.
- Archive version/model/source and data role manifests with documented provenance and no raw third-party spectral source redistribution.

**Reproducibility source:** `docs/PHASE5_COMPUTATIONAL_SOFTWARE_UTILITY_VERIFIED_RESULTS_20261015.md`; GitHub Actions runs `38618746013` and `38619103980`.
