"""Streamlit MVP for criterion-level screening of synthetic demonstration cases."""

import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path


# Streamlit executes this file with mvp as sys.path[0], so add the repository
# root explicitly before importing the reusable src modules.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import streamlit as st

from src.case_data import (
    build_screening_case,
    filter_criterion_ids,
    filter_trial_ids,
    get_selected_assessment,
    list_patient_ids,
    load_reference_assessments,
)
from src.config import ConfigurationError, DEFAULT_SCREENING_MODEL, PROCESSED_DIR
from src.custom_case import prepare_custom_case
from src.review_routing import route_screening_result
from src.screening import screen_one_criterion


PERSISTENT_NOTICE = (
    "Demonstration with public synthetic data only. Not for clinical or enrolment decisions."
)
CUSTOM_WARNING = "Synthetic demonstration data only. Do not enter real patient information."


@st.cache_data(show_spinner=False)
def load_dataset_assessments():
    """Cache only the read-only structurally validated reference data."""
    return load_reference_assessments(PROCESSED_DIR)


def _fingerprint(value: dict) -> str:
    serialised = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialised.encode("utf-8")).hexdigest()


def _current_result(fingerprint: str):
    stored = st.session_state.get("screening_result")
    if stored and stored["fingerprint"] != fingerprint:
        st.session_state.pop("screening_result", None)
    return st.session_state.get("screening_result")


def _store_error(fingerprint: str, message: str) -> None:
    st.session_state["screening_error"] = {
        "fingerprint": fingerprint,
        "message": message,
    }


def _show_stored_error(fingerprint: str) -> None:
    error = st.session_state.get("screening_error")
    if error and error["fingerprint"] != fingerprint:
        st.session_state.pop("screening_error", None)
    error = st.session_state.get("screening_error")
    if error:
        st.error(error["message"])


def _run_screening(case: dict, fingerprint: str, ground_truth_label: str | None = None) -> None:
    st.session_state.pop("screening_result", None)
    st.session_state.pop("screening_error", None)
    try:
        result, metadata = screen_one_criterion(case, model_name=DEFAULT_SCREENING_MODEL)
        routing = route_screening_result(result["predicted_label"])
        st.session_state["screening_result"] = {
            "fingerprint": fingerprint,
            "mode": st.session_state["screening_mode"],
            "result": result,
            "metadata": metadata,
            "routing": asdict(routing),
            "ground_truth_label": ground_truth_label,
        }
    except ConfigurationError:
        _store_error(
            fingerprint,
            "Screening is not configured. Set OPENAI_API_KEY before submitting an assessment.",
        )
    except ValueError as error:
        _store_error(fingerprint, f"Validation error: {error}")
    except Exception:
        _store_error(
            fingerprint,
            "The screening request failed. No assessment result was produced.",
        )


def _render_result(fingerprint: str) -> None:
    stored = _current_result(fingerprint)
    _show_stored_error(fingerprint)
    if not stored:
        return

    result = stored["result"]
    metadata = stored["metadata"]
    routing = stored["routing"]

    st.subheader("Screening result")
    st.write(f"**Predicted label:** `{result['predicted_label']}`")
    st.write(f"**Rationale:** {result['rationale']}")
    st.write(f"**Evidence sentence IDs:** `{result['evidence_sentence_ids']}`")
    st.write(f"**Review route:** `{routing['route']}`")
    st.write(f"**Queue required:** `{routing['queue_required']}`")
    st.info("Human confirmation remains required before any clinical action.")

    st.caption(
        f"Model: {metadata['model']} | Prompt: {metadata['prompt_version']} | "
        f"Latency: {metadata['latency_seconds']} seconds | "
        f"Input tokens: {metadata['input_tokens']} | Output tokens: {metadata['output_tokens']}"
    )

    if stored["mode"] == "Dataset case":
        with st.expander("Evaluation-only comparison"):
            ground_truth_label = stored["ground_truth_label"]
            st.write(f"**Ground-truth label:** `{ground_truth_label}`")
            st.write(
                "**Agreement:** "
                f"`{result['predicted_label'] == ground_truth_label}`"
            )


def _render_dataset_mode(assessments_df) -> None:
    patient_id = st.selectbox("Patient ID", list_patient_ids(assessments_df))
    trial_id = st.selectbox("Trial ID", filter_trial_ids(assessments_df, patient_id))
    criterion_id = st.selectbox(
        "Criterion ID", filter_criterion_ids(assessments_df, patient_id, trial_id)
    )
    assessment = get_selected_assessment(assessments_df, patient_id, trial_id, criterion_id)
    case = build_screening_case(assessment)

    st.subheader("Synthetic patient summary")
    st.text(case["patient_summary"])
    st.subheader("Selected criterion")
    st.write(f"**Type:** `{case['criterion_type']}`")
    st.write(case["criterion_text"])

    fingerprint = _fingerprint({"mode": "Dataset case", "case": case})
    st.session_state["screening_mode"] = "Dataset case"
    if st.button("Run screening", type="primary", key="dataset_submit"):
        _run_screening(case, fingerprint, str(assessment["ground_truth_label"]))
    _render_result(fingerprint)


def _render_custom_mode() -> None:
    st.warning(CUSTOM_WARNING)
    patient_summary = st.text_area("Synthetic patient summary")
    criterion_type = st.selectbox("Criterion type", ["inclusion", "exclusion"])
    criterion_text = st.text_area("Criterion text")

    fingerprint = _fingerprint({
        "mode": "Custom synthetic case",
        "patient_summary": patient_summary,
        "criterion_type": criterion_type,
        "criterion_text": criterion_text,
    })
    st.session_state["screening_mode"] = "Custom synthetic case"
    if st.button("Submit synthetic case", type="primary", key="custom_submit"):
        try:
            case = prepare_custom_case(patient_summary, criterion_type, criterion_text)
        except (TypeError, ValueError) as error:
            st.session_state.pop("screening_result", None)
            _store_error(fingerprint, f"Validation error: {error}")
        else:
            _run_screening(case, fingerprint)
    _render_result(fingerprint)


def main() -> None:
    st.set_page_config(page_title="Clinical-Trial Eligibility Copilot")
    st.title("Clinical-Trial Eligibility Copilot")
    st.info(PERSISTENT_NOTICE)

    try:
        assessments_df = load_dataset_assessments()
    except Exception:
        st.error("Reference data could not be loaded or failed structural validation.")
        return

    mode = st.radio("Screening mode", ["Dataset case", "Custom synthetic case"])
    if mode == "Dataset case":
        _render_dataset_mode(assessments_df)
    else:
        _render_custom_mode()


if __name__ == "__main__":
    main()
