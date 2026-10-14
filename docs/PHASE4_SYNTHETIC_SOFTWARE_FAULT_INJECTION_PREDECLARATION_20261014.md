# Phase 4 — Predeclared Synthetic Software Failure-Injection Test Protocol

**Timestamp/design date:** 2026-10-14. **Applies only to frozen v2 software engineering and synthetic input handling.** No MSP acquisition, no chemical source labels, no case outcomes from the original 609 or 466, no retraining, no new risk decisions, no user study. Running this cannot improve evidence about chemical identification accuracy or manuscript algorithmic novelty.

## Test unit and pass/fail specifications

1. **Same nominal integer m/z bin:** two or more synthetically supplied positive peaks mapped to the same rounded mass must sum their original intensity, not overwrite it. Python round-to-nearest-even must be respected.
2. **Invalid/unsupported peaks:** nonfinite/invalid peak values and nonpositive intensities are ignored as currently specified; out-of-range `m/z` values are excluded and counted; input with no usable EI peak must be rejected.
3. **Zero effective weighted norm:** a nominal m/z=0-only spectrum has positive unweighted intensity but `m^1 sqrt(I)` norm zero; refuse scoring rather than return a numerical probability.
4. **Feature integrity:** 12 observables must be produced reproducibly in the exact frozen order from valid synthetic 8,455-reference similarity arrays; incorrect dimensionality must be rejected.
5. **No false RI fusion:** current v2 EI-only single-spectrum and batch input must fail explicitly on nonempty Kovats RI, rather than silently applying legacy v1 calibration.
6. **Required batch data validation:** reject missing spectrum ID/mass/intensity columns and empty input.
7. **Source/index/model authentication:** pristine exact-SHA frozen artifacts must pass; byte-corrupted test-local copies of the pinned HGB model and reference-index must each fail pre-inference. Do not tamper with production assets.
8. **Scope negative control:** synthetic tests must not label any historically uncertified 5%/10% operating point as certified.

## Exclusions

No true source-independent spectroscopy; no authentic-standard analyte, no open-set absent-library label, no new unknown spectrum, no RI/conformal v2 validation, no comparative user study and no chemical identification "accuracy". A passed test demonstrates correct rejection and numerical invariants in the specified software only.

**Execution:** `pytest -q tests/test_phase4_v2_software_fault_injection.py`, controlled by the independent GitHub Actions workflow `.github/workflows/phase4-synthetic-software-fault-gate.yml`. Archive the workflow execution result; if a check fails, fix the software/test claim transparently, not by changing frozen inference or silently dropping the failing case.
