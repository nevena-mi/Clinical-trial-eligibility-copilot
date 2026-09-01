import json
from unittest.mock import Mock
from urllib.error import URLError

import pytest

from src import n8n_client
from src.n8n_client import (
    N8NConfigurationError,
    N8NPayloadError,
    N8NResponseError,
    N8NSubmissionError,
    build_review_payload,
    submit_review_payload,
)


CASE = {
    "patient_id": "P1",
    "patient_summary": "1. Synthetic patient summary.",
    "trial_id": "T1",
    "trial_title": "Synthetic trial",
    "criterion_id": "C1",
    "criterion_type": "exclusion",
    "criterion_text": "The patient must not have the excluded condition.",
}
RESULT = {
    "predicted_label": "UNKNOWN",
    "evidence_sentence_ids": [],
    "rationale": "The available summary is insufficient.",
}
METADATA = {
    "model": "gpt-4.1",
    "prompt_version": "v2_abstention_rules",
    "response_id": "response-1",
}
PAYLOAD = build_review_payload(CASE, RESULT, METADATA)


class FakeResponse:
    def __init__(self, body, status=200):
        self.body = body
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def test_build_payload_excludes_ground_truth_and_optional_source_id():
    payload = build_review_payload(
        CASE,
        {**RESULT, "ground_truth_label": "NOT_MET"},
        METADATA,
    )

    assert payload["evaluation_mode"] is False
    assert "ground_truth_label" not in payload
    assert "source_annotation_id" not in payload


def test_build_payload_includes_review_context_exactly():
    payload = build_review_payload(CASE, RESULT, METADATA)

    assert payload["patient_summary"] == CASE["patient_summary"]
    assert payload["trial_title"] == CASE["trial_title"]
    assert payload["criterion_text"] == CASE["criterion_text"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("patient_summary", ""),
        ("patient_summary", "   "),
        ("patient_summary", 123),
        ("trial_title", ""),
        ("trial_title", "   "),
        ("trial_title", None),
        ("criterion_text", ""),
        ("criterion_text", "   "),
        ("criterion_text", []),
    ],
)
def test_build_payload_rejects_blank_review_context(field, value):
    case = {**CASE, field: value}

    with pytest.raises(N8NPayloadError, match="non-empty string"):
        build_review_payload(case, RESULT, METADATA)


@pytest.mark.parametrize("field", ["patient_summary", "trial_title", "criterion_text"])
def test_build_payload_rejects_missing_review_context(field):
    case = {key: value for key, value in CASE.items() if key != field}

    with pytest.raises(N8NPayloadError, match=field):
        build_review_payload(case, RESULT, METADATA)


@pytest.mark.parametrize(
    "mapping_name,field",
    [
        ("case", "patient_id"),
        ("result", "evidence_sentence_ids"),
        ("metadata", "response_id"),
    ],
)
def test_build_payload_wraps_missing_required_keys(mapping_name, field):
    mappings = {"case": CASE, "result": RESULT, "metadata": METADATA}
    mappings[mapping_name] = {
        key: value for key, value in mappings[mapping_name].items() if key != field
    }

    with pytest.raises(N8NPayloadError, match=field):
        build_review_payload(mappings["case"], mappings["result"], mappings["metadata"])


def test_build_payload_includes_dataset_source_id_when_available():
    payload = build_review_payload(
        CASE, RESULT, METADATA, source_annotation_id=463
    )

    assert payload["source_annotation_id"] == 463


@pytest.mark.parametrize("label", ["MET", "NOT_MET", "INVALID", None])
def test_review_payload_rejects_non_review_labels_before_http(label, monkeypatch):
    http_call = Mock()
    monkeypatch.setattr(n8n_client, "urlopen", http_call)
    result = {**RESULT, "predicted_label": label}

    with pytest.raises(N8NPayloadError, match="UNKNOWN or NOT_APPLICABLE"):
        build_review_payload(CASE, result, METADATA)
    http_call.assert_not_called()


def test_submit_payload_posts_json_and_validates_response(monkeypatch):
    monkeypatch.setenv("N8N_REVIEW_WEBHOOK_URL", "https://example.test/hook")
    response = FakeResponse(json.dumps({
        "route": "HUMAN_REVIEW",
        "queue_status": "OPEN",
        "queue_id": "response-1",
        "message": "Queued.",
    }).encode())
    http_call = Mock(return_value=response)
    monkeypatch.setattr(n8n_client, "urlopen", http_call)

    result = submit_review_payload(PAYLOAD, timeout_seconds=7)

    assert result.route == "HUMAN_REVIEW"
    assert result.queue_status == "OPEN"
    assert result.queue_id == "response-1"
    request = http_call.call_args.args[0]
    timeout = http_call.call_args.kwargs["timeout"]
    assert request.method == "POST"
    assert json.loads(request.data) == PAYLOAD
    assert timeout == 7


def test_missing_url_is_configuration_error_without_http(monkeypatch):
    monkeypatch.delenv("N8N_REVIEW_WEBHOOK_URL", raising=False)
    http_call = Mock()
    monkeypatch.setattr(n8n_client, "urlopen", http_call)

    with pytest.raises(N8NConfigurationError, match="N8N_REVIEW_WEBHOOK_URL"):
        submit_review_payload(PAYLOAD)
    http_call.assert_not_called()


@pytest.mark.parametrize("failure", [TimeoutError(), URLError("offline")])
def test_network_failures_are_submission_errors(monkeypatch, failure):
    monkeypatch.setenv("N8N_REVIEW_WEBHOOK_URL", "https://example.test/hook")
    monkeypatch.setattr(n8n_client, "urlopen", Mock(side_effect=failure))

    with pytest.raises(N8NSubmissionError, match="request failed"):
        submit_review_payload(PAYLOAD)


def test_non_2xx_response_is_submission_error(monkeypatch):
    monkeypatch.setenv("N8N_REVIEW_WEBHOOK_URL", "https://example.test/hook")
    monkeypatch.setattr(n8n_client, "urlopen", Mock(return_value=FakeResponse(b"{}", 500)))

    with pytest.raises(N8NSubmissionError, match="HTTP status 500"):
        submit_review_payload(PAYLOAD)


def test_invalid_json_is_response_error(monkeypatch):
    monkeypatch.setenv("N8N_REVIEW_WEBHOOK_URL", "https://example.test/hook")
    monkeypatch.setattr(n8n_client, "urlopen", Mock(return_value=FakeResponse(b"not json")))

    with pytest.raises(N8NResponseError, match="invalid JSON"):
        submit_review_payload(PAYLOAD)


@pytest.mark.parametrize(
    "response",
    [
        {"route": "NO_ROUTINE_QUEUE", "queue_status": "OPEN", "queue_id": "q", "message": "ok"},
        {"route": "HUMAN_REVIEW", "queue_status": "NOT_QUEUED", "queue_id": "q", "message": "ok"},
        {"route": "HUMAN_REVIEW", "queue_status": "OPEN", "queue_id": "", "message": "ok"},
        {"route": "HUMAN_REVIEW", "queue_status": "OPEN", "queue_id": "q", "message": ""},
    ],
)
def test_invalid_response_schema_is_rejected(monkeypatch, response):
    monkeypatch.setenv("N8N_REVIEW_WEBHOOK_URL", "https://example.test/hook")
    body = json.dumps(response).encode()
    monkeypatch.setattr(n8n_client, "urlopen", Mock(return_value=FakeResponse(body)))

    with pytest.raises(N8NResponseError):
        submit_review_payload(PAYLOAD)
