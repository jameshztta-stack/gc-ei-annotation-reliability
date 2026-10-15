# GC–EI–MS Annotation Tool

**Current public software: version 2.0.2**

[Open the web application](https://gc-ei-annotation.streamlit.app/) · [Software DOI: 10.5281/zenodo.23373447](https://doi.org/10.5281/zenodo.23373447)

## Overview

The GC–EI–MS Annotation Tool assists with **tentative compound annotation** from gas chromatography–electron ionization mass spectra. It searches a defined reference library of **8,455 chemical-connectivity entries**, reports up to ten ranked candidates for a single spectrum, and provides spectral similarity, the difference between the two highest similarity scores, and a machine-learning estimate of **agreement with the publisher-reported connectivity label**.

The application works in a web browser. Researchers can enter or upload one EI mass spectrum, or upload a CSV containing multiple spectra. Single-spectrum results include a downloadable list of ten ranked candidates; batch results provide a downloadable summary containing the leading annotation for each spectrum.

**Scientific interpretation:** Reported candidates are tentative library matches at the level of the **first 14 characters of the InChIKey**. The confidence score does not represent an experimentally confirmed identification probability for an unknown sample. Results do not establish stereochemistry, identification of a compound absent from the reference library, or transferability to all instruments and laboratories. Confirm important chemical assignments using suitable independent evidence.

## Data input

**Single spectrum:** CSV columns `mz,intensity`, with one ion peak per row:

```csv
mz,intensity
41,82.1
43,44.6
69,71.5
93,100
```

**Batch spectra:** CSV columns `spectrum_id,mz,intensity`, with one spectrum ID repeated for all its peaks:

```csv
spectrum_id,mz,intensity
Sample_1,41,82.1
Sample_1,93,100
Sample_2,43,65.2
Sample_2,71,100
```

The application provides downloadable templates. Retention-index information is not combined with EI similarity in this implementation.

## Computational method

- **Reference data:** 8,455 InChIKey-first14 identities selected from the published MS-DIAL GC–EI library.
- **Candidate ranking:** conventional cosine similarity after nominal-mass binning and `m/z × √intensity` weighting.
- **Reliability assessment:** a 12-feature histogram gradient boosting classifier estimates whether the already highest-ranked candidate agrees with its publisher-reported first14 connectivity label. The classifier **does not reorder the candidates**.
- **Optional screening:** a standard criterion (model score ≥0.87) and a strict criterion (model score ≥0.94 and top-two score difference ≥0.20). These criteria **do not provide certified error rates** for new spectra.
- **Output:** single-spectrum top-ten candidate table and annotation summary; batch top-hit summary; confidence-related fields; source/library/model identifiers, where applicable.

### Evaluation

In an **in-reference, within-MS-DIAL evaluation involving 609 source-labelled query spectra**, the top-ranked connectivity agreed with the published label for **394/609 (64.70%)** cases; the top-five and top-ten counts were **489/609** and **509/609**, respectively. The standard screening criterion selected **198/609** cases, including **12 source-label disagreements**; the strict criterion selected **38/609**, with **zero observed disagreements**. These results are **retrospective observations**, not experimentally independent chemical-identification accuracy or guaranteed future error rates.

A separate analysis of selected spectra from published SWGDRUG and RECETOX collections is described in the associated research materials. Original laboratory acquisition independence has not been established.

## Data provenance and reproducibility

The computational implementation verifies the following SHA-256 checksums before using the corresponding source or model files:

| Resource | SHA-256 |
|---|---|
| Original public MS-DIAL source | `a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70` |
| 8,455-reference index | `2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01` |
| Reliability model | `a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13` |

**Original spectral library:** Hiroshi Tsugawa, MS-DIAL public GC–EI–MS/Kovats-RI library, [Zenodo DOI 10.5281/zenodo.21910638](https://doi.org/10.5281/zenodo.21910638).

The original MSP spectra are downloaded from their publisher and are not included in this repository. The **MIT licence applies to software code only**, not automatically to spectra obtained from third-party sources. See [data provenance](docs/DATA_PROVENANCE.md).

For local execution:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Citation

**Software:** Zothantluanga, J. H. *GC–EI–MS Annotation Tool*. Version 2.0.2. Jazer Research Lab (2026). [DOI: 10.5281/zenodo.23373447](https://doi.org/10.5281/zenodo.23373447).

**Data:** Cite the [MS-DIAL GC–EI–MS source](https://doi.org/10.5281/zenodo.21910638) in studies using the associated reference spectra.

**Developed and maintained by Dr. James H. Zothantluanga**, Research Director, Jazer Research Lab, Aizawl, Mizoram, India.
