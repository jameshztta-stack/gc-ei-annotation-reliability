from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from gcei.bootstrap import SOURCE_RECORD, ensure_runtime_assets
from gcei.reference_builder import EXPECTED_SHA256
from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv
from gcei.v2_bootstrap import ensure_v2_assets, V2_HGB
from gcei.v2_engine import GCEIV2Engine, V2_N_REFERENCE, V2_REFERENCE_SHA256, V2_HGB_SHA256

ROOT = Path(__file__).resolve().parent
APP_VERSION = '2.0.0'
REFERENCE_IDENTITY_COUNT = 8543
V2_MODE = 'Research v2: frozen EI/HGB, 8,455 identities'
V1_MODE = 'Legacy v1: 8,543 identities, historical RI and conformal'

SINGLE_TEMPLATE = """mz,intensity
41,82.1
43,44.6
69,71.5
93,100
121,18.3
136,14.2
"""

BATCH_TEMPLATE = """spectrum_id,mz,intensity,ri
Peak_1,41,82.1,
Peak_1,93,100,
Peak_2,43,65.2,939
Peak_2,71,100,939
"""
V2_BATCH_TEMPLATE = """spectrum_id,mz,intensity
Peak_1,41,82.1
Peak_1,93,100
Peak_2,43,65.2
Peak_2,71,100
"""

