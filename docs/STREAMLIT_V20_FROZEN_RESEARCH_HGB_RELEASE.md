# Streamlit v2.0.0 — exact frozen research reference and HGB integration

Release preparation: 14 October 2026. **Main scientific claim:** This app enables a
separate 8,455-identity, EI-only *exploratory research v2* software configuration,
with frozen original first14 reference indices and the exact HGB fitted on
previously selected 1,410 development queries. **It is NOT certified accurate
identification of an experimental substance or a 5%/10% risk guarantee.**

## Frozen references and models

| Asset | Version and immutable SHA-256 |
|---|---|
| Original MS-DIAL EI MSP source: 28,220 records | a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70 |
| Research v2 selected 8,455 first14 reference index | 2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01 |
| Original frozen HGB correct-first14 classifier, 1,410 dev rows | a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13 |
| Original 1,410 development feature ledger SHA | 67a209e835279852a91e92abad7a3598fd38f6fd6978082b75c46d6eb4a745ce |

v2 inference uses original nominal EI masses 0–6420, sums duplicate
m/z-bin positive intensities, applies exactly float64 **m/z¹ × sqrt(intensity)**
weighted and L2-normalized cosine to the entire first14-ordered 8,455
reference panel, with stable reference ordinal tie handling.
The HGB operates on 12 fixed search-observable features using original source
nominal positive peak counts/intensity support and cosine ranks/spacing.
Only preexisting original 1,410 development labels fitted that HGB.

The original serialized model is committed from a successful GitHub Actions
build that reproduced the old SHA **byte for byte**. The pre-pinned 8,455
index was copied from the original Phase1.6 archival artifact, *not*
reconstructed or tuned from later correctness. The release source contains
only the indices, associated metadata and trusted model bytes; original
third-party EI spectra are downloaded from their public publisher
and verified byte for byte, not redistributed with software.

## User application behavior

- **Research v2 is default**: frozen 8,455 original reference, EI-only cosine,
  HGB score, 10 candidate ranks, source/checksum disclosures and separately
  applied original 5%/10% historical acceptance *rules*.
- Legacy v1 remains selectable as a **separate original 8,543 first14 reference
  and matching v1 model**. Its original RI and nominal 90% conformal behavior
  are available only inside legacy v1; the two models/ref pools are not mixed.
- Fixed v2 thresholds: nominal 10%-target requires HGB ≥0.87; nominal 5%-target
  requires HGB ≥0.94 AND top-one minus top-two EI cosine ≥0.20. Both
  **FAILED formal independent selective-risk certification**. A passing
  threshold is not confirmed identification or guaranteed performance.
- **No v2 Kovats RI fusion**, **no v2 nominal conformal set**, **no v2 out-of-library
  or stereoisomer identification**. Any RI input in the v2 batch is rejected
  when nonempty. The v2 rank list is not misrepresented as a calibrated
  coverage/uncertainty candidate set.
- CSV exports include the current model selection, source SHA, reference
  SHA, HGB model SHA, top candidates, margin, score and uncertified risk
  decisions.
- The live model reports first14 database-connectivity candidate matches;
  no authentication of true material chemical identity, original sampling
  provenance or standalone clinical/forensic decision suitability.

## What 609 source-locked test performance actually demonstrated

The original predeclared one-shot 609 previously reserved MS-DIAL query
benchmark selected compounds **already in the search reference**. It showed
m¹ top1 published first14 agreement **394/609 = 64.70%**, top5 **489/609**,
top10 **509/609**. Frozen HGB Brier was **0.1406**, AUROC **0.8633**
on these within-source database labels. Original 10%-target threshold
accepted **198/609** with **12 observed label mismatches**; original 5%-target
accepted **38/609** with **zero observed mismatches**. These observed rates
**do NOT certify** future 10% or 5% conditional errors or confirm chemical
identification; only 6.2% of 609 pass the stricter rule. Original 609 data
are permanently **spent**, not a new clean test for any model changed now.

Source experiment ancestry and truly independent authentic standard truth
have not been demonstrated. Moreover 69 original 609 source labels were
seen in the earlier 466-source retrospective chemical subset; all 609
remain in their original denominator.

## Validation, reproducibility and deployment

A dedicated release builder copies the **unchanged original Phase1.6 reference
index** and rebuilds the **exact original trusted HGB** under numpy 2.3.5 /
scikit-learn 1.8.0. SHA mismatch aborts. Streamlit generates searchable
original-source EI reference matrices with the exact locked indices and
does not silently replace them with its legacy 8,543 reference. The engine
stores its original unweighted peak bins separately so the 12 HGB features
do not accidentally get measured on transformed m/z-weighted intensities.

Dedicated unit tests must verify EI features, exact source/model checks,
RI rejection in v2, batch output, acceptance logic and v1 unchanged.
The source-native app parity workflow replays the **already spent 609**
only to check **software implementation parity**, never to fit a model or
present as new scientific validation. Deployment requires GitHub unit CI,
legacy reproducibility and this exact app parity run to pass. External
Streamlit hosting may redeploy on a merged main branch, but success at
GitHub does **not** independently establish that the public URL loaded.

No separate independent source experimental validation, measured authentic
reference standard, 5%/10% prospective risk certification or publishable
algorithmic novelty is asserted by the software update.
