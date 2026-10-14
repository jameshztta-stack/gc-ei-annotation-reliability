"""Minimal researcher interface for frozen GC–EI–MS v2 and isolated legacy v1.

Software v2.0.1 changes PRESENTATION only. Numerical models, source-reference
identity, model hashes and historical acceptance masks are unchanged.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st

from gcei.bootstrap import SOURCE_RECORD, ensure_runtime_assets
from gcei.engine import GCEIEngine, parse_single_spectrum_text, read_spectrum_csv
from gcei.reference_builder import EXPECTED_SHA256
from gcei.v2_bootstrap import V2_HGB, ensure_v2_assets
from gcei.v2_engine import GCEIV2Engine, V2_HGB_SHA256, V2_N_REFERENCE, V2_REFERENCE_SHA256

APP_VERSION = "2.0.1"
V2_MODE = "v2 · EI + HGB"
V1_MODE = "v1 · Legacy EI / RI"
SINGLE_EXAMPLE = "mz,intensity\n41,82.1\n43,44.6\n69,71.5\n93,100\n"
V2_BATCH_EXAMPLE = "spectrum_id,mz,intensity\nA,41,82.1\nA,93,100\nB,43,65.2\nB,71,100\n"
V1_BATCH_EXAMPLE = (
    "spectrum_id,mz,intensity,ri\nA,41,82.1,\nA,93,100,\n"
    "B,43,65.2,939\nB,71,100,939\n"
)

st.set_page_config(
    page_title="GC–EI–MS Annotation",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
<style>
.block-container {max-width: 930px; padding-top: 2.2rem; padding-bottom: 3.5rem;}
h1 {letter-spacing: -0.045em; font-weight: 700; margin-bottom: 0.15rem;}
h2, h3 {letter-spacing: -0.02em;}
[data-testid="stMetric"] {padding: 0.25rem 0;}
[data-testid="stMetricLabel"] {font-size: .82rem;}
div[data-testid="stVerticalBlock"] {gap: .6rem;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_engine(model_name: str):
    if model_name == V2_MODE:
        return GCEIV2Engine(ensure_v2_assets(), V2_HGB)
    if model_name == V1_MODE:
        return GCEIEngine(ensure_runtime_assets())
    raise ValueError("Unknown reference/model configuration.")


def request_fingerprint(*parts) -> str:
    h = hashlib.sha256()
    for part in parts:
        data = part if isinstance(part, bytes) else repr(part).encode("utf-8")
        h.update(len(data).to_bytes(8, "big"))
        h.update(data)
    return h.hexdigest()


def result_summary(result, use_v2: bool, accepted: bool) -> pd.DataFrame:
    return pd.DataFrame([{
        "software_version": APP_VERSION,
        "model_configuration": "frozen-v2" if use_v2 else "legacy-v1",
        "reference_first14_count": V2_N_REFERENCE if use_v2 else 8543,
        "original_source_sha256": EXPECTED_SHA256,
        "v2_reference_index_sha256": V2_REFERENCE_SHA256 if use_v2 else "",
        "v2_hgb_model_sha256": V2_HGB_SHA256 if use_v2 else "",
        "top1_name": result.top1.get("display_name", result.top1.get("name", "")),
        "top1_formula": result.top1.get("formula", ""),
        "top1_connectivity_id": result.top1.get("connectivity_id", ""),
        "top1_similarity": result.top1.get("similarity"),
        "historical_model_score": result.confidence,
        "top1_top2_cosine_margin": result.margin if use_v2 else "",
        "historical_acceptance_rule_met": accepted,
        "selected_error_target": result.risk_target,
        "selected_error_rate_certified": False,
        "independent_chemical_identity_authenticated": False,
        "v1_nominal_set_size": "" if use_v2 else result.conformal90_size,
        "external_set_coverage_certified": False,
        "ri_delta_top1": result.ri_delta_top1,
        "interpretation": "Tentative first14 connectivity-level library annotation",
    }])


def small_candidates(frame: pd.DataFrame) -> pd.DataFrame:
    columns = ["rank", "display_name", "formula", "similarity", "connectivity_id"]
    shown = frame[[c for c in columns if c in frame.columns]].copy()
    return shown.rename(columns={
        "rank": "Rank", "display_name": "Candidate",
        "formula": "Formula", "similarity": "Similarity",
        "connectivity_id": "Connectivity",
    })


def render_single(result, use_v2: bool) -> None:
    st.divider()
    st.subheader("Annotation results")
    accepted = result.accepted if use_v2 else result.confidence >= result.risk_threshold
    status = "Meets historical acceptance rule" if accepted else "Below historical acceptance rule"
    st.caption(status + " · All compound assignments remain tentative.")

    name = result.top1.get("display_name", result.top1.get("name", "Unlabelled candidate"))
    st.markdown("**Top-ranked library candidate**")
    st.write(name)

    m1, m2, m3 = st.columns(3)
    m1.metric("Similarity", f"{float(result.top1['similarity']):.3f}")
    m2.metric("Model score", f"{result.confidence:.1%}",
              help="Historical estimate of correct database connectivity label; not an authenticated identification probability.")
    if use_v2:
        m3.metric("Top-two margin", f"{result.margin:.3f}")
    else:
        m3.metric("Nominal set size", str(result.conformal90_size))

    st.markdown("**Ranked candidates**")
    st.dataframe(small_candidates(result.top10), use_container_width=True, hide_index=True)

    with st.expander("Download results"):
        d1, d2 = st.columns(2)
        d1.download_button(
            "Annotation summary (CSV)",
            data=result_summary(result, use_v2, accepted).to_csv(index=False).encode(),
            file_name="gcei_annotation_summary.csv",
            mime="text/csv", use_container_width=True,
        )
        d2.download_button(
            "All candidate details (CSV)",
            data=result.top10.to_csv(index=False).encode(),
            file_name="gcei_top10_candidates.csv",
            mime="text/csv", use_container_width=True,
        )
        if not use_v2:
            st.download_button(
                "Legacy nominal candidate set (CSV)",
                data=result.conformal90.to_csv(index=False).encode(),
                file_name="gcei_legacy_nominal_90_set.csv",
                mime="text/csv",
            )

    if result.warnings or not use_v2:
        with st.expander("Interpretation details"):
            if not use_v2:
                st.caption(
                    "v1's nominal 90% candidate set has no independently demonstrated "
                    "coverage for new instruments or laboratories."
                )
                st.dataframe(small_candidates(result.conformal90.head(30)),
                             hide_index=True, use_container_width=True)
            if result.ri_delta_top1 is not None:
                st.write(f"Top-candidate |ΔRI|: {result.ri_delta_top1:.1f}")
            for note in result.warnings:
                st.write("• " + note)


st.title("GC–EI–MS Annotation")
st.caption("Spectral library search · connectivity-level candidate ranking")

a, b = st.columns([1.2, 1])
with a:
    model_name = st.selectbox(
        "Reference model",
        [V2_MODE, V1_MODE],
        help="Frozen research v2 and historical v1 use different reference libraries and confidence models.",
    )
with b:
    analysis_mode = st.radio("Analysis", ["Single spectrum", "Batch"], horizontal=True)

use_v2 = model_name == V2_MODE
st.caption(
    "8,455 reference identities · EI-only" if use_v2
    else "8,543 reference identities · optional Kovats RI"
)
left, right = st.columns([1, 1])
with left:
    threshold_label = st.selectbox(
        "Historical decision rule",
        ["10% target", "5% target"],
        help="Original research threshold, not a certified future-error guarantee.",
    )
risk_target = .10 if threshold_label.startswith("10%") else .05

if analysis_mode == "Single spectrum":
    method = st.radio("Provide spectrum", ["Paste peaks", "Upload CSV"], horizontal=True)
    with st.form("single_annotation_form"):
        raw_text = None
        raw_file = None
        if method == "Paste peaks":
            raw_text = st.text_area(
                "m/z, intensity",
                placeholder=SINGLE_EXAMPLE,
                value="",
                height=160,
                help="One pair per line, separated by commas or spaces. Header optional.",
            )
        else:
            raw_file = st.file_uploader(
                "Spectrum CSV", type=["csv"],
                help="Two columns: mz,intensity.",
            )
        use_ri = False
        supplied_ri = None
        if not use_v2:
            use_ri = st.checkbox("Use Kovats RI", value=False,
                                 help="Only when the experimental and reference chromatographic conditions are comparable.")
            if use_ri:
                supplied_ri = st.number_input("Kovats RI", min_value=1., value=1000., step=1.)
        submitted = st.form_submit_button("Analyze spectrum", type="primary", use_container_width=True)

    payload = raw_text if method == "Paste peaks" else (raw_file.getvalue() if raw_file else b"")
    signature = request_fingerprint(model_name, analysis_mode, method, payload,
                                    risk_target, supplied_ri)
    if submitted:
        try:
            if method == "Paste peaks":
                peaks = parse_single_spectrum_text(raw_text or "")
            else:
                if not raw_file:
                    raise ValueError("Choose a spectrum CSV before analyzing.")
                peaks = read_spectrum_csv(raw_file.getvalue())
            with st.spinner("Analyzing spectrum…"):
                result = load_engine(model_name).analyze(
                    peaks, kovats_ri=supplied_ri if use_ri else None,
                    risk_target=risk_target,
                )
            st.session_state["single_result"] = (signature, result)
        except (ValueError, RuntimeError, OSError) as exc:
            st.session_state.pop("single_result", None)
            st.error(str(exc))
        except Exception:
            st.session_state.pop("single_result", None)
            st.error("The analysis could not be completed. Check the input and reference availability.")

    stored = st.session_state.get("single_result")
    if stored and stored[0] == signature:
        render_single(stored[1], use_v2)

else:
    with st.form("batch_annotation_form"):
        file = st.file_uploader(
            "Batch CSV", type=["csv"],
            help="One row per ion peak: spectrum_id,mz,intensity. RI is available only in legacy v1.",
        )
        submitted = st.form_submit_button("Analyze batch", type="primary", use_container_width=True)

    contents = file.getvalue() if file else b""
    signature = request_fingerprint(model_name, analysis_mode, contents, risk_target)
    if submitted:
        try:
            if not file:
                raise ValueError("Choose a batch CSV before analyzing.")
            import io
            df = pd.read_csv(io.BytesIO(contents))
            with st.spinner("Analyzing spectra…"):
                out = load_engine(model_name).analyze_batch(df, risk_target=risk_target)
            out.insert(0, "software_version", APP_VERSION)
            out["configuration"] = "frozen-v2" if use_v2 else "legacy-v1"
            out["reference_first14_count"] = V2_N_REFERENCE if use_v2 else 8543
            out["original_source_sha256"] = EXPECTED_SHA256
            out["selected_error_rate_certified"] = False
            st.session_state["batch_result"] = (signature, out)
        except (ValueError, RuntimeError, OSError) as exc:
            st.session_state.pop("batch_result", None)
            st.error(str(exc))
        except Exception:
            st.session_state.pop("batch_result", None)
            st.error("Batch analysis could not be completed. Check the CSV format.")

    stored = st.session_state.get("batch_result")
    if stored and stored[0] == signature:
        df = stored[1]
        st.divider()
        st.subheader("Batch results")
        st.caption(f"{len(df)} spectra · tentative library annotations")
        primary = [
            "spectrum_id", "top1_name", "top1_formula", "top1_connectivity_id",
            "top_similarity", "historical_HGB_score", "predicted_top1_correctness",
            "historical_acceptance_rule_met", "passes_empirical_operating_point",
        ]
        shown = df[[z for z in primary if z in df.columns]]
        st.dataframe(shown, use_container_width=True, hide_index=True)
        st.download_button("Download full batch results (CSV)",
                           df.to_csv(index=False).encode(),
                           file_name="gcei_batch_annotations.csv", mime="text/csv")

with st.expander("Input examples"):
    x, y = st.columns(2)
    with x:
        st.caption("Single spectrum")
        st.code(SINGLE_EXAMPLE, language="text")
        st.download_button("Single CSV template", SINGLE_EXAMPLE.encode(),
                           file_name="gcei_single_template.csv", mime="text/csv")
    with y:
        st.caption("Batch spectra")
        example = V2_BATCH_EXAMPLE if use_v2 else V1_BATCH_EXAMPLE
        st.code(example, language="text")
        st.download_button("Batch CSV template", example.encode(),
                           file_name="gcei_batch_template.csv", mime="text/csv")

with st.expander("Methods, limitations & provenance"):
    st.markdown(
        "**Interpretation:** All annotations represent source-reported InChIKey-first14 "
        "connectivity hypotheses, not independently verified chemical identities. "
        "The 5% and 10% historical acceptance targets are **not certified future-error guarantees**. "
        "Authentic standards or orthogonal evidence are required for confirmed identification."
    )
    if use_v2:
        st.write(
            "**Research v2:** 8,455 frozen source-indexed reference identities; "
            "m/z¹ × √intensity EI cosine; 12-feature development-fitted HGB. "
            "In the original within-MS-DIAL closed-library 609-query evaluation, "
            "394/609 source-label top-one matches were observed. Source acquisition "
            "independence, open-world identification and full molecular-form truth "
            "were not established. The 609 cases are already spent as an untouched test."
        )
        st.write(
            "Original 10%-target rule: HGB ≥0.87; 198/609 accepted, 12 source-label "
            "mismatches. Original 5%-target rule: HGB ≥0.94 and top-two margin ≥0.20; "
            "38/609 accepted, zero observed mismatches. Neither is formally certified. "
            "RI fusion and conformal candidate sets were not calibrated for v2."
        )
        st.caption(f"v2 reference index SHA-256: {V2_REFERENCE_SHA256}")
        st.caption(f"v2 frozen HGB SHA-256: {V2_HGB_SHA256}")
    else:
        st.write(
            "**Legacy v1:** 8,543 source-indexed reference identities. "
            "Optional RI-assisted ranking and a nominal 90% candidate set use "
            "the original v1 calibration only; external-laboratory coverage "
            "has not been established."
        )
    st.caption(f"Original MS-DIAL MSP SHA-256: {EXPECTED_SHA256}")
    st.markdown(
        f"[Original MS-DIAL source]({SOURCE_RECORD}) · "
        "[Software source](https://github.com/jameshztta-stack/gc-ei-annotation-reliability) · "
        "[Previous v1.0.0 archive](https://doi.org/10.5281/zenodo.23143113)"
    )
    st.caption(
        "The v1.0.0 DOI refers to the previous software release, not to this v2.0.1 version."
    )

st.caption(f"v{APP_VERSION} · Jazer Research Lab · Research use; tentative annotations only")
