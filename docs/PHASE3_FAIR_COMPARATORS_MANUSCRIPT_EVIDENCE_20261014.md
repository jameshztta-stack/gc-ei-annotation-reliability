# Phase 3 — Fair confidence baselines, paired retrospective statistics and software contribution

Date: **14 October 2026**. **Research-only, previously exposed outcome analysis.**
No model, threshold, reference index, deployment or source data was changed in this phase.

## Scope and frozen assets

The live EI-only v2.0.2 uses the frozen **8,455 InChIKey-first14 reference index**, nominal `m/z^1 * sqrt(intensity)` weighted cosine and original 12-feature HistGradientBoosting classifier. Source-matched reference search still determines top-1; the confidence model estimates whether that first-ranked **database connectivity label** agrees with the source label. Confidence does not alter underlying top-1 retrieval.

- 609 original source-reserved MS-DIAL test identities **already scored once and permanently spent**, not fresh validation. Original outcome CSV SHA-256 `62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7`.
- 1,410 previously exposed development queries with nested out-of-fold probability models. Ledger SHA-256 `67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce`.
- 466 already exposed, selection-filtered SWGDRUG/RECETOX EI spectra, containing **419 unique** source first14 identities and **unverified** acquisition independence. Ledger SHA-256 `09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b`.
- Original unmodified research source commit: `9d5c57a44e57d3eed94c82930c2868e451573676`.

## Direct comparison on the same 609 source-labelled cases

| Screening/ranking signal for *top-1 correctness* | AUROC | Brier score |
|---|---:|---:|
| Highest EI cosine similarity, uncalibrated | 0.7067 | Not comparable as a raw probability |
| Top-1 minus top-2 EI similarity, uncalibrated | 0.8127 | Not comparable as a raw probability |
| Frozen HGB probability-like score | **0.8633** | 0.1406 |

HGB AUROC minus margin AUROC = **0.0506**; versus cosine alone = **0.1566**. A supplementary descriptive, row-paired 3,000-resample bootstrap gave approximate 95% intervals of **0.0276 to 0.0735**, and **0.1162 to 0.2014**, respectively. These are not prospective or source-independent intervals; source acquisition lineage was not established.

The original fixed historical **10%-target** rule (`HGB >= 0.87`) accepted **198/609**, with **12** wrong database labels; the **5%-target** rule (`HGB >= 0.94 AND top1-top2 margin >= 0.20`) accepted **38/609**, with **0** wrong labels. **Neither rule is certified** for its named error target. These historical rules **must not be retuned from 609/466 outcomes**.

### Matched acceptance rates (post hoc, NOT prespecified operating thresholds)

All comparators accept the same **K highest** observations for their respective signal, using stable source-order tie resolution.

| Accepted K (of 609) | HGB incorrect | Margin-only incorrect | Cosine-only incorrect |
|---:|---:|---:|---:|
| 38 | 0 | 1 | 10 |
| 198 | 12 | **11** | 45 |
| 305 | **31** | 41 | 68 |
| 457 | **92** | 108 | 120 |
| 609 | 215 | 215 | 215 |

**Important distinction:** Top-K HGB-only at K=38 and the historical dual-condition 5% rule each contain 38 cases and have 0 observed errors, but only **36 of the accepted cases are shared**; their membership is not identical. Do **not** call the HGB-only top-K comparison an evaluation of the dual-condition decision rule.

The margin-only baseline is slightly better at K=198 (11 vs 12 errors); therefore, superiority is **not uniform** along the risk–coverage curve. Report curves, not only a favorable AUROC.

### Reliability

- 609 frozen HGB: **Brier 0.140645**, 10 equal-width-bin ECE **0.04494**; Brier skill versus constant observed-prevalence prediction approximately **38.42%**. Mean HGB score is not a probability that a chemical material was authenticated.
- The 0.2–0.3 score bin contains **67**, of which **10** have correct source first14 labels: observed correct fraction 0.149 versus mean HGB score approximately 0.248. Thus, the original model can be miscalibrated locally even with moderate overall ECE.
- In the **540/609** identities not overlapping the earlier 466 first14 set: HGB AUROC **0.8694**, margin AUROC **0.8287**, top-score AUROC **0.7028**. Still **previously spent** and source-dependent, not a clean untouched new test.

