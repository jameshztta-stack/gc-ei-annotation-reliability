# Publication release checklist

## Scientific lock

- [x] Publication spectral weighting frozen.
- [x] 90% conformal calibration frozen.
- [x] 95% conformal calibration documented in manuscript but web tool defaults to 90%.
- [x] EI confidence model frozen.
- [x] EI+RI confidence model frozen.
- [x] Empirical 10% and 5% target-error thresholds frozen.
- [x] Botanical regression outputs frozen.
- [x] Out-of-library recognition excluded from user-facing positive claims.

## Public repository

- [ ] GitHub repository created.
- [ ] CI passes on public repository.
- [ ] Full release validation workflow passes.
- [ ] Repository URL confirmed in `CITATION.cff`.

## Streamlit

- [ ] App deployed from GitHub `main`.
- [ ] First-boot Zenodo download works.
- [ ] Reference assets build within deployment resource limits.
- [ ] Single-spectrum mode tested.
- [ ] Batch mode tested.
- [ ] CSV downloads tested.
- [ ] RI mode tested.
- [ ] Mobile layout inspected.

## v1.0.0 release

- [ ] Version changed from release candidate to `1.0.0`.
- [ ] `CHANGELOG.md` updated.
- [ ] Git tag/release `v1.0.0` created.
- [ ] Zenodo archive created.
- [ ] DOI inserted into `CITATION.cff` and manuscript.
- [ ] Live app URL inserted into manuscript.
- [ ] Jazer Research Lab landing page linked.
