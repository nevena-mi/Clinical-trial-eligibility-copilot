import pytest

from src.custom_case import number_patient_summary, prepare_custom_case


def test_numbers_unnumbered_summary_from_zero():
    assert number_patient_summary("First sentence. Second sentence!") == (
        "0. First sentence.\n1. Second sentence!"
    )


def test_preserves_valid_zero_based_numbering_and_trims_text():
    assert number_patient_summary("  0. First sentence.  \n1. Second sentence. ") == (
        "0. First sentence.\n1. Second sentence."
    )


@pytest.mark.parametrize("summary", ["0. First\n2. Skipped", "0. First\n0. Duplicate", "0. First\nsecond"])
def test_invalid_existing_numbering_is_rebuilt(summary):
    assert number_patient_summary(summary).startswith("0. First\n1.")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("patient_summary", "  "),
        ("criterion_type", ""),
        ("criterion_text", "  "),
        ("patient_id", None),
    ],
)
def test_empty_or_non_string_inputs_fail_before_strip(field, value):
    values = {
        "patient_summary": "A summary.",
        "criterion_type": "inclusion",
        "criterion_text": "A criterion.",
    }
    values[field] = value
    with pytest.raises((TypeError, ValueError), match=field):
        prepare_custom_case(**values)


@pytest.mark.parametrize("field", ["patient_summary", "criterion_type", "criterion_text"])
def test_non_string_required_inputs_are_rejected(field):
    values = {
        "patient_summary": "A summary.",
        "criterion_type": "inclusion",
        "criterion_text": "A criterion.",
    }
    values[field] = 123
    with pytest.raises(TypeError, match=f"{field} must be a string"):
        prepare_custom_case(**values)


def test_invalid_criterion_type_fails():
    with pytest.raises(ValueError, match="criterion_type must be inclusion or exclusion"):
        prepare_custom_case("A summary.", "other", "A criterion.")


def test_builds_model_ready_case_with_stable_synthetic_defaults():
    case = prepare_custom_case(
        "  A summary.  ",
        " inclusion ",
        " A criterion. ",
        patient_id="  synthetic-patient-1 ",
    )

    assert case == {
        "patient_id": "synthetic-patient-1",
        "patient_summary": "0. A summary.",
        "trial_id": "custom-trial",
        "trial_title": "Synthetic custom trial",
        "criterion_id": "custom-criterion",
        "criterion_type": "inclusion",
        "criterion_text": "A criterion.",
    }
    assert "ground_truth_label" not in case
