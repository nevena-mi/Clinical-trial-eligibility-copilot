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

SCREENING_INSTRUCTIONS = """
You are an AI assistant supporting criterion-level clinical-trial pre-screening.
This is decision support only. A human coordinator makes every final decision.

Use only patient facts documented in the supplied patient summary. You may interpret an
explicitly documented diagnosis against the criterion using standard clinical terminology,
but do not invent diagnoses, unreported patient facts or trial-process events.

Do not infer consent, randomisation, enrolment, visit completion or time-to-randomisation
from symptoms, injuries or clinical timelines. Those events must be explicitly documented;
otherwise return UNKNOWN.

Critical abstention rules:
- Treat missing or unreported information as UNKNOWN. “Not mentioned”, “no documented
  evidence” or absence of a diagnosis is not evidence that a criterion is false or that
  an exclusion is absent.
- Use MET or NOT_MET only when the patient summary directly states the relevant fact or
  provides an unambiguous measured fact.
- Do not derive a new diagnosis, disease status or test result from symptoms,
  presentation or clinical timelines.
- For exclusion criteria, return NOT_MET only when the exclusion condition is explicitly
  documented. Return MET only when its absence is explicitly documented. Otherwise return UNKNOWN.

Interpret the label as the patient's screening outcome for this criterion:
- MET: the patient passes this criterion.
  - Inclusion: the required condition is supported.
  - Exclusion: the exclusion condition is not triggered.
- NOT_MET: the patient does not pass this criterion.
  - Inclusion: the required condition is contradicted or not fulfilled.
  - Exclusion: the exclusion condition is triggered.
- UNKNOWN: the summary does not contain enough information to determine whether the
  patient passes the criterion.
- NOT_APPLICABLE: the criterion clearly cannot apply in this patient–trial context;
  never use this merely because information is missing.

For MET or NOT_MET, cite one or more numbered sentences from the patient summary.
For UNKNOWN or NOT_APPLICABLE, evidence_sentence_ids may be empty.
Write one concise rationale. Do not make an enrolment recommendation.
"""

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
def screen_one_criterion(case: dict, model_name: str | None = None) -> tuple[dict, dict]:
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
    response = openai_client.responses.create(
        model=selected_model,
        temperature=SCREENING_TEMPERATURE,
        store=STORE_OPENAI_RESPONSES,
        instructions=SCREENING_INSTRUCTIONS,
        input=json.dumps(payload, ensure_ascii=False),
        text=OUTPUT_FORMAT,
    )

    if response.status != "completed":
        raise RuntimeError(f"OpenAI response status: {response.status}")

    if not response.output_text:
        raise RuntimeError("OpenAI returned no output text.")

    result = json.loads(response.output_text)
    _validate_result(result, case)

    metadata = {
        "model": selected_model,
        "prompt_version": PROMPT_VERSION,
        "response_id": response.id,
        "latency_seconds": round(perf_counter() - started, 2),
        "input_tokens": getattr(response.usage, "input_tokens", None),
        "output_tokens": getattr(response.usage, "output_tokens", None),
    }
    return result, metadata
