# Deployment guide

## GitHub repository

The public repository is:

`jameshztta-stack/gc-ei-annotation-reliability`

Before a formal software release, verify the repository URL, author metadata, manuscript citation, software version and Zenodo DOI metadata.

## Streamlit Community Cloud

The application is deployed from the `main` branch with `app.py` as the entry point.

For a new deployment:

1. Sign in to Streamlit Community Cloud with GitHub.
2. Select **Create app** or **Deploy an app**.
3. Select this repository.
4. Use branch `main`.
5. Set the main file path to `app.py`.
6. Use Python 3.13 when available.
7. Deploy the application.

No secret is required for the default public-source configuration.

### First startup

The first startup requires internet access because the application obtains the public MSP from the original Zenodo record. The source file is checked against the expected SHA-256 value before use.

The application then constructs the reference matrix and metadata locally. Streamlit caches the prepared engine for reuse during the process lifetime.

## Public application checks

Before release, verify at minimum:

- one EI-only botanical example from `examples/example_single_CdeL_P02.csv`;
- the 12-spectrum botanical batch example;
- one manually entered spectrum;
- one RI-assisted spectrum;
- the 10% and 5% empirical operating points;
- CSV downloads;
- invalid-input handling;
- RI disagreement warnings;
- desktop and mobile rendering.

The 12 botanical examples must reproduce the values in `tests/botanical_expected.csv` within the stated numerical tolerances.

## Release procedure

After the application and repository checks have passed:

1. confirm version `1.0.0` in the application and citation metadata;
2. confirm `CHANGELOG.md`;
3. run the final CI and reproducibility workflows;
4. create the GitHub tag `v1.0.0` and the corresponding release;
5. archive the release in Zenodo and obtain the software DOI;
6. add the DOI to `CITATION.cff`, README and the application;
7. update the manuscript Data and Code Availability statement;
8. add the live application, GitHub and DOI links to the Jazer Research Lab page.
