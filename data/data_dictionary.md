# Data Dictionary

## Dataset purpose

This dataset supports evaluation of an AI-assisted clinical-trial pre-screening copilot. It contains 30 synthetic patient summaries and 120 selected patient–trial–criterion assessments derived from the public TrialGPT criterion-annotation dataset.

No real patient data is used.

## `data/processed/patients.csv`

| Column | Type | Description |
|---|---|---|
| `patient_id` | string | Stable identifier for one synthetic patient |
| `patient_summary` | string | De-identified synthetic clinical note used as model input |

One row represents one synthetic patient.  
Expected row count: 30.

## `data/processed/trial_criteria.csv`

| Column | Type | Description |
|---|---|---|
| `criterion_id` | string | Project-generated identifier for one selected criterion |
| `trial_id` | string | ClinicalTrials.gov NCT identifier |
| `trial_title` | string | Public trial title |
| `criterion_type` | string | `inclusion` or `exclusion` |
| `criterion_text` | string | Public eligibility-criterion text |

One row represents one selected trial criterion.

## `data/processed/ground_truth.csv`

| Column | Type | Description |
|---|---|---|
| `source_annotation_id` | integer | Original TrialGPT annotation identifier |
| `patient_id` | string | Links to `patients.csv` |
| `trial_id` | string | ClinicalTrials.gov NCT identifier |
| `criterion_id` | string | Links to `trial_criteria.csv` |
| `criterion_type` | string | `inclusion` or `exclusion` |
| `ground_truth_label` | string | Normalised expert reference label |
| `expert_eligibility` | string | Original TrialGPT expert label |
| `expert_evidence_sentence_ids` | string | Sentence index or indices identified by the expert as evidence |
| `gpt4_eligibility` | string | Published TrialGPT baseline-model label; retained for comparison only |
| `gpt4_explanation` | string | Published TrialGPT baseline-model explanation; retained for comparison only |
| `explanation_correctness` | string | Expert assessment of the published baseline explanation |
| `training` | boolean | Original TrialGPT dataset split indicator; not used as this project’s train/test split |

One row represents one patient × trial × criterion assessment.  
Expected row count: 120.

## Normalised ground-truth labels

| Project label | Meaning |
|---|---|
| `MET` | The available patient summary supports the criterion. For exclusion criteria, this means the exclusion is not present. |
| `NOT_MET` | The patient summary contradicts the criterion. For exclusion criteria, this means the exclusion is present. |
| `UNKNOWN` | The available summary contains insufficient information to assess the criterion. |
| `NOT_APPLICABLE` | The criterion is not meaningfully applicable in the patient–trial context. |

## Source

The public source is the [TrialGPT Criterion Annotations dataset](https://huggingface.co/datasets/ncbi/TrialGPT-Criterion-Annotations), based on synthetic patient cases and public ClinicalTrials.gov trial criteria.