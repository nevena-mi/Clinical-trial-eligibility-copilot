# Dashboard Documentation

## Purpose

The Tableau dashboard summarises the criterion-level evaluation of the
Clinical-trial eligibility copilot. It helps clinical, operational, and AI
governance stakeholders assess model performance, safety, review workload,
latency, and estimated API cost before considering a controlled pilot.

The dashboard uses public synthetic TrialGPT-derived data only. It supports
human review and does not make eligibility or enrolment decisions.

## Data sources

| Source | Purpose |
|---|---|
| `data/raw/trialgpt/trialgpt_criterion_annotations.parquet` | Source annotations used to construct the synthetic evaluation cohort |
| `data/processed/patients.csv` | Synthetic patient summaries |
| `data/processed/trial_criteria.csv` | Clinical-trial inclusion and exclusion criteria |
| `data/processed/ground_truth.csv` | Reference labels for criterion-level assessments |
| `data/processed/llm_assessment_results.csv` | Model predictions, rationales, evidence references, latency, and token metadata |
| `data/processed/dashboard_metrics.csv` | Pre-calculated headline metrics used in the dashboard |
| `data/processed/error_confusion_matrix.csv` | Comparison of predicted and reference labels |
| `data/processed/error_patterns.csv` | Error-pattern analysis |

## Metrics and rationale

| Metric | Result | Why it matters |
|---|---:|---|
| Assessments processed | 120 | Confirms the completed locked evaluation cohort |
| Exact agreement | 72.5% (87/120) | Overall agreement with the reference label |
| Unsafe MET rate | 5.9% (1/17) | Safety-focused error: a reference `NOT_MET` case predicted as `MET`; lower is safer |
| UNKNOWN recall | 92.3% (48/52) | Shows whether genuinely uncertain cases are correctly abstained from |
| Review rate | 59.2% | Indicates the expected human-review workload |
| Median latency | 1.01 seconds | Indicates responsiveness for criterion-level screening |
| Total estimated API cost | $0.2556 | Cost of the completed 120-assessment evaluation |
| Estimated cost per assessment | ~$0.0021 | Directional unit cost for scenario planning |

## How to navigate

1. Open `clinical_trial_eligibility_dashboard.twb` in Tableau.
2. Start with the headline KPI section for the completed-evaluation summary.
3. Review the predicted-versus-reference label breakdown to identify where the
   model agrees or disagrees with the reference labels.
4. Use the safety and abstention metrics to assess whether risky positive
   predictions or uncertainty handling need further work.
5. Use latency and cost metrics for pilot planning.
6. Review error-pattern views before interpreting agreement alone.

## Interpretation and limitations

- The evaluation uses public synthetic data and is not evidence of clinical
  validity or production readiness.
- Exact agreement does not replace safety analysis: unsafe `MET` predictions
  deserve disproportionate attention.
- A high review rate is intentional in this POC because uncertainty is routed
  to a human coordinator rather than treated as an automated decision.
- Cost estimates cover model calls only. Production costs would also include
  clinical validation, security, integration, training, governance, and
  enterprise-tool licensing.

## Screenshot

A screenshot of the completed Tableau dashboard is available in
`dashboard/tableau_screenshots/`.