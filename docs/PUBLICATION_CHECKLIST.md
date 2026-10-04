# Publication checklist

## Scientific consistency

- [x] Spectral weighting matches the study.
- [x] 90% and 95% conformal calibration values are documented.
- [x] EI confidence model matches the study.
- [x] EI+RI confidence model matches the study.
- [x] Empirical 10% and 5% target-error thresholds are included.
- [x] Botanical example outputs are available for reproducibility checking.
- [x] Out-of-library recognition is not presented as a validated capability.
- [x] RI ranking-change and large-ΔRI warnings are regression-tested.

## Public repository

- [x] GitHub repository created.
- [x] CI enabled on the public repository.
- [x] Reproducibility check completes using the original Zenodo source.
- [x] Repository URL included in `CITATION.cff`.
- [x] Single-spectrum and batch CSV templates included.
- [x] Citation guidance included.
- [x] Developer and maintainer information included.
- [x] Botanical challenge datasets documented.
- [x] Public-facing documentation reviewed for concise scientific language.

## Streamlit

- [x] App deployed from GitHub `main`.
- [x] First-startup Zenodo download tested.
- [x] Reference files build within deployment resource limits.
- [x] Single-spectrum EI-only mode tested.
- [x] EI+RI mode tested.
- [x] 10% and 5% operating points tested.
- [x] Batch mode tested against all 12 botanical regression spectra.
- [x] CSV downloads tested.
- [x] Invalid-input handling tested.
- [x] RI disagreement warnings tested.
- [x] Mobile layout inspected.

## Publication version

- [x] Version changed to `1.0.0`.
- [x] `CHANGELOG.md` updated.
- [x] Final CI and reproducibility workflows passed after the documentation and interface review.
- [ ] GitHub tag `v1.0.0` created.
- [ ] GitHub release created.
- [ ] Zenodo archive created.
- [ ] Software DOI inserted into `CITATION.cff`, README, app and manuscript.
- [ ] Associated publication citation inserted into README/app after publication details are available.
- [ ] Live app URL inserted into manuscript.
- [ ] Jazer Research Lab page linked.
