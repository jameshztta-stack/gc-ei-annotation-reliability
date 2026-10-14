# Streamlit v1.0.1 — scientific clarity, reproducible exports, source integrity

Release preparation: 14 October 2026. The public Streamlit **v1.0.1 interface** retains exactly the **v1.0.0 numerical model artifacts, 8,543-entry reference, EI weighting, conformal margins, RI fusion parameters and historical selection thresholds**. This is a non-model-changing scientific communication, usability and source-transfer patch. It is NOT deployment of research v2 (8,455 entries). Do not cite research v2 performance as actual live v1.0.1 accuracy.

## User-visible changes

- Visible and expanded description of scope: annotations are **tentative** and first14 connectivity-based; model score is a source-dependent historical estimate rather than an authenticated identification probability.
- The originally labelled 5% and 10% risk **targets remain uncertified** (no false claim of bounded future errors). A passing result uses neutral informational wording instead of a green success banner.
- The candidate-set **nominal 90%** confidence label explicitly warns that prospective 90% coverage is unverified across sources, instruments, samples and calibration shifts. Retains complete download, data tables, default numerical candidate values and identical inference paths.
- Sidebar reports software interface version 1.0.1, original 8,543-connectivity v1 reference, and complete publisher source SHA-256.
- Single and batch CSV exports retain existing machine-readable column labels for backward compatibility, with **additional** source checksum, app-version and noncertified scientific-status flags.
- Batch uses same original inference but rejects a spectrum when a supplied RI is contradictory across rows, negative, nonfinite or nonnumeric. Missing RI is allowed. A consistent positive finite Kovats RI still works.
- Startup downloader can use an *independently accessible historical publisher URL for the exact same source bytes* if the first Zenodo record is unavailable or serves nonmatching bytes. All downloaded candidates are SHA-256 checked before atomic placement; any nonmatching file is rejected, the frozen source SHA is never replaced, and the original third-party spectra are never redistributed.

## Scientific interpretation, model integrity, and security

The v1.0.0 reference is **8,543 first14 connectivities**, and the archived v1 model JSON files remain byte-identical. In contrast, the separately developed v2 research reference **8,455 first14 connectivity compounds**, HGB score and within-MS-DIAL heldout outcome **394/609** are different. No one should attribute those v2 metrics or acceptance counts to the live v1 runtime.

Original 609 v2 within-MS-DIAL source-label accuracy does NOT establish independent laboratory source, physical authentic standard truth, open-world chemical identification or finite-sample 5%/10% errors. The original v2 609 is permanently evaluated and cannot become an untouched test for a v1.0.1 software change.

No experimental v2 reranker, threshold or calibrator is transferred to the live application; its model version remains the public research v1 configuration. No net inference-quality improvement is claimed. Updates are publicly auditable via PR/commit history and existing GitHub regression/reproducibility checks.

No raw SWGDRUG or RECETOX source peaks are redistributed or licensed by this app's MIT software license. The original MS-DIAL source is obtained from the publisher (or the same immutable exact-SHA historical copy) as before. Users must evaluate upstream data terms independently.

## Deployment checklist

1. Run GitHub pull-request **CI** (unit tests) and **Reproducibility check** workflow against the original SHA-pinned MSP and v1 model reference. A static import/compile check should validate \`app.py\`; new tests must check source transfer and RI consistency.
2. Merge the reviewed patch branch to **main**, preserving the v1.0.0 tag/release. Streamlit Community Cloud projects configured to deploy \`main\` may automatically restart; merging to GitHub **does not independently prove that an external Streamlit hosting service deployed successfully**.
3. Verify the hosting app URL from its actual deployment configuration (unknown to repo metadata), confirm version 1.0.1 in the sidebar, import and analyse a sample EI spectrum, check CSV downloads, batch results and relevant error warnings. Obtain app host logs if source retrieval or memory limits prevent startup.
4. Retain the original v1.0.0 frozen tag/DOI. A subsequent **v2.0 model upgrade** requires an isolated versioned runtime, matched 8,455 reference/model artifacts, cross-run inference parity and accurate performance disclosures. Do not blend v1 and v2 configuration.

## Intentionally not claimed

- Certified 5%/10% future selected-risk guarantees
- Verified 90%/95% prospective candidate-set coverage on independent laboratory data
- Confirmed identity of authentic chemical standards or stereoisomers
- Accuracy superiority over FastEI, NIST, LLM4MS or other contemporary GC–EI–MS software
- Conversion of a v2 development/HGB model into the unchanged v1 model
- Live Streamlit host redeployment without inspecting the host
