"""HTTP client and payload helpers for the synthetic human-review queue."""

import json
import os
from dataclasses import dataclass
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


VALID_REVIEW_LABELS = {"UNKNOWN", "NOT_APPLICABLE"}
EXPECTED_ROUTE = "HUMAN_REVIEW"
EXPECTED_QUEUE_STATUS = "OPEN"


class N8NConfigurationError(RuntimeError):
    """Raised when the review-queue endpoint is not configured."""


class N8NSubmissionError(RuntimeError):
    """Raised when a review-queue request cannot be completed."""


class N8NPayloadError(N8NSubmissionError):
    """Raised when a payload is not valid for a review-queue submission."""


class N8NResponseError(N8NSubmissionError):
    """Raised when n8n returns an invalid queue response."""


@dataclass(frozen=True)
class N8NQueueResponse:
    route: str
    queue_status: str
    queue_id: str
    message: str


def _required_payload_value(
    mapping: Mapping[str, object],
    field_name: str,
    mapping_name: str,
) -> object:
    if field_name not in mapping:
        raise N8NPayloadError(
            f"Missing required {mapping_name} field: {field_name}."
        )
    return mapping[field_name]


def _required_text(
    mapping: Mapping[str, object],
    field_name: str,
    mapping_name: str,
) -> str:
    value = _required_payload_value(mapping, field_name, mapping_name)
    if not isinstance(value, str) or not value.strip():
        raise N8NPayloadError(
            f"{mapping_name}.{field_name} must be a non-empty string."
        )
    return value


def build_review_payload(
    case: Mapping[str, object],
    result: Mapping[str, object],
    metadata: Mapping[str, object],
    *,
    source_annotation_id: object | None = None,
) -> dict[str, object]:
    """Build a live review payload without evaluation-only ground truth."""
    predicted_label = _required_payload_value(result, "predicted_label", "result")
    if not isinstance(predicted_label, str) or predicted_label not in VALID_REVIEW_LABELS:
        raise N8NPayloadError(
            "Review-queue submissions require predicted_label UNKNOWN or NOT_APPLICABLE."
        )

    payload = {
        "patient_id": _required_payload_value(case, "patient_id", "case"),
        "patient_summary": _required_text(case, "patient_summary", "case"),
        "trial_id": _required_payload_value(case, "trial_id", "case"),
        "trial_title": _required_text(case, "trial_title", "case"),
        "criterion_id": _required_payload_value(case, "criterion_id", "case"),
        "criterion_type": _required_payload_value(case, "criterion_type", "case"),
        "criterion_text": _required_text(case, "criterion_text", "case"),
        "predicted_label": predicted_label,
        "evidence_sentence_ids": _required_payload_value(
            result, "evidence_sentence_ids", "result"
        ),
        "rationale": _required_payload_value(result, "rationale", "result"),
        "model": _required_payload_value(metadata, "model", "metadata"),
        "prompt_version": _required_payload_value(
            metadata, "prompt_version", "metadata"
        ),
        "response_id": _required_payload_value(metadata, "response_id", "metadata"),
        "evaluation_mode": False,
    }
    if source_annotation_id is not None:
        payload["source_annotation_id"] = source_annotation_id
    return payload


def _validate_submission_payload(payload: Mapping[str, object]) -> None:
    predicted_label = payload.get("predicted_label")
    if not isinstance(predicted_label, str) or predicted_label not in VALID_REVIEW_LABELS:
        raise N8NPayloadError(
            "Review-queue submissions require predicted_label UNKNOWN or NOT_APPLICABLE."
        )


def _response_text(response) -> bytes:
    body = response.read()
    if isinstance(body, str):
        return body.encode("utf-8")
    return body


def _parse_queue_response(body: bytes) -> N8NQueueResponse:
    try:
        parsed = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise N8NResponseError("n8n returned invalid JSON.") from error

    if not isinstance(parsed, dict):
        raise N8NResponseError("n8n returned an invalid response object.")
    values = {
        "route": parsed.get("route"),
        "queue_status": parsed.get("queue_status"),
        "queue_id": parsed.get("queue_id"),
        "message": parsed.get("message"),
    }
    if values["route"] != EXPECTED_ROUTE:
        raise N8NResponseError("n8n returned an unexpected review route.")
    if values["queue_status"] != EXPECTED_QUEUE_STATUS:
        raise N8NResponseError("n8n returned an unexpected queue status.")
    if not isinstance(values["queue_id"], str) or not values["queue_id"].strip():
        raise N8NResponseError("n8n returned an invalid queue ID.")
    if not isinstance(values["message"], str) or not values["message"].strip():
        raise N8NResponseError("n8n returned an invalid queue message.")
    return N8NQueueResponse(**values)


def submit_review_payload(
    payload: Mapping[str, object],
    *,
    timeout_seconds: float = 10.0,
) -> N8NQueueResponse:
    """Submit a validated live review payload to n8n."""
    _validate_submission_payload(payload)
    webhook_url = os.getenv("N8N_REVIEW_WEBHOOK_URL")
    if not webhook_url or not webhook_url.strip():
        raise N8NConfigurationError(
            "N8N_REVIEW_WEBHOOK_URL is required to submit a review case."
        )

    request = Request(
        webhook_url,
        data=json.dumps(dict(payload), ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status = response.status
            body = _response_text(response)
    except HTTPError as error:
        raise N8NSubmissionError(f"n8n submission returned HTTP status {error.code}.") from error
    except (TimeoutError, URLError, OSError) as error:
        raise N8NSubmissionError("The n8n review-queue request failed.") from error

    if not 200 <= status < 300:
        raise N8NSubmissionError(f"n8n submission returned HTTP status {status}.")
    return _parse_queue_response(body)
