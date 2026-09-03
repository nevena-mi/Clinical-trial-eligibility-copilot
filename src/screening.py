import json
import re
from time import perf_counter

from src.config import (
    DEFAULT_SCREENING_MODEL,
    PROMPT_VERSION,
    SCREENING_TEMPERATURE,
    STORE_OPENAI_RESPONSES,
    get_openai_client,
)
from langsmith import traceable

from src.prompts import get_screening_instructions



OUTPUT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "criterion_screening_result",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "criterion_id": {"type": "string"},
                "predicted_label": {
                    "type": "string",
                    "enum": ["MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"],
                },
                "evidence_sentence_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                },
                "rationale": {"type": "string"},
            },
            "required": ["criterion_id", "predicted_label", "evidence_sentence_ids", "rationale"],
            "additionalProperties": False,
        },
    }
}

def _validate_result(result: dict, case: dict) -> None:
    valid_labels = {"MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"}
    valid_sentence_ids = {
        int(sentence_id)
        for sentence_id in re.findall(r"(?m)^\s*(\d+)\.", case["patient_summary"])
    }

    if result["criterion_id"] != case["criterion_id"]:
        raise ValueError("Returned criterion_id does not match the input criterion_id.")
    if result["predicted_label"] not in valid_labels:
        raise ValueError("Returned an invalid eligibility label.")
    if not isinstance(result["evidence_sentence_ids"], list):
        raise ValueError("evidence_sentence_ids must be a list.")
    if not set(result["evidence_sentence_ids"]).issubset(valid_sentence_ids):
        raise ValueError("Returned evidence references a sentence not present in the patient summary.")
    if result["predicted_label"] in {"MET", "NOT_MET"} and not result["evidence_sentence_ids"]:
        raise ValueError("MET and NOT_MET outputs require evidence from the patient summary.")
    if not result["rationale"].strip():
        raise ValueError("Returned rationale is empty.")

@traceable(name="criterion_level_screening", run_type="chain")
def screen_one_criterion(
    case: dict,
    model_name: str | None = None,
    *,
    reasoning_effort: str | None = None,
    temperature: float | None = SCREENING_TEMPERATURE,
    configuration_id: str | None = None,
    prompt_version: str = PROMPT_VERSION,
) -> tuple[dict, dict]:
    required_fields = {
        "patient_id", "patient_summary", "trial_id", "trial_title",
        "criterion_id", "criterion_type", "criterion_text",
    }
    missing_fields = required_fields.difference(case)
    if missing_fields:
        raise ValueError(f"Missing required input fields: {sorted(missing_fields)}")

    selected_model = model_name or DEFAULT_SCREENING_MODEL
    payload = {field: case[field] for field in required_fields}

    openai_client = get_openai_client()
    started = perf_counter()
    request_kwargs = {
        "model": selected_model,
        "store": STORE_OPENAI_RESPONSES,
        "instructions": get_screening_instructions(prompt_version),
        "input": json.dumps(payload, ensure_ascii=False),
        "text": OUTPUT_FORMAT,
    }
    if temperature is not None:
        request_kwargs["temperature"] = temperature
    if reasoning_effort is not None:
        request_kwargs["reasoning"] = {"effort": reasoning_effort}

    response = openai_client.responses.create(**request_kwargs)

    if response.status != "completed":
        raise RuntimeError(f"OpenAI response status: {response.status}")

    if not response.output_text:
        raise RuntimeError("OpenAI returned no output text.")

    result = json.loads(response.output_text)
    _validate_result(result, case)

    metadata = {
        "model": selected_model,
        "prompt_version": prompt_version,
        "configuration_id": configuration_id,
        "reasoning_effort": reasoning_effort,
        "response_id": response.id,
        "latency_seconds": round(perf_counter() - started, 2),
        "input_tokens": getattr(response.usage, "input_tokens", None),
        "output_tokens": getattr(response.usage, "output_tokens", None),
    }
    return result, metadata
