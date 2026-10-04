# GC–EI Annotation Reliability Tool v1.0.0

Version 1.0.0 is the first public release of the GC–EI Annotation Reliability Tool.

The software implements the validated v1.1 GC–EI–MS annotation workflow developed in the associated study. It ranks connectivity-level EI library candidates, estimates top-1 correctness, reports a calibrated 90% candidate set, and applies empirical 10% or 5% target-error operating points. Kovats retention index can be incorporated when the experimental chromatographic system is sufficiently comparable with the reference RI system.

## Main features

- single-spectrum and batch analysis;
- `m/z^1 × intensity^0.5` weighted-cosine EI similarity;
- connectivity-level candidate ranking;
- predicted top-1 correctness;
- 90% split-conformal candidate sets;
- empirical 10% and 5% target-error decisions;
- optional EI+RI ranking;
- explicit warnings when RI changes the EI-only top candidate or when RI disagreement is large;
- downloadable result tables and candidate sets;
- downloadable CSV input templates;
- fail-safe handling of malformed or non-positive input.

## Reference data and reproducibility

The reference library is reconstructed at runtime from the public MS-DIAL EI/Kovats-RI dataset deposited on Zenodo. The source file is verified by SHA-256 before use. The repository does not redistribute the original MSP file.

The release includes automated checks of the reconstructed reference matrix, RI vector and metadata, together with regression testing against 12 independent botanical challenge spectra from coriander, cumin and fennel.

The *Ilex umbellulata* dataset is documented separately as an annotation-ambiguity and abstention case study rather than as a ground-truth accuracy benchmark.

## Interpretation

Outputs are tentative spectral-library annotations. Definitive compound identification requires an authentic standard or suitable orthogonal confirmation. Low confidence or a broad candidate set should not be interpreted as evidence that a compound is absent from the reference library.

The supplied calibration values and empirical decision thresholds are specific to the reference distribution used in the study. They should not be transferred directly to another EI library without independent reconstruction and validation.

## Validation before release

Before preparation of v1.0.0, the public application was checked for:

- EI-only and EI+RI single-spectrum analysis;
- 10% and 5% empirical operating points;
- 12-spectrum batch regression;
- CSV export integrity;
- malformed-input handling;
- RI-ranking-change warnings;
- desktop and mobile rendering;
- end-to-end reference reconstruction from the original Zenodo source.

The final CI and reproducibility workflows passed before release preparation.

## Citation

If results from this software contribute to published work, cite both the associated research article and the archived software release.

**Software release:** Zothantluanga JH. *GC–EI Annotation Reliability Tool*, version 1.0.0. Zenodo. 2026. DOI: [10.5281/zenodo.23143113](https://doi.org/10.5281/zenodo.23143113).

**Associated article:** citation will be added after publication.

## Developer and maintainer

Dr. James H. Zothantluanga  
Research Director, Jazer Research Lab  
Aizawl, Mizoram 796005, India
