# GC–EI Annotation Reliability Tool

**Version 1.0.0**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23143113.svg)](https://doi.org/10.5281/zenodo.23143113)

Reference implementation of the validated v1.1 uncertainty-aware GC–EI–MS library-annotation workflow.

## Scope

For a user-supplied EI spectrum, the software returns:

- the highest-ranked connectivity-level library candidate;
- the top 10 ranked candidates;
- `m/z^1 × intensity^0.5` weighted-cosine similarity;
- predicted top-1 correctness;
- a 90% split-conformal candidate set;
- an empirical 10% or 5% target-error decision;
- optional Kovats-RI-assisted scoring;
- downloadable single-spectrum and batch results.

Outputs are tentative spectral-library annotations. Definitive identification requires an authentic standard or suitable orthogonal confirmation. Low confidence or a broad candidate set is not evidence that a compound is absent from the reference library.

## Validated scientific workflow

Version 1.0.0 implements the validated v1.1 scientific settings:

- connectivity identity = first 14 characters of InChIKey;
- exact-spectrum duplicates removed before benchmark development;
- EI score = `m/z^1 × intensity^0.5` weighted cosine;
- conformal margins derived from the publication calibration identities;
- confidence models derived from the publication calibration split;
- empirical selective-prediction thresholds derived from the publication risk-calibration analysis;
- RI fusion = `0.8 × EI + 0.2 × exp[-0.5 × (ΔRI/10)^2]`.

No model fitting or recalibration occurs when a user submits a spectrum.

## Input format

### Single spectrum

Use two columns, one ion peak per row:

```csv
mz,intensity
41,82.1
43,44.6
69,71.5
93,100
121,18.3
136,14.2
```

Template: [`examples/template_single_spectrum.csv`](examples/template_single_spectrum.csv)

### Batch spectra

Use one row per ion peak. Repeat `spectrum_id` for all peaks belonging to the same spectrum.

```csv
spectrum_id,mz,intensity,ri
Peak_1,41,82.1,
Peak_1,93,100,
Peak_2,43,65.2,939
Peak_2,71,100,939
```

The `ri` column is optional. When RI is available, enter the Kovats RI and repeat the same value for all rows belonging to that spectrum. Do not enter raw retention time.

Template: [`examples/template_batch_spectra.csv`](examples/template_batch_spectra.csv)

The Streamlit interface also provides direct CSV-template downloads.

## Reference library

The study used the public MS-DIAL EI/Kovats-RI spectral library deposited by Hiroshi Tsugawa:

**Tsugawa H. `msdial_eimslib_kovatsri`. Zenodo. DOI: 10.5281/zenodo.21910638.**

Source file: `GCMS DB-Public-KovatsRI-VS3.msp`.

The upstream MSP and derived reference matrix are not redistributed in this repository. At runtime, the software obtains the exact source file from the Zenodo record, verifies its SHA-256 checksum, and reconstructs the validated v1.1 reference assets locally. See [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md).

## Independent botanical challenge data

Botanical spectra were kept separate from model development and calibration.

The public regression set contains 12 spectra from coriander, cumin and fennel. Historical annotations were used only for descriptive comparison, not as authenticated ground truth. A separate *Ilex umbellulata* case set was used to examine annotation ambiguity and abstention behavior rather than to calculate accuracy.

See [`docs/BOTANICAL_CHALLENGE_SETS.md`](docs/BOTANICAL_CHALLENGE_SETS.md) for the full interpretation.

## Reproducibility

Run:

```bash
python scripts/check_reproducibility.py
```

The validation rebuilds the reference assets, verifies the reference SHA-256 fingerprints of the spectral matrix, RI vector and metadata, and reruns the 12 independent botanical challenge spectra against the validated v1.1 outputs.

To use a local copy of the exact MSP:

```bash
python scripts/check_reproducibility.py --msp "/path/GCMS DB-Public-KovatsRI-VS3.msp"
```

The complete reproducibility workflow runs automatically on pull requests and `main`.

## Local use

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

To use an existing local MSP instead of downloading it at runtime, define `GCEI_MSP_PATH` before launch.

## Use with another EI library

The supplied conformal margins, confidence models and empirical thresholds are specific to the reference distribution used in the study. They must not be transferred directly to another library. A different reference library requires independent duplicate screening, query/reference construction, calibration, model fitting and validation.

## Citation

If results from this software contribute to a publication, cite both the associated research article and the archived software release.

**Associated article:** citation to be inserted after publication.

**Software release:** Zothantluanga JH. *GC–EI Annotation Reliability Tool*, version 1.0.0. Zenodo. 2026. DOI: [10.5281/zenodo.23143113](https://doi.org/10.5281/zenodo.23143113).

## Developer and maintainer

**Dr. James H. Zothantluanga**  
Research Director, Jazer Research Lab  
Aizawl, Mizoram 796005, India

## License

Software: MIT License. Third-party spectral data are not covered by the software license. See [`NOTICE`](NOTICE) and [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md).
