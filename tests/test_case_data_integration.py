from pathlib import Path

from src.case_data import (
    filter_criterion_ids,
    filter_trial_ids,
    get_selected_assessment,
    list_patient_ids,
    load_reference_assessments,
    validate_locked_assessments,
)


def test_repository_processed_dataset_is_a_valid_locked_cohort():
    data_dir = Path(__file__).resolve().parents[1] / "data" / "processed"
    assessments = validate_locked_assessments(
        load_reference_assessments(data_dir), expected_rows=120
    )

    patient_id = list_patient_ids(assessments)[0]
    trial_id = filter_trial_ids(assessments, patient_id)[0]
    criterion_id = filter_criterion_ids(assessments, patient_id, trial_id)[0]
    selected = get_selected_assessment(assessments, patient_id, trial_id, criterion_id)

    assert selected["patient_id"] == patient_id
    assert selected["trial_id"] == trial_id
    assert selected["criterion_id"] == criterion_id