st.set_page_config(page_title="GC–EI Annotation Reliability Tool", page_icon="🧪", layout="wide")
st.markdown(
    """
<style>
html, body, [class*="css"] { font-family: Inter, Arial, sans-serif; }
.block-container { max-width: 1180px; padding-top: 2rem; }
.small-note { color: #5f6b6d; font-size: 0.92rem; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_engine(selection):
    if selection == V2_MODE:
        return GCEIV2Engine(ensure_v2_assets(), V2_HGB)
    return GCEIEngine(ensure_runtime_assets())


st.title("GC–EI Annotation Reliability Tool")
st.caption("Connectivity-level GC–EI–MS research annotation and source-dependent uncertainty")
with st.sidebar:
    st.markdown("### Select annotation configuration")
    selection = st.radio("Reference and model", [V2_MODE, V1_MODE], index=0)
    use_v2 = selection == V2_MODE
    st.write(f"**Interface version:** {APP_VERSION}")
    st.write(f"**Reference identities:** {V2_N_REFERENCE if use_v2 else REFERENCE_IDENTITY_COUNT:,}")
    st.caption("MS-DIAL original source SHA-256:")
    st.code(EXPECTED_SHA256, language="text")
    if use_v2:
        st.caption("Frozen v2 reference index SHA-256:")
        st.code(V2_REFERENCE_SHA256, language="text")
        st.caption("Frozen development-trained HGB SHA-256:")
        st.code(V2_HGB_SHA256, language="text")
        st.warning("The historical 5% and 10% target-error rules are not certified.")
    else:
        st.info("This retains original v1 reference/model and separate historical RI/conformal settings.")

if use_v2:
    st.info(
        "**Active: research v2, EI-only.** The frozen model matched 394/609 "
        "publisher-reported first14 labels in its within-MS-DIAL closed-library "
        "test (64.70%). No independent laboratory validation, authentic chemical "
        "identity confirmation, or certified 5%/10% risk guarantee exists. "
        "v2 RI fusion and conformal sets are NOT provided."
    )
else:
    st.info(
        "**Active: legacy v1.** Historical confidence/RI estimates and nominal "
        "conformal candidate sets are source-dependent. The separate v2 results "
        "do not apply to this legacy reference/model."
    )

with st.expander("Scope and interpretation", expanded=False):
    if use_v2:
        st.markdown("""
**v2 model:** frozen 8,455 first14 InChIKey connectivity reference, original
float64 nominal EI m/z^1 × sqrt(intensity) full-library cosine, and exact
original 12-feature development-fitted HGB confidence score.

**One-time 609 within-source test:** 394/609 first14 labels matched at top1,
489/609 within top5, and 509/609 within top10. Reference compounds were
present in the search library by design. Physical chemical standards,
separate laboratory acquisitions and future unknown-sample identification
have not been verified.

Original 10%-target threshold: HGB >= 0.87 (198 accepted, 12 mismatches).
Original 5%-target threshold: HGB >= 0.94 AND top1–top2 cosine gap >= 0.20
(38 accepted, 0 observed mismatches). **NEITHER is a certified bound on
future error**. The 609 is now permanently spent as an untouched test.

**No v2 RI fusion, conformal candidate set or out-of-library detector**
was calibrated in this research. Do not borrow any of those from v1.
All hit labels represent source-reported chemical connectivity, NOT
experimentally authenticated compound identity or stereoisomer truth.
Confirm important findings with authentic standards or orthogonal methods.
""")
    else:
        st.markdown(
        """
The tool ranks library compounds by **first14 InChIKey connectivity** using nominal electron-ionization
spectra. Its top-hit correctness score and **nominal 90%** candidate set are estimates derived from
the historical source distribution, not verified real-world chemical identification probabilities.

The 5% and 10% target-error thresholds were selected empirically and **are not independent
statistical certificates**. The candidate-set coverage and model calibration have not been
verified on independently acquired laboratory samples, other instruments, other reference
libraries, or compounds missing from the reference. This tool does not resolve exact
stereoisomers or authenticate the measured chemical material.

Optional Kovats RI should only be supplied when chromatographic systems are comparable;
its benefit is not independently established for other instruments.

All matches are **tentative annotations**. Confirm compound identity with an authentic
standard or orthogonal evidence. Low confidence or a large set does not prove
that a compound is absent from the library. The newer 8,455-identity v2 research
evaluation does not describe performance of this separate 8,543-identity app.
        """
    )

with st.expander("Input format and CSV templates", expanded=False):
    st.markdown(
        """
**Single spectrum** — use two columns: `mz,intensity`. Enter one ion peak per row.

**Batch spectra** — use `spectrum_id,mz,intensity,ri`. Repeat the same `spectrum_id` for every peak belonging to that spectrum.
The `ri` column is optional; leave it blank when Kovats RI is unavailable. If RI is supplied, use the same RI value for all rows of that spectrum.
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        st.code(SINGLE_TEMPLATE, language="text")
        st.download_button(
            "Download single-spectrum CSV template",
            SINGLE_TEMPLATE.encode(),
            file_name="gcei_single_spectrum_template.csv",
            mime="text/csv",
        )
    with c2:
        batch_template = V2_BATCH_TEMPLATE if use_v2 else BATCH_TEMPLATE
        st.code(batch_template, language="text")
        st.download_button(
            "Download batch CSV template",
            batch_template.encode(),
            file_name="gcei_batch_template.csv",
            mime="text/csv",
        )

try:
    with st.spinner("Preparing the checksum-verified reference library..."):
        engine = load_engine(selection)
except Exception:
    st.error("Reference/model initialization was blocked: the exact original source or SHA-256-locked artifacts are unavailable. No alternative dataset or model was accepted.")
    st.stop()

mode = st.radio("Analysis mode", ["Single spectrum", "Batch spectra"], horizontal=True)
risk_label = st.selectbox(
    "Historical decision threshold (not certified error control)",
    ["10% target error (more coverage)", "5% target error (stricter)"],
)
risk_target = 0.10 if risk_label.startswith("10%") else 0.05
st.caption("Historical empirical thresholds only. **Neither target error level is independently certified** for future samples.")

if mode == "Single spectrum":
    source = st.radio("Spectrum input", ["Paste peaks", "Upload CSV"], horizontal=True)
    peaks = None
    if source == "Paste peaks":
        text = st.text_area(
            "Paste m/z and intensity values",
            value=SINGLE_TEMPLATE,
            height=190,
        )
        try:
            peaks = parse_single_spectrum_text(text)
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Spectrum parsing failed. Check the input format and values.")
    else:
        uploaded = st.file_uploader("Upload CSV with columns mz,intensity", type=["csv"])
        if uploaded is not None:
            try:
                peaks = read_spectrum_csv(uploaded.getvalue())
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error("CSV parsing failed. Check the file structure and values.")

    use_ri = False if use_v2 else st.checkbox("Use comparable Kovats RI (legacy v1 only)")
    query_ri = None
    if use_ri:
        query_ri = st.number_input("Experimental Kovats RI", min_value=1.0, value=1000.0, step=1.0)
        st.warning(
            "Enter Kovats RI, not raw retention time. RI-assisted scoring is valid only when the experimental and reference chromatographic systems are reasonably comparable."
        )

    if st.button("Analyze spectrum", type="primary"):
        if peaks is None or len(peaks) == 0:
            st.error("No valid spectrum was provided.")
        else:
            try:
                r = engine.analyze(peaks, kovats_ri=query_ri if use_ri else None, risk_target=risk_target)
                if (r.accepted if use_v2 else r.confidence >= r.risk_threshold):
                    st.info(r.decision)
                    st.caption("The score passes a historical threshold, not a confirmed chemical identity or error-rate guarantee.")
                else:
                    st.warning(r.decision)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Top candidate", str(r.top1.get("display_name", r.top1.get("name", ""))))
                c2.metric("Similarity", f"{r.top1.get('similarity', 0):.4f}")
                c3.metric("Historical model score", f"{100*r.confidence:.1f}%", help="Source-dependent model estimate, not an authenticated compound identity probability.")
                if use_v2:
                    c4.metric("Top1–top2 EI margin", f"{r.margin:.4f}")
                else:
                    c4.metric("Nominal 90% set size", f"{r.conformal90_size}", help="External coverage not established.")

                if r.ri_delta_top1 is not None:
                    st.write(f"**Top-candidate |ΔRI|:** {r.ri_delta_top1:.1f} RI units")
                for warning in r.warnings:
                    st.warning(warning)

                st.subheader("Top 10 candidates")
                st.dataframe(r.top10, use_container_width=True, hide_index=True)

                if not use_v2:
                    st.subheader("Legacy v1 nominal 90% candidate set")
                    st.dataframe(r.conformal90.head(100), use_container_width=True, hide_index=True)
                    st.caption("External 90% coverage not established; download full original set if needed.")
                else:
                    st.caption("v2 top 10 is a ranked list, NOT a conformal confidence set.")

                summary = pd.DataFrame([{
                    "mode": r.mode,
                    "configuration": "research-v2" if use_v2 else "legacy-v1",
                    "reference_index_sha256": V2_REFERENCE_SHA256 if use_v2 else "",
                    "frozen_HGB_sha256": V2_HGB_SHA256 if use_v2 else "",
                    "top1_top2_cosine_margin": r.margin if use_v2 else "",
                    "historical_rule_met": r.accepted if use_v2 else r.confidence >= r.risk_threshold,
                    "software_version": APP_VERSION,
                    "reference_first14_count": V2_N_REFERENCE if use_v2 else REFERENCE_IDENTITY_COUNT,
                    "source_msp_sha256": EXPECTED_SHA256,
                    "source_independent_error_guarantee": False,
                    "top1_name": r.top1.get("display_name", r.top1.get("name", "")),
                    "top1_formula": r.top1.get("formula", ""),
                    "top1_connectivity_id": r.top1.get("connectivity_id", ""),
                    "top_similarity": r.top1.get("similarity", ""),
                    "predicted_top1_correctness": r.confidence,
                    "conformal90_set_size": "" if use_v2 else r.conformal90_size,
                    "conformal90_external_coverage_certified": False,
                    "risk_target": r.risk_target,
                    "risk_threshold": r.risk_threshold,
                    "ri_delta_top1": r.ri_delta_top1,
                    "decision": r.decision,
                }])
                st.download_button(
                    "Download result summary (CSV)",
                    summary.to_csv(index=False).encode(),
                    file_name="gcei_annotation_summary.csv",
                    mime="text/csv",
                )
                st.download_button("Download top-10 candidates (CSV)",
                    r.top10.to_csv(index=False).encode(), file_name="gcei_top10_candidates.csv", mime="text/csv")
                if not use_v2:
                    st.download_button("Download complete nominal 90% legacy v1 set (CSV)",
                        r.conformal90.to_csv(index=False).encode(), file_name="gcei_legacy_nominal_set.csv", mime="text/csv")
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error("Spectrum analysis failed. Check the input and try again.")

else:
    st.write("Upload a long-format CSV with `spectrum_id`, `mz`, and `intensity`. The optional `ri` column contains Kovats RI.")
    uploaded = st.file_uploader("Batch CSV", type=["csv"], key="batch")
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(30), use_container_width=True, hide_index=True)
            if st.button("Analyze batch", type="primary"):
                out = engine.analyze_batch(df, risk_target=risk_target)
                st.info(f"Analyzed {len(out)} spectra; all reported identities are tentative.")
                out.insert(0, "software_version", APP_VERSION)
                out["reference_first14_count"] = V2_N_REFERENCE if use_v2 else REFERENCE_IDENTITY_COUNT
                out["configuration"] = "research-v2" if use_v2 else "legacy-v1"
                out["source_msp_sha256"] = EXPECTED_SHA256
                out["source_independent_error_guarantee"] = False
                st.dataframe(out, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download batch results (CSV)",
                    out.to_csv(index=False).encode(),
                    file_name="gcei_batch_results.csv",
                    mime="text/csv",
                )
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Batch analysis failed. Check the CSV structure and values.")

st.divider()
st.markdown(
    f"**Reference library:** [MS-DIAL public EI/Kovats-RI dataset on Zenodo]({SOURCE_RECORD}). "
    "The source MSP is obtained from the original publisher record (or its byte-identical historical copy), checked against the frozen SHA-256 and never redistributed here."
)

st.markdown("**Citation**")
st.markdown(
    "If results from this tool contribute to a publication, cite the associated research article and the archived software release.  \n"
    "**Software release:** Zothantluanga JH. *GC–EI Annotation Reliability Tool*, version 1.0.0. Zenodo. 2026. "
    "DOI: [10.5281/zenodo.23143113](https://doi.org/10.5281/zenodo.23143113).  \n"
    "**Associated article:** citation will be added after publication."
)

st.caption(
    "Developed and maintained by Dr. James H. Zothantluanga, Research Director, Jazer Research Lab, "
    "Aizawl, Mizoram 796005, India."
)
st.caption(f"Interface v{APP_VERSION} | {selection} | No independent source-wide identity or risk certification.")
