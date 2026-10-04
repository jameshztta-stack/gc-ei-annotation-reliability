from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from gcei.bootstrap import SOURCE_RECORD, ensure_runtime_assets
from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="GC–EI Annotation Reliability Tool", page_icon="🧪", layout="wide")
st.markdown(
    """
<style>
html, body, [class*="css"] { font-family: Inter, Arial, sans-serif; }
.block-container { max-width: 1180px; padding-top: 2rem; }
.small-note { color: #5f6b6d; font-size: 0.92rem; }
.result-box { border: 1px solid #dfe7e7; border-radius: 12px; padding: 1rem 1.1rem; background: #fbfdfd; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_engine():
    assets = ensure_runtime_assets()
    return GCEIEngine(assets)


st.title("GC–EI Annotation Reliability Tool")
st.caption("A reliability layer for conventional GC–EI–MS spectral-library annotation • publication workflow v1.1")

with st.expander("What this tool does and does not do", expanded=False):
    st.markdown(
        """
This research tool applies the frozen method described in the associated study. It ranks reference identities,
constructs a calibrated 90% candidate set, estimates the probability that the top-ranked identity is correct,
and can abstain at calibration-derived empirical operating points.

**Important:** the output is a *library-based tentative annotation*. It does not replace an authentic reference
standard or suitable orthogonal confirmation. Low confidence or a broad candidate set is also not proof that the
compound is absent from the reference library.
        """
    )

try:
    with st.spinner("Preparing the validated publication reference library. First launch may take a little longer..."):
        engine = load_engine()
except Exception:
    st.error("The validated reference library could not be prepared automatically. Please refresh the app and try again.")
    st.stop()

mode = st.radio("Analysis mode", ["Single spectrum", "Batch spectra"], horizontal=True)
risk_label = st.selectbox(
    "Empirical operating point",
    ["10% target error (more coverage)", "5% target error (stricter)"],
)
risk_target = 0.10 if risk_label.startswith("10%") else 0.05
st.caption("These are calibration-derived empirical operating points, not formal future-error guarantees.")

if mode == "Single spectrum":
    source = st.radio("Spectrum input", ["Paste peaks", "Upload CSV"], horizontal=True)
    peaks = None
    if source == "Paste peaks":
        text = st.text_area(
            "Paste m/z and intensity values",
            value="mz,intensity\n41,82.1\n43,44.6\n69,71.5\n93,100\n121,18.3\n136,14.2",
            height=190,
        )
        try:
            peaks = parse_single_spectrum_text(text)
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("The pasted spectrum could not be parsed. Please verify the input format and try again.")
    else:
        uploaded = st.file_uploader("Upload CSV with columns mz,intensity", type=["csv"])
        if uploaded is not None:
            try:
                peaks = read_spectrum_csv(uploaded.getvalue())
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error("The uploaded spectrum CSV could not be read. Please verify the file format and try again.")

    use_ri = st.checkbox("I have a Kovats retention index measured under conditions considered comparable with the reference RI system")
    query_ri = None
    if use_ri:
        query_ri = st.number_input("Experimental Kovats RI", min_value=1.0, value=1000.0, step=1.0)
        st.warning(
            "Enter Kovats RI, not raw retention time. RI-assisted scoring should only be used when the experimental "
            "RI is reasonably comparable with the reference system; the study showed that benefit decreased as RI disagreement increased."
        )

    if st.button("Analyze spectrum", type="primary"):
        if peaks is None or len(peaks) == 0:
            st.error("Provide a valid spectrum first.")
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
                st.caption("The complete candidate set is available in the CSV download even when more than 100 rows are retained.")

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
                st.error("The spectrum could not be analyzed. Please verify the input and try again.")

else:
    st.write("Upload a long-format CSV. Required columns: `spectrum_id`, `mz`, `intensity`. Optional column: `ri`.")
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
            st.error("The batch file could not be analyzed. Please verify the CSV format and try again.")

st.divider()
st.markdown(
    f"Reference library source: [MS-DIAL public EI/Kovats-RI dataset on Zenodo]({SOURCE_RECORD}). "
    "The upstream MSP is downloaded from the original record at runtime and is not redistributed in this repository."
)
st.caption("Version 0.2.0 scientific-reproducibility repair candidate · Frozen v1.1 scientific parameters.")
