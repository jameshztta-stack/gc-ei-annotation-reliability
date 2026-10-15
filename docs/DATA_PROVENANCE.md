# Data provenance and reference-library handling

> **Important version boundary (clarified 15 October 2026):** The historical generic reference-library workflow described below corresponds to the older **v1 library of 8,543 first14 identities**, **not** the currently deployed **v2.0.2 GC–EI–MS workflow**, whose frozen reference contains **8,455 identities** and a separately pinned 12-feature HGB model. Both historical source versions are retained; do **not** mix their identity sets, algorithms or RI/conformal claims. For current v2 use the exact SHA-256 identifiers below, `models/v2/release_manifest.json`, `gcei/v2_engine.py` and the v2-specific audits. Neither research phase redistributes the original publisher MSP.

## Current v2.0.2 source/reproducibility lock

- Original MS-DIAL source library: **28,220** MSP records, SHA-256 `a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70` (publisher Zenodo DOI `10.5281/zenodo.21910638`).
- Corrected v2 audit selection: **13,111** retained distinct source-spectrum fingerprints; **8,455** reference first14 identities with frozen reference-index SHA-256 `2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01`.
- Fixed v2 HGB SHA-256 `a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13`. Spectral retrieval m/z¹ × sqrt(intensity), HGB top-hit correctness assessment; **no current v2 RI fusion and no conformal future coverage claims**.
- Only tentative database chemical-connectivity annotation is represented; neither prospective 5% nor 10% risk certification succeeded. Upstream license metadata are incomplete: **1,119/13,111** retained source records have no per-record LICENSE value. No assumption of public-domain rights or data redistribution permissions is implied.
- See `docs/PHASE6_SUPPLEMENTARY_DATA_AND_EXCEPTION_EVIDENCE_20261015.md` for source, chemical exceptions, licensing, split roles and reviewer-facing supplemental provenance.

## Historical v1 source-handling and reference rules

## Upstream source

Method development used the public MS-DIAL EI/Kovats-RI spectral library deposited by Hiroshi Tsugawa on Zenodo:

- Zenodo record: `https://zenodo.org/records/21910638`
- DOI: `10.5281/zenodo.21910638`
- source file: `GCMS DB-Public-KovatsRI-VS3.msp`

The software checks the downloaded or local source file against the expected SHA-256 value stored in `gcei/bootstrap.py` before building the reference library.

## Data handling

This repository does **not** redistribute:

1. the upstream MSP file; or
2. the derived reference spectral matrix and candidate metadata generated from that MSP.

The original Zenodo record remains the source for the third-party dataset.

On first launch, the software:

1. downloads the source file from the Zenodo record unless `GCEI_MSP_PATH` points to an exact local copy;
2. verifies the expected SHA-256 checksum;
3. parses the MSP using the study preprocessing rules;
4. builds the reference matrix and metadata locally;
5. deletes the temporary downloaded MSP.

Generated reference files are excluded by `.gitignore` and are not distributed with the software.

## Preprocessing rules

The reference builder applies the preprocessing used during method development:

- nominal m/z values use the same Python round-to-nearest-integer behavior;
- repeated nominal masses are summed;
- peaks with non-positive intensity are removed;
- exact-spectrum keys are generated from sorted nominal masses and intensities rounded to eight decimal places;
- exact spectra mapped to more than one connectivity identity are excluded;
- known non-molecular or artifact names are excluded;
- connectivity identity is defined by the first 14 characters of the InChIKey;
- one reference spectrum is selected per connectivity identity using the same seed and calibration/test identity lists used during method development.

The resulting reference library contains 8,543 connectivity-level identities.
