import importlib
import json
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import dotenv


def test_screening_imports_without_api_key_and_initialises_before_timing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *_args, **_kwargs: None)
    monkeypatch.setattr("langsmith.traceable", lambda **_kwargs: lambda function: function)
    sys.modules.pop("src.config", None)
    sys.modules.pop("src.screening", None)
    screening = importlib.import_module("src.screening")

    events = []
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
    client = SimpleNamespace(responses=SimpleNamespace(create=Mock(return_value=response)))

    def get_client():
        events.append("client")
        return client

    times = iter((10.0, 10.25))
    monkeypatch.setattr(screening, "get_openai_client", get_client)
    monkeypatch.setattr(screening, "perf_counter", lambda: (events.append("timer") or next(times)))

    result, metadata = screening.screen_one_criterion({
        "patient_id": "P1",
        "patient_summary": "0. The required fact is documented.",
        "trial_id": "T1",
        "trial_title": "Trial one",
        "criterion_id": "C1",
        "criterion_type": "inclusion",
        "criterion_text": "The required fact is present.",
    })

    assert events[:2] == ["client", "timer"]
    assert result["predicted_label"] == "MET"
    assert metadata["latency_seconds"] == 0.25
    client.responses.create.assert_called_once()
