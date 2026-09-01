# Phase 4 — Model Comparison and Prompt Evaluation

## Objective

Compare the existing GPT-4.1 baseline with a stronger model on the same locked evaluation cohort.

The comparison will determine whether improved model quality justifies any additional cost and latency. Model selection will prioritise safety and criterion-level agreement rather than cost alone.

The experiment will change one variable at a time:

1. Compare models using the existing prompt.
2. Analyse remaining errors.
3. Consider prompt changes only if the error analysis identifies a clear, addressable weakness.

Automated tests will not call paid APIs. Actual model comparison runs will be started manually and will call the OpenAI API.

## Existing Baseline

The locked baseline consists of:

- Model: `gpt-4.1`
- Prompt version: `v2_abstention_rules`
- Evaluation cases: 120
- Patients: 30
- Exact agreement: 72.5% (`87/120`)
- Unsafe `MET` rate: 5.9% (`1/17`)
- `UNKNOWN` recall: 92.3% (`48/52`)
- Human-review rate: 59.2% (`71/120`)
- Median latency: 1.01 seconds
- Recorded API cost: approximately `$0.2556`

The existing baseline prediction file remains unchanged:

`data/processed/llm_predictions_gpt41_v2.csv`

The baseline documentation remains in:

`evaluation/initial_model_analysis.md`

## Candidate Configuration

The first candidate configuration will be:

| Setting | Value |
|---|---|
| Model | `gpt-5.6-sol` |
| Reasoning effort | `medium` |
| Prompt version | `v2_abstention_rules` |
| Evaluation cohort | Same locked 120 assessments |
| Temperature or sampling settings | Use only settings supported by the selected model |
| Configuration ID | `gpt56sol-medium-v2` |

The candidate prediction file will be:

`data/processed/llm_predictions_gpt56sol_medium_v2.csv`

The candidate run must not overwrite the GPT-4.1 baseline or any previous model output.

## Phase 4.1 — Comparison Infrastructure

### Purpose

Prepare reproducible model configuration, execution, validation, metrics and comparison outputs before spending money on API calls.

### Steps

1. Add explicit support for reasoning effort where supported by the selected model.
2. Preserve the existing GPT-4.1 execution behaviour.
3. Record the following metadata for every candidate assessment:

   - model;
   - model-configuration ID;
   - reasoning effort;
   - prompt version;
   - response ID;
   - status;
   - latency;
   - input tokens;
   - output tokens;
   - error message.

4. Add a model-aware pricing registry.

5. Record the pricing source and the date on which the price was checked.

6. Fail clearly when pricing for a model is unavailable instead of silently applying GPT-4.1 prices.

7. Add deterministic unit tests using mocked model responses.

8. Keep ordinary test execution independent of OpenAI credentials and paid services.

### Documentation

Document configuration conventions and execution commands in:

`evaluation/model_comparison.md`

Record model pricing assumptions in either:

- a clearly named section of `evaluation/model_comparison.md`; or
- a model-pricing configuration file referenced by that document.

## Phase 4.2 — Candidate Smoke Run

### Purpose

Confirm that the candidate model works with the current structured-output schema and prompt before running all 120 cases.

### Sample

Select approximately 12–15 representative cases covering:

- all four reference labels;
- inclusion and exclusion criteria;
- known GPT-4.1 disagreements;
- the existing unsafe `MET` case;
- cases with and without evidence sentence IDs;
- straightforward and ambiguous criteria.

The selected case IDs must be documented so the smoke run can be reproduced.

### Execution

Run the candidate model manually against the smoke sample.

This is the first step that makes paid OpenAI API calls.

Example output:

`data/processed/llm_predictions_gpt56sol_medium_v2_smoke.csv`

### Smoke-Run Acceptance Criteria

The candidate can proceed to the full run only if:

- every selected case produces a valid structured response;
- every predicted label belongs to the four-label schema;
- evidence sentence IDs are valid;
- no unexpected configuration or API compatibility error occurs;
- response metadata is recorded;
- the candidate does not produce an obviously unsafe result on the known safety-critical example.

If the smoke run fails, correct only the technical compatibility issue and rerun the smoke sample. Do not change the prompt merely to improve smoke-test scores.

### Documentation

Add the following to `evaluation/model_comparison.md`:

- smoke-sample selection;
- candidate configuration;
- success and error counts;
- initial latency and token observations;
- decision to proceed, revise or stop.

## Phase 4.3 — Full Locked-Cohort Run

### Purpose

Generate a directly comparable candidate result for all 120 locked assessments.

### Preconditions

Before starting the full paid run:

- the smoke run has passed;
- the expected API cost has been estimated;
- the output path has been verified;
- the baseline file is protected from overwrite;
- the user has explicitly authorised the full run.

### Execution

Run `gpt-5.6-sol` with reasoning effort `medium` and prompt `v2_abstention_rules` on the same 120 assessments used for GPT-4.1.

Use resume-safe execution so an interrupted run can continue without repeating successful assessments.

### Full-Run Acceptance Criteria

The completed candidate result must contain:

- exactly 120 rows;
- exactly 120 unique `source_annotation_id` values;
- the same source annotation IDs as the baseline;
- no duplicate assessments;
- no missing required fields;
- valid labels only;
- valid evidence references;
- a recorded status for every assessment;
- consistent model, prompt and reasoning metadata.

Any failed assessments must be resolved or clearly documented before aggregate comparison.

## Phase 4.4 — Metrics and Comparison Data

### Purpose

Generate reusable, dashboard-ready data from the saved raw model outputs.

No OpenAI calls are made in this phase. The analysis reads the already saved GPT-4.1 and GPT-5.6 Sol CSV files.

### Required Metrics

Calculate for each model configuration:

- exact criterion-level agreement;
- agreement count;
- disagreement count;
- macro F1;
- per-label precision;
- per-label recall;
- per-label F1;
- confusion matrix;
- unsafe `MET` count and rate;
- `UNKNOWN` recall;
- human-review count and rate;
- successful and failed assessment counts;
- median and mean latency;
- total input tokens;
- total output tokens;
- estimated total cost;
- estimated cost per assessment.

Use the term **exact agreement** rather than clinical accuracy because the dataset measures agreement with reference annotations and does not validate real-world patient outcomes.

### Dashboard-Ready CSV Files

Create the following files:

#### `data/processed/model_comparison_assessments.csv`

One row per assessment and model configuration.

Required fields should include:

- source annotation ID;
- patient ID;
- trial ID;
- criterion ID;
- criterion type;
- ground-truth label;
- predicted label;
- agreement flag;
- safety-error flag;
- review-required flag;
- model;
- configuration ID;
- prompt version;
- reasoning effort;
- latency;
- token counts;
- estimated row cost;
- status and error message.

This is the primary Tableau detail-level data source.

#### `data/processed/model_comparison_metrics.csv`

One row per model configuration and metric.

Suggested columns:

- configuration ID;
- model;
- prompt version;
- reasoning effort;
- metric name;
- metric value;
- numerator;
- denominator;
- unit.

This supports KPI cards and model-level comparison charts.

#### `data/processed/model_comparison_confusion_matrix.csv`

One row per model configuration, reference label and predicted label combination.

Suggested columns:

- configuration ID;
- model;
- ground-truth label;
- predicted label;
- case count.

This supports confusion-matrix views.

#### `data/processed/model_comparison_error_patterns.csv`

One row per disagreement or defined error category.

Suggested columns:

- configuration ID;
- source annotation ID;
- criterion type;
- ground-truth label;
- predicted label;
- error category;
- safety significance;
- rationale;
- evidence sentence IDs.

This supports error-pattern analysis and presentation examples.

## Phase 4.5 — Analysis and Model Decision

### Decision Priority

Evaluate candidate configurations in this order:

1. Safety-critical behaviour.
2. Exact agreement and per-label performance.
3. Reliable abstention and `UNKNOWN` handling.
4. Human-review workload.
5. Technical reliability.
6. Cost and latency.

### Candidate Acceptance Gates

The candidate should normally be selected only if:

- unsafe `MET` results do not increase above the baseline;
- exact agreement improves above 72.5%;
- `UNKNOWN` recall does not fall materially below the baseline;
- all 120 assessments complete successfully;
- cost and latency remain acceptable for a human-reviewed pre-screening workflow.

A model with slightly higher agreement must not be selected if it creates a worse safety profile.

If no model dominates every metric, document the trade-off explicitly rather than claiming a single model is universally better.

### Documentation

Create:

`evaluation/model_comparison.md`

