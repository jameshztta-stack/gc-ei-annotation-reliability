# GC–EI Annotation Reliability Tool

**Version 0.2.0**

An interactive implementation of the uncertainty-aware GC–EI–MS library-annotation method developed in our study. The tool is intended to help researchers decide whether a conventional GC–EI library-search result supports a single tentative candidate, a calibrated set of candidates, or no exact single-candidate annotation.

## What the tool returns

For a user-supplied EI spectrum, the current version returns:

- highest-ranked connectivity-level candidate;
- top-10 candidate list;
- calibrated `m/z^1 × intensity^0.5` EI similarity;
- predicted probability that the highest-ranked candidate is correct;
- 90% split-conformal candidate set and candidate-set size;
- empirical 10% or 5% target-error selective-prediction decision;
- optional RI-assisted scoring when a **Kovats RI** is supplied;
- downloadable single-spectrum and batch results.

The software does **not** claim authentic-standard identification. Low confidence or a broad candidate set also does **not** prove that a compound is absent from the reference library.

## Method implemented

The tool implements the methodological choices and calibration values used in the study:

- identity = first 14 characters of InChIKey;
- exact-spectrum duplication removed before benchmark development;
- EI score = `m/z^1 × intensity^0.5` weighted cosine;
- conformal margins derived from the publication calibration identities;
- confidence model derived from the publication calibration split;
- empirical selective-prediction thresholds derived from the publication risk-calibration analysis;
- optional RI fusion = `0.8 × EI + 0.2 × exp[-0.5 × (ΔRI/10)^2]`.

The web application applies these published parameters directly to user-supplied spectra.

## Reference library

The study used the public MS-DIAL EI/Kovats-RI spectral library:

**Tsugawa H. `msdial_eimslib_kovatsri`. Zenodo. DOI: 10.5281/zenodo.21910638.**

File used in the study: `GCMS DB-Public-KovatsRI-VS3.msp`.

The upstream MSP and the derived reference matrix are **not stored in this repository**. At first launch, the program obtains the source file from the original Zenodo record, verifies its SHA-256 checksum, and constructs the required reference files locally. See [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md).

## Quick start

```bash
python -m venv .venv
```

Activate the environment and then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The first launch prepares the reference-library files. To use an already downloaded exact MSP instead of downloading it again, define `GCEI_MSP_PATH` before launching the app.

## Input format

### Single spectrum

```text
mz,intensity
41,82.1
43,44.6
69,71.5
93,100
121,18.3
136,14.2
```

### Batch spectra

```text
spectrum_id,mz,intensity,ri
Peak_1,41,82.1,939
Peak_1,93,100,939
Peak_2,43,65.2,
Peak_2,71,100,
```

The `ri` column is optional and must contain **Kovats retention index**, not raw retention time.

## Reproducibility

The repository contains automated checks for the reference-library construction and the 12 botanical example spectra used in the study. See [`docs/VERIFICATION.md`](docs/VERIFICATION.md).

## Deployment

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the GitHub, Streamlit Community Cloud, and Zenodo publication steps.

## Reuse with a different EI library

The software can be adapted to another EI reference library, but the publication conformal margins and confidence thresholds should not be transferred directly to a different library. A new library requires screening for exact duplicates and identity leakage, construction of independent query/reference spectra, calibration of conformal nonconformity scores, and refitting and validation of the confidence model.

## License

The project software is released under the MIT License. Third-party spectral data are not included under that license. See [`NOTICE`](NOTICE) and [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md).

## Citation

The final manuscript citation and Zenodo software DOI will be added when the software is archived for publication. `CITATION.cff` is included so GitHub can expose the preferred software citation metadata.
