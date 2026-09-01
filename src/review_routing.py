"""Deterministic live review routing for model screening results.

The route names match the current n8n workflow: ``HUMAN_REVIEW`` and
``NO_ROUTINE_QUEUE``. The latter means only that ``queue_required`` is false; it is
not a clinical decision and human confirmation remains required.
"""

from dataclasses import dataclass


VALID_LABELS = {"MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"}
HUMAN_REVIEW = "HUMAN_REVIEW"
NO_ROUTINE_QUEUE = "NO_ROUTINE_QUEUE"


@dataclass(frozen=True)
class ReviewRoutingResult:
    route: str
    queue_required: bool
    reason: str
    human_confirmation_required: bool


def route_screening_result(predicted_label: str) -> ReviewRoutingResult:
    """Route a live model label without using evaluation ground truth."""
    if not isinstance(predicted_label, str) or predicted_label not in VALID_LABELS:
        raise ValueError(f"Invalid predicted_label: {predicted_label!r}")

    if predicted_label in {"UNKNOWN", "NOT_APPLICABLE"}:
        return ReviewRoutingResult(
            route=HUMAN_REVIEW,
            queue_required=True,
            reason="Model uncertainty or non-applicability requires coordinator review.",
            human_confirmation_required=True,
        )
    return ReviewRoutingResult(
        route=NO_ROUTINE_QUEUE,
        queue_required=False,
        reason="No priority queue condition triggered; human confirmation remains required.",
        human_confirmation_required=True,
    )
