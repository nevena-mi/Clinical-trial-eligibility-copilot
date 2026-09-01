import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.case_data import (
    build_screening_case,
    load_reference_assessments,
    validate_locked_assessments,
)
from src.config import (
    ConfigurationError,
    DEFAULT_SCREENING_MODEL,
    EXPECTED_EVALUATION_ROWS,
    PROCESSED_DIR,
    PROMPT_VERSION,
    PROJECT_ROOT,
    SCREENING_TEMPERATURE,
)
from src.model_config import ModelConfigurationError, get_model_configuration
from src.screening import screen_one_criterion


DEFAULT_OUTPUT_PATH = PROCESSED_DIR / "llm_predictions.csv"

RESULT_COLUMNS = [
    "source_annotation_id", "patient_id", "trial_id", "trial_title", "criterion_id",
    "criterion_type", "criterion_text", "ground_truth_label", "predicted_label",
    "evidence_sentence_ids", "rationale", "configuration_id", "reasoning_effort",
    "model", "prompt_version", "response_id",
    "latency_seconds", "input_tokens", "output_tokens", "run_timestamp", "status",
    "error_message",
]


def load_annotation_manifest(
    manifest_path: Path,
    assessments_df: pd.DataFrame,
) -> pd.DataFrame:
    """Load and validate a 15-row ordered annotation manifest."""
    manifest = pd.read_csv(manifest_path)
    required_columns = {"smoke_order", "source_annotation_id"}
    missing = required_columns.difference(manifest.columns)
    if missing:
        raise ValueError(f"Manifest is missing required columns: {sorted(missing)}")
    if len(manifest) != 15:
        raise ValueError(f"Manifest must contain exactly 15 rows; found {len(manifest)}.")
    for column in required_columns:
        numeric = pd.to_numeric(manifest[column], errors="coerce")
        if numeric.isna().any() or not numeric.eq(numeric.astype("int64")).all():
            raise ValueError(f"Manifest {column} values must be integers.")
        manifest[column] = numeric.astype("int64")
    if manifest["source_annotation_id"].duplicated().any():
        raise ValueError("Manifest source_annotation_id values must be unique.")
    if sorted(manifest["smoke_order"].tolist()) != list(range(1, 16)):
        raise ValueError("Manifest smoke_order values must be unique and contiguous from 1 to 15.")
    known_ids = set(assessments_df["source_annotation_id"])
    manifest_ids = set(manifest["source_annotation_id"])
    if not manifest_ids.issubset(known_ids):
        raise ValueError("Manifest contains unknown source_annotation_id values.")
    indexed = assessments_df.set_index("source_annotation_id")
    selected = indexed.loc[manifest.sort_values("smoke_order")["source_annotation_id"]].reset_index()
    for column in {"patient_id", "trial_id", "criterion_id", "criterion_type"}.intersection(manifest.columns):
        expected = manifest.sort_values("smoke_order")[column].tolist()
        if selected[column].tolist() != expected:
            raise ValueError(f"Manifest {column} values do not match reference assessments.")
    return selected

def save_results(records: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records, columns=RESULT_COLUMNS).to_csv(output_path, index=False)


def _validate_resume_metadata(
    existing_df: pd.DataFrame,
    *,
    model: str,
    prompt_version: str,
    configuration_id: str,
    reasoning_effort: str | None,
    explicit_configuration: bool,
) -> pd.DataFrame:
    missing_columns = set(RESULT_COLUMNS).difference(existing_df.columns)
    metadata_defaults = {"configuration_id": "legacy", "reasoning_effort": ""}
    if explicit_configuration:
        missing_metadata = missing_columns.intersection(metadata_defaults)
        if missing_metadata:
            raise ValueError(
                "Cannot resume an explicit configuration: output is missing "
                f"columns {sorted(missing_metadata)}."
            )
    unsupported_missing_columns = missing_columns.difference(metadata_defaults)
    if unsupported_missing_columns:
        raise ValueError(
            f"Cannot resume: output is missing columns {sorted(unsupported_missing_columns)}."
        )
    if not explicit_configuration:
        for column, default in metadata_defaults.items():
            if column not in existing_df:
                existing_df[column] = default

    successful_df = existing_df.loc[existing_df["status"].eq("success")]
    expected_metadata = {"model": model, "prompt_version": prompt_version}
    if explicit_configuration:
        expected_metadata.update({
            "configuration_id": configuration_id,
            "reasoning_effort": reasoning_effort,
        })
    for column, expected in expected_metadata.items():
        if not successful_df[column].eq(expected).all():
            raise ValueError(
                f"Cannot resume: successful rows have a {column} mismatch."
            )
    return existing_df


