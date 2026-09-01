import argparse
import json

import pandas as pd

from src.config import DEFAULT_SCREENING_MODEL, PROCESSED_DIR
from src.screening import screen_one_criterion

BASELINE_PATH = PROCESSED_DIR / "dashboard_baseline.csv"
PATIENTS_PATH = PROCESSED_DIR / "patients.csv"

TEST_CASES = [
    {"name": "unknown_randomisation_timing", "source_annotation_id": 463, "expected_label": "UNKNOWN"},
    {"name": "met_age_threshold", "source_annotation_id": 570, "expected_label": "MET"},
    {"name": "not_met_psychiatric_exclusion", "source_annotation_id": 135, "expected_label": "NOT_MET"},
]

def load_test_case(
    baseline_df: pd.DataFrame,
    patients_df: pd.DataFrame,
    test_config: dict,
) -> tuple[dict, str]:
    selected = baseline_df.loc[
        baseline_df["source_annotation_id"].eq(test_config["source_annotation_id"])
    ]
    if len(selected) != 1:
        raise ValueError(
            f"Expected one row for annotation {test_config['source_annotation_id']}; found {len(selected)}."
        )

    row = selected.iloc[0]
    if row["ground_truth_label"] != test_config["expected_label"]:
        raise ValueError(f"Reference label changed for {test_config['name']}.")

    patient_summary = patients_df.loc[
        patients_df["patient_id"].eq(row["patient_id"]), "patient_summary"
    ]
    if len(patient_summary) != 1:
        raise ValueError(f"Expected one patient summary for {row['patient_id']}; found {len(patient_summary)}.")

    case = {
        "patient_id": row["patient_id"],
        "patient_summary": patient_summary.iloc[0],
        "trial_id": row["trial_id"],
        "trial_title": row["trial_title"],
        "criterion_id": row["criterion_id"],
        "criterion_type": row["criterion_type"],
        "criterion_text": row["criterion_text"],
    }
    return case, row["ground_truth_label"]

def main(model_name: str) -> None:
    baseline_df = pd.read_csv(BASELINE_PATH)
    patients_df = pd.read_csv(PATIENTS_PATH)
    agreements = []

    for test_config in TEST_CASES:
        case, reference_label = load_test_case(baseline_df, patients_df, test_config)
        result, metadata = screen_one_criterion(case, model_name=model_name)
        agrees = result["predicted_label"] == reference_label
        agreements.append(agrees)

        print(f"\n{'=' * 70}\nTest: {test_config['name']}")
        print(f"Model: {metadata['model']} | Prompt: {metadata['prompt_version']}")
        print(f"Patient: {case['patient_id']} | Trial: {case['trial_id']} | Criterion: {case['criterion_id']}")
        print(f"Type: {case['criterion_type']}\nCriterion: {case['criterion_text']}")
        print("\nLLM result")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nReference comparison")
        print(f"Expected label: {reference_label}")
        print(f"Predicted label: {result['predicted_label']}")
        print(f"Agreement: {agrees}")
        print("\nRun metadata")
        print(json.dumps(metadata, indent=2))

    print(f"\n{'=' * 70}\nAgreement summary: {sum(agreements)}/{len(agreements)} fixed smoke-test cases.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fixed screening smoke tests.")
    parser.add_argument("--model", default=DEFAULT_SCREENING_MODEL, help="Model ID; overrides SCREENING_MODEL for this run.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args.model)
