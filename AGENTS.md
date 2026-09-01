# AGENTS.md

## Project

Clinical-Trial Eligibility Copilot is a human-reviewed AI decision-support prototype for criterion-level clinical-trial prescreening.

The current implementation uses public synthetic TrialGPT-derived data. It must never be presented as a clinical decision system or as validated for real patient use.

## Core product boundary

The system may:

- compare synthetic patient evidence with one trial criterion;
- return `MET`, `NOT_MET`, `UNKNOWN`, or `NOT_APPLICABLE`;
- provide a concise rationale and evidence-sentence references;
- route uncertain or flagged results to human review;
- expose model, prompt, latency, cost, and monitoring metadata.

The system must not:

- make final eligibility or enrolment decisions;
- process real patient or identifiable health data;
- infer facts not present in the supplied evidence;
- present evaluation ground truth to the model;
- use evaluation-only ground truth rules in live decision logic.

Human review remains mandatory before any clinical action.

## Project reference documents

Before implementing a change, inspect the relevant existing documents:

- `README.md`
- `use_case_definition.md`
- `implementation_plan.md`
- `data/data_dictionary.md`
- `data/validation_rules.md`
- `poc/poc_documentation.md`
- `evaluation/initial_model_analysis.md`

These documents provide project context but may require updating during Round 2. Verify their content against the current code, data and agreed scope before relying on them.

If implementation changes documented behaviour, update the affected document in the same task. Do not silently contradict an established product boundary or decision.

## Working approach

Work on one defined user story or implementation step at a time.

Before changing files:

1. state the intended outcome;
2. identify the files likely to change;
3. explain any important design decision briefly;
4. ask for confirmation if the change expands scope or changes established behaviour.

After changing files:

1. summarise the changes;
2. show the relevant validation or test results;
3. identify remaining limitations;
4. update the implementation plan when a planned step is completed.

Do not commit, push, delete tracked artifacts, or change credentials unless explicitly requested.

Preserve unrelated user changes in the working tree.

## Implementation priorities

Prioritise in this order:

1. safety and human-review boundaries;
2. correct and reproducible behaviour;
3. clear error handling;
4. traceability and observability;
5. usability;
6. performance and visual polish.

Prefer the smallest implementation that satisfies the current acceptance criteria.

## Code structure

- Keep reusable screening and validation logic in `src/`.
- Keep the Streamlit interface in `mvp/`.
- Keep tests in `tests/`.
- Keep exploratory analysis in `notebooks/01_explore_trialgpt_data.ipynb`.
- Keep model-comparison analysis in `notebooks/02_model_comparison.ipynb`.
- Keep generated evaluation outputs in `data/processed/`.
- Do not duplicate screening logic inside Streamlit or notebooks.
- Prefer Python scripts for reproducible processing; use notebooks for analysis and visualisation.

## Data handling

Use only public synthetic project data.

For custom cases, display this warning:

> Synthetic demonstration data only. Do not enter real patient information.

Validate required fields before model execution. Do not log secrets, API keys, credentials, or unnecessary input data.

Ground-truth labels are evaluation data. Hide them until after prediction and never include them in model prompts.

## Model and prompt evaluation

Maintain the existing GPT-4.1 and `v2_abstention_rules` run as the Round 1 baseline.

When comparing models:

- use the same evaluation cases and prompt first;
- record model and prompt versions;
- preserve raw predictions;
- do not overwrite baseline outputs;
- compare unsafe MET rate, UNKNOWN recall, exact agreement, review rate, invalid outputs, latency, and estimated cost;
- document limitations of the evaluation set.

When testing prompt changes, assign a new prompt version instead of modifying the baseline invisibly.

## n8n and review routing

The POC routes `UNKNOWN` and `NOT_APPLICABLE` results to human review.

Ground-truth-based unsafe-MET detection is evaluation-only and must be labelled accordingly.

A failed n8n or Notion request must not:

- erase the screening result;
- report that a queue item was created;
- convert the model output into a final eligibility decision.

Queue submission should be explicit and its success or failure should be visible to the user.

## Configuration and secrets

- Load secrets from the project-root `.env`.
- Keep `.env` excluded from Git.
- Document required variables in `.env.example` without real values.
- Do not expose secrets in logs, screenshots, notebooks, fixtures, or documentation.
- Avoid adding a dependency unless it is required and documented.

## Testing and verification

For relevant changes, run:

```bash
python -m compileall -q src mvp
pytest -q
git diff --check
```

Also validate modified JSON files with:

```bash
python -m json.tool PATH_TO_FILE > /dev/null
```

Add or update tests for:

- input validation;
- label-schema validation;
- evidence-reference validation;
- routing decisions;
- error handling;
- deterministic non-model helper functions.

Do not call paid model APIs during ordinary unit tests.

## Documentation standard

Use concise Markdown with descriptive headings.

Document:

- how to run the feature;
- required inputs and expected outputs;
- assumptions;
- safety boundaries;
- demo-versus-production limitations;
- known errors or unavailable integrations.

Use British English consistently where practical.

## Completion rule

A task is complete only when:

- its acceptance criteria are satisfied;
- relevant tests pass;
- documentation is updated;
- no secrets or real patient data are introduced;
- limitations and human-review boundaries remain explicit.

