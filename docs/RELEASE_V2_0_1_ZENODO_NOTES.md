# GC–EI Annotation Reliability Tool v2.0.1

## What's changed

**A cleaner interface for GC–EI–MS researchers.** The annotation page now presents the reference-model selector, single-spectrum/batch input, one analysis action, ranked candidates and concise result metrics. Long methodological descriptions, validation warnings, source hashes, input examples and detailed downloads are organized into collapsed panels, with scientific caveats still readily available.

- Minimal, centered Streamlit layout with a neutral white theme.
- The exact frozen **v2 research configuration** (8,455 source-locked first14 reference identities and development-trained 12-feature HGB model) remains the default.
- Original **legacy v1** (8,543 identities with its separate RI and nominal conformal settings) remains available.
- Source data and model loading occurs on analysis, rather than monopolizing the page while it opens.
- Single/batch results remain downloadable, with the correct model/version/asset provenance and explicit uncertified-risk fields.
- Technical validation details and original-source citations remain accessible under *Methods, limitations & provenance*.
- No changes to spectral weighting, reference identity selection, matching tie-breaks, HGB features/model, historical decision rules or source-data checksums.

## Interpretation and scientific limits

The software reports **tentative, connectivity-level database-label candidates**. The one-time original within-MS-DIAL heldout study matched **394/609 (64.70%)** source-reported first14 labels at top1 on reference-included compounds. **This is not independent experimental identity authentication.** The 10%-target rule accepted 198/609 with 12 publisher-label mismatches; the stricter 5%-target accepted 38/609 with zero observed mismatches. **Neither target is a certified bound on errors for future laboratory samples.** No v2 retention-index recalibration, prospective conformal coverage, unknown out-of-library detection or exact chemical-species confirmation has been demonstrated.

Independent replay of the originally spent 609 cases previously established **exact software parity** between the deployed v2 engine and frozen research results. Those cases cannot be used as a new untouched test set for changing models or thresholds. Version 2.0.1 changes presentation, not the scientific inference method.

## Reproducibility and licensing

Source code: https://github.com/jameshztta-stack/gc-ei-annotation-reliability

Web app: https://gc-ei-annotation.streamlit.app/

The MIT software archive contains the locked **8,455-record reference index and trusted HGB model**, but does **not** redistribute the original MS-DIAL publisher EI spectral peak database or third-party SWGDRUG/RECETOX raw spectra. The application retrieves the source from the publisher (or a byte-identical source URL) and checks the original frozen MSP SHA-256 before use.

**Original source SHA-256:** a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70

**v2 reference-index SHA-256:** 2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01

**v2 HGB model SHA-256:** a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13

## Zenodo new-version policy

This GitHub release should create a **new Zenodo software version 2.0.1**, linked to the previously archived v1.0.0 version, if the GitHub repository is enabled in the owner's Zenodo GitHub integration. The **existing v1.0.0 version-specific DOI 10.5281/zenodo.23143113 must remain unchanged**. The new v2.0.1 version DOI must be checked on Zenodo *after publication*, then cited for this new software; do not reuse the old DOI as though it describes v2.

If the GitHub/Zenodo webhook is not connected or fails, the repository owner can use the **New version** action on the previous Zenodo record and upload a ZIP snapshot of the GitHub v2.0.1 tag. Do not create an unrelated Zenodo software record if a linked new-version draft is available. Record the actual new DOI only once Zenodo publishes it.
