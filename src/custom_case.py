"""Prepare synthetic custom cases without model or integration dependencies.

Sentence preparation is deliberately deterministic rather than linguistically complete.
Abbreviations, decimal points and prose without clear sentence boundaries may be split
less accurately than a clinical NLP sentence segmenter.
"""

import re


CASE_FIELDS = (
    "patient_id", "patient_summary", "trial_id", "trial_title",
    "criterion_id", "criterion_type", "criterion_text",
)
_NUMBERED_LINE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
_LEADING_NUMBER = re.compile(r"^\s*\d+[.)]\s*")
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+|\s*\n\s*")


def _clean_string(value, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must not be empty.")
    return cleaned


def _valid_numbered_lines(summary: str) -> list[str] | None:
    lines = [line for line in summary.splitlines() if line.strip()]
    matches = [_NUMBERED_LINE.fullmatch(line) for line in lines]
    if not lines or any(match is None for match in matches):
        return None
    sentence_ids = [int(match.group(1)) for match in matches if match is not None]
    if sentence_ids != list(range(len(sentence_ids))):
        return None
    return [match.group(2).strip() for match in matches if match is not None]


def number_patient_summary(patient_summary: str) -> str:
    """Return a zero-based, screening-compatible numbered patient summary."""
    summary = _clean_string(patient_summary, "patient_summary")
    numbered_lines = _valid_numbered_lines(summary)
    if numbered_lines is None:
        parts = [
            _LEADING_NUMBER.sub("", part).strip()
            for part in _SENTENCE_BOUNDARY.split(summary)
        ]
        sentences = [part for part in parts if part]
    else:
        sentences = numbered_lines
    if not sentences:
        raise ValueError("patient_summary must contain at least one sentence.")
    return "\n".join(f"{index}. {sentence}" for index, sentence in enumerate(sentences))


def prepare_custom_case(
    patient_summary: str,
    criterion_type: str,
    criterion_text: str,
    *,
    patient_id: str = "custom-patient",
    trial_id: str = "custom-trial",
    criterion_id: str = "custom-criterion",
    trial_title: str = "Synthetic custom trial",
) -> dict[str, str]:
    """Validate and build the model-ready case for a synthetic custom assessment."""
    cleaned_type = _clean_string(criterion_type, "criterion_type").lower()
    if cleaned_type not in {"inclusion", "exclusion"}:
        raise ValueError("criterion_type must be inclusion or exclusion.")

    cleaned_values = {
        "patient_id": _clean_string(patient_id, "patient_id"),
        "trial_id": _clean_string(trial_id, "trial_id"),
        "criterion_id": _clean_string(criterion_id, "criterion_id"),
        "trial_title": _clean_string(trial_title, "trial_title"),
        "criterion_text": _clean_string(criterion_text, "criterion_text"),
    }
    return {
        "patient_id": cleaned_values["patient_id"],
        "patient_summary": number_patient_summary(patient_summary),
        "trial_id": cleaned_values["trial_id"],
        "trial_title": cleaned_values["trial_title"],
        "criterion_id": cleaned_values["criterion_id"],
        "criterion_type": cleaned_type,
        "criterion_text": cleaned_values["criterion_text"],
    }
