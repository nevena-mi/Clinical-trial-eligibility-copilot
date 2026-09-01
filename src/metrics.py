import argparse
import math
from numbers import Integral, Real
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import PROJECT_ROOT
from src.pricing import PricingError, estimate_cost, get_model_pricing

REVIEW_LABELS = {"UNKNOWN", "NOT_APPLICABLE"}

def safe_rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else np.nan


def _integer_token_count(value, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (Integral, Real)):
        raise PricingError(f"Successful {field_name} token counts must be integers.")
    if not math.isfinite(float(value)) or float(value) < 0 or not float(value).is_integer():
        raise PricingError(
            f"Successful {field_name} token counts must be non-negative integers."
        )
    return int(value)


def estimate_prediction_costs(df: pd.DataFrame) -> pd.Series:
    """Estimate costs for successful rows using each row's recorded model."""
    if "model" not in df.columns:
        raise PricingError("Prediction rows must contain a model for cost estimation.")
    if df["model"].isna().any() or df["model"].eq("").any():
        raise PricingError("Every prediction row must contain a model for cost estimation.")
    for model in df["model"].unique():
        get_model_pricing(model)

    successful_df = df.loc[df["status"] == "success"]
    return successful_df.apply(
        lambda row: estimate_cost(
            row["model"],
            _integer_token_count(row["input_tokens"], "input"),
            _integer_token_count(row["output_tokens"], "output"),
        ),
        axis=1,
    )

def main(predictions_path: str) -> None:
    predictions_file = Path(predictions_path)
    if not predictions_file.is_absolute():
        predictions_file = PROJECT_ROOT / predictions_file

    df = pd.read_csv(predictions_file)
    estimated_costs = estimate_prediction_costs(df)
    df = df[df["status"] == "success"].copy()

    df["agreement_flag"] = (df["predicted_label"] == df["ground_truth_label"]).astype(int)
    df["unsafe_met_flag"] = ((df["ground_truth_label"] == "NOT_MET") & (df["predicted_label"] == "MET")).astype(int)
    df["ground_truth_unknown_flag"] = (df["ground_truth_label"] == "UNKNOWN").astype(int)
    df["unknown_recalled_flag"] = ((df["ground_truth_label"] == "UNKNOWN") & (df["predicted_label"] == "UNKNOWN")).astype(int)
    df["review_required_flag"] = df["predicted_label"].isin(REVIEW_LABELS).astype(int)
    df["estimated_cost_usd"] = estimated_costs

    total = len(df)
    actual_not_met = int((df["ground_truth_label"] == "NOT_MET").sum())
    actual_unknown = int(df["ground_truth_unknown_flag"].sum())
    unsafe_met = int(df["unsafe_met_flag"].sum())
    unknown_recalled = int(df["unknown_recalled_flag"].sum())

    metrics = [
        {"metric_name": "Assessments processed", "value": total, "numerator": total, "denominator": total, "unit": "count", "definition": "Successful criterion-level LLM assessments."},
        {"metric_name": "Exact agreement", "value": df["agreement_flag"].mean(), "numerator": int(df["agreement_flag"].sum()), "denominator": total, "unit": "percent", "definition": "Predicted label exactly matches the expert reference label."},
        {"metric_name": "Unsafe MET rate", "value": safe_rate(unsafe_met, actual_not_met), "numerator": unsafe_met, "denominator": actual_not_met, "unit": "percent", "definition": "Reference NOT_MET assessments incorrectly predicted as MET; lower is safer."},
        {"metric_name": "UNKNOWN recall", "value": safe_rate(unknown_recalled, actual_unknown), "numerator": unknown_recalled, "denominator": actual_unknown, "unit": "percent", "definition": "Reference UNKNOWN assessments correctly returned as UNKNOWN."},
        {"metric_name": "Review rate", "value": df["review_required_flag"].mean(), "numerator": int(df["review_required_flag"].sum()), "denominator": total, "unit": "percent", "definition": "Predictions labelled UNKNOWN or NOT_APPLICABLE and routed for clarification or contextual review."},
        {"metric_name": "Median latency", "value": df["latency_seconds"].median(), "numerator": np.nan, "denominator": np.nan, "unit": "seconds", "definition": "Median API response time per assessment."},
        {"metric_name": "Mean latency", "value": df["latency_seconds"].mean(), "numerator": np.nan, "denominator": np.nan, "unit": "seconds", "definition": "Average API response time per assessment."},
        {"metric_name": "P95 latency", "value": df["latency_seconds"].quantile(0.95), "numerator": np.nan, "denominator": np.nan, "unit": "seconds", "definition": "95th-percentile API response time per assessment."},
        {"metric_name": "Total estimated API cost", "value": df["estimated_cost_usd"].sum(), "numerator": np.nan, "denominator": np.nan, "unit": "USD", "definition": "Estimated text-token cost using the model recorded for each row."},
        {"metric_name": "Estimated cost per assessment", "value": df["estimated_cost_usd"].mean(), "numerator": np.nan, "denominator": np.nan, "unit": "USD", "definition": "Estimated text-token cost per successful assessment using row-level model pricing."},
    ]

    output_dir = PROJECT_ROOT / "data" / "processed"
    assessment_output = output_dir / "llm_assessment_results.csv"
    metrics_output = output_dir / "dashboard_metrics.csv"

    df.to_csv(assessment_output, index=False)
    pd.DataFrame(metrics).to_csv(metrics_output, index=False)

    print("\nEvaluation summary")
    print(f"Assessments: {total}")
    print(f"Exact agreement: {df['agreement_flag'].mean():.1%}")
    print(f"Unsafe MET rate: {safe_rate(unsafe_met, actual_not_met):.1%} ({unsafe_met}/{actual_not_met})")
    print(f"UNKNOWN recall: {safe_rate(unknown_recalled, actual_unknown):.1%} ({unknown_recalled}/{actual_unknown})")
    print(f"Review rate: {df['review_required_flag'].mean():.1%}")
    print(f"Median latency: {df['latency_seconds'].median():.2f} s")
    print(f"Total estimated cost: ${df['estimated_cost_usd'].sum():.4f}")
    print(f"\nSaved: {assessment_output}")
    print(f"Saved: {metrics_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", default="data/processed/llm_predictions_gpt41_v2.csv")
    args = parser.parse_args()
    main(args.predictions)
