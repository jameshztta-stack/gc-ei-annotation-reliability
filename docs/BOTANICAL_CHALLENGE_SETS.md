# Botanical challenge datasets

The botanical spectra were kept separate from method development. They were not used to choose spectral weighting, fit the confidence models, determine conformal margins, or set the empirical operating thresholds.

## Coriander, cumin and fennel

Twelve spectra were used as an independent post-development challenge set:

- coriander: 5 spectra;
- cumin: 4 spectra;
- fennel: 3 spectra.

These spectra were searched against the validated public reference library using the finalized EI-only workflow. Historical compound annotations were retained only for descriptive comparison and were not treated as authenticated ground truth.

The tool agreed descriptively with the historical annotation for 8 of 12 spectra and differed for 4 of 12. The disagreements were concentrated mainly among closely related monoterpene-rich spectra. In those cases, the broader conformal candidate sets and lower predicted top-1 correctness values were useful because they showed where a single library hit should not be overinterpreted.

The 12 spectra are retained in `examples/example_batch_12_botanical.csv` and are used as end-to-end regression cases for the public software.

## Ilex umbellulata

The *Ilex umbellulata* GC–MS material was used separately as an ambiguity case study rather than as a ground-truth accuracy set. Fifteen historically reported features were reassessed with the finalized annotation workflow.

Four of the 15 cases agreed with the first-ranked historical/NIST candidate, whereas 11 did not. No accuracy percentage was assigned because the historical identities were tentative and were not confirmed with authentic standards.

This case set was useful for a different reason from the coriander/cumin/fennel challenge set: it tested how the method behaves when the original GC–MS report contains substantial annotation ambiguity and a chemically broader, non-essential-oil profile. It therefore served as a stress test for candidate-set width, confidence and abstention rather than as a conventional accuracy benchmark.

## Interpretation

The botanical analyses are application and stress-test datasets. They are intentionally separate from calibration and model development. Their purpose is to show how the reliability framework behaves on real botanical GC–MS spectra, including cases where conventional single-hit reporting is uncertain.
