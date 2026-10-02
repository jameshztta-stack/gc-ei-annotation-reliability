# Phase 2 re-audit — GC–EI Annotation Reliability Tool 0.2.0-rc1

## Scope

Phase 2 converted the validated Phase 1 prototype into a public-release architecture suitable for GitHub, Streamlit deployment, and later Zenodo archiving.

The re-audit specifically checked:

- preservation of frozen v1.1 scientific outputs;
- safe handling of the third-party public MSP;
- reproducibility of public reference-library reconstruction;
- Streamlit deployment requirements;
- source-code/package completeness;
- scientific interpretation boundaries.

## Third-party data decision

The original MS-DIAL MSP and the derived reference matrix/metadata are not included in this public release candidate.

The public source record is:

`https://zenodo.org/records/21910638`

DOI: `10.5281/zenodo.21910638`

The Phase 2 bootstrap retrieves the publication file from the original Zenodo record, verifies its SHA-256 checksum, derives the publication reference assets locally, and removes the temporary MSP.

This avoids treating the project software license as permission to redistribute the upstream dataset.

## Source MSP verification

Expected file:

`GCMS DB-Public-KovatsRI-VS3.msp`

Expected SHA-256:

`6bc2c7dfcf5a2a80227674229e6bd93e0af0880cbc3f87586f36ef9b31fd9132`

The exact file used during local Phase 2 re-audit matched this checksum.

## Reference reconstruction audit

Public builder output:

- connectivity-level reference identities: **8,543**
- m/z vector range: **0–587**
- transformed reference matrix shape: **8,543 × 588**

Reference reconstruction was compared against the validated Phase 1 reference assets.

SHA-256 fingerprints were identical for:

- connectivity identifiers;
- representative record indices;
- RI vector;
- dense publication reference matrix.

The reconstructed metadata columns used for inference were also identical.

Therefore, the public bootstrap architecture reconstructs the same frozen reference library without shipping the source MSP or its derived matrix.

## Botanical regression audit

All 12 independent botanical challenge spectra were rerun using the newly reconstructed public reference assets.

Result:

- top candidate identity: **12/12 exact match**
- 90% candidate-set size: **12/12 exact match**
- top similarity: all within `1 × 10^-6`
- predicted top-1 correctness: all within `1 × 10^-6`

The reference-builder output therefore reproduces the frozen v1.1 botanical deployment results.

## EI+RI spot audit

The public reference reconstruction was also checked previously against valid-RI test spectra during Phase 1. The web engine retained the publication RI-fusion rule and fixed RI-specific model/calibration constants.

Important interpretation boundary retained in the app:

- RI is optional;
- the user must supply a Kovats RI, not raw retention time;
- RI should be used only when chromatographic conditions are reasonably comparable;
- warnings are produced for larger top-candidate RI disagreements.

## Performance audit

Using the publication MSP on the current audit system, public reference reconstruction required approximately:

- **4.3 s** wall time;
- **~532 MB** peak resident memory during parsing/reconstruction.

The resulting runtime assets are much smaller than the source MSP and are cached by the Streamlit process.

The deployment therefore appears realistic for ordinary cloud/web use, but live Streamlit memory behavior must still be checked after deployment.

## Package completeness

The release candidate includes:

- `app.py` — Streamlit application;
- `gcei/` — reusable inference and reference-builder modules;
- `models/` — frozen model/calibration parameters;
- `scripts/prepare_reference.py` — explicit reference preparation;
- `scripts/validate_release.py` — end-to-end publication regression check;
- `tests/` — parser and frozen botanical expected outputs;
- `examples/` — single and batch user examples;
- `.github/workflows/ci.yml` — lightweight CI;
- `.github/workflows/release-validation.yml` — manual full-source regression workflow;
- `requirements.txt` — exact package pins;
- `LICENSE` — MIT software license;
- `NOTICE` — third-party-data notice;
- `CITATION.cff` and `.zenodo.json` — scholarly software metadata;
- deployment, provenance, scientific-boundary, and release-checklist documentation.

## Remaining Phase 3 checks

The following are intentionally not marked complete yet:

1. create the real public GitHub repository;
2. run GitHub Actions on the public repository;
3. deploy the app on Streamlit Community Cloud;
4. verify first-boot download/build behavior on Streamlit;
5. perform live desktop/mobile smoke tests;
6. freeze and tag `v1.0.0` only after live validation;
7. archive `v1.0.0` on Zenodo and insert the resulting DOI into the manuscript.

## Phase 2 conclusion

**PASS — public-release candidate is scientifically consistent with the validated Phase 1/v1.1 workflow and is ready for GitHub/Streamlit deployment testing.**
