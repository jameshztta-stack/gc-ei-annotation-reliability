# Changelog

## 1.0.0 — 2026-10-04

- Prepared the public v1.0.0 release of the GC–EI Annotation Reliability Tool.
- Preserved the validated v1.1 scientific workflow and calibration parameters.
- Verified end-to-end reconstruction of the reference assets against reference SHA-256 fingerprints.
- Reproduced all 12 botanical regression spectra within fixed numerical tolerances.
- Verified single-spectrum EI-only and EI+RI inference, 10% and 5% empirical operating points, conformal candidate sets, and downloadable CSV output.
- Added fail-safe handling for malformed or non-positive inputs without exposing internal tracebacks.
- Added warnings when RI assistance changes the EI-only top candidate and when the original EI-only candidate shows large RI disagreement.
- Added downloadable single-spectrum and batch CSV templates with direct input instructions.
- Added citation guidance and developer/maintainer information.
- Documented the independent coriander, cumin, fennel and *Ilex umbellulata* challenge analyses.
- Refined interface and documentation language for concise scientific presentation.
- Verified desktop and mobile rendering of the public Streamlit application.

## 0.2.0 — 2026-10-02

- Added the GitHub/Streamlit implementation of the GC–EI annotation method.
- Added automatic acquisition of the upstream MS-DIAL MSP from its original Zenodo record.
- Added SHA-256 verification of the source file used in the study.
- Kept the upstream spectral library and derived reference matrix outside the repository.
- Added EI and EI+RI confidence models and calibration constants used in the study.
- Added single-spectrum and batch Streamlit interfaces.
- Added result interpretation and CSV downloads.
- Added botanical reproducibility checks.
- Added GitHub Actions tests, citation metadata, data provenance, deployment guidance, and scientific interpretation documentation.