## Model complexity ablation from original 1,410 nested out-of-fold development

| Model | AUROC | Brier |
|---|---:|---:|
| 5-feature logistic | 0.85147 | 0.14835 |
| 12-feature logistic | **0.85560** | 0.14675 |
| 12-feature HGB | 0.85528 | **0.14416** |

The numerical Brier improvement of HGB over 12-feature logistic is **0.00258**; a descriptive paired 3,000-resample bootstrap returned a 95% interval of approximately **−0.0013 to +0.0064**, including zero. **Do not assert definitive architectural superiority of HGB**, especially given exposed development data and correlated validation roles.

## Error taxonomy to report

In the **609** source-locked cases (all included): **394** top-1 matches, **95** correct source labels at ranks 2–5, **20** at ranks 6–10, and **100** below rank 10.

In the previously examined **466** selected-source cases: **334** top-1 matches, **67** at ranks 2–5, **6** at ranks 6–10 and **59** below top 10. Among **132** incorrect first14 top-1 candidates, **50** have the same molecular formula as the publisher-matched reference (potential constitutional isomer ambiguity) and **82** have different formula. These are chemical-descriptor comparisons, not authenticated ground truth.

## Software contribution — independently inspectable claims

The current app is **version 2.0.2**, exposing one current v2 model. Existing source supports:

1. Single-spectrum and batch inputs, documented input templates, and top-10 indexed EI candidate ranking from the **8,455** frozen database-connectivity reference.
2. HGB score; explicit historical-rule decisions; plain-language disclaimers about uncertified 5%/10% targets and absent authentic-standard confirmation.
3. CSV downloads of ranked candidates/batch annotations and the original source, reference-index and model SHA-256 provenance information.
4. Source checks at runtime and reproducibility test/parity reports. A 609-case replay previously checked **software equivalence**, not new scientific accuracy.
5. Clear separation from old v1, which used a different **8,543-reference** model and separate RI/conformal configuration; **v2 cannot claim v1 RI fusion or v1 conformal coverage**.

Do not claim name-search of the whole library unless separately demonstrated in the software interface; here 'library search' means spectral nearest-candidate ranking.

Suggested primary manuscript figures: **(1)** frozen EI workflow and model/split lineage; **(2)** paired AUROC and matched risk–acceptance curves; **(3)** reliability bins including exact denominators; **(4)** error taxonomy and annotated ambiguous-matches examples; **(5)** software screenshots and a checksum-backed reproduction table.

## Reviewer-style claim boundary

**Defensible:** Within-source and retrospective source-selected evidence indicates that combining search-observable features in a frozen HGB estimator can better rank top-1 first14 correctness than cosine alone, while practical software supplies provenance-aware ambiguous library matches.

**Not defensible:** New EI spectral search algorithm; HGB universally superior to simpler logistic alternatives; improved underlying top-1 retrieval caused by confidence prediction; chemically authenticated identity; independent experimental provenance for 609/466; valid controlled 5%/10% future errors; prospectively calibrated 90% v2 conformal sets; out-of-library detection; head-to-head superiority to NIST or other modern EI models.

**External laboratory experiments are not a prerequisite for completion of this explicitly computational study**, but absence of independently authenticated material/source transfer must remain a substantial manuscript limitation.

## Machine-readable results

See `audits/phase3_retrospective_confidence_20261014/phase3_paired_summary.json`,
`609_paired_risk_coverage.csv`, and `466_paired_risk_coverage.csv`. The new `scripts/phase3_paired_confidence_audit.py` independently recomputes all main statistics from SHA-pinned archives. The GitHub Action `.github/workflows/phase3-fair-confidence-audit.yml` replays those archived (spent) ledgers and compares every accepted-case count to the committed descriptive curves. It is an **engineering/scientific reproduction check, not fresh external validation**.
