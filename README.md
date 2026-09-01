# Clinical-trial eligibility copilot

A decision-support proof of concept for criterion-level clinical-trial
eligibility screening. The system assesses one patient–trial criterion at a
time, returns a structured label with rationale and evidence references, and
routes uncertain or safety-relevant results to a human-review queue.

This is an educational capstone project using public synthetic TrialGPT-derived
data. It is not a clinical decision system and does not make eligibility,
enrolment, or treatment decisions.

## Project purpose

Clinical-trial teams often need to compare patient information against numerous
inclusion and exclusion criteria. This POC demonstrates a controlled workflow
that:

1. evaluates one criterion at a time using GPT-4.1;
2. returns `MET`, `NOT_MET`, `UNKNOWN`, or `NOT_APPLICABLE`;
3. records rationale, evidence-sentence references, latency, tokens, and model
   metadata;
4. routes uncertain and evaluation-only safety cases to a human coordinator;
5. provides dashboard and LangSmith evidence for performance and observability.

## Round 1 deliverables

- Research pack: `research/`
- Tableau dashboard and documentation: `dashboard/`
- Automation workflow and evidence: `poc/`
- LangSmith monitoring evidence: `langsmith/`
- Cost and timeline estimate: `cost_timeline_estimate.md`
- Round 1 presentation and decision: added after the teaching-staff presentation

## Repository structure

```text
clinical-trial-eligibility-copilot/
├── data/
│   ├── raw/trialgpt/                 # Public source annotation data
│   ├── processed/                    # Prepared data, predictions, metrics
│   ├── data_dictionary.md
│   └── validation_rules.md
├── research/                         # Sector research, risks, use cases
├── notebooks/                        # Data exploration notebook
├── mvp/                              # Streamlit MVP
├── src/                              # Screening, validation, metrics code
├── tests/                            # Deterministic and integration tests
├── dashboard/                        # Tableau workbook, screenshot, documentation
├── poc/                              # n8n workflow, samples, screenshots, documentation
├── langsmith/                        # Trace screenshots and monitoring note
├── evaluation/                       # Initial evaluation analysis
├── compliance/                       # Expanded for Round 2
├── feedback/                         # Round 1 decision added after presentation
├── cost_timeline_estimate.md
├── requirements.txt
└── .env.example
```

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Create your local environment file

```bash
cp .env.example .env
```

Add your own OpenAI API key and, if using monitoring, LangSmith API key. Never
commit `.env`.

For explicit human-review queue submission, set `N8N_REVIEW_WEBHOOK_URL` to the
approved n8n webhook URL. The MVP reads this value only when the user clicks the
queue-submission button.

## Run the Streamlit MVP

```bash
streamlit run mvp/app.py
```

The MVP supports dataset cases from the processed synthetic data and custom
synthetic cases. Screening runs only after an explicit button click. A successful
`UNKNOWN` or `NOT_APPLICABLE` result can then be sent to n8n only after a second
explicit click. `MET` and `NOT_MET` results are not submitted by the MVP.

Synthetic MVP review submissions include the patient summary, trial title,
criterion type and text, and cited evidence sentence IDs so the coordinator can
inspect the criterion and the cited patient-summary sentences. Ground truth is
evaluation-only and is never sent by Streamlit. The current increment does not
add new Notion property mappings.

Client-side duplicate prevention applies only to the current Streamlit session.
Production use requires server-side idempotency using `queue_id` or another
stable key.

## Run the screening POC

Run a small smoke test and write a new output file:

```bash
python -m src.run_screening \
  --limit 3 \
  --output data/processed/smoke_run.csv
```

Run the full locked 120-assessment evaluation:

```bash
python -m src.run_screening \
  --output data/processed/llm_predictions_full.csv
```

The screening output includes the predicted label, evidence-sentence IDs,
rationale, model and prompt version, response ID, latency, token usage, and
run status.

## Generate dashboard metrics

The completed evaluation evidence in this repository was generated from
`data/processed/llm_predictions_gpt41_v2.csv`.

```bash
python -m src.metrics \
  --predictions data/processed/llm_predictions_gpt41_v2.csv
```

This writes assessment-level results and headline metrics into
`data/processed/`.

See [dashboard documentation](dashboard/dashboard_documentation.md) for the
metrics, data sources, dashboard navigation, and interpretation boundaries.

## Run the automation POC

1. Import `poc/n8n_workflow.json` into n8n.
2. Create a Notion connection and share the review-queue database with it.
3. In the Webhook node, select **Using Respond to Webhook Node**.
4. Click **Listen for test event**.
5. POST the representative payload from `poc/sample_input.json` to the test
   URL.
6. Verify that the appropriate route is returned and that qualifying cases are
   added to the n8n and Notion review queues.

See [POC documentation](poc/poc_documentation.md) for workflow logic,
screenshots, reproduction steps, and production limitations.

## Monitoring

LangSmith traces provide trace-level evidence of model inputs, structured
outputs, prompt version, token usage, latency, and metadata for public
synthetic test cases.

See [LangSmith monitoring documentation](langsmith/monitoring_documentation.md)
and the screenshots in `langsmith/screenshots/`.

## Evaluation results

The completed 120-assessment GPT-4.1 evaluation produced:

| Metric | Result |
| --- | ---: |
| Exact agreement | 72.5% (87/120) |
| Unsafe MET rate | 5.9% (1/17) |
| UNKNOWN recall | 92.3% (48/52) |
| Review rate | 59.2% |
| Median latency | 1.01 seconds |
| Total estimated API cost | $0.2556 |
| Estimated cost per assessment | ~$0.0021 |

Exact agreement alone is not treated as sufficient evidence of safety.
`MET` predictions that conflict with a reference `NOT_MET` result receive
specific attention, while uncertain results are intentionally routed for human
review.

## Limitations

- Public synthetic data only; no real patient data.
- Criterion-level assessment is not a complete patient-level eligibility
  decision.
- The POC does not replace clinical judgment, protocol review, or informed
  consent processes.
- Notion and n8n are demonstration components, not validated clinical systems.
- The Streamlit MVP uses public synthetic data and submits only explicit review
  actions; it is not a production queue integration.
- Production integrations should normally use authorised source-system
  references or deep links instead of copying unnecessary patient data, with
  approved access controls and data minimisation.
- Client-side duplicate prevention is session-scoped; production requires
  server-side idempotency.
- Production use would require clinical validation, secure integration,
  privacy and security controls, access management, retention policies, and
  formal governance.

## License and data note

The repository contains project code and derived evaluation artifacts. Review
the provenance and licence of the underlying TrialGPT-derived source data
before any reuse outside this educational capstone context.
