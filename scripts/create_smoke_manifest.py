"""Create the deterministic model-comparison smoke-test manifest."""

import argparse
import json
from pathlib import Path

import pandas as pd

from src.case_data import load_reference_assessments, validate_locked_assessments
from src.config import EXPECTED_EVALUATION_ROWS, PROCESSED_DIR, PROJECT_ROOT


MANIFEST_COLUMNS = [
    "smoke_order", "source_annotation_id", "patient_id", "trial_id", "criterion_id",
    "criterion_type", "ground_truth_label", "baseline_predicted_label",
    "baseline_agreement", "baseline_safety_flag", "baseline_evidence_present",
    "selection_reason",
]
VALID_LABELS = {"MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"}
BASELINE_REQUIRED_COLUMNS = {
    "source_annotation_id", "patient_id", "trial_id", "criterion_id",
    "criterion_type", "ground_truth_label", "predicted_label",
    "evidence_sentence_ids", "status", "model", "prompt_version",
}
SMOKE_INPUT_COLUMNS = {
    "source_annotation_id", "patient_id", "trial_id", "criterion_id",
    "criterion_type", "ground_truth_label", "baseline_predicted_label",
    "baseline_agreement", "baseline_safety_flag", "baseline_evidence_present",
}
QUOTA_TARGETS = {
    "criterion_type=inclusion": 5,
    "criterion_type=exclusion": 5,
    "ground_truth=MET": 2,
    "ground_truth=NOT_MET": 2,
    "ground_truth=UNKNOWN": 2,
    "ground_truth=NOT_APPLICABLE": 2,
    "agreement=agreement": 4,
    "agreement=disagreement": 4,
    "outcome=review": 5,
    "outcome=no-routine-queue": 5,
    "evidence=present": 3,
    "evidence=absent": 3,
    "unique_patients": 12,
    "unique_trials": 12,
}
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "evaluation" / "model_comparison_smoke_manifest.csv"
DEFAULT_BASELINE_PATH = PROCESSED_DIR / "llm_predictions_gpt41_v2.csv"


def _require_columns(frame: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = columns.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required {name} columns: {sorted(missing)}")


def _validate_manifest_schema(manifest: pd.DataFrame) -> None:
    if not manifest.columns.is_unique:
        raise ValueError("Smoke manifest columns must be unique.")
    if any(str(column).endswith(".1") for column in manifest.columns):
        raise ValueError("Smoke manifest columns must not end with '.1'.")
    if list(manifest.columns) != MANIFEST_COLUMNS:
        raise ValueError(
            "Smoke manifest columns must exactly match the required order: "
            f"{MANIFEST_COLUMNS}"
        )


def _parse_evidence(value, annotation_id) -> list[int]:
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Invalid baseline evidence JSON for source_annotation_id {annotation_id}."
        ) from error
    if not isinstance(parsed, list) or any(
        isinstance(item, bool) or not isinstance(item, int) for item in parsed
    ):
        raise ValueError(
            f"Baseline evidence must be a JSON list of integers for source_annotation_id {annotation_id}."
        )
    return parsed


def validate_baseline(
    reference_df: pd.DataFrame,
    baseline_df: pd.DataFrame,
    expected_rows: int = EXPECTED_EVALUATION_ROWS,
) -> pd.DataFrame:
    """Validate and join the locked reference cohort to the GPT-4.1 baseline."""
    _require_columns(reference_df, {"source_annotation_id", "ground_truth_label"}, "reference")
    _require_columns(baseline_df, BASELINE_REQUIRED_COLUMNS, "baseline")
    if len(reference_df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} reference rows; found {len(reference_df)}.")
    if len(baseline_df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} baseline rows; found {len(baseline_df)}.")
    if baseline_df["source_annotation_id"].isna().any() or baseline_df["source_annotation_id"].duplicated().any():
        raise ValueError("Baseline source_annotation_id values must be present and unique.")
    if reference_df["source_annotation_id"].isna().any() or reference_df["source_annotation_id"].duplicated().any():
        raise ValueError("Reference source_annotation_id values must be present and unique.")
    if baseline_df[list(BASELINE_REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Baseline required values must not be missing.")
    for column in BASELINE_REQUIRED_COLUMNS:
        if baseline_df[column].map(lambda value: isinstance(value, str) and not value.strip()).any():
            raise ValueError(f"Baseline required values must not be blank in {column}.")
    if set(baseline_df["source_annotation_id"]) != set(reference_df["source_annotation_id"]):
        raise ValueError("Baseline annotation IDs must exactly match the locked reference cohort.")
    if not baseline_df["status"].eq("success").all():
        raise ValueError("Every baseline row must have status=success.")
    if not baseline_df["model"].eq("gpt-4.1").all():
        raise ValueError("Every baseline row must use model gpt-4.1.")
    if not baseline_df["prompt_version"].eq("v2_abstention_rules").all():
        raise ValueError("Every baseline row must use prompt version v2_abstention_rules.")
    if not baseline_df["predicted_label"].isin(VALID_LABELS).all():
        raise ValueError("Baseline predicted labels contain invalid values.")

    evidence_present = []
    for row in baseline_df.itertuples(index=False):
        evidence_present.append(bool(_parse_evidence(
            row.evidence_sentence_ids, row.source_annotation_id
        )))

    reference_labels = reference_df.set_index("source_annotation_id")["ground_truth_label"]
    mismatches = baseline_df.apply(
        lambda row: row.ground_truth_label != reference_labels[row.source_annotation_id],
        axis=1,
    )
    if mismatches.any():
        raise ValueError("Baseline ground-truth labels do not match the locked reference data.")

    joined = baseline_df.copy()
    joined["baseline_predicted_label"] = joined["predicted_label"]
    joined["baseline_evidence_present"] = evidence_present
    joined["baseline_agreement"] = joined["predicted_label"].eq(joined["ground_truth_label"])
    joined["baseline_safety_flag"] = (
        joined["ground_truth_label"].eq("NOT_MET") & joined["predicted_label"].eq("MET")
    )
    return joined


def _coverage_tags(row: pd.Series) -> set[str]:
    return {
        f"ground_truth={row.ground_truth_label}",
        f"criterion_type={row.criterion_type}",
        f"agreement={'agreement' if row.baseline_agreement else 'disagreement'}",
        f"outcome={'review' if row.baseline_predicted_label in {'UNKNOWN', 'NOT_APPLICABLE'} else 'no-routine-queue'}",
        f"evidence={'present' if row.baseline_evidence_present else 'absent'}",
    } | ({"unsafe"} if row.baseline_safety_flag else set())


def _quota_categories(
    row: pd.Series,
    counts: dict[str, int],
    selected_patients: set[object],
    selected_trials: set[object],
) -> set[str]:
    categories = {
        f"criterion_type={row.criterion_type}",
        f"ground_truth={row.ground_truth_label}",
        f"agreement={'agreement' if row.baseline_agreement else 'disagreement'}",
        f"outcome={'review' if row.baseline_predicted_label in {'UNKNOWN', 'NOT_APPLICABLE'} else 'no-routine-queue'}",
        f"evidence={'present' if row.baseline_evidence_present else 'absent'}",
    }
    applicable = {
        category for category in categories
        if counts.get(category, 0) < QUOTA_TARGETS[category]
    }
    if row.patient_id not in selected_patients and counts["unique_patients"] < QUOTA_TARGETS["unique_patients"]:
        applicable.add("unique_patients")
    if row.trial_id not in selected_trials and counts["unique_trials"] < QUOTA_TARGETS["unique_trials"]:
        applicable.add("unique_trials")
    return applicable


def _increment_quotas(
    row: pd.Series,
    counts: dict[str, int],
    selected_patients: set[object],
    selected_trials: set[object],
) -> None:
    for category in _quota_categories(row, counts, selected_patients, selected_trials):
        counts[category] += 1
    selected_patients.add(row.patient_id)
    selected_trials.add(row.trial_id)


def _unmet_quotas(counts: dict[str, int]) -> list[str]:
    return [
        f"{category}: {counts[category]}/{target}"
        for category, target in QUOTA_TARGETS.items()
        if counts[category] < target
    ]


def build_smoke_manifest(joined_df: pd.DataFrame, sample_size: int = 15) -> pd.DataFrame:
    """Select a deterministic, coverage-oriented smoke sample."""
    missing_columns = SMOKE_INPUT_COLUMNS.difference(joined_df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required smoke-selection columns: {sorted(missing_columns)}"
        )
    if sample_size != 15:
        raise ValueError("The smoke manifest must contain exactly 15 assessments.")
    working = joined_df.sort_values("source_annotation_id").reset_index(drop=True).copy()
    selected_ids: list[object] = []
    reasons: dict[object, str] = {}
    selected_patients: set[object] = set()
    selected_trials: set[object] = set()
    counts = {category: 0 for category in QUOTA_TARGETS}

    mandatory = working.loc[working["baseline_safety_flag"]]
    if len(mandatory) > sample_size:
        raise ValueError(
            f"Mandatory baseline unsafe cases ({len(mandatory)}) exceed the "
            f"{sample_size}-case smoke sample size."
        )
    for row in mandatory.itertuples(index=False):
        row_series = pd.Series(row._asdict())
        selected_ids.append(row.source_annotation_id)
        reasons[row.source_annotation_id] = "mandatory: baseline unsafe MET case"
        _increment_quotas(row_series, counts, selected_patients, selected_trials)

    while len(selected_ids) < sample_size and _unmet_quotas(counts):
        remaining = working.loc[~working["source_annotation_id"].isin(selected_ids)].copy()
        if remaining.empty:
            break
        remaining["uncovered_count"] = remaining.apply(
            lambda row: len(_quota_categories(row, counts, selected_patients, selected_trials)),
            axis=1,
        )
        remaining["new_patient"] = ~remaining["patient_id"].isin(selected_patients)
        remaining["new_trial"] = ~remaining["trial_id"].isin(selected_trials)
        candidate = remaining.sort_values(
            ["uncovered_count", "new_patient", "new_trial", "source_annotation_id"],
            ascending=[False, False, False, True],
        ).iloc[0]
        annotation_id = candidate["source_annotation_id"]
        new_categories = sorted(
            _quota_categories(candidate, counts, selected_patients, selected_trials)
        )
        diversity = []
        if bool(candidate["new_patient"]):
            diversity.append("new patient")
        if bool(candidate["new_trial"]):
            diversity.append("new trial")
        reasons[annotation_id] = "coverage: " + ", ".join(new_categories)
        if diversity:
            reasons[annotation_id] += "; diversity: " + ", ".join(diversity)
        selected_ids.append(annotation_id)
        _increment_quotas(candidate, counts, selected_patients, selected_trials)

    while len(selected_ids) < sample_size:
        remaining = working.loc[~working["source_annotation_id"].isin(selected_ids)].copy()
        if remaining.empty:
            break
        remaining["new_patient"] = ~remaining["patient_id"].isin(selected_patients)
        remaining["new_trial"] = ~remaining["trial_id"].isin(selected_trials)
        candidate = remaining.sort_values(
            ["new_patient", "new_trial", "source_annotation_id"],
            ascending=[False, False, True],
        ).iloc[0]
        annotation_id = candidate["source_annotation_id"]
        diversity = []
        if bool(candidate["new_patient"]):
            diversity.append("new patient")
        if bool(candidate["new_trial"]):
            diversity.append("new trial")
        reasons[annotation_id] = "fill: deterministic diversity selection"
        if diversity:
            reasons[annotation_id] += "; " + ", ".join(diversity)
        selected_ids.append(annotation_id)
        _increment_quotas(candidate, counts, selected_patients, selected_trials)

    unmet = _unmet_quotas(counts)
    if len(selected_ids) != sample_size or unmet:
        raise ValueError(
            "Unable to construct the required smoke sample; unmet quotas: "
            f"{unmet or ['sample_size: incomplete']}"
        )

    selected = working.set_index("source_annotation_id").loc[selected_ids].reset_index()
    selected.insert(0, "smoke_order", range(1, sample_size + 1))
    selected["selection_reason"] = selected["source_annotation_id"].map(reasons)
    manifest = selected[MANIFEST_COLUMNS]
    _validate_manifest_schema(manifest)
    return manifest


def create_manifest(
    data_dir: Path = PROCESSED_DIR,
    baseline_path: Path = DEFAULT_BASELINE_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    overwrite: bool = False,
) -> pd.DataFrame:
    output_path = Path(output_path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Manifest already exists: {output_path}. Use --overwrite to replace it.")
    reference_df = validate_locked_assessments(
        load_reference_assessments(data_dir), expected_rows=EXPECTED_EVALUATION_ROWS
    )
    baseline_df = pd.read_csv(baseline_path)
    manifest = build_smoke_manifest(validate_baseline(reference_df, baseline_df))
    _validate_manifest_schema(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(output_path, index=False)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create the deterministic comparison smoke manifest.")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    create_manifest(baseline_path=args.baseline, output_path=args.output, overwrite=args.overwrite)
    print(f"Created smoke manifest: {args.output}")
