import json
from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd
import pytest

from src import metrics, screening
from src.model_config import (
    ModelConfigurationError,
    get_model_configuration,
)
from src.pricing import PricingError, estimate_cost, get_model_pricing


CASE = {
    "patient_id": "P1",
    "patient_summary": "0. The required fact is documented.",
    "trial_id": "T1",
    "trial_title": "Trial one",
    "criterion_id": "C1",
    "criterion_type": "inclusion",
    "criterion_text": "The required fact is present.",
}


def _mock_client():
    response = SimpleNamespace(
        status="completed",
        output_text=json.dumps({
            "criterion_id": "C1",
            "predicted_label": "MET",
            "evidence_sentence_ids": [0],
            "rationale": "The summary states the required fact.",
        }),
        id="response-test",
        usage=SimpleNamespace(input_tokens=10, output_tokens=8),
    )
    return SimpleNamespace(responses=SimpleNamespace(create=Mock(return_value=response)))


def test_legacy_screening_request_keeps_temperature_and_no_reasoning(monkeypatch):
    client = _mock_client()
    monkeypatch.setattr(screening, "get_openai_client", lambda: client)

    screening.screen_one_criterion(CASE)

    request = client.responses.create.call_args.kwargs
    assert request["temperature"] == 0
    assert "reasoning" not in request


def test_candidate_screening_request_uses_reasoning_without_temperature(monkeypatch):
    client = _mock_client()
    monkeypatch.setattr(screening, "get_openai_client", lambda: client)

    _, metadata = screening.screen_one_criterion(
        CASE,
        model_name="gpt-5.6-sol",
        reasoning_effort="medium",
        temperature=None,
        configuration_id="gpt56sol-medium-v2",
    )

    request = client.responses.create.call_args.kwargs
    assert request["reasoning"] == {"effort": "medium"}
    assert "temperature" not in request
    assert metadata["configuration_id"] == "gpt56sol-medium-v2"
    assert metadata["reasoning_effort"] == "medium"
    assert metadata["response_id"] == "response-test"


def test_model_configurations_are_registered():
    candidate = get_model_configuration("gpt56sol-medium-v2")

    assert candidate.model == "gpt-5.6-sol"
    assert candidate.prompt_version == "v2_abstention_rules"
    assert candidate.reasoning_effort == "medium"
    assert candidate.temperature is None


def test_unknown_model_configuration_is_rejected():
    with pytest.raises(ModelConfigurationError, match="Unknown model configuration"):
        get_model_configuration("unknown")


def test_pricing_is_model_specific_and_unknown_models_fail():
    assert get_model_pricing("gpt-4.1").input_usd_per_million == 2
    assert get_model_pricing("gpt-5.6-sol").output_usd_per_million == 20
    assert estimate_cost("gpt-5.6-sol", 10, 8) == pytest.approx(0.0002)

    with pytest.raises(PricingError, match="No pricing"):
        get_model_pricing("unknown")


def test_metrics_uses_the_model_recorded_on_each_row():
    predictions = pd.DataFrame([
        {"model": "gpt-4.1", "status": "success", "input_tokens": 1_000, "output_tokens": 1_000},
        {"model": "gpt-5.6-sol", "status": "success", "input_tokens": 1_000, "output_tokens": 1_000},
    ])

    costs = metrics.estimate_prediction_costs(predictions)

    assert costs.tolist() == pytest.approx([0.01, 0.024])


def test_metrics_accepts_integer_valued_float_tokens():
    predictions = pd.DataFrame([
        {"model": "gpt-4.1", "status": "success", "input_tokens": 1000.0, "output_tokens": 1000.0},
    ])

    assert metrics.estimate_prediction_costs(predictions).tolist() == pytest.approx([0.01])


@pytest.mark.parametrize(
    "input_tokens,output_tokens",
    [(None, 1), (1, None), (1.5, 1), (1, 1.5)],
)
def test_metrics_rejects_missing_or_fractional_successful_tokens(input_tokens, output_tokens):
    predictions = pd.DataFrame([{
        "model": "gpt-4.1",
        "status": "success",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }])

    with pytest.raises(PricingError, match="token counts"):
        metrics.estimate_prediction_costs(predictions)


@pytest.mark.parametrize("model", [None, "unknown"])
def test_metrics_rejects_missing_or_unknown_models(model):
    predictions = pd.DataFrame([
        {"model": model, "status": "success", "input_tokens": 1, "output_tokens": 1},
    ])

    with pytest.raises(PricingError):
        metrics.estimate_prediction_costs(predictions)
