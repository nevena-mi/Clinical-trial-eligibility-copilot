import pytest

from src.review_routing import HUMAN_REVIEW, NO_ROUTINE_QUEUE, route_screening_result


@pytest.mark.parametrize("label", ["UNKNOWN", "NOT_APPLICABLE"])
def test_uncertain_labels_require_human_review(label):
    result = route_screening_result(label)

    assert result.route == HUMAN_REVIEW
    assert result.queue_required is True
    assert result.human_confirmation_required is True


@pytest.mark.parametrize("label", ["MET", "NOT_MET"])
def test_definite_labels_do_not_require_priority_queue(label):
    result = route_screening_result(label)

    assert result.route == NO_ROUTINE_QUEUE
    assert result.queue_required is False
    assert result.human_confirmation_required is True
    assert "human confirmation" in result.reason


@pytest.mark.parametrize("label", ["", "INVALID", None, 1])
def test_invalid_labels_are_rejected(label):
    with pytest.raises(ValueError, match="Invalid predicted_label"):
        route_screening_result(label)


def test_routing_result_is_immutable_and_contains_no_ground_truth():
    result = route_screening_result("MET")

    assert "ground_truth_label" not in result.__dict__
    with pytest.raises(AttributeError):
        result.route = HUMAN_REVIEW
