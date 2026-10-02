# Data provenance and reference-library handling

## Upstream source

The associated study used the public MS-DIAL EI/Kovats-RI spectral library deposited by Hiroshi Tsugawa on Zenodo:

- Zenodo record: `https://zenodo.org/records/21910638`
- DOI: `10.5281/zenodo.21910638`
- file used in the study: `GCMS DB-Public-KovatsRI-VS3.msp`

The software verifies the SHA-256 hash of the downloaded or local source before building the reference library. The expected hash is stored in `gcei/bootstrap.py`.

## Data handling

This repository does **not** redistribute:

1. the upstream MSP file; or
2. the derived reference spectral matrix and candidate metadata generated from that MSP.

The original Zenodo record remains the source for the third-party dataset.

On first launch, the program:

1. downloads the source from the original Zenodo record unless `GCEI_MSP_PATH` points to a local copy;
2. verifies the expected SHA-256 checksum;
3. parses the MSP using the preprocessing rules described in the study;
4. builds the local reference matrix and metadata;
5. deletes the temporary downloaded MSP.

The generated reference files are excluded by `.gitignore` and are not distributed with the software.

## Preprocessing rules

The reference builder applies the same preprocessing used in the study:

- nominal m/z values are obtained by the Python round-to-nearest-integer behavior used in the study;
- repeated nominal masses are summed;
- peaks with non-positive intensity are removed;
- exact-spectrum keys are generated from sorted nominal masses and intensities rounded to eight decimal places;
- exact spectra mapped to more than one connectivity identity are excluded;
- known non-molecular/artifact names are excluded;
- connectivity identity is the first 14 characters of the InChIKey;
- one reference spectrum is selected per connectivity identity using the same seed and calibration/test identity lists used in the study.

The resulting reference library contains 8,543 connectivity-level identities.