def run_screening(
    limit: int | None,
    output_path: Path,
    resume: bool,
    overwrite: bool,
    model_name: str,
    configuration_id: str | None = None,
    annotation_manifest_path: Path | None = None,
) -> None:
    if limit is not None and limit < 1:
        raise ValueError("--limit must be at least 1.")
    if resume and overwrite:
        raise ValueError("Use either --resume or --overwrite, not both.")
    if annotation_manifest_path is not None and limit is not None:
        raise ValueError("--limit cannot be used with --annotation-manifest.")

    output_path = (
        output_path if output_path.is_absolute() else PROJECT_ROOT / output_path
    ).resolve()
    if configuration_id:
        try:
            configuration = get_model_configuration(configuration_id)
        except ModelConfigurationError as error:
            raise ConfigurationError(str(error)) from error
        if configuration.prompt_version != PROMPT_VERSION:
            raise ConfigurationError(
                f"Configuration {configuration_id} requires prompt version "
                f"{configuration.prompt_version}; active PROMPT_VERSION is {PROMPT_VERSION}."
            )
        protected_path = (PROCESSED_DIR / "llm_predictions_gpt41_v2.csv").resolve()
        if output_path == protected_path:
            raise ValueError("Candidate configuration cannot overwrite the protected GPT-4.1 baseline file.")
        model_name = configuration.model
    else:
        configuration = None
    selected_prompt = configuration.prompt_version if configuration else PROMPT_VERSION
    selected_reasoning = configuration.reasoning_effort if configuration else None
    selected_configuration_id = configuration.configuration_id if configuration else "legacy"
    assessments_df = validate_locked_assessments(
        load_reference_assessments(PROCESSED_DIR),
        expected_rows=EXPECTED_EVALUATION_ROWS,
    )
    if annotation_manifest_path is not None:
        manifest_path = (
            annotation_manifest_path
            if annotation_manifest_path.is_absolute()
            else PROJECT_ROOT / annotation_manifest_path
        ).resolve()
        assessments_df = load_annotation_manifest(manifest_path, assessments_df)

    if output_path.exists() and not resume and not overwrite:
        raise FileExistsError(
            f"{output_path} already exists. Use --resume, --overwrite or another --output path."
        )

    records = []
    completed_ids = set()

    if resume and output_path.exists():
        existing_df = pd.read_csv(output_path)
        existing_df = _validate_resume_metadata(
            existing_df,
            model=model_name,
            prompt_version=selected_prompt,
            configuration_id=selected_configuration_id,
            reasoning_effort=selected_reasoning,
            explicit_configuration=configuration_id is not None,
        )
        if annotation_manifest_path is not None:
            manifest_ids = set(assessments_df["source_annotation_id"])
            existing_ids = set(existing_df["source_annotation_id"].dropna())
            if not existing_ids.issubset(manifest_ids):
                raise ValueError("Cannot resume: output contains rows outside the annotation manifest.")
            manifest_order = dict(
                zip(assessments_df["source_annotation_id"], range(len(assessments_df)))
            )
            existing_df = existing_df.assign(
                _manifest_order=existing_df["source_annotation_id"].map(manifest_order)
            ).sort_values("_manifest_order").drop(columns="_manifest_order")
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
        f"Model: {model_name} | Prompt: {selected_prompt} | "
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
            result, metadata = screen_one_criterion(
                build_screening_case(row),
                model_name=model_name,
                reasoning_effort=selected_reasoning,
                temperature=(
                    configuration.temperature
                    if configuration
                    else SCREENING_TEMPERATURE
                ),
                configuration_id=selected_configuration_id,
            )
            record = {
                **base_record,
                "predicted_label": result["predicted_label"],
                "evidence_sentence_ids": json.dumps(result["evidence_sentence_ids"]),
                "rationale": result["rationale"],
                "configuration_id": metadata["configuration_id"],
                "reasoning_effort": metadata["reasoning_effort"],
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
                "configuration_id": selected_configuration_id,
                "reasoning_effort": selected_reasoning,
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
    parser.add_argument("--output", type=Path, default=None, help="CSV output path.")
    parser.add_argument("--model", default=None, help="Model ID; overrides SCREENING_MODEL for this run.")
    parser.add_argument("--configuration-id", help="Registered model configuration ID for a reproducible run.")
    parser.add_argument("--annotation-manifest", type=Path, help="Ordered annotation manifest for selective execution.")
    parser.add_argument("--resume", action="store_true", help="Skip rows already saved with status=success.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    args = parser.parse_args()
    if args.configuration_id and args.model is not None:
        parser.error("Use either --model or --configuration-id, not both.")
    if args.annotation_manifest is not None and args.limit is not None:
        parser.error("--limit cannot be used with --annotation-manifest.")
    if args.configuration_id == "gpt56sol-medium-v2" and args.output is None:
        parser.error("--configuration-id gpt56sol-medium-v2 requires an explicit --output path.")
    if args.configuration_id and args.output is not None:
        resolved_output = (
            args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
        ).resolve()
        protected_path = (PROCESSED_DIR / "llm_predictions_gpt41_v2.csv").resolve()
        if resolved_output == protected_path:
            parser.error("The candidate configuration cannot overwrite the protected GPT-4.1 baseline file.")
    if args.output is None:
        args.output = DEFAULT_OUTPUT_PATH
    if args.model is None:
        args.model = DEFAULT_SCREENING_MODEL
    return args

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    args = parse_args()
    run_screening(
        args.limit,
        args.output,
        args.resume,
        args.overwrite,
        args.model,
        args.configuration_id,
        args.annotation_manifest,
    )
