# Scientific interpretation

The web application implements the validated method described in the study. Results should be interpreted within the limits of that validation.

## Output interpretation

Each analysis reports:

- the highest-scoring connectivity-level library candidate;
- a calibrated candidate set;
- the estimated probability that the top-ranked candidate is correct;
- an empirical selective-prediction decision.

The result is a **tentative spectral-library annotation**.

## Limitations

The software does not provide:

- authentic-standard confirmation;
- stereochemical identification beyond the connectivity-level representation;
- a formal 5% or 10% future-error guarantee;
- validated out-of-library detection;
- evidence of absence from the reference library when confidence is low.

## Retention index

RI-assisted mode is optional. In the validation study, its benefit was greatest when query and reference RI values were compatible and decreased as RI disagreement increased.

Kovats RI should therefore be used only when the experimental chromatographic system is reasonably comparable with the reference RI system. Raw retention time must not be entered as RI.

## Use with another reference library

The supplied calibration values are specific to the reference distribution used in the study. A different EI reference library requires independent validation, including:

1. screening for exact-spectrum duplication and identity leakage;
2. construction of independent replicate query/reference spectra;
3. a disjoint calibration dataset;
4. recalibration of conformal margins;
5. refitting and validation of the confidence model;
6. new risk-coverage and selective-prediction analysis.
