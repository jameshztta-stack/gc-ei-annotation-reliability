# Deployment guide

## 1. GitHub

Create a public repository and upload the complete contents of this release candidate.

Suggested repository name:

`gc-ei-annotation-reliability`

Before the final publication release, update:

- repository URL in `CITATION.cff` if needed;
- author metadata;
- manuscript citation;
- final Zenodo DOI;
- version from release candidate to `1.0.0`.

## 2. Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud using GitHub.
2. Select **Create app** / **Deploy an app**.
3. Select this GitHub repository.
4. Branch: `main`.
5. Main file path: `app.py`.
6. In Advanced settings, select Python 3.13 if available.
7. Deploy.

No secret is required for the default public-source workflow.

### First startup

The first application startup needs internet access because the server obtains the public MSP directly from the original Zenodo record. The source file is SHA-256 verified before use.

The reference builder then creates the runtime matrix and metadata. `load_engine()` is wrapped with Streamlit resource caching, so the engine is reused during the process lifetime.

## 3. Live scientific smoke test

After deployment, test at minimum:

- one EI-only botanical example from `examples/example_single_CdeL_P02.csv`;
- the 12-spectrum batch example;
- a manually entered short spectrum;
- one spectrum with optional RI;
- CSV downloads;
- mobile and desktop rendering.

The deployed botanical example should reproduce the expected values stored in `tests/botanical_expected.csv` within the stated floating-point tolerance.

## 4. Publication release

Only after live deployment passes the smoke test:

1. change package/app version to `1.0.0`;
2. update the changelog;
3. create GitHub release/tag `v1.0.0`;
4. archive the software release in Zenodo;
5. obtain the software DOI;
6. update the manuscript Data and Code Availability statement and citation metadata;
7. create/update the Jazer Research Lab landing page with the live app, GitHub, and DOI links.

Do not describe the software as `v1.0.0` before this sequence is complete.
