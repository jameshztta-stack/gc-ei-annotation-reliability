# GC–EI–MS annotation manuscript v0.2 — Q1-sensitive, software-oriented draft

**Draft assembled:** 14 October 2026. **Research version:** fixed v2.0.2, 8,455 MS-DIAL connectivity reference identities, 12-feature frozen HGB, no RI/conformal v2. **Target positioning:** chemometric Original Software Publication / computational evaluation; title, abstract and headings require author review and journal guide conformity. No scientific model was refitted for this draft.

## Recommended title

**Auditable GC–EI–MS Library Annotation: Reproducible Software and Retrospective Evaluation of Top-Hit Reliability**

Other candid titles:
- **Evaluating the Reliability of GC–EI Mass-Spectral Library Matches: A Reproducible Computational and Software Study**
- **Beyond the Highest EI Spectral Match: Auditable Database-Connectivity Annotation with Retrospective Confidence Screening**

Avoid "novel mass spectral identification", "validated 5% error control", "independent chemical identification", "new HGB EI retrieval", "conformal" or "retention-index-integrated" in the current v2 title.

## Draft abstract (for manuscript, descriptive not prospective)

Electron-ionization (EI) mass-spectral library searching ranks candidate compounds by spectral similarity, but a high-scoring first match does not necessarily justify a unique chemical annotation. We implemented an auditable computational workflow that preserves conventional library ranking while separately estimating the reliability of its highest-ranked database-connectivity candidate. A public MS-DIAL EI collection was curated into a fixed reference of 8,455 InChIKey-first14 connectivity identities. Spectral ranking used mass-weighted cosine similarity, and a frozen 12-feature histogram gradient boosting classifier scored agreement between the first-ranked candidate and the publisher-reported connectivity label. Previously reserved, now evaluated within-source MS-DIAL queries (n = 609) and an independently published but retrospectively selected SWGDRUG/RECETOX source panel (n = 466) were examined without refitting either the similarity function or confidence model. On the 609-query benchmark, 394/609 (64.70%) publisher connectivity labels were ranked first. Correct-versus-incorrect top-hit discrimination yielded AUROC 0.8633 for the confidence model, compared with 0.8127 for the top-two similarity margin and 0.7067 for top cosine similarity; the HGB Brier score was 0.1406. Historical acceptance rules retained 198/609 cases with 12 mismatches and 38/609 cases with zero mismatches, respectively; neither attained a certified prospective 10% or 5% error guarantee. A checksum-verified open software implementation provides ranked candidates, explicit scope warnings, batch analysis, and provenance-linked exports. These results support transparent **tentative database-connectivity annotation**, not authentic-standard chemical identification or independently validated source transfer.

### Draft highlights (non-promotional)

- Frozen GC–EI spectral matching and correctness scoring are computationally reproducible.
- HGB discriminates source-labelled top-hit correctness better than cosine alone.
- A simple top-two similarity margin can match or exceed HGB at some acceptance levels.
- Neither historical 10%- nor 5%-target rule is statistically certified for future queries.
- Public software exports tentative candidate rankings with pinned-source provenance.

### Keywords
GC–EI–MS; library searching; chemometrics; confidence estimation; selective prediction; reproducibility; chemical annotation

## Main manuscript structure

### 1. Introduction

1. EI spectral retrieval is standard, and mass/intensity weighting is historical rather than a newly invented method (Stein & Scott, 1994).
2. Highest-score-only interpretation is limited by similarities, overlapping candidates and identity/source uncertainty; prior probability estimators already distinguish conditional in-library accuracy (Stein, 1994).
3. Prior first–second score-margin false-match control (Kim & Zhang, 2015), spectral uniqueness/RI-aware NIST research (McGlynn et al., 2025), and newer EI embedding/reranking/isomer/OOL methods demonstrate an extensive existing field.
4. **Specific open practical need:** a transparent, versioned source-dependent correctness-assessment implementation which separates published connectivity labels, retrieval rank, confidence, descriptive abstention and chemical-sample inference.
5. Define study objectives as: (a) source and identity curation + deterministic software, (b) unchanged EI ranking, (c) same-case retrospective HGB vs score and margin comparison, (d) failure/uncertainty taxonomy with full denominators, (e) reproducible user workflow without promising authenticated chemical identification.

### 2. Materials and computational methods

2.1 Original public MS-DIAL MSP acquisition and original publisher/source checksum (28,220 records; SHA recorded in GitHub).

2.2 Source quality, chemical-key/fingerprint checks and **frozen 8,455-entry** first14 reference, 13,111 retained source spectra, 2,019 original query-capable groups; disclose exceptions and 294 heterogeneous full standard InChIKeys.

2.3 Original **1,410 historical development** roles: 201 initial similarity development, 383 confidence-fitting, 403 originally risk calibration, 423 originally conformal calibration; historical results have been **exposed** and repurposed for exploratory model development, not fresh confirmatory calibration.

2.4 Mathematical EI similarity `m/z^1 sqrt(I)`, single source spectrum per first14 connectivity, deterministic tie precedence, and 12 search-observable HGB features. Explain precisely that HGB never reorders the reference library top-1.

2.5 Immutable first-score **609** originally reserved MS-DIAL query set (**now spent**) and separately 466 previously-exposed source-selected SWGDRUG/RECETOX entries (370+96, **419** unique connectivity labels). Original first14 overlap 69/609 with the previous 466 source panel, 540 other. Source acquisition-lab ancestry unresolved. No chemical authentic-standard performance inference.

