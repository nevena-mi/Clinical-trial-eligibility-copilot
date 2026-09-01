import json

import pandas as pd
import pytest

from scripts import create_smoke_manifest as smoke
from src.run_screening import load_annotation_manifest


def _joined_rows():
    labels = ["MET", "NOT_MET", "UNKNOWN", "NOT_APPLICABLE"]
    rows = []
    for index in range(15):
        ground_truth = labels[index % 4]
        predicted = ground_truth if index % 3 else "UNKNOWN"
        if index == 0:
            ground_truth, predicted = "NOT_MET", "MET"
        rows.append({
            "source_annotation_id": index + 1,
            "patient_id": f"P{index + 1}",
            "trial_id": f"T{index + 1}",
            "criterion_id": f"C{index + 1}",
            "criterion_type": "inclusion" if index % 2 else "exclusion",
            "ground_truth_label": ground_truth,
            "predicted_label": predicted,
            "baseline_predicted_label": predicted,
            "baseline_agreement": ground_truth == predicted,
            "baseline_safety_flag": ground_truth == "NOT_MET" and predicted == "MET",
            "baseline_evidence_present": index % 2 == 0,
        })
    return pd.DataFrame(rows)


def test_smoke_selection_is_deterministic_and_covers_required_tags():
    joined = _joined_rows()

    first = smoke.build_smoke_manifest(joined)
    second = smoke.build_smoke_manifest(joined)

    assert first.equals(second)
    assert len(first) == 15
    assert list(first.columns) == smoke.MANIFEST_COLUMNS
    assert first.columns.is_unique
    assert not any(str(column).endswith(".1") for column in first.columns)
    assert first["smoke_order"].tolist() == list(range(1, 16))
    assert first["source_annotation_id"].is_unique
    assert set(first["ground_truth_label"]) == smoke.VALID_LABELS
    assert set(first["criterion_type"]) == {"inclusion", "exclusion"}
    assert set(first["baseline_agreement"]) == {True, False}
    assert set(first["baseline_safety_flag"]) == {True, False}
    assert set(first["baseline_evidence_present"]) == {True, False}
    assert first.loc[first["baseline_safety_flag"], "source_annotation_id"].tolist() == [1]
    assert first["selection_reason"].map(bool).all()
    assert (first["criterion_type"] == "inclusion").sum() >= 5
    assert (first["criterion_type"] == "exclusion").sum() >= 5
    assert first["ground_truth_label"].value_counts().min() >= 2
    assert first["baseline_agreement"].sum() >= 4
    assert (~first["baseline_agreement"]).sum() >= 4
    assert first["baseline_predicted_label"].isin({"UNKNOWN", "NOT_APPLICABLE"}).sum() >= 5
    assert first["baseline_predicted_label"].isin({"MET", "NOT_MET"}).sum() >= 5
    assert first["baseline_evidence_present"].sum() >= 3
    assert (~first["baseline_evidence_present"]).sum() >= 3
    assert first["patient_id"].nunique() >= 12
    assert first["trial_id"].nunique() >= 12


def test_smoke_manifest_csv_round_trip_preserves_exact_schema(tmp_path):
    manifest = smoke.build_smoke_manifest(_joined_rows())
    path = tmp_path / "manifest.csv"
    manifest.to_csv(path, index=False)

    loaded = pd.read_csv(path)

    assert list(loaded.columns) == smoke.MANIFEST_COLUMNS
    assert loaded.columns.is_unique
    assert not any(str(column).endswith(".1") for column in loaded.columns)


def test_smoke_selection_rejects_missing_required_columns():
    joined = _joined_rows().drop(columns="baseline_predicted_label")

    with pytest.raises(ValueError, match="baseline_predicted_label"):
        smoke.build_smoke_manifest(joined)


def test_smoke_selection_rejects_too_many_mandatory_unsafe_cases():
    joined = pd.concat([_joined_rows(), _joined_rows().assign(source_annotation_id=16)])
    joined["ground_truth_label"] = "NOT_MET"
    joined["baseline_predicted_label"] = "MET"
    joined["baseline_agreement"] = False
    joined["baseline_safety_flag"] = True

    with pytest.raises(ValueError, match="exceed"):
        smoke.build_smoke_manifest(joined)


def test_smoke_selection_reports_unsatisfied_quotas():
    joined = _joined_rows()
    joined["criterion_type"] = "inclusion"

    with pytest.raises(ValueError, match="criterion_type=exclusion"):
        smoke.build_smoke_manifest(joined)


