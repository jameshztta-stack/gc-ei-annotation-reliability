from __future__ import annotations

import io
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from gcei.bootstrap import ensure_reference_assets
from gcei.engine import AnnotationEngine, parse_peak_csv, parse_peak_text


ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"
RUNTIME_DIR = ROOT / "runtime_assets"

st.set_page_config(
    page_title="GC–EI Annotation Reliability Tool",
    page_icon="🧪",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def load_engine() -> AnnotationEngine:
    source_override = os.environ.get("GCEI_MSP_PATH")
    assets = ensure_reference_assets(
        runtime_dir=RUNTIME_DIR,
        source_msp=Path(source_override) if source_override else None,
    )
    return AnnotationEngine.from_files(
        reference_npz=assets.reference_npz,
        metadata_csv=assets.metadata_csv,
        model_ei_json=MODEL_DIR / "model_ei.json",
        model_ri_json=MODEL_DIR / "model_ri.json",
        calibration_json=MODEL_DIR / "calibration.json",
    )


def interpretation_box(result: dict) -> None:
    decision = result["decision"]
    if decision == "Empirically accepted at the 5% target-error operating point":
        st.success(decision)
    elif decision == "Empirically accepted at the 10% target-error operating point":
        st.success(decision)
    elif result["candidate_set_size_90"] <= 10 and result["predicted_top1_correctness"] >= 0.70:
        st.info("Top candidate is comparatively well supported, but remains a library-based tentative annotation.")
    else:
        st.warning("Ambiguous result: retain the candidate set and/or seek additional orthogonal evidence before exact annotation.")


def show_single_result(result: dict) -> None:
    interpretation_box(result)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Top candidate", result["top_candidate_name"])
    c2.metric("Similarity", f'{result["top_similarity"]:.4f}')
    c3.metric("Predicted top-1 correctness", f'{100*result["predicted_top1_correctness"]:.1f}%')
    c4.metric("90% candidate-set size", result["candidate_set_size_90"])

    if result.get("used_ri"):
        delta = result.get("top_candidate_delta_ri")
        if delta is not None:
            st.write(f"**Top-candidate |ΔRI|:** {delta:.1f} RI units")
            if delta > 50:
                st.error("Large RI disagreement (>50 units). The manuscript sensitivity analysis showed that RI fusion can become detrimental at large disagreement.")
            elif delta > 20:
                st.warning("Moderate-to-large RI disagreement (>20 units). Interpret RI-assisted ranking cautiously.")

    top_df = pd.DataFrame(result["top10"])
    set_df = pd.DataFrame(result["candidate_set_90"])

    st.subheader("Top 10 candidates")
    st.dataframe(top_df, use_container_width=True, hide_index=True)

    st.subheader("90% conformal candidate set")
    st.dataframe(set_df, use_container_width=True, hide_index=True)

    export_summary = pd.DataFrame([result["summary_row"]])
    st.download_button(
        "Download result summary (CSV)",
        export_summary.to_csv(index=False).encode(),
        file_name="gcei_annotation_summary.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download 90% candidate set (CSV)",
        set_df.to_csv(index=False).encode(),
        file_name="gcei_candidate_set_90.csv",
        mime="text/csv",
    )


st.title("GC–EI Annotation Reliability Tool")
st.caption("A reliability layer for conventional GC–EI–MS spectral-library annotation")

with st.expander("What this tool does and does not do", expanded=False):
    st.markdown(
        """
This research tool reproduces the frozen publication workflow. It ranks reference identities,
constructs a calibrated 90% candidate set, estimates the probability that the top-ranked identity
is correct, and can abstain at empirical calibration-derived operating points.

**Important:** the output is a *library-based tentative annotation*. It does not replace an
authentic reference standard or another suitable orthogonal confirmation method. A low-confidence
result is not proof that the compound is absent from the library.
        """
    )

try:
    with st.spinner("Preparing the publication reference library. First launch may take a little longer..."):
        engine = load_engine()
except Exception as exc:
    st.error("The reference library could not be prepared automatically.")
    st.exception(exc)
    st.stop()

mode = st.radio("Analysis mode", ["Single spectrum", "Batch spectra"], horizontal=True)

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
            peaks = parse_peak_text(text)
        except Exception as exc:
            st.error(str(exc))
    else:
        uploaded = st.file_uploader("Upload CSV with columns mz,intensity", type=["csv"])
        if uploaded is not None:
            try:
                peaks = parse_peak_csv(uploaded.getvalue())
            except Exception as exc:
                st.error(str(exc))

    use_ri = st.checkbox("I have a Kovats retention index measured under conditions considered comparable with the reference RI system")
    query_ri = None
    if use_ri:
        query_ri = st.number_input("Experimental Kovats RI", min_value=1.0, value=1000.0, step=1.0)
        st.caption("Enter Kovats RI, not raw retention time. RI-assisted results should be interpreted cautiously when chromatographic conditions are not comparable.")

    if st.button("Analyze spectrum", type="primary"):
        if peaks is None or len(peaks) == 0:
            st.error("Provide a valid spectrum first.")
        else:
            result = engine.annotate(peaks, query_ri=query_ri)
            show_single_result(result)

else:
    st.write("Upload a long-format CSV. Required columns: `spectrum_id`, `mz`, `intensity`. Optional column: `ri`.")
    uploaded = st.file_uploader("Batch CSV", type=["csv"], key="batch")

    if uploaded is not None:
        raw = uploaded.getvalue()
        try:
            df = pd.read_csv(io.BytesIO(raw))
            required = {"spectrum_id", "mz", "intensity"}
            missing = required.difference(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
        except Exception as exc:
            st.error(str(exc))
            df = None

        if df is not None and st.button("Analyze batch", type="primary"):
            rows = []
            all_candidates = []
            progress = st.progress(0)
            groups = list(df.groupby("spectrum_id", sort=False))

            for i, (spectrum_id, group) in enumerate(groups, start=1):
                peaks = list(zip(group["mz"].astype(float), group["intensity"].astype(float)))
                query_ri = None
                if "ri" in group.columns:
                    valid_ri = pd.to_numeric(group["ri"], errors="coerce").dropna()
                    if len(valid_ri):
                        query_ri = float(valid_ri.iloc[0])

                result = engine.annotate(peaks, query_ri=query_ri)
                summary = dict(result["summary_row"])
                summary["spectrum_id"] = spectrum_id
                rows.append(summary)

                for cand in result["candidate_set_90"]:
                    rec = dict(cand)
                    rec["spectrum_id"] = spectrum_id
                    all_candidates.append(rec)

                progress.progress(i / len(groups))

            summary_df = pd.DataFrame(rows)
            candidate_df = pd.DataFrame(all_candidates)
            st.subheader("Batch summary")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download batch summary (CSV)",
                summary_df.to_csv(index=False).encode(),
                file_name="gcei_batch_summary.csv",
                mime="text/csv",
            )
            st.download_button(
                "Download all 90% candidate sets (CSV)",
                candidate_df.to_csv(index=False).encode(),
                file_name="gcei_batch_candidate_sets_90.csv",
                mime="text/csv",
            )

st.divider()
st.caption("Publication release candidate 0.2.0-rc1 · Source code and scientific documentation are provided with the repository.")
