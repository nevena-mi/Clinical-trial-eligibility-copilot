# Data Validation Rules

## Source-data controls

| Rule | Validation |
|---|---|
| Synthetic data only | The project uses public TrialGPT synthetic patient summaries; no real patient data is added. |
| Patient identifier present | Every `patient_id` must be non-null and unique in `patients.csv`. |
| Patient summary present | Every `patient_summary` must be non-null and non-empty. |
| Criterion identifier present | Every `criterion_id` must be unique in `trial_criteria.csv`. |
| Criterion text present | Every `criterion_text` must be non-null and non-empty. |
| Valid criterion type | `criterion_type` must be `inclusion` or `exclusion`. |
| Valid ground-truth label | `ground_truth_label` must be `MET`, `NOT_MET`, `UNKNOWN` or `NOT_APPLICABLE`. |
| Referential integrity | Every assessment patient ID must exist in `patients.csv`; every criterion ID must exist in `trial_criteria.csv`. |
| Unique assessment | Every `source_annotation_id` must occur once in `ground_truth.csv`. |
| Cohort completeness | The locked evaluation dataset must contain 30 unique patients and 120 patient–trial–criterion assessments. |
| Assessment coverage | Each selected patient must have four selected criterion assessments. |

## Evaluation-cohort design controls

The source dataset is naturally imbalanced. The locked 120-row evaluation subset is intentionally safety-enriched to include sufficient `NOT_MET`, `UNKNOWN` and `NOT_APPLICABLE` cases.

This improves the ability to measure unsafe false positives and inappropriate guessing. It is not intended to estimate real-world prevalence of eligibility outcomes.

## Model-output controls

Each future model prediction must contain:

- `patient_id`, `trial_id` and `criterion_id`
- predicted label: `MET`, `NOT_MET`, `UNKNOWN` or `NOT_APPLICABLE`
- evidence sentence ID(s) or explicit statement that no supporting evidence is available
- concise rationale
- mandatory human-review flag
- model name, prompt version, timestamp, latency and estimated cost

Predictions with missing identifiers, invalid labels, missing rationale or unsupported evidence are treated as validation failures and excluded from headline performance metrics until reviewed.