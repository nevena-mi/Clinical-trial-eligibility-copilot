import argparse
import json
import re
from pathlib import Path

import pandas as pd

from src.case_data import load_reference_assessments
from src.config import (
    DEFAULT_SCREENING_MODEL,
    EXPECTED_EVALUATION_ROWS,
    PROCESSED_DIR,
    PROMPT_VERSION,
    PROJECT_ROOT,
)

VALID_LABELS = {"MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"}
VALID_STATUSES = {"success", "error"}

REQUIRED_PREDICTION_COLUMNS = {
    "source_annotation_id", "patient_id", "trial_id", "trial_title", "criterion_id",
    "criterion_type", "criterion_text", "ground_truth_label", "predicted_label",
    "evidence_sentence_ids", "rationale", "model", "prompt_version", "response_id",
    "latency_seconds", "input_tokens", "output_tokens", "run_timestamp", "status",
    "error_message",
}

def _sentence_ids(note: str) -> set[int]:
    return {int(value) for value in re.findall(r"(?m)^\s*(\d+)\.", note)}

def _parse_evidence_ids(value) -> list[int]:
    parsed = json.loads(value)
    if not isinstance(parsed, list) or not all(isinstance(item, int) for item in parsed):
        raise ValueError("evidence_sentence_ids must be a JSON list of integers.")
    return parsed

