import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.config import (
    DEFAULT_SCREENING_MODEL,
    EXPECTED_EVALUATION_ROWS,
    PROCESSED_DIR,
    PROMPT_VERSION,
    PROJECT_ROOT,
)
from src.screening import screen_one_criterion


GROUND_TRUTH_PATH = PROCESSED_DIR / "ground_truth.csv"
PATIENTS_PATH = PROCESSED_DIR / "patients.csv"
CRITERIA_PATH = PROCESSED_DIR / "trial_criteria.csv"
DEFAULT_OUTPUT_PATH = PROCESSED_DIR / "llm_predictions.csv"

RESULT_COLUMNS = [
    "source_annotation_id", "patient_id", "trial_id", "trial_title", "criterion_id",
    "criterion_type", "criterion_text", "ground_truth_label", "predicted_label",
    "evidence_sentence_ids", "rationale", "model", "prompt_version", "response_id",
    "latency_seconds", "input_tokens", "output_tokens", "run_timestamp", "status",
    "error_message",
]

def load_assessments() -> pd.DataFrame:
    ground_truth_df = pd.read_csv(GROUND_TRUTH_PATH)
    patients_df = pd.read_csv(PATIENTS_PATH)
    criteria_df = pd.read_csv(CRITERIA_PATH)

    assessments_df = ground_truth_df.merge(
        patients_df, on="patient_id", how="left", validate="many_to_one"
    ).merge(
        criteria_df,
        on=["criterion_id", "trial_id", "criterion_type"],
        how="left",
        validate="many_to_one",
    )

    required_columns = [
        "source_annotation_id", "patient_id", "patient_summary", "trial_id",
        "trial_title", "criterion_id", "criterion_type", "criterion_text",
        "ground_truth_label",
    ]
    missing_columns = set(required_columns).difference(assessments_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if len(assessments_df) != EXPECTED_EVALUATION_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_EVALUATION_ROWS} locked assessments; found {len(assessments_df)}."
        )
    if assessments_df[required_columns].isna().any().any():
        raise ValueError("One or more required assessment values are missing.")
    if assessments_df["source_annotation_id"].duplicated().any():
        raise ValueError("source_annotation_id must be unique.")

    return assessments_df.sort_values("source_annotation_id").reset_index(drop=True)

def build_case(row: pd.Series) -> dict:
    return {
        "patient_id": row["patient_id"],
        "patient_summary": row["patient_summary"],
        "trial_id": row["trial_id"],
        "trial_title": row["trial_title"],
        "criterion_id": row["criterion_id"],
        "criterion_type": row["criterion_type"],
        "criterion_text": row["criterion_text"],
    }

def save_results(records: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records, columns=RESULT_COLUMNS).to_csv(output_path, index=False)

def run_screening(
    limit: int | None,
    output_path: Path,
    resume: bool,
    overwrite: bool,
    model_name: str,
) -> None:
    if limit is not None and limit < 1:
        raise ValueError("--limit must be at least 1.")
    if resume and overwrite:
        raise ValueError("Use either --resume or --overwrite, not both.")

    output_path = output_path if output_path.is_absolute() else PROJECT_ROOT / output_path
    assessments_df = load_assessments()

    if output_path.exists() and not resume and not overwrite:
        raise FileExistsError(
            f"{output_path} already exists. Use --resume, --overwrite or another --output path."
        )

    records = []
    completed_ids = set()

    if resume and output_path.exists():
        existing_df = pd.read_csv(output_path)
        missing_columns = set(RESULT_COLUMNS).difference(existing_df.columns)
        if missing_columns:
            raise ValueError(f"Cannot resume: output is missing columns {sorted(missing_columns)}.")
        records = existing_df.to_dict("records")
        completed_ids = set(
            existing_df.loc[existing_df["status"].eq("success"), "source_annotation_id"]
            .dropna()
            .astype(int)
        )
        print(f"Resuming: skipping {len(completed_ids)} successful assessment(s).")

    pending_df = assessments_df.loc[
        ~assessments_df["source_annotation_id"].isin(completed_ids)
    ].copy()

    if limit is not None:
        pending_df = pending_df.head(limit)

    print(
        f"Model: {model_name} | Prompt: {PROMPT_VERSION} | "
        f"Running: {len(pending_df)} assessment(s) | Output: {output_path}"
    )

    for position, (_, row) in enumerate(pending_df.iterrows(), start=1):
        base_record = {
            "source_annotation_id": row["source_annotation_id"],
            "patient_id": row["patient_id"],
            "trial_id": row["trial_id"],
            "trial_title": row["trial_title"],
            "criterion_id": row["criterion_id"],
            "criterion_type": row["criterion_type"],
            "criterion_text": row["criterion_text"],
            "ground_truth_label": row["ground_truth_label"],
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            result, metadata = screen_one_criterion(build_case(row), model_name=model_name)
            record = {
                **base_record,
                "predicted_label": result["predicted_label"],
                "evidence_sentence_ids": json.dumps(result["evidence_sentence_ids"]),
                "rationale": result["rationale"],
                "model": metadata["model"],
                "prompt_version": metadata["prompt_version"],
                "response_id": metadata["response_id"],
                "latency_seconds": metadata["latency_seconds"],
                "input_tokens": metadata["input_tokens"],
                "output_tokens": metadata["output_tokens"],
                "status": "success",
                "error_message": "",
            }
            print(f"[{position}/{len(pending_df)}] {row['criterion_id']}: {result['predicted_label']}")
        except Exception as error:
            record = {
                **base_record,
                "predicted_label": "",
                "evidence_sentence_ids": "[]",
                "rationale": "",
                "model": model_name,
                "prompt_version": PROMPT_VERSION,
                "response_id": "",
                "latency_seconds": None,
                "input_tokens": None,
                "output_tokens": None,
                "status": "error",
                "error_message": f"{type(error).__name__}: {error}",
            }
            print(f"[{position}/{len(pending_df)}] {row['criterion_id']}: ERROR — {record['error_message']}")

        records.append(record)
        save_results(records, output_path)

    results_df = pd.DataFrame(records, columns=RESULT_COLUMNS)
    successful_runs = results_df["status"].eq("success").sum()
    failed_runs = results_df["status"].eq("error").sum()
    print(f"\nFinished. Successful: {successful_runs} | Errors: {failed_runs} | Saved: {output_path}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run screening across the locked evaluation cohort.")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of pending assessments to run.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="CSV output path.")
    parser.add_argument("--model", default=DEFAULT_SCREENING_MODEL, help="Model ID; overrides SCREENING_MODEL for this run.")
    parser.add_argument("--resume", action="store_true", help="Skip rows already saved with status=success.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    return parser.parse_args()

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    args = parse_args()
    run_screening(args.limit, args.output, args.resume, args.overwrite, args.model)