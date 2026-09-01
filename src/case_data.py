"""Pure loading and selection helpers for synthetic screening cases."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


PATIENT_COLUMNS = {"patient_id", "patient_summary"}
CRITERION_COLUMNS = {
    "criterion_id", "trial_id", "trial_title", "criterion_type", "criterion_text",
}
GROUND_TRUTH_COLUMNS = {
    "source_annotation_id", "patient_id", "trial_id", "criterion_id",
    "criterion_type", "ground_truth_label",
}
CASE_COLUMNS = [
    "patient_id", "patient_summary", "trial_id", "trial_title", "criterion_id",
    "criterion_type", "criterion_text",
]
CRITERION_KEY = ["trial_id", "criterion_id", "criterion_type"]
ASSESSMENT_KEY = ["patient_id", "trial_id", "criterion_id", "criterion_type"]


@dataclass(frozen=True)
class ReferenceTables:
    patients: pd.DataFrame
    trial_criteria: pd.DataFrame
    ground_truth: pd.DataFrame


def _require_columns(frame: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required {name} columns: {sorted(missing)}")


def _require_values(frame: pd.DataFrame, columns: list[str], name: str) -> None:
    if frame[columns].isna().any().any():
        raise ValueError(f"One or more required {name} values are missing.")
    for column in columns:
        if frame[column].map(lambda value: isinstance(value, str) and not value.strip()).any():
            raise ValueError(f"One or more required {name} values are empty in {column}.")


def _require_unique(frame: pd.DataFrame, columns: list[str], name: str) -> None:
    if frame.duplicated(columns).any():
        raise ValueError(f"{name} must be unique on {columns}.")


def load_reference_tables(data_dir: Path) -> ReferenceTables:
    """Load and structurally validate the three reference CSV files."""
    data_dir = Path(data_dir)
    patients = pd.read_csv(data_dir / "patients.csv")
    trial_criteria = pd.read_csv(data_dir / "trial_criteria.csv")
    ground_truth = pd.read_csv(data_dir / "ground_truth.csv")

    _require_columns(patients, PATIENT_COLUMNS, "patient")
    _require_columns(trial_criteria, CRITERION_COLUMNS, "trial-criteria")
    _require_columns(ground_truth, GROUND_TRUTH_COLUMNS, "ground-truth")
    _require_values(patients, ["patient_id", "patient_summary"], "patient")
    _require_values(
        trial_criteria,
        ["criterion_id", "trial_id", "trial_title", "criterion_type", "criterion_text"],
        "trial-criteria",
    )
    _require_values(
        ground_truth,
        [
            "source_annotation_id", "patient_id", "trial_id", "criterion_id",
            "criterion_type", "ground_truth_label",
        ],
        "ground-truth",
    )

    _require_unique(patients, ["patient_id"], "patient records")
    _require_unique(trial_criteria, CRITERION_KEY, "trial-criteria records")
    _require_unique(ground_truth, ["source_annotation_id"], "assessments by source_annotation_id")
    _require_unique(ground_truth, ASSESSMENT_KEY, "assessments by patient-trial-criterion")

    if not trial_criteria["criterion_type"].isin({"inclusion", "exclusion"}).all():
        raise ValueError("criterion_type must be inclusion or exclusion.")
    if not ground_truth["ground_truth_label"].isin(
        {"MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"}
    ).all():
        raise ValueError("ground_truth_label contains an invalid value.")

    if not set(ground_truth["patient_id"]).issubset(set(patients["patient_id"])):
        raise ValueError("Assessments reference patient IDs missing from patients.csv.")
    criterion_keys = set(map(tuple, trial_criteria[CRITERION_KEY].to_numpy()))
    assessment_keys = set(map(tuple, ground_truth[CRITERION_KEY].to_numpy()))
    if not assessment_keys.issubset(criterion_keys):
        raise ValueError(
            "Assessments reference trial-criteria records missing from trial_criteria.csv."
        )

    return ReferenceTables(patients, trial_criteria, ground_truth)


def load_reference_assessments(data_dir: Path) -> pd.DataFrame:
    """Return structurally validated assessments joined to reference data."""
    tables = load_reference_tables(data_dir)
    assessments = tables.ground_truth.merge(
        tables.patients, on="patient_id", how="left", validate="many_to_one"
    ).merge(
        tables.trial_criteria, on=CRITERION_KEY, how="left", validate="many_to_one"
    )
    _require_values(
        assessments,
        [
            "source_annotation_id", "patient_id", "patient_summary", "trial_id",
            "trial_title", "criterion_id", "criterion_type", "criterion_text",
            "ground_truth_label",
        ],
        "assessment",
    )
    return assessments.sort_values("source_annotation_id").reset_index(drop=True)


def validate_locked_assessments(
    assessments_df: pd.DataFrame,
    expected_rows: int,
) -> pd.DataFrame:
    """Validate evaluation-cohort completeness after structural loading."""
    if len(assessments_df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} locked assessments; found {len(assessments_df)}.")
    _require_unique(assessments_df, ["source_annotation_id"], "locked assessments")
    patient_counts = assessments_df.groupby("patient_id").size()
    if len(patient_counts) != 30 or not patient_counts.eq(4).all():
        raise ValueError("Locked assessments must contain 30 patients with four assessments each.")
    return assessments_df


def build_screening_case(assessment_row: pd.Series) -> dict[str, str]:
    _require_values(pd.DataFrame([assessment_row]), CASE_COLUMNS, "screening case")
    return {column: assessment_row[column] for column in CASE_COLUMNS}


def list_patient_ids(assessments_df: pd.DataFrame) -> list[str]:
    return sorted(assessments_df["patient_id"].drop_duplicates().tolist())


def filter_trial_ids(assessments_df: pd.DataFrame, patient_id: str) -> list[str]:
    selected = assessments_df.loc[assessments_df["patient_id"].eq(patient_id), "trial_id"]
    return sorted(selected.drop_duplicates().tolist())


def filter_criterion_ids(
    assessments_df: pd.DataFrame,
    patient_id: str,
    trial_id: str,
) -> list[str]:
    selected = assessments_df.loc[
        assessments_df["patient_id"].eq(patient_id)
        & assessments_df["trial_id"].eq(trial_id),
        "criterion_id",
    ]
    return sorted(selected.drop_duplicates().tolist())


def get_selected_assessment(
    assessments_df: pd.DataFrame,
    patient_id: str,
    trial_id: str,
    criterion_id: str,
) -> pd.Series:
    selected = assessments_df.loc[
        assessments_df["patient_id"].eq(patient_id)
        & assessments_df["trial_id"].eq(trial_id)
        & assessments_df["criterion_id"].eq(criterion_id)
    ]
    if len(selected) != 1:
        raise ValueError(
            "Expected exactly one assessment for "
            f"patient={patient_id}, trial={trial_id}, criterion={criterion_id}; found {len(selected)}."
        )
    return selected.iloc[0]