2.6 Fair numerical baselines: raw top cosine, raw top1-top2 margin, fitted HGB correctness score; AUROC and same-case K-selected risk/error curve; probability Brier and bin reliability for HGB only. Historical fixed thresholds separately from descriptive K-matched points. Non-independent row-bootstrap intervals are merely descriptive, not subject-level transport uncertainty.

2.7 Software architecture, specific SHA/model environment, exact source verification, input parsing and rejection/warnings, v2 strict EI-only limitations, batch/single parity, frozen 12 botanical demo peaks **as software-only regression inputs**. No v1 conformal/RI findings transferred to v2.

### 3. Results

3.1 Curation/data-integrity transparency and chemical-key exceptions, no physical-experiment authentication.

3.2 Original 609 within-source: 394/609 first14 top1; 489/609 top5; 509/609 top10. Fixed reference, no HGB effect on retrieval.

3.3 Paired correctness screening AUROCs: HGB 0.8633; top margin 0.8127; top score 0.7067. Development OOF comparison 12f HGB Brier 0.14416 versus 12f logistic 0.14675: incremental, **not** robust proof of architecture superiority.

3.4 609 HGB Brier 0.14064; ten equal-width-bin ECE 0.04494; exact bin numerators. Explicitly note low-score miscalibration: score bin [0.2,0.3) n=67, only 10 publisher-label top1 agreements, mean score ~0.248.

3.5 Original historical 10%-target acceptance: **198/609**, **12** wrong; 5%-target **38/609**, **0** wrong. **Both NOT certified for target errors**. K=198 HGB 12 wrong, margin 11 wrong, top score 45 wrong; HGB does not win at every coverage.

3.6 Previously-exposed 466 source-selected: 334/466 source-label top1, HGB AUROC 0.87009, mean source attribution caveat and 419 unique labels. 466 source panel is not a new external test and cannot be pooled with original 609.

3.7 Error taxonomy: 609 ranks 1,2–5,6–10,>10 respectively **394/95/20/100**; the historical 466 analogous **334/67/6/59**. Chemistry caveats: same-formula incorrect candidates are *possible* constitutional isomers rather than confirmed misidentified samples.

3.8 Software proof: exact frozen inference parity on all 609 previously used cases, separate independent numerical audits and 12-botanical-peak input batch/single export regression. Distinguish software reproducibility from experimentally independent analytical truth.

### 4. Discussion

4.1 What correctness discrimination adds to fixed candidate rankings; neither an EI ranker nor a new basic algorithm.

4.2 Why some high-confidence outputs can still be incorrect (source label errors/chemical isomers/calibration shifts), no artificial certainty.

4.3 Comparison with prior art (Stein 1994 twice; Kim and Zhang 2015; McGlynn 2025; matchms, FastEI, LLM4MS, atomic reranking, recent EI probabilistic and out-of-library studies). **No cross-study percentage ranking**.

4.4 Limits: task only source first14 in-reference, no authentication, source-family dependence, input deconvolution/noise, no stereochemistry, no mixed peak separation, no RI/conformal v2, no OOL, empirical risk thresholds uncertified, retrospective tested curves.

4.5 Computational reproducibility/chemical annotation reporting benefit; future *optional* research directions include software fault injection and source-lineage audits. Do NOT imply these were conducted if not.

### 5. Conclusion

A reproducible implementation can expose the reliability limitations of source-labelled EI library retrieval by coupling unmodified spectral rankings with descriptive correctness estimation and explicit uncertainty reporting. Within-source retrospective discrimination provides useful evidence for ranking which matches warrant scrutiny, but it does not establish general error guarantees or independent molecular-identification accuracy.

## Figures and tables to generate/refer to

- **Main Figure 1:** source/spectrum fingerprint and chemical-connectivity/split lineage (original 28,220 → 13,111 → 8,455; 1,410 dev + 609 single-use; 466 external-source-selected retrospective), clear no-acquisition-independence boundary.
- **Main Figure 2:** baseline AUROC and full matched acceptance/error curves for 609, plus sample counts.
- **Main Figure 3:** HGB reliability diagram for 609 (bin n / count correct shown), independent auxiliary 466 in supplement.
- **Main Figure 4:** 609 hit-rank error taxonomy + 466 source-labelled confusion subdivisions, NO inferred experimental truth.
- **Main Figure 5:** actual v2 output structure: source SHA, top10 ranked candidates, immutable model, warning and single/batch example; figure derives from actual app, not a synthetic screenshot.
- **Main Table 1:** original dataset role, DOI, checksum, unit of independence, source-of-truth boundary.
- **Main Table 2:** previously exposed 1410 nested-OOF comparisons and 609/466 SAME-CASE comparisons, with independent denominators and no unsupported new p values.
- **Main Table 3:** historical 10/5 thresholds with accepted counts, wrong counts, observed error and NOT CERTIFIED; plus descriptive matched acceptance.
- **Supplementary:** source licence and access; exact role manifests; chemical exceptions; 466 source-specific records; all rank-order risk curves; model/processing SHA; CI provenance, DOI and code; exact finite-sample claims excluded.

## Originality and sources to check before author sign-off

See `PHASE4_PUBLISHED_PRIOR_ART_NOVELTY_AUDIT_20261014.md` for full DOI matrix and `PHASE4_ELSEVIER_JOURNAL_TARGETING_20261014.md` for journal/category rationale. The scientific article should **not** cite the software DOI as a peer-reviewed method validation, and no unrelated v1 RI/conformal numeric results should be presented as v2 results.

**Open review issues before submission:** editor's original software eligibility, quantitative user workflow utility beyond bundling existing methods, reproducibility by independent human, reference-license screening, exact current journal author guide, source-lab transfer caveat. These are **not** paper acceptance guarantees. No fabricated reference/benchmark/human user evaluation.
