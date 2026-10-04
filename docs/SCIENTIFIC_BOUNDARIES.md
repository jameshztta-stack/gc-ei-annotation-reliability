# Scientific interpretation

The web application implements the validated method described in the associated study. Interpretation should remain within the same scientific limits.

## Output interpretation

Each analysis reports:

- the highest-scoring connectivity-level library identity;
- a calibrated candidate set;
- the estimated probability that the top-ranked candidate is correct;
- an empirical selective-prediction decision.

The output is a **tentative spectral-library annotation**.

## Limitations

The software does not establish:

- authentic-standard confirmation;
- stereochemical identity beyond the connectivity-level representation;
- a formal 5% or 10% future-error guarantee;
- reliable out-of-library detection;
- absence from the reference library when confidence is low.

## Retention index

RI-assisted mode is optional. The validated study showed the greatest benefit when query and reference RI values were compatible, with diminishing or negative benefit as disagreement increased.

Kovats RI should therefore be supplied only when the experimental chromatographic system is reasonably comparable with the reference RI system. Raw retention time must not be entered as RI.

## Use with another reference library

The supplied calibration values are specific to the reference distribution used in the study. A different EI reference library requires, at minimum:

1. screening for exact-spectrum duplication and identity leakage;
2. construction of independent replicate query/reference spectra;
3. a disjoint calibration dataset;
4. recalibration of conformal nonconformity margins;
5. refitting and validation of the confidence model;
6. new risk-coverage and selective-prediction evaluation.
