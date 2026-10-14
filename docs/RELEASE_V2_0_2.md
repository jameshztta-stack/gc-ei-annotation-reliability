# GC–EI–MS Annotation Tool — Software v2.0.2

## Changes for researchers

The public Streamlit application now presents the **current GC–EI–MS annotation model only**. The previous software configurations remain available solely as historical GitHub/Zenodo archives, not as a website model selector.

The landing page explains what the application actually does: EI mass-spectrum library matching against **8,455 connectivity references**, showing top-ten candidate matches, spectral similarities and model-derived confidence estimates. **Single-spectrum and batch CSV templates are visible and downloadable before their respective input fields**. Users then upload or paste spectra and analyze them. Results retain downloadable summary and detailed candidate CSV files.

Unnecessary panels, source SHA-256 strings, algorithm-development jargon and several large highlighted messages have been removed from the main display. Essential study caveats are accessible through a plain *About the method and its limitations* expander, with deeper source and model provenance nested inside. Citation guidance is accessible separately.

Developer credit is explicit: **Developed and maintained by Dr. James H. Zothantluanga, Research Director, Jazer Research Lab, Aizawl, Mizoram, India.**

## Scope of changes and scientific guarantees

This is an **interface and documentation update**. It retains byte-identical original HGB model file and 8,455-identity reference index, same publisher original MSP SHA, same m/z¹×√intensity weighted cosine, same 12 model features, stable numerical ordering and previously selected historical 5% and 10% screening rules. No new model fit, calibration or study population changes have been made.

The original within-MS-DIAL 609-query benchmark achieved **394/609 (64.70%)** first14 source-label top-one agreement. This is not an independently authenticated compound identification rate. Historical 10%-target selected 198/609 with 12 mismatches; historical 5%-target selected 38/609 with no observed mismatches. **Neither is a certified bound on future errors.** No v2 retention-index fusion, independent prospective conformal-set coverage or robust unknown/out-of-library detection is included. Interpret all outputs as tentative connectivity-level annotations and confirm important chemical claims independently.

No measured spectra from the MS-DIAL source library, SWGDRUG or RECETOX are redistributed under the MIT software licence. Source data are obtained from the original publisher and checked against the original SHA-256.

## Attribution and citation

- **Software:** Zothantluanga, J. H. *GC–EI–MS Annotation Tool*, version **2.0.2** (2026). The new version-specific Zenodo DOI will be added to the website **after its public publication and independent verification**.
- **Article:** A related study manuscript is not yet published. No invented article citation or DOI is provided.
- **Original library:** Tsugawa H., MS-DIAL public EI library, https://doi.org/10.5281/zenodo.21910638 .
- **Developer:** Dr. James H. Zothantluanga, Research Director, Jazer Research Lab, Aizawl, Mizoram, India.

This version should be published as a **new software version** in the existing Zenodo version chain, preserving both earlier v1.0.0 and v2.0.1 DOI records and connecting through concept DOI 10.5281/zenodo.23143112. Do not edit the older published records. The app and README will link the new DOI only once the public Zenodo API confirms it.
