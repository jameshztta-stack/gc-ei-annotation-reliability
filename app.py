from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from gcei.bootstrap import SOURCE_RECORD, ensure_runtime_assets
from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv

ROOT = Path(__file__).resolve().parent

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
def load_engine():
    assets = ensure_runtime_assets()
    return GCEIEngine(assets)


st.title("GC–EI Annotation Reliability Tool")
st.caption("Uncertainty-aware GC–EI–MS library annotation with calibrated uncertainty estimates")

with st.expander("Scope and interpretation", expanded=False):
    st.markdown(
        """
The tool ranks connectivity-level library candidates from EI spectra, returns a calibrated 90% candidate set,
estimates top-1 correctness, and applies fixed empirical 10% or 5% target-error operating points.
Kovats RI can be included when the experimental chromatographic system is comparable with the reference RI system.

Results are **tentative library annotations**. Definitive identification requires an authentic standard or suitable
orthogonal confirmation. Low confidence or a broad candidate set is not evidence that a compound is absent from the reference library.
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
        st.code(BATCH_TEMPLATE, language="text")
        st.download_button(
            "Download batch CSV template",
            BATCH_TEMPLATE.encode(),
            file_name="gcei_batch_template.csv",
            mime="text/csv",
        )

try:
    with st.spinner("Preparing the validated reference library..."):
        engine = load_engine()
except Exception:
    st.error("Reference-library initialization failed. Reload the app and try again.")
    st.stop()

mode = st.radio("Analysis mode", ["Single spectrum", "Batch spectra"], horizontal=True)
risk_label = st.selectbox(
    "Empirical operating point",
    ["10% target error (more coverage)", "5% target error (stricter)"],
)
risk_target = 0.10 if risk_label.startswith("10%") else 0.05
st.caption("Calibration-derived empirical operating points; they are not formal future-error guarantees.")

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

    use_ri = st.checkbox("Use a Kovats retention index measured under conditions comparable with the reference RI system")
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
                if r.confidence >= r.risk_threshold:
                    st.success(r.decision)
                else:
                    st.warning(r.decision)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Top candidate", str(r.top1.get("display_name", r.top1.get("name", ""))))
                c2.metric("Similarity", f"{r.top1.get('similarity', 0):.4f}")
                c3.metric("Predicted top-1 correctness", f"{100*r.confidence:.1f}%")
                c4.metric("90% candidate-set size", f"{r.conformal90_size}")

                if r.ri_delta_top1 is not None:
                    st.write(f"**Top-candidate |ΔRI|:** {r.ri_delta_top1:.1f} RI units")
                for warning in r.warnings:
                    st.warning(warning)

                st.subheader("Top 10 candidates")
                st.dataframe(r.top10, use_container_width=True, hide_index=True)

                st.subheader("90% conformal candidate set")
                st.dataframe(r.conformal90.head(100), use_container_width=True, hide_index=True)
                st.caption("The complete candidate set is included in the CSV download when more than 100 rows are retained.")

                summary = pd.DataFrame([{
                    "mode": r.mode,
                    "top1_name": r.top1.get("display_name", r.top1.get("name", "")),
                    "top1_formula": r.top1.get("formula", ""),
                    "top1_connectivity_id": r.top1.get("connectivity_id", ""),
                    "top_similarity": r.top1.get("similarity", ""),
                    "predicted_top1_correctness": r.confidence,
                    "conformal90_set_size": r.conformal90_size,
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
                st.download_button(
                    "Download complete 90% candidate set (CSV)",
                    r.conformal90.to_csv(index=False).encode(),
                    file_name="gcei_candidate_set_90.csv",
                    mime="text/csv",
                )
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
                st.success(f"Analyzed {len(out)} spectra.")
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
    "The source MSP is obtained from the original record at runtime and is not redistributed in this repository."
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
st.caption("Version 1.0.0")
