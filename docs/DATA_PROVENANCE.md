# Data provenance and chemical reference preparation

This document describes the spectral data and reference selection used by the **GC–EI–MS Annotation Tool, version 2.1.0**.

## Original EI spectral source

The study uses the publicly deposited MS-DIAL GC–EI–MS/Kovats-RI spectral library provided by Hiroshi Tsugawa:

- Source record: [Zenodo DOI 10.5281/zenodo.21910638](https://doi.org/10.5281/zenodo.21910638)
- MSP file: `GCMS DB-Public-KovatsRI-VS3.msp`
- Original records: **28,220**
- Original-file SHA-256: `a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70`

The software obtains the original MSP from the publisher or accepts an exact local copy through `GCEI_MSP_PATH`. A SHA-256 verification check ensures that the expected source file is used before reference construction.

## Reference preparation

The study's predefined inclusion and chemical-representation rules produced **13,111 retained distinct EI spectral fingerprints** associated with **8,455 InChIKey-first14 connectivity identities**. The application uses **one specified reference spectrum per connectivity identity** and the complete reference manifest SHA-256 `2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01`.

The numerical preprocessing applies the corresponding specified procedures: positive-intensity ion peaks, nominal mass binning by Python's rounding convention, summation of repeated nominal ions, `m/z × √intensity` weighting and unit-vector normalization before cosine comparison. Reference eligibility also uses the predefined molecular identifier, formula and duplicate-spectrum quality rules. See `gcei/v2_bootstrap.py`, `gcei/v2_engine.py` and `models/v2/reference_index.csv` for the executable specification.

The specified reliability model was developed using 1,410 designated development observations. The reference search and classifier have different roles: EI cosine determines the candidates' ranks, while the 12-feature classifier estimates whether the first candidate agrees with the publisher-provided connectivity label. The model SHA-256 is `a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13`.

## Chemical identity and source limitations

- The first 14 characters of an InChIKey encode connectivity-level information, **not a complete stereochemical or authentic-standard identification**.
- Among the retained spectra, **294 connectivity groups** contained more than one regenerated full Standard InChIKey, and **373 records** carried source-name qualifiers warranting review.
- **Six source records** involving **four connectivity groups** showed advanced InChIKey-layer differences despite agreement at the first14 connectivity level.
- Different source records and spectral fingerprints do not establish that the underlying substances were measured by independent laboratories or instrument runs. Original acquisition independence could not be verified from the available source metadata.
- **1,119 of 13,111** retained source records lacked an explicit per-record `LICENSE` field. Missing metadata do not establish that spectra are in the public domain or that all downstream uses are permitted.
- The existing in-reference source-label evaluations are **not an experimentally authenticated chemical-identification accuracy assessment**, and confidence screening does not establish guaranteed future error rates.

## Access rights and software distribution

The repository does **not** include the original publisher MSP or redistribute the reference peak arrays constructed from it. Reference files are generated locally from the publisher-hosted source after checking the source checksum, and their generated runtime files are excluded from the repository. Source availability and use remain subject to the original rights holders' conditions.

The repository's MIT software licence governs software source code. The original CompMS MSP spectral-library files are labelled **CC BY 4.0** on the [official CompMS licence page](https://systemsomicslab.github.io/compms/license/main.html); proper attribution, licence notice and consideration of any applicable separately contributed rights remain required. SWGDRUG and RECETOX comparison-data conditions are distinct; see [data use and attribution](DATA_USE_AND_ATTRIBUTION.md).

For the supported public application and its outputs, see the [project overview](../README.md) and [Streamlit application](https://gc-ei-annotation.streamlit.app/). The source-controlled software release is [GC–EI–MS Annotation Tool v2.1.0](https://github.com/jameshztta-stack/gc-ei-annotation-reliability/releases/tag/v2.1.0). Its separate Zenodo version DOI should be cited only when confirmed.
