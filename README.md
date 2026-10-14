# GC–EI–MS Annotation Tool

**Version 2.0.2 — researcher-facing EI mass-spectrum library annotation**

[Open the app](https://gc-ei-annotation.streamlit.app/) · [Zenodo version history](https://doi.org/10.5281/zenodo.23143112)

## What this tool does

The **GC–EI–MS Annotation Tool** compares electron-ionization mass spectra with a reference library of **8,455 chemical-connectivity identities**, ranks the ten nearest spectral candidates, and reports similarity and a model-derived confidence score. Analyze one spectrum or multiple spectra from CSV, then download candidate annotations and source provenance.

**Interpretation:** Outputs are tentative InChIKey-first14 chemical-connectivity database matches. They do not establish authentic-standard molecular identity, stereochemistry, independent experimental source provenance or validated future error guarantees. Confirm compound identities with authentic standards or appropriate independent evidence.

## Input templates

Single spectrum: **mz,intensity**, one ion peak per line:

    mz,intensity
    41,82.1
    43,44.6
    69,71.5
    93,100

Batch spectra: **spectrum_id,mz,intensity**, repeating the same spectrum ID for all peaks within a spectrum:

    spectrum_id,mz,intensity
    Sample_1,41,82.1
    Sample_1,93,100
    Sample_2,43,65.2
    Sample_2,71,100

Template downloads and input descriptions appear **above** the upload/paste fields in the Streamlit app. Kovats RI is not supported by the current research model. The original v1 remains available as an archived software version, not a selectable model on the live website.

## Current computational configuration

- **Reference:** 8,455 original MS-DIAL EI first14 connectivity identities; exact source data SHA verified at runtime.
- **Spectral ranking:** nominal EI m/z¹ × sqrt(intensity), float64 weighted L2 cosine.
- **Confidence:** the already developed 12-feature HistGradientBoosting classifier, trained on the original 1,410 development spectra. No refitting or update from the 609 case outcomes.
- **Optional confidence screening:** original 10%-target rule (HGB probability ≥0.87), and strict 5%-target rule (HGB probability ≥0.94 AND top-two score margin ≥0.20). **Neither is a certified future error bound.**
- **Results:** top ten ranked library candidates, similarity, confidence estimate, screening decision and CSV files with study provenance.
- **Not offered by this model:** RI fusion, calibrated future conformal coverage, chemical detection outside the search library, exact molecular-form or authentic-standard confirmation.

### Evaluation and its limits

The original one-time 609-query closed-reference within-MS-DIAL test produced **394/609 (64.70%)** top-one publisher-reported first14 label agreement; top-five **489/609** and top-ten **509/609**. This is not an experimentally independent authentic-standard accuracy estimate. The original historical 10%-target rule accepted **198/609** (12 source-label mismatches); the stricter 5%-target rule accepted **38/609** (zero observed source-label mismatches). Neither passed valid independent risk certification.

The 609 evaluation is permanently spent as an untouched test and may only be replayed to check software parity, not to tune and advertise a newly independent evaluation. See [research method/limitations](docs/STREAMLIT_V20_FROZEN_RESEARCH_HGB_RELEASE.md) and [version 2.0.2 release notes](docs/RELEASE_V2_0_2.md).

## Source, code and reproducibility

- Original MS-DIAL publisher source SHA-256: a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70
- v2 reference index SHA-256: 2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01
- Original HGB model SHA-256: a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13
- Source: Tsugawa H., MS-DIAL public GC–EI–MS/Kovats-RI database, [Zenodo DOI 10.5281/zenodo.21910638](https://doi.org/10.5281/zenodo.21910638).

Upstream EI source spectra are not redistributed. The MIT software license does not supersede upstream database rights. See [data provenance](docs/DATA_PROVENANCE.md).

Local installation:

    python -m pip install -r requirements.txt
    streamlit run app.py

## How to cite

**Software:** Zothantluanga, J. H. *GC–EI–MS Annotation Tool*, version 2.0.2. Jazer Research Lab, 2026. Use the **v2.0.2 version-specific Zenodo DOI when published**; do not cite [v2.0.1](https://doi.org/10.5281/zenodo.23372495) as a replacement. [All-version concept DOI](https://doi.org/10.5281/zenodo.23143112).

**Research article:** The related evaluation manuscript is not yet a published paper. Cite it separately only after publication.

**Original spectral library:** Cite the [MS-DIAL EI source](https://doi.org/10.5281/zenodo.21910638) if you used the associated reference spectra.

**Developed and maintained by Dr. James H. Zothantluanga**, Research Director, Jazer Research Lab, Aizawl, Mizoram, India.
