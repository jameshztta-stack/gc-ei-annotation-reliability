"""GC–EI–MS Annotation Tool, version 2.0.2.

The app uses a defined 8,455-entry EI reference library, weighted cosine
similarity, and a twelve-feature model for scoring the first-ranked candidate.
"""
from __future__ import annotations

import hashlib
import io

import pandas as pd
import streamlit as st

from gcei.bootstrap import SOURCE_RECORD
from gcei.engine import parse_single_spectrum_text, read_spectrum_csv
from gcei.reference_builder import EXPECTED_SHA256
from gcei.v2_bootstrap import V2_HGB, ensure_v2_assets
from gcei.v2_engine import (
    GCEIV2Engine, V2_HGB_SHA256, V2_N_REFERENCE, V2_REFERENCE_SHA256,
)

APP_VERSION = "2.0.2"
SINGLE_EXAMPLE = "mz,intensity\n41,82.1\n43,44.6\n69,71.5\n93,100\n"
BATCH_EXAMPLE = (
    "spectrum_id,mz,intensity\n"
    "Sample_1,41,82.1\nSample_1,93,100\n"
    "Sample_2,43,65.2\nSample_2,71,100\n"
)

st.set_page_config(
    page_title="GC–EI–MS Annotation Tool",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
<style>
.block-container {max-width: 890px; padding-top: 2.3rem; padding-bottom: 3rem;}
h1 {font-weight: 700; letter-spacing: -0.038em; margin-bottom: .2rem;}
h2, h3 {letter-spacing: -.015em;}
[data-testid="stMetric"] {padding: .2rem 0;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_engine():
    """Always load the one current source-verified 8,455-entry EI configuration."""
    return GCEIV2Engine(ensure_v2_assets(), V2_HGB)


def fingerprint(*parts) -> str:
    digest = hashlib.sha256()
    for part in parts:
        data = part if isinstance(part, bytes) else repr(part).encode("utf-8")
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def top_candidates(table: pd.DataFrame) -> pd.DataFrame:
    selected = ["rank", "display_name", "formula", "similarity", "connectivity_id"]
    return table[selected].rename(columns={
        "rank": "Rank", "display_name": "Candidate",
        "formula": "Formula", "similarity": "Similarity",
        "connectivity_id": "Connectivity ID",
    }).copy()


def summary_row(result) -> pd.DataFrame:
    return pd.DataFrame([{
        "software_version": APP_VERSION,
        "reference_connectivity_count": V2_N_REFERENCE,
        "original_source_sha256": EXPECTED_SHA256,
        "reference_index_sha256": V2_REFERENCE_SHA256,
        "hgb_model_sha256": V2_HGB_SHA256,
        "top1_name": result.top1.get("display_name", ""),
        "top1_formula": result.top1.get("formula", ""),
        "top1_connectivity_id": result.top1.get("connectivity_id", ""),
        "top1_similarity": result.top1.get("similarity"),
        "top_hit_reliability_score": result.confidence,
        "top1_top2_margin": result.margin,
        "screening_setting": result.risk_target,
        "screening_criterion_met": result.accepted,
        "target_error_rate_certified": False,
        "chemical_identity_independently_confirmed": False,
        "interpretation": "Tentative first14-connectivity library annotation",
    }])


def render_results(result) -> None:
    st.divider()
    st.subheader("Annotation results")
    status = (
        "Meets the selected confidence-screening rule"
        if result.accepted
        else "Does not meet the selected confidence-screening rule"
    )
    st.caption(status + ". Library matches are tentative, not confirmed identifications.")

    name = result.top1.get("display_name", "") or "Unnamed library candidate"
    st.markdown(f"**Top candidate: {name}**")
    m1, m2, m3 = st.columns(3)
    m1.metric("Spectral similarity", f"{result.top1['similarity']:.3f}")
    m2.metric(
        "Confidence score", f"{result.confidence:.1%}",
        help="Estimated agreement with the library connectivity label based on the original study; not independently verified identification probability.",
    )
    m3.metric("Top-two difference", f"{result.margin:.3f}")

    st.markdown("**Top 10 candidate matches**")
    st.dataframe(top_candidates(result.top10), use_container_width=True, hide_index=True)

    a, b = st.columns(2)
    with a:
        st.download_button(
            "Download result summary",
            summary_row(result).to_csv(index=False).encode("utf-8"),
            file_name="gc_ei_ms_annotation_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with b:
        st.download_button(
            "Download candidate table",
            result.top10.to_csv(index=False).encode("utf-8"),
            file_name="gc_ei_ms_top10_candidates.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with st.expander("Result interpretation"):
        st.write(
            "The confidence score estimates agreement with the reference-library "
            "connectivity label. It is not a validated probability of confirming "
            "the chemical identity of an unknown experimental sample."
        )
        if result.accepted:
            st.write("The selected screening rule was met; this is not a guaranteed error rate.")
        else:
            st.write("The selected screening rule was not met. Interpret any single assignment cautiously.")
        for warning in result.warnings:
            st.write("• " + warning)


st.title("GC–EI–MS Annotation Tool")
st.write(
    "Identify **possible compound matches** from electron-ionization (EI) mass spectra. "
    f"The tool compares your peaks with a library of **{V2_N_REFERENCE:,} chemical-connectivity "
    "references**, ranks the 10 closest candidates, and provides spectral similarity and "
    "confidence scores. You can analyze one spectrum or multiple spectra in a batch."
)
st.caption(
    "For research use. Results are tentative library annotations; confirm important "
    "identifications using authentic standards or complementary evidence."
)

analysis_mode = st.radio(
    "Analysis type", ["Single spectrum", "Batch spectra"], horizontal=True,
)

st.subheader("1. Prepare your data")
if analysis_mode == "Single spectrum":
    st.write(
        "Use a CSV with two columns: **mz** (mass-to-charge ratio) and "
        "**intensity**. Enter one ion peak per row, without extra fields."
    )
    st.code(SINGLE_EXAMPLE, language="text")
    st.download_button(
        "Download single-spectrum template",
        SINGLE_EXAMPLE.encode("utf-8"),
        file_name="gc_ei_ms_single_template.csv",
        mime="text/csv",
    )
else:
    st.write(
        "Use a CSV with **spectrum_id, mz, intensity**. Repeat the same "
        "**spectrum_id** for all peaks belonging to one spectrum. "
        "Each unique ID is analyzed separately. Retention-index data are not used."
    )
    st.code(BATCH_EXAMPLE, language="text")
    st.download_button(
        "Download batch template",
        BATCH_EXAMPLE.encode("utf-8"),
        file_name="gc_ei_ms_batch_template.csv",
        mime="text/csv",
    )

st.subheader("2. Analyze")
with st.expander("Confidence screening (optional)"):
    screening = st.selectbox(
        "Selection rule",
        ["Standard (score ≥0.87)", "Strict (score ≥0.94 and margin ≥0.20)"],
        help="These settings affect which results are flagged for further review, "
             "not the ranking of compounds. They do not guarantee an error rate for new samples.",
    )
    st.caption(
        "The two screening criteria were evaluated retrospectively. "
        "Neither provides a validated error-rate guarantee for new samples."
    )
risk_target = .10 if screening.startswith("Standard") else .05

if analysis_mode == "Single spectrum":
    method = st.radio("Spectrum input", ["Paste peaks", "Upload CSV"], horizontal=True)
    with st.form("single_spectrum_form"):
        raw_text, uploaded = None, None
        if method == "Paste peaks":
            raw_text = st.text_area(
                "Peak list (mz, intensity)",
                placeholder="41,82.1\n43,44.6\n69,71.5",
                height=140,
            )
        else:
            uploaded = st.file_uploader(
                "Upload spectrum CSV", type=["csv"],
                help="Use the single-spectrum template above.",
            )
        submitted = st.form_submit_button(
            "Analyze spectrum", type="primary", use_container_width=True,
        )

    payload = raw_text if method == "Paste peaks" else (
        uploaded.getvalue() if uploaded is not None else b""
    )
    key = fingerprint("single", method, payload, risk_target)
    if submitted:
        try:
            if method == "Paste peaks":
                peaks = parse_single_spectrum_text(raw_text or "")
            else:
                if uploaded is None:
                    raise ValueError("Upload a CSV file using the template above.")
                peaks = read_spectrum_csv(uploaded.getvalue())
            with st.spinner("Analyzing spectrum…"):
                result = load_engine().analyze(peaks, risk_target=risk_target)
            st.session_state["single_annotation"] = (key, result)
        except (ValueError, RuntimeError, OSError) as exc:
            st.session_state.pop("single_annotation", None)
            st.error(str(exc))
        except Exception:
            st.session_state.pop("single_annotation", None)
            st.error("Analysis could not be completed. Check your input or try again.")

    prior = st.session_state.get("single_annotation")
    if prior and prior[0] == key:
        render_results(prior[1])
else:
    with st.form("batch_spectra_form"):
        uploaded = st.file_uploader(
            "Upload batch CSV", type=["csv"],
            help="Use the three-column batch template above.",
        )
        submitted = st.form_submit_button(
            "Analyze batch", type="primary", use_container_width=True,
        )
    payload = uploaded.getvalue() if uploaded is not None else b""
    key = fingerprint("batch", payload, risk_target)
    if submitted:
        try:
            if uploaded is None:
                raise ValueError("Upload a batch CSV using the template above.")
            df = pd.read_csv(io.BytesIO(payload))
            with st.spinner("Analyzing spectra…"):
                results = load_engine().analyze_batch(df, risk_target=risk_target)
            results.insert(0, "software_version", APP_VERSION)
            results["reference_connectivity_count"] = V2_N_REFERENCE
            results["original_source_sha256"] = EXPECTED_SHA256
            results["target_error_rate_certified"] = False
            st.session_state["batch_annotation"] = (key, results)
        except (ValueError, RuntimeError, OSError) as exc:
            st.session_state.pop("batch_annotation", None)
            st.error(str(exc))
        except Exception:
            st.session_state.pop("batch_annotation", None)
            st.error("Batch analysis failed. Check the CSV structure and peak values.")

    prior = st.session_state.get("batch_annotation")
    if prior and prior[0] == key:
        results = prior[1]
        st.divider()
        st.subheader("Annotation results")
        st.caption(f"{len(results)} spectra analyzed · tentative matches")
        columns = [
            "spectrum_id", "top1_name", "top1_formula",
            "top1_connectivity_id", "top_similarity",
            "top_hit_reliability_score", "screening_criterion_met",
        ]
        st.dataframe(
            results[[x for x in columns if x in results.columns]],
            hide_index=True, use_container_width=True,
        )
        st.download_button(
            "Download batch results",
            results.to_csv(index=False).encode("utf-8"),
            file_name="gc_ei_ms_batch_results.csv",
            mime="text/csv",
        )

with st.expander("About the method and its limitations"):
    st.write(
        "The software uses electron-ionization spectral similarity and a machine-learning "
        "confidence score to rank matches from a library of 8,455 reference connectivity "
        "identities (first 14 characters of InChIKey). It does not establish exact "
        "stereochemical identity, laboratory source independence, or the identity "
        "of an analyte absent from the library."
    )
    st.write(
        "In a within-library evaluation of 609 spectra, the highest-ranked candidate "
        "agreed with 394 publisher-provided connectivity labels (64.70%). "
        "These data did not independently verify chemical identity. The optional "
        "confidence-screening criteria are not certified error guarantees "
        "for future experimental samples."
    )
    st.write(
        "Retention-index fusion and calibrated candidate sets are not currently "
        "provided by this version. Use external experimental confirmation "
        "when compound identity is important."
    )
    with st.expander("Software and data provenance"):
        st.caption(f"Version: {APP_VERSION} · Reference identities: {V2_N_REFERENCE:,}")
        st.caption(f"Reference index SHA-256: {V2_REFERENCE_SHA256}")
        st.caption(f"Confidence model SHA-256: {V2_HGB_SHA256}")
        st.caption(f"Original mass-spectral source SHA-256: {EXPECTED_SHA256}")
        st.markdown(
            f"[Original EI spectral library]({SOURCE_RECORD}) · "
            "[Software source code](https://github.com/jameshztta-stack/gc-ei-annotation-reliability)"
        )

with st.expander("How to cite"):
    st.markdown(
        "**Software:** Zothantluanga, J. H. *GC–EI–MS Annotation Tool*. "
        "Jazer Research Lab. Version 2.0.2, 2026. "
        "[Zenodo DOI: 10.5281/zenodo.23373447](https://doi.org/10.5281/zenodo.23373447)."
    )
    st.markdown(
        f"**Original spectral library:** Cite the [MS-DIAL source record]({SOURCE_RECORD}) "
        "in studies that use this reference database."
    )
    st.markdown(
        "**Developed and maintained by:** Dr. James H. Zothantluanga, "
        "Research Director, Jazer Research Lab, Aizawl, Mizoram, India."
    )

st.caption(
    f"Version {APP_VERSION} · Developed and maintained by Dr. James H. Zothantluanga "
    "· Jazer Research Lab, Aizawl, Mizoram, India"
)
