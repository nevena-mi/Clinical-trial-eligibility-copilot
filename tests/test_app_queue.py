from unittest.mock import Mock

import pytest

from mvp import app
from src.n8n_client import N8NQueueResponse, N8NSubmissionError


@pytest.fixture(autouse=True)
def clear_session_state():
    app.st.session_state.clear()
    yield
    app.st.session_state.clear()


def _stored_result(*, queue_required=True):
    return {
        "fingerprint": "case-1",
        "routing": {"queue_required": queue_required},
        "case": {"patient_id": "P1"},
        "result": {"predicted_label": "UNKNOWN"},
        "metadata": {"response_id": "response-1"},
        "source_annotation_id": None,
    }


def test_no_queue_result_cannot_render_submission_button():
    assert not app._queue_button_allowed(
        _stored_result(queue_required=False), "case-1", None
    )


def test_successful_submission_cannot_be_submitted_again():
    submission = {"fingerprint": "case-1", "status": "success"}

    assert not app._queue_button_allowed(_stored_result(), "case-1", submission)


def test_failed_submission_remains_available_for_retry():
    submission = {"fingerprint": "case-1", "status": "error"}

    assert app._queue_button_allowed(_stored_result(), "case-1", submission)


def test_changed_input_cannot_submit_stale_result():
    assert not app._queue_button_allowed(_stored_result(), "case-2", None)


def test_successful_submission_reruns_and_hides_button(monkeypatch):
    stored = _stored_result()
    response = N8NQueueResponse("HUMAN_REVIEW", "OPEN", "queue-1", "Queued.")
    submit = Mock(return_value=response)
    rerun = Mock()
    monkeypatch.setattr(app, "build_review_payload", Mock(return_value={"payload": True}))
    monkeypatch.setattr(app, "submit_review_payload", submit)
    monkeypatch.setattr(app.st, "rerun", rerun)

    app._submit_stored_result(stored)

    submission = app.st.session_state["queue_submission"]
    assert submission["status"] == "success"
    assert submission["response"] == {
        "route": "HUMAN_REVIEW",
        "queue_status": "OPEN",
        "queue_id": "queue-1",
        "message": "Queued.",
    }
    assert rerun.call_count == 1
    assert submit.call_count == 1
    assert not app._queue_button_allowed(
        stored, stored["fingerprint"], submission
    )


def test_failed_submission_reruns_and_preserves_result_for_retry(monkeypatch):
    stored = _stored_result()
    app.st.session_state["screening_result"] = stored
    submit = Mock(side_effect=N8NSubmissionError("offline"))
    rerun = Mock()
    monkeypatch.setattr(app, "build_review_payload", Mock(return_value={"payload": True}))
    monkeypatch.setattr(app, "submit_review_payload", submit)
    monkeypatch.setattr(app.st, "rerun", rerun)

    app._submit_stored_result(stored)

    submission = app.st.session_state["queue_submission"]
    assert app.st.session_state["screening_result"] == stored
    assert submission["status"] == "error"
    assert "screening result was preserved" in submission["message"]
    assert rerun.call_count == 1
    assert submit.call_count == 1
    assert app._queue_button_allowed(stored, stored["fingerprint"], submission)
