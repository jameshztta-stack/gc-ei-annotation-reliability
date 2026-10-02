# Reproducibility verification

The software can reconstruct the reference-search files from the original MS-DIAL EI/Kovats-RI dataset and reproduce the expected outputs for the example spectra supplied with this repository.

## Reference data

The source dataset is the creator-hosted Zenodo record `21910638` (DOI `10.5281/zenodo.21910638`). The original MSP and the derived reference matrix are not redistributed here. The software obtains the source file from the original record, verifies its SHA-256 checksum, and constructs the reference files locally.

## Reproducibility checks

The supplied scripts check that:

- the expected reference identities are reconstructed;
- the reference RI information is reproduced;
- the 12 botanical example spectra return the expected top candidate;
- the 90% conformal candidate-set sizes are reproduced;
- spectral similarities and predicted top-1 correctness agree with the values used in the study within numerical tolerance.

These checks are intended to make the implementation transparent and reproducible without redistributing the third-party spectral library.
