# Botanical challenge datasets

The botanical spectra were kept separate from method development. They were not used to select spectral weighting, fit the confidence models, determine conformal margins, or set the empirical operating thresholds.

## Coriander, cumin and fennel

Twelve spectra were used as an independent post-development challenge set:

- coriander: 5 spectra;
- cumin: 4 spectra;
- fennel: 3 spectra.

The spectra were searched against the validated public reference library using the final EI-only workflow. Historical compound annotations were retained for descriptive comparison only and were not treated as authenticated ground truth.

The top-ranked result agreed descriptively with the historical annotation for 8 of 12 spectra and differed for 4 of 12. Most disagreements involved closely related monoterpene-rich spectra. These cases were informative because the broader candidate sets and lower predicted top-1 correctness values showed where a single library hit should not be reported without qualification.

The 12 spectra are provided in `examples/example_batch_12_botanical.csv` and are used as end-to-end regression cases for the public software.

## Ilex umbellulata

The *Ilex umbellulata* GC–MS dataset was assessed separately as an ambiguity case study rather than as a ground-truth accuracy set. Fifteen historically reported features were reassessed with the final annotation workflow.

Four of the 15 cases agreed with the first-ranked historical/NIST candidate, whereas 11 did not. No accuracy estimate was calculated because the historical identities were tentative and had not been confirmed with authentic standards.

The *Ilex* dataset therefore served as a stress test for candidate-set width, confidence and abstention in a chemically broader, non-essential-oil profile. Its role was different from the coriander/cumin/fennel challenge set: it examined annotation uncertainty rather than agreement with historical labels.

## Interpretation

These botanical datasets are application and stress-test datasets. They are separate from calibration and model development and are intended to show how the reliability framework behaves on real botanical GC–MS spectra, including cases in which conventional single-hit reporting is uncertain.