def test_candidate_can_reduce_multiple_distinct_quota_categories():
    joined = _joined_rows()
    selected_patients = set()
    selected_trials = set()
    matches = joined.loc[
        joined["ground_truth_label"].eq("NOT_APPLICABLE")
        & joined["criterion_type"].eq("inclusion")
        & joined["baseline_agreement"].eq(True)
        & joined["baseline_predicted_label"].eq("NOT_APPLICABLE")
        & joined["baseline_evidence_present"].eq(False)
        & ~joined["patient_id"].isin(selected_patients)
        & ~joined["trial_id"].isin(selected_trials)
    ]
    assert not matches.empty
    row = matches.sort_values("source_annotation_id").iloc[0]
    counts = {category: 0 for category in smoke.QUOTA_TARGETS}

    categories = smoke._quota_categories(row, counts, selected_patients, selected_trials)

    assert "ground_truth=NOT_APPLICABLE" in categories
    assert "criterion_type=inclusion" in categories
    assert "agreement=agreement" in categories
    assert "outcome=review" in categories
    assert "evidence=absent" in categories
    assert "unique_patients" in categories
    assert "unique_trials" in categories


@pytest.mark.parametrize("field", ["status", "model", "prompt_version", "predicted_label", "evidence_sentence_ids"])
def test_baseline_validation_rejects_invalid_required_fields(field):
    reference = pd.DataFrame([{"source_annotation_id": 1, "ground_truth_label": "MET"}])
    baseline = pd.DataFrame([{
        "source_annotation_id": 1,
        "patient_id": "P1",
        "trial_id": "T1",
        "criterion_id": "C1",
        "criterion_type": "inclusion",
        "ground_truth_label": "MET",
        "predicted_label": "MET",
        "evidence_sentence_ids": "[]",
        "status": "success",
        "model": "gpt-4.1",
        "prompt_version": "v2_abstention_rules",
    }])
    baseline.loc[0, field] = {
        "status": "error",
        "model": "other",
        "prompt_version": "v1",
        "predicted_label": "BAD",
        "evidence_sentence_ids": "not-json",
    }[field]

    with pytest.raises(ValueError):
        smoke.validate_baseline(reference, baseline, expected_rows=1)


def test_baseline_validation_rejects_ground_truth_mismatch():
    reference = pd.DataFrame([{"source_annotation_id": 1, "ground_truth_label": "NOT_MET"}])
    baseline = pd.DataFrame([{
        "source_annotation_id": 1,
        "patient_id": "P1",
        "trial_id": "T1",
        "criterion_id": "C1",
        "criterion_type": "inclusion",
        "ground_truth_label": "MET",
        "predicted_label": "MET",
        "evidence_sentence_ids": json.dumps([]),
        "status": "success",
        "model": "gpt-4.1",
        "prompt_version": "v2_abstention_rules",
    }])

    with pytest.raises(ValueError, match="ground-truth"):
        smoke.validate_baseline(reference, baseline, expected_rows=1)


def _assessment_frame():
    return pd.DataFrame([
        {"source_annotation_id": index, "patient_id": f"P{index}", "trial_id": f"T{index}", "criterion_id": f"C{index}", "criterion_type": "inclusion"}
        for index in range(1, 16)
    ])


def _manifest_frame():
    return pd.DataFrame({"smoke_order": range(1, 16), "source_annotation_id": range(1, 16)})


def test_manifest_loader_preserves_authoritative_order(tmp_path):
    manifest = _manifest_frame().iloc[::-1]
    path = tmp_path / "manifest.csv"
    manifest.to_csv(path, index=False)

    selected = load_annotation_manifest(path, _assessment_frame())

    assert selected["source_annotation_id"].tolist() == list(range(1, 16))


@pytest.mark.parametrize(
    "change",
    [
        lambda frame: frame.drop(columns="source_annotation_id"),
        lambda frame: frame.assign(smoke_order=[1] * 15),
        lambda frame: frame.assign(smoke_order=list(range(1, 15)) + [16]),
        lambda frame: frame.assign(source_annotation_id=list(range(1, 15)) + [99]),
    ],
)
def test_manifest_loader_rejects_malformed_manifest(tmp_path, change):
    path = tmp_path / "manifest.csv"
    change(_manifest_frame()).to_csv(path, index=False)

    with pytest.raises(ValueError):
        load_annotation_manifest(path, _assessment_frame())
