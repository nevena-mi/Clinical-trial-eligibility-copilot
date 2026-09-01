import pandas as pd
import pytest

from src.case_data import (
    build_screening_case,
    filter_criterion_ids,
    filter_trial_ids,
    get_selected_assessment,
    list_patient_ids,
    load_reference_assessments,
    load_reference_tables,
    validate_locked_assessments,
)


def _write_fixture(data_dir, *, patients=None, criteria=None, assessments=None):
    patients = patients or [
        {"patient_id": "P2", "patient_summary": "0. Second patient."},
        {"patient_id": "P1", "patient_summary": "0. First patient."},
    ]
    criteria = criteria or [
        {
            "criterion_id": "C2", "trial_id": "T1", "trial_title": "Trial one",
            "criterion_type": "exclusion", "criterion_text": "Criterion two",
        },
        {
            "criterion_id": "C1", "trial_id": "T1", "trial_title": "Trial one",
            "criterion_type": "inclusion", "criterion_text": "Criterion one",
        },
    ]
    assessments = assessments or [
        {
            "source_annotation_id": 2, "patient_id": "P1", "trial_id": "T1",
            "criterion_id": "C2", "criterion_type": "exclusion", "ground_truth_label": "UNKNOWN",
        },
        {
            "source_annotation_id": 1, "patient_id": "P1", "trial_id": "T1",
            "criterion_id": "C1", "criterion_type": "inclusion", "ground_truth_label": "MET",
        },
    ]
    pd.DataFrame(patients).to_csv(data_dir / "patients.csv", index=False)
    pd.DataFrame(criteria).to_csv(data_dir / "trial_criteria.csv", index=False)
    pd.DataFrame(assessments).to_csv(data_dir / "ground_truth.csv", index=False)


def test_load_and_select_case_data(tmp_path):
    _write_fixture(tmp_path)

    assessments = load_reference_assessments(tmp_path)

    assert list_patient_ids(assessments) == ["P1"]
    assert filter_trial_ids(assessments, "P1") == ["T1"]
    assert filter_criterion_ids(assessments, "P1", "T1") == ["C1", "C2"]
    selected = get_selected_assessment(assessments, "P1", "T1", "C1")
    assert build_screening_case(selected) == {
        "patient_id": "P1",
        "patient_summary": "0. First patient.",
        "trial_id": "T1",
        "trial_title": "Trial one",
        "criterion_id": "C1",
        "criterion_type": "inclusion",
        "criterion_text": "Criterion one",
    }


@pytest.mark.parametrize(
    ("filename", "column"),
    [("patients.csv", "patient_summary"), ("trial_criteria.csv", "criterion_text"), ("ground_truth.csv", "ground_truth_label")],
)
def test_missing_required_column_fails(tmp_path, filename, column):
    _write_fixture(tmp_path)
    frame = pd.read_csv(tmp_path / filename).drop(columns=column)
    frame.to_csv(tmp_path / filename, index=False)

    with pytest.raises(ValueError, match="Missing required"):
        load_reference_tables(tmp_path)


def test_missing_required_value_fails(tmp_path):
    _write_fixture(tmp_path)
    frame = pd.read_csv(tmp_path / "patients.csv")
    frame.loc[0, "patient_summary"] = pd.NA
    frame.to_csv(tmp_path / "patients.csv", index=False)

    with pytest.raises(ValueError, match="required patient values"):
        load_reference_tables(tmp_path)


def test_duplicate_trial_criteria_composite_key_fails(tmp_path):
    _write_fixture(tmp_path, criteria=[
        {
            "criterion_id": "C1", "trial_id": "T1", "trial_title": "Trial one",
            "criterion_type": "inclusion", "criterion_text": "One",
        },
        {
            "criterion_id": "C1", "trial_id": "T1", "trial_title": "Trial one",
            "criterion_type": "inclusion", "criterion_text": "Duplicate",
        },
    ])

    with pytest.raises(ValueError, match="trial-criteria records"):
        load_reference_tables(tmp_path)


@pytest.mark.parametrize("duplicate_column", ["source_annotation_id", "patient-trial-criterion"])
def test_duplicate_assessment_key_fails(tmp_path, duplicate_column):
    _write_fixture(tmp_path)
    assessments = pd.read_csv(tmp_path / "ground_truth.csv")
    if duplicate_column == "source_annotation_id":
        assessments.loc[1, "source_annotation_id"] = assessments.loc[0, "source_annotation_id"]
    else:
        assessments.loc[1, ["patient_id", "trial_id", "criterion_id", "criterion_type"]] = assessments.loc[0, ["patient_id", "trial_id", "criterion_id", "criterion_type"]].values
    assessments.to_csv(tmp_path / "ground_truth.csv", index=False)

    with pytest.raises(ValueError, match="assessments"):
        load_reference_tables(tmp_path)


def test_missing_linked_record_fails(tmp_path):
    _write_fixture(tmp_path)
    criteria = pd.read_csv(tmp_path / "trial_criteria.csv").iloc[[0]]
    criteria.to_csv(tmp_path / "trial_criteria.csv", index=False)

    with pytest.raises(ValueError, match="trial-criteria records missing"):
        load_reference_tables(tmp_path)


def test_selection_requires_exactly_one_row():
    assessments = pd.DataFrame([
        {"patient_id": "P1", "trial_id": "T1", "criterion_id": "C1"},
        {"patient_id": "P1", "trial_id": "T1", "criterion_id": "C1"},
    ])

    with pytest.raises(ValueError, match="found 2"):
        get_selected_assessment(assessments, "P1", "T1", "C1")
    with pytest.raises(ValueError, match="found 0"):
        get_selected_assessment(assessments.iloc[:1], "P9", "T1", "C1")


def test_locked_validation_requires_explicit_expected_row_count(tmp_path):
    _write_fixture(tmp_path)
    assessments = load_reference_assessments(tmp_path)

    with pytest.raises(ValueError, match="Expected 3"):
        validate_locked_assessments(assessments, expected_rows=3)
