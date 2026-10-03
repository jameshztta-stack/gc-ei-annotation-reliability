# Reproducibility verification

The software reconstructs the frozen v1.1 reference-search assets from the original MS-DIAL EI/Kovats-RI dataset and checks the outputs of the 12 independent botanical challenge spectra used in the study.

## Reference data

The source dataset is the creator-hosted Zenodo record `21910638` (DOI `10.5281/zenodo.21910638`). The exact source file is `GCMS DB-Public-KovatsRI-VS3.msp`, with publication SHA-256:

`a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70`

The original MSP and the derived reference matrix are not redistributed in this repository. The software obtains the source file from the original record, verifies its checksum, and constructs the runtime reference assets locally.

## Frozen scientific fingerprints

The reproducibility check validates the scientifically relevant reconstructed assets against frozen SHA-256 fingerprints:

- sparse reference matrix: `be75298636574bed4534788fabfc8647566fa27f10377ffe265ebc47a28de976`;
- reference RI vector: `01c2017a781362a4354e9e7c94c87caf8e86bf04c972a53ca8279675637f332b`;
- canonical reference metadata: `66c1ae7dac23e6dc08ab2a5e07418c9c2de0981e96101574ab6f3eb8ba646068`.

A fingerprint mismatch causes validation to fail rather than silently applying the frozen calibration to a different reconstructed reference library.

## Botanical regression checks

After the reference fingerprints pass, the validation reruns all 12 botanical challenge spectra and checks, within fixed numerical tolerances:

- highest-ranked candidate;
- EI similarity;
- 90% conformal candidate-set size;
- predicted top-1 correctness.

Run the complete validation with:

```bash
python scripts/check_reproducibility.py
```

or provide the exact local MSP explicitly:

```bash
python scripts/check_reproducibility.py --msp "/path/GCMS DB-Public-KovatsRI-VS3.msp"
```

The GitHub reproducibility workflow executes this end-to-end validation on the repair branch, pull requests and `main`.
