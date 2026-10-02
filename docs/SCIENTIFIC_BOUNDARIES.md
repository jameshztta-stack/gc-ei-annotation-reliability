# Scientific interpretation boundaries

The web tool is an implementation of the publication workflow and should be interpreted within the same scientific boundaries as the manuscript.

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

The publication study showed strong benefit when query/reference RI values were compatible, but diminishing or negative benefit as RI disagreement increased.

Users should therefore provide a Kovats RI only when the chromatographic conditions are considered sufficiently comparable to the reference RI system.

Raw retention time must not be entered as RI.

## Different reference libraries

The software framework may be adapted to another EI reference library. However, the publication calibration values are specific to the publication reference distribution.

A new library requires, at minimum:

1. exact-spectrum and identity-leakage audit;
2. construction of independent replicate query/reference spectra;
3. a disjoint calibration dataset;
4. recalibration of conformal nonconformity margins;
5. refitting and validation of the confidence model;
6. new risk–coverage and selective-prediction evaluation.
