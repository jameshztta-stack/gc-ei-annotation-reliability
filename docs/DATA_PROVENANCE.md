# Data provenance and reference-library handling

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
