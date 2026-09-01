import sys
from unittest.mock import Mock

import pandas as pd
import pytest

from src import run_screening
from src.config import ConfigurationError


def test_candidate_requires_explicit_output(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_screening", "--configuration-id", "gpt56sol-medium-v2"],
    )

    with pytest.raises(SystemExit):
        run_screening.parse_args()


def test_candidate_cannot_use_protected_baseline_output(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_screening",
            "--configuration-id",
            "gpt56sol-medium-v2",
            "--output",
            "data/processed/llm_predictions_gpt41_v2.csv",
        ],
    )

    with pytest.raises(SystemExit):
        run_screening.parse_args()


def test_candidate_cannot_use_resolved_protected_baseline_output(monkeypatch):
    protected = run_screening.PROCESSED_DIR / "llm_predictions_gpt41_v2.csv"
    equivalent_path = protected.parent / "nested" / ".." / protected.name
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_screening",
            "--configuration-id",
            "gpt56sol-medium-v2",
            "--output",
            str(equivalent_path),
        ],
    )

    with pytest.raises(SystemExit):
        run_screening.parse_args()


def test_legacy_cli_keeps_default_output_and_model(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_screening"])

    args = run_screening.parse_args()

    assert args.output == run_screening.DEFAULT_OUTPUT_PATH
    assert args.model == run_screening.DEFAULT_SCREENING_MODEL
    assert args.configuration_id is None


def test_legacy_run_does_not_infer_registered_configuration(tmp_path, monkeypatch):
    assessments = pd.DataFrame([{
        "source_annotation_id": 1,
        "patient_id": "P1",
        "trial_id": "T1",
        "trial_title": "Trial",
        "criterion_id": "C1",
        "criterion_type": "inclusion",
        "criterion_text": "Criterion",
        "ground_truth_label": "MET",
        "patient_summary": "0. Fact",
    }])
    screen = Mock(return_value=(
        {
            "predicted_label": "MET",
            "evidence_sentence_ids": [0],
            "rationale": "Supported.",
        },
        {
            "configuration_id": "legacy",
            "reasoning_effort": None,
            "model": "environment-model",
            "prompt_version": "environment-prompt",
            "response_id": "response-1",
            "latency_seconds": 0.1,
            "input_tokens": 1,
            "output_tokens": 1,
        },
    ))
    monkeypatch.setattr(run_screening, "DEFAULT_SCREENING_MODEL", "environment-model")
    monkeypatch.setattr(run_screening, "PROMPT_VERSION", "environment-prompt")
    monkeypatch.setattr(run_screening, "SCREENING_TEMPERATURE", 0.4)
    monkeypatch.setattr(run_screening, "load_reference_assessments", lambda *_args: assessments)
    monkeypatch.setattr(run_screening, "validate_locked_assessments", lambda df, **_kwargs: df)
    monkeypatch.setattr(run_screening, "build_screening_case", lambda row: dict(row))
    monkeypatch.setattr(run_screening, "screen_one_criterion", screen)
    monkeypatch.setattr(run_screening, "save_results", Mock())

    run_screening.run_screening(
        limit=1,
        output_path=tmp_path / "legacy.csv",
        resume=False,
        overwrite=False,
        model_name="environment-model",
    )

    call = screen.call_args.kwargs
    assert call["model_name"] == "environment-model"
    assert call["reasoning_effort"] is None
    assert call["temperature"] == 0.4
    assert call["configuration_id"] == "legacy"


def test_candidate_prompt_conflict_fails_before_loading_data(tmp_path, monkeypatch):
    monkeypatch.setattr(run_screening, "PROMPT_VERSION", "v1_other_prompt")
    monkeypatch.setattr(
        run_screening,
        "load_reference_assessments",
        lambda *_args: pytest.fail("reference data should not be loaded"),
    )

    with pytest.raises(ConfigurationError, match="requires prompt version"):
        run_screening.run_screening(
            limit=1,
            output_path=tmp_path / "candidate.csv",
            resume=False,
            overwrite=False,
            model_name=run_screening.DEFAULT_SCREENING_MODEL,
            configuration_id="gpt56sol-medium-v2",
        )


def test_configuration_and_explicit_model_cannot_be_combined(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_screening",
            "--configuration-id",
            "gpt56sol-medium-v2",
            "--model",
            "gpt-4.1",
            "--output",
            "candidate.csv",
        ],
    )

    with pytest.raises(SystemExit):
        run_screening.parse_args()


def _resume_frame(**overrides):
    row = {column: "" for column in run_screening.RESULT_COLUMNS}
    row.update({
        "source_annotation_id": 1,
        "status": "success",
        "model": "gpt-5.6-sol",
        "prompt_version": "v2_abstention_rules",
        "configuration_id": "gpt56sol-medium-v2",
        "reasoning_effort": "medium",
    })
    row.update(overrides)
    return pd.DataFrame([row])


def test_candidate_resume_rejects_legacy_metadata():
    legacy = _resume_frame().drop(columns=["configuration_id", "reasoning_effort"])

    with pytest.raises(ValueError, match="missing.*configuration_id"):
        run_screening._validate_resume_metadata(
            legacy,
            model="gpt-5.6-sol",
            prompt_version="v2_abstention_rules",
            configuration_id="gpt56sol-medium-v2",
            reasoning_effort="medium",
            explicit_configuration=True,
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("model", "gpt-4.1"),
        ("prompt_version", "v1"),
        ("configuration_id", "other"),
        ("reasoning_effort", "high"),
    ],
)
def test_resume_rejects_selected_run_metadata_mismatch(field, value):
    with pytest.raises(ValueError, match=field):
        run_screening._validate_resume_metadata(
            _resume_frame(**{field: value}),
            model="gpt-5.6-sol",
            prompt_version="v2_abstention_rules",
            configuration_id="gpt56sol-medium-v2",
            reasoning_effort="medium",
            explicit_configuration=True,
        )


def test_legacy_resume_backfills_metadata_and_checks_model_and_prompt():
    legacy = _resume_frame(
        model="environment-model",
        prompt_version="environment-prompt",
    ).drop(columns=["configuration_id", "reasoning_effort"])

    resumed = run_screening._validate_resume_metadata(
        legacy,
        model="environment-model",
        prompt_version="environment-prompt",
        configuration_id="legacy",
        reasoning_effort=None,
        explicit_configuration=False,
    )

    assert resumed["configuration_id"].tolist() == ["legacy"]
    assert resumed["reasoning_effort"].tolist() == [""]
