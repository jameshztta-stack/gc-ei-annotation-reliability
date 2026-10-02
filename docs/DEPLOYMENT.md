# Deployment guide

## 1. GitHub

Create a public repository and upload the project files.

Suggested repository name:

`gc-ei-annotation-reliability`

Before publication, update:

- repository URL in `CITATION.cff` if needed;
- author metadata;
- manuscript citation;
- Zenodo DOI;
- software version to `1.0.0` when the public web application is ready.

## 2. Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud using GitHub.
2. Select **Create app** / **Deploy an app**.
3. Select this GitHub repository.
4. Branch: `main`.
5. Main file path: `app.py`.
6. In Advanced settings, select Python 3.13 if available.
7. Deploy.

No secret is required for the default public-source configuration.

### First startup

The first application startup needs internet access because the server obtains the public MSP directly from the original Zenodo record. The source file is SHA-256 verified before use.

The application then constructs the reference matrix and metadata. `load_engine()` is cached by Streamlit so the prepared engine can be reused during the process lifetime.

## 3. Public application checks

After deployment, test at minimum:

- one EI-only botanical example from `examples/example_single_CdeL_P02.csv`;
- the 12-spectrum batch example;
- a manually entered short spectrum;
- one spectrum with optional RI;
- CSV downloads;
- mobile and desktop rendering.

The botanical examples should reproduce the expected values stored in `tests/botanical_expected.csv` within the stated numerical tolerance.

## 4. Publication version

After the public application has been checked:

1. change the software version to `1.0.0`;
2. update the changelog;
3. create GitHub tag/version `v1.0.0`;
4. archive the software in Zenodo;
5. obtain the software DOI;
6. update the manuscript Data and Code Availability statement and citation metadata;
7. create or update the Jazer Research Lab page with the live app, GitHub, and DOI links.
