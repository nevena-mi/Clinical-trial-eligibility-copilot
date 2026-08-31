# Automation POC Documentation

## Purpose

This n8n proof of concept receives a criterion-level screening result and routes
cases needing human review into a review queue. It demonstrates an auditable
handoff from the AI screening output to a human coordinator; it does not make
an automated eligibility or enrolment decision.


## Workflow

```text
Receive screening result
→ Classify review route
→ Queue required?
  ├─ Yes → Create review-queue record
  │       → Create a database page
  │       → Confirm review queued
  └─ No  → Confirm no queue needed
```


## Tools

| Tool | Role |
| --- | --- |
| Python screening POC | Produces structured criterion-level screening results |
| n8n | Receives results, applies routing logic, and returns a response |
| n8n Data Table | Stores queued-review records during the POC |
| Notion database | Displays human-review cases in a simple coordinator queue |

## Input

The webhook receives a JSON screening result containing, among other fields:

- `source_annotation_id`
- `patient_id`
- `trial_id`
- `criterion_id`
- `criterion_type`
- `predicted_label`
- `ground_truth_label`
- `rationale`
- `evidence_sentence_ids`
- `model`
- `prompt_version`

`poc/sample_input.json` contains a representative example.

## Routing logic

The **Classify review route** node assigns a route based on the screening result.

| Condition | Route | Queue required |
| --- | --- | --- |
| Predicted label is `UNKNOWN` or `NOT_APPLICABLE` | `HUMAN_REVIEW` | Yes |
| Reference is `NOT_MET` but model predicts `MET` | `SAFETY_ESCALATION_EVALUATION_ONLY` | Yes |
| Other results | No routine review route | No |

The safety-escalation rule is evaluation-only. It uses the reference label to demonstrate how unsafe outcomes could be detected during testing; a production workflow cannot depend on ground truth, which is unavailable in live use.

## Queued-case record

For queued cases, the workflow:

1. Inserts a record into the n8n `eligibility_review_queue` data table.
2. Creates a corresponding Notion database page.
3. Sets the queue status to `OPEN`.
4. Returns a JSON confirmation to the webhook caller.

The Notion record includes the review case title, queue status, route, patient ID, trial ID, criterion ID, predicted label, rationale, evidence references, model, prompt version, and queue ID.

## Evidence

Screenshots in `poc/screenshots/` show:

- A routed case in the n8n queue.
- A case that does not require a queue.
- The working true and false workflow branches.
- Rows created in the Notion review-queue database.

## How to reproduce

1. Import `poc/n8n_workflow.json` into n8n.
2. Create or select credentials for the Notion connection.
3. Share the Notion review-queue database with that connection.
4. Set the Webhook node response mode to **Using Respond to Webhook Node**.
5. In test mode, click **Listen for test event** in the Webhook node.
6. Send the example payload from `poc/sample_input.json` to the displayed test URL.
7. Verify that a qualifying case creates an n8n queue record and a Notion page.
8. Send a non-qualifying case and verify that it receives the no-queue response.

## Limits versus production

- The POC uses public synthetic data only.
- The test webhook URL is not a production integration endpoint.
- Notion is used as a simple demonstration queue, not a validated clinical workflow system.
- There is no authentication, role-based reviewer assignment, SLA management, duplicate prevention, audit-log retention policy, or secure clinical-system integration.
- Human review remains mandatory before any clinical action.