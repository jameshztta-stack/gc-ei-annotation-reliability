# Data provenance and reference-library handling

## Upstream source

The associated study used the public MS-DIAL EI/Kovats-RI spectral library deposited by Hiroshi Tsugawa on Zenodo:

- Zenodo record: `https://zenodo.org/records/21910638`
- DOI: `10.5281/zenodo.21910638`
- publication file used by this workflow: `GCMS DB-Public-KovatsRI-VS3.msp`

The software verifies the SHA-256 hash of the downloaded/local source before building the runtime reference library. The expected hash is stored in `gcei/bootstrap.py`.

## Redistribution decision

The Phase 2 release candidate does **not** redistribute:

1. the upstream MSP file; or
2. the derived reference spectral matrix and candidate metadata generated from that MSP.

This conservative design was chosen because the upstream Zenodo record should remain the authoritative distribution point for the third-party dataset.

On first launch, the program:

1. downloads the exact source from the original Zenodo record (unless `GCEI_MSP_PATH` points to a local copy);
2. verifies the expected SHA-256 checksum;
3. parses and audits the MSP using the publication rules;
4. builds a local reference matrix and metadata in `runtime_assets/`;
5. deletes the temporary downloaded MSP.

The runtime assets are excluded by `.gitignore` and are not part of the software release.

## Publication preprocessing rules

The reference builder reproduces the publication preprocessing:

- nominal m/z values are obtained by Python round-to-nearest-integer behavior used in the validated workflow;
- repeated nominal masses are summed;
- peaks with non-positive intensity are removed;
- exact-spectrum keys are generated from sorted nominal masses and intensities rounded to eight decimal places;
- exact spectra mapped to more than one connectivity identity are excluded;
- known non-molecular/artifact names are excluded;
- connectivity identity is the first 14 characters of the InChIKey;
- one fixed reference spectrum is selected per connectivity identity using the publication seed and fixed calibration/test identity lists.

The resulting publication reference library contains 8,543 connectivity-level identities.
