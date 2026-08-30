# Initial LLM Screening Analysis and Error Review

## Purpose

This document records the first evaluated run of the clinical-trial eligibility pre-screening POC. It separates technical validation, performance metrics and manual error review.

The POC provides criterion-level decision support only. It does not make enrolment decisions; a human clinical-trial coordinator remains responsible for every final decision.

## Evaluation scope

| Item                       | Value                                                                  |
| -------------------------- | ---------------------------------------------------------------------- |
| Dataset                    | NCBI TrialGPT Criterion Annotations                                    |
| Data type                  | Public synthetic patient summaries paired with clinical-trial criteria |
| Locked evaluation cohort   | 120 patient–trial–criterion assessments                                |
| Synthetic patients         | 30                                                                     |
| Ground-truth labels        | `MET`, `NOT_MET`, `UNKNOWN`, `NOT_APPLICABLE`                          |
| Model                      | `gpt-4.1`                                                              |
| Prompt version             | `v2_abstention_rules`                                                  |
| Temperature                | 0                                                                      |
| Run output                 | `data/processed/llm_predictions_gpt41_v2.csv`                          |
| Enriched assessment output | `data/processed/llm_assessment_results.csv`                            |
| Dashboard metric output    | `data/processed/dashboard_metrics.csv`                                 |

The cohort is intentionally enriched with uncertain and safety-relevant cases. It is an evaluation subset for this POC, not a prevalence estimate of real clinical-trial populations.

## Technical validation

The saved output was validated after the batch run. All 120 assessments completed successfully.

| Validation check                                          | Result |
| --------------------------------------------------------- | ------ |
| Required columns present                                  | Pass   |
| Expected row count: 120                                   | Pass   |
| Unique source annotation IDs                              | Pass   |
| Valid processing statuses                                 | Pass   |
| All rows successful                                       | Pass   |
| Valid output labels                                       | Pass   |
| Complete fields for successful rows                       | Pass   |
| Consistent model: `gpt-4.1`                               | Pass   |
| Consistent prompt: `v2_abstention_rules`                  | Pass   |
| Full coverage of locked reference cohort                  | Pass   |
| Patient, trial, criterion and reference-label consistency | Pass   |
| Evidence IDs are valid note sentence IDs                  | Pass   |
| Non-negative latency values                               | Pass   |
| Non-negative token counts                                 | Pass   |

This validates output completeness, traceability and structural quality. It does not by itself prove that every clinical judgement is correct.

## Fixed smoke tests

Three fixed cases were tested before the full batch run using `gpt-4.1`.

| Test case                       | Expected label | Result |
| ------------------------------- | -------------: | -----: |
| Missing randomisation timing    |      `UNKNOWN` |   Pass |
| Age threshold: age ≥18          |          `MET` |   Pass |
| Psychiatric exclusion criterion |      `NOT_MET` |   Pass |

Result: **3/3 fixed smoke-test cases agreed with the reference labels.**

## Evaluation results

| Metric                        |         Result | Interpretation                                                                                      |
| ----------------------------- | -------------: | --------------------------------------------------------------------------------------------------- |
| Assessments processed         |            120 | Full locked cohort completed                                                                        |
| Exact agreement               | 72.5% (87/120) | Predicted label exactly matched the expert reference                                                |
| Unsafe `MET` rate             |    5.9% (1/17) | One reference `NOT_MET` assessment was incorrectly predicted as `MET`; lower is safer               |
| `UNKNOWN` recall              |  92.3% (48/52) | The model usually abstained when the expert reference indicated insufficient information            |
| Review rate                   | 59.2% (71/120) | Predictions labelled `UNKNOWN` or `NOT_APPLICABLE` require clarification or contextual human review |
| Median latency                |   1.01 seconds | Typical API response time per criterion assessment                                                  |
| Total estimated API cost      |        $0.2556 | Estimated token cost of the 120-assessment run                                                      |
| Estimated cost per assessment |       ~$0.0021 | Total estimated cost divided by 120 assessments                                                     |

Estimated cost uses GPT-4.1 text-token rates of $2.00 per million input tokens and $8.00 per million output tokens.

## Metric definitions

* **Exact agreement:** predicted label equals expert reference label.
* **Unsafe `MET` rate:** among assessments with reference label `NOT_MET`, the proportion incorrectly predicted as `MET`. This is the main false-positive safety metric because it could advance a patient despite an unmet criterion.
* **`UNKNOWN` recall:** among reference `UNKNOWN` assessments, the proportion predicted as `UNKNOWN`. Higher recall indicates appropriate abstention when evidence is insufficient.
* **Review rate:** proportion of predictions labelled `UNKNOWN` or `NOT_APPLICABLE`. These results are routed for human clarification or contextual review rather than treated as automated clearance.
* **Latency:** measured API response time for one criterion-level assessment.
* **Estimated API cost:** calculated from recorded input and output tokens; infrastructure, monitoring and human-review costs are excluded.

## Manual review of the safety-critical error

One unsafe false positive was identified.

| Field           | Finding                                                                                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Criterion type  | Inclusion                                                                                                                                                                      |
| Reference label | `NOT_MET`                                                                                                                                                                      |
| LLM prediction  | `MET`                                                                                                                                                                          |
| Criterion       | Clinical presentation suggestive of influenza virus infection, including sudden high fever, cough, headache, muscle and joint pain, severe malaise, sore throat and runny nose |
| LLM rationale   | The model cited sudden high fever, severe headache and joint pain as evidence of influenza-like illness                                                                        |

The patient note documented sudden high fever, chills, facial flushing, epistaxis, severe headache and joint pain. It did not document cough, severe malaise, sore throat or runny nose. It also contained leukopenia, increased haematocrit and thrombocytopenia.

### Error interpretation

The model treated partial symptom overlap as sufficient evidence for `MET`. The expert reference label was `NOT_MET`.

This is an **unsafe false positive caused by overgeneralisation from partial symptom overlap**. The model should not treat a subset of compatible symptoms as confirmation that the full criterion is satisfied.

### Required control

* Human review remains mandatory for all screening recommendations.
* This case will be retained as a regression test for any future prompt revision.
* Any production-oriented version would require additional clinical validation, version-controlled terminology/rules and prospective evaluation before use.

## Current limitations

* The 120-row cohort is a bounded POC evaluation set, not a real-world deployment dataset.
* Only one full 120-row run was completed with `gpt-4.1`; no full head-to-head model comparison is claimed in this project phase.
* Manual semantic review has so far focused on the one safety-critical false positive. The remaining disagreements still require categorisation.
* Evidence IDs are structurally validated, but full clinical assessment of evidence sufficiency is not yet complete.
* The POC does not use a validated clinical ontology or rule engine. It permits only limited interpretation of explicitly documented clinical terminology and does not infer unreported facts, diagnoses or trial-process events.

## Next steps

1. Categorise the remaining 32 disagreements by error type.
2. Review a stratified sample of correct and incorrect rationales with an LLM judge and human spot checks.
3. Load `llm_assessment_results.csv` and `dashboard_metrics.csv` into Tableau.
4. Document monitoring results in LangSmith.
5. Build the n8n human-review routing POC using the model output labels and review flag.


## Error-pattern tables

### Confusion matrix

| ground_truth_label   |   MET |   NOT_APPLICABLE |   NOT_MET |   UNKNOWN |   All |
|:---------------------|------:|-----------------:|----------:|----------:|------:|
| MET                  |    24 |                0 |         1 |         7 |    32 |
| NOT_APPLICABLE       |     3 |                3 |         4 |         9 |    19 |
| NOT_MET              |     1 |                0 |        12 |         4 |    17 |
| UNKNOWN              |     1 |                0 |         3 |        48 |    52 |
| All                  |    29 |                3 |        20 |        68 |   120 |

### Disagreement patterns by criterion type

| ground_truth_label   | predicted_label   | criterion_type   |   count |
|:---------------------|:------------------|:-----------------|--------:|
| MET                  | UNKNOWN           | exclusion        |       7 |
| NOT_APPLICABLE       | UNKNOWN           | exclusion        |       7 |
| NOT_APPLICABLE       | NOT_MET           | exclusion        |       4 |
| NOT_APPLICABLE       | MET               | exclusion        |       3 |
| UNKNOWN              | NOT_MET           | inclusion        |       3 |
| NOT_APPLICABLE       | UNKNOWN           | inclusion        |       2 |
| NOT_MET              | UNKNOWN           | exclusion        |       2 |
| NOT_MET              | UNKNOWN           | inclusion        |       2 |
| MET                  | NOT_MET           | exclusion        |       1 |
| NOT_MET              | MET               | inclusion        |       1 |
| UNKNOWN              | MET               | inclusion        |       1 |