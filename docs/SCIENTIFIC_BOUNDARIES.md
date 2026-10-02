# Scientific interpretation

The web tool implements the method described in the associated study and should be interpreted within the same scientific limits as the manuscript.

## What a result means

A result provides:

- the highest-scoring connectivity-level library identity;
- a calibrated candidate set;
- a model-estimated probability that the top-ranked candidate is correct;
- an empirical selective-prediction decision.

The result is a **tentative spectral-library annotation**.

## What a result does not mean

The tool does not establish:

- authentic-standard confirmation;
- stereochemical identity beyond the connectivity-level representation;
- a formal 5% or 10% future-error guarantee;
- reliable out-of-library detection;
- proof that a low-confidence spectrum is absent from the reference library.

## Retention index

RI-assisted mode is optional.

The study showed a strong benefit when query/reference RI values were compatible, but diminishing or negative benefit as RI disagreement increased.

Users should therefore provide a Kovats RI only when the chromatographic conditions are considered sufficiently comparable to the reference RI system.

Raw retention time must not be entered as RI.

## Different reference libraries

The software may be adapted to another EI reference library. However, the calibration values supplied here are specific to the reference distribution used in the study.

A new library requires, at minimum:

1. screening for exact-spectrum duplication and identity leakage;
2. construction of independent replicate query/reference spectra;
3. a disjoint calibration dataset;
4. recalibration of conformal nonconformity margins;
5. refitting and validation of the confidence model;
6. new risk–coverage and selective-prediction evaluation.