It must contain:

- objective and hypothesis;
- baseline and candidate configurations;
- locked-cohort definition;
- smoke-run approach;
- full-run execution details;
- metric definitions;
- complete comparison table;
- safety analysis;
- cost and latency comparison;
- limitations;
- recommended model;
- reason for the recommendation.

Create:

`evaluation/model_error_analysis.md`

It must contain:

- disagreement categories;
- safety-critical errors;
- inclusion versus exclusion patterns;
- label-confusion patterns;
- representative anonymised synthetic examples;
- likely model limitations;
- errors that may be addressable through prompting;
- errors unlikely to be solved through prompting alone.

Use:

`notebooks/02_model_comparison.ipynb`

The notebook will:

- read saved CSV files;
- reproduce comparison tables and charts;
- perform no OpenAI API calls;
- avoid embedding credentials;
- show the transformation from raw predictions to comparison outputs.

## Phase 4.6 — Optional Prompt Improvement

Prompt improvement begins only after the same-prompt model comparison is complete.

### Trigger

Create a new prompt only if the error analysis identifies a repeated and addressable problem, such as:

- misinterpretation of exclusion criteria;
- unsupported assumptions from missing evidence;
- inconsistent use of `NOT_APPLICABLE`;
- incorrect evidence sentence references;
- failure to distinguish criterion-level assessment from trial-level eligibility.

### Method

1. Define the targeted prompt change.
2. Assign a new prompt version, such as `v3_<specific_change>`.
3. Preserve the selected model configuration.
4. Run a small regression sample first.
5. Run the full locked cohort only if the regression sample improves the targeted behaviour without introducing new safety errors.
6. Save the result in a new file; never overwrite the v2 result.

This preserves attribution:

- model comparison: model changes, prompt remains v2;
- prompt comparison: model remains fixed, prompt changes.

## Tableau Dashboard Direction

The existing Tableau workbook should be extended rather than creating a separate workbook solely for the second model.

The implementation work will produce the CSV files. Tableau development will be completed manually.

Recommended Tableau changes:

- connect the four model-comparison CSV files;
- add a `Configuration ID` or `Model` filter;
- update existing KPI views so the selected model controls the displayed metrics;
- add a model-comparison dashboard or story page;
- compare exact agreement, unsafe `MET`, `UNKNOWN` recall, review rate, latency and cost;
- add confusion matrices by model;
- add an error-pattern view;
- retain a clear distinction between evaluation metrics and live MVP operation.

After the Tableau work is complete, update:

`dashboard/dashboard_documentation.md`

Document:

- CSV sources used;
- Tableau relationships or joins;
- filters;
- calculated fields;
- dashboard sheets;
- metric definitions;
- refresh procedure;
- screenshots;
- limitations.

The Tableau workbook can be returned to the repository after the manual changes are complete.

## LangSmith Documentation

After the comparison runs, update:

`langsmith/monitoring_documentation.md`

Document:

- project and trace naming;
- model and prompt metadata;
- candidate smoke and full-run traces;
- token and latency observations;
- trace screenshots;
- synthetic-data limitation;
- separation between AI traces and n8n workflow audit events.

Do not include API keys, webhook URLs or other credentials.

## Definition of Done

Phase 4 is complete when:

- the GPT-4.1 baseline remains unchanged;
- the candidate smoke run is documented;
- the candidate full result contains 120 valid assessments;
- both configurations use the same locked cohort and prompt;
- raw model outputs are preserved separately;
- comparison metrics are reproducible;
- all four dashboard-ready CSV files exist;
- safety, quality, review workload, latency and cost are compared;
- a model recommendation is documented;
- remaining errors and limitations are explicit;
- automated tests pass without paid API calls;
- API calls occur only during manually authorised model runs;
- no secrets or real patient data are introduced;
- Tableau and LangSmith documentation are updated after their manual work is complete.

## Relationship to Other Project Documents

For Phase 4 model-comparison work, this document is the authoritative implementation plan.

Repository-wide development and safety rules remain defined in `AGENTS.md`. Clinical scope, label meanings and human-review boundaries remain defined in `use_case_definition.md`.

Consult the main `implementation_plan.md` only when a proposed change affects another project phase, overall MVP scope or shared architectural decisions. In case of conflict, stop and request clarification rather than making assumptions.