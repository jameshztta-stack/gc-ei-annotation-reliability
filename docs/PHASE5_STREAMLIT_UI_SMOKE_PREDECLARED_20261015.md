# Phase 5 addendum — Predeclared headless Streamlit UI smoke tests (2026-10-15)

Separate **supplementary engineering check**, beyond original 12-case engine demo and retrospective review-routing protocol. No model/source/data modification.

- Render the **actual** repository `app.py` (v2.0.2) using Streamlit's native `st.testing.v1.AppTest` simulator.
- Confirm no uncaught render exceptions, exact GC–EI–MS title, single-spectrum entry, user-facing two-target disclosure, source and model provenance information, and two alternative user input modes.
- Switch to batch mode without deploying any production app or touching authentic spectral data; check batch template and its required CSV fields.
- Where supported by AppTest, verify the warning text that limits claims to tentative connectivity labels and specifies uncertified target error, and present source/provenance and how-to-cite content. Do not assert simulated UI operation represents live browser/network availability or evaluated human ease of use.
- Failing test is a **real software QA issue** to log, not a negative analytical chemistry validation result. If a current app defect requires modification, introduce a separate version-controlled candidate patch, preserve v2 model and original released application archival history, and do NOT merge without explicit user instruction.

Version: `streamlit==1.61.1` already frozen in original requirements. Test command: `pytest -q tests/test_phase5_app_ui_smoke.py`. This test uses only app script execution, no sample identity labels, no network/browser, no engine inference and no future-risk certification.