def validate_predictions(
    predictions_path: Path,
    expected_model: str,
    expected_configuration_id: str | None = None,
    expected_reasoning_effort: str | None = None,
) -> dict:
    predictions_path = predictions_path if predictions_path.is_absolute() else PROJECT_ROOT / predictions_path
    predictions_df = pd.read_csv(predictions_path)
    reference_df = load_reference_assessments(PROCESSED_DIR)

    errors = []
    checks = {}

    missing_columns = REQUIRED_PREDICTION_COLUMNS.difference(predictions_df.columns)
    checks["required_columns"] = not missing_columns
    if missing_columns:
        errors.append(f"Missing prediction columns: {sorted(missing_columns)}")

    checks["expected_row_count"] = len(predictions_df) == EXPECTED_EVALUATION_ROWS
    if not checks["expected_row_count"]:
        errors.append(f"Expected {EXPECTED_EVALUATION_ROWS} prediction rows; found {len(predictions_df)}.")

    checks["unique_source_annotation_id"] = not predictions_df["source_annotation_id"].duplicated().any()
    if not checks["unique_source_annotation_id"]:
        errors.append("source_annotation_id contains duplicates.")

    checks["valid_statuses"] = predictions_df["status"].isin(VALID_STATUSES).all()
    if not checks["valid_statuses"]:
        errors.append("Invalid status value found.")

    checks["all_successful"] = predictions_df["status"].eq("success").all()
    if not checks["all_successful"]:
        failed_count = (~predictions_df["status"].eq("success")).sum()
        errors.append(f"{failed_count} row(s) did not complete successfully.")

    success_df = predictions_df.loc[predictions_df["status"].eq("success")].copy()

    checks["valid_labels"] = success_df["predicted_label"].isin(VALID_LABELS).all()
    if not checks["valid_labels"]:
        errors.append("One or more successful rows contain an invalid predicted label.")

    required_success_fields = ["predicted_label", "rationale", "model", "prompt_version", "response_id", "run_timestamp"]
    missing_success_values = success_df[required_success_fields].isna().any().any()
    checks["complete_success_fields"] = not missing_success_values
    if missing_success_values:
        errors.append("One or more successful rows have missing required output values.")

    checks["model_consistency"] = success_df["model"].eq(expected_model).all()
    if not checks["model_consistency"]:
        found_models = sorted(success_df["model"].dropna().unique().tolist())
        errors.append(f"Expected model {expected_model}; found {found_models}.")

    if expected_configuration_id is not None:
        checks["configuration_consistency"] = (
            "configuration_id" in success_df
            and success_df["configuration_id"].eq(expected_configuration_id).all()
        )
        if not checks["configuration_consistency"]:
            errors.append(f"Expected configuration {expected_configuration_id}.")

    if expected_reasoning_effort is not None:
        checks["reasoning_consistency"] = (
            "reasoning_effort" in success_df
            and success_df["reasoning_effort"].eq(expected_reasoning_effort).all()
        )
        if not checks["reasoning_consistency"]:
            errors.append(f"Expected reasoning effort {expected_reasoning_effort}.")

    checks["prompt_consistency"] = success_df["prompt_version"].eq(PROMPT_VERSION).all()
    if not checks["prompt_consistency"]:
        found_prompts = sorted(success_df["prompt_version"].dropna().unique().tolist())
        errors.append(f"Expected prompt version {PROMPT_VERSION}; found {found_prompts}.")

    reference_ids = set(reference_df["source_annotation_id"])
    prediction_ids = set(predictions_df["source_annotation_id"])
    missing_reference_ids = reference_ids.difference(prediction_ids)
    unexpected_prediction_ids = prediction_ids.difference(reference_ids)
    checks["reference_coverage"] = not missing_reference_ids and not unexpected_prediction_ids
    if missing_reference_ids:
        errors.append(f"Missing reference IDs: {sorted(missing_reference_ids)}")
    if unexpected_prediction_ids:
        errors.append(f"Unexpected prediction IDs: {sorted(unexpected_prediction_ids)}")

    comparison_columns = [
        "source_annotation_id", "patient_id", "trial_id", "criterion_id",
        "criterion_type", "ground_truth_label",
    ]
    comparison_df = predictions_df[comparison_columns].merge(
        reference_df[comparison_columns],
        on="source_annotation_id",
        how="left",
        suffixes=("_prediction", "_reference"),
        validate="one_to_one",
    )

    mismatched_fields = []
    for column in comparison_columns[1:]:
        mismatch = comparison_df[f"{column}_prediction"].ne(comparison_df[f"{column}_reference"])
        if mismatch.any():
            mismatched_fields.append(column)

    checks["reference_field_consistency"] = not mismatched_fields
    if mismatched_fields:
        errors.append(f"Prediction fields do not match locked reference data: {mismatched_fields}")

    evidence_errors = []
    reference_notes = reference_df.set_index("source_annotation_id")["patient_summary"].to_dict()

    for row in success_df.itertuples(index=False):
        try:
            evidence_ids = _parse_evidence_ids(row.evidence_sentence_ids)
            note_sentence_ids = _sentence_ids(reference_notes[row.source_annotation_id])

            if not set(evidence_ids).issubset(note_sentence_ids):
                evidence_errors.append(f"{row.source_annotation_id}: invalid evidence sentence ID.")
            if row.predicted_label in {"MET", "NOT_MET"} and not evidence_ids:
                evidence_errors.append(f"{row.source_annotation_id}: {row.predicted_label} has no evidence ID.")
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            evidence_errors.append(f"{row.source_annotation_id}: {error}")

    checks["evidence_structure_and_ids"] = not evidence_errors
    errors.extend(evidence_errors)

    checks["non_negative_latency"] = success_df["latency_seconds"].ge(0).all()
    if not checks["non_negative_latency"]:
        errors.append("One or more latency values are negative or missing.")

    checks["non_negative_tokens"] = (
        success_df["input_tokens"].ge(0).all() and success_df["output_tokens"].ge(0).all()
    )
    if not checks["non_negative_tokens"]:
        errors.append("One or more token values are negative or missing.")

    return {
        "valid": not errors,
        "prediction_file": str(predictions_path),
        "rows": len(predictions_df),
        "successful_rows": len(success_df),
        "errors": errors,
        "checks": checks,
    }

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate saved LLM screening predictions.")
    parser.add_argument("--predictions", type=Path, required=True, help="Predictions CSV to validate.")
    parser.add_argument("--model", default=DEFAULT_SCREENING_MODEL, help="Expected model ID.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    report = validate_predictions(args.predictions, args.model)

    print("\nValidation report")
    print(f"Valid: {report['valid']}")
    print(f"Rows: {report['rows']} | Successful: {report['successful_rows']}")

    for check_name, passed in report["checks"].items():
        print(f"{'PASS' if passed else 'FAIL'} — {check_name}")

    if report["errors"]:
        print("\nErrors")
        for error in report["errors"]:
            print(f"- {error}")
        raise SystemExit(1)
