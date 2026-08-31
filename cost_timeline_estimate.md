# Cost and Timeline Estimate

## Scope and basis

This estimate covers a controlled, human-reviewed pilot of the Clinical-trial
eligibility copilot. The POC uses public synthetic TrialGPT-derived data and
does not include a production clinical-system deployment.

The completed synthetic evaluation processed 120 criterion-level assessments
using GPT-4.1.

| Observed metric | Value |
| --- | ---: |
| Assessments processed | 120 |
| Total model cost | $0.2556 |
| Average cost per assessment | $0.0021 |
| Median latency | 1.01 seconds |

## Upfront pilot cost estimate

This is an illustrative internal-effort estimate, not a vendor quotation.

| Workstream | Assumption | Estimated cost |
| --- | --- | ---: |
| Clinical scope and rule review | 40 hours × €90/hour | €3,600 |
| Data mapping and controlled test integration | 80 hours × €85/hour | €6,800 |
| Workflow and review-queue configuration | 48 hours × €80/hour | €3,840 |
| Evaluation, dashboard, and documentation | 40 hours × €80/hour | €3,200 |
| Privacy and security review | 24 hours × €110/hour | €2,640 |
| Training and pilot handover | 16 hours × €75/hour | €1,200 |
| Subtotal |  | €21,280 |
| Contingency | 10% of subtotal | €2,128 |
| **Estimated upfront pilot cost** |  | **€23,408** |

## Illustrative monthly operating cost

Assumption: 100 approved pilot patient summaries per month, screened against
3 candidate trials with 20 criteria each.

**100 patients × 3 trials × 20 criteria = 6,000 assessments per month**

| Item | Assumption | Estimate |
| --- | --- | ---: |
| Model/API assessments | 6,000 criterion-level assessments/month | 6,000 |
| Estimated model/API cost | 6,000 × ~$0.0021 | ~$12.60/month |
| n8n, Notion, and LangSmith | Existing or free-tier POC tooling | Not estimated |
| Human review | Depends on the routed-case volume and clinical workflow | Not estimated |

The raw LLM cost is small relative to the effort required for clinical
validation, secure integration, governance, and reviewer operations.

## Assumptions

| Assumption | Rationale and boundary |
| --- | --- |
| Public synthetic data only | No real patient data is processed in the POC. |
| Human review is mandatory | The system supports prioritisation and documentation; it does not make final eligibility or enrolment decisions. |
| Existing tools can be used in the pilot | n8n, Notion, Tableau, and LangSmith are treated as existing or free-tier tools for this estimate. |
| No enterprise integration is included | EHR, CTMS, identity-management, audit-retention, and enterprise licensing work are excluded. |
| Three trials and 20 criteria per trial | A simple scenario for estimating the assessment volume. |
| 100 patient summaries per month | A directional controlled-pilot volume, not a demand forecast. |
| Blended day-rate assumptions | Labour rates are illustrative internal or contractor-equivalent rates and must be validated before procurement. |

## Indicative pilot timeline

| Phase | Duration | Output |
| --- | --- | --- |
| Scope and clinical-rule review | Week 1 | Approved pilot scope and escalation rules |
| Data mapping and controlled integration | Weeks 2–3 | Approved input format and secure test workflow |
| Workflow, monitoring, and reviewer-queue configuration | Weeks 3–4 | Review routing, audit trail, and dashboard |
| Controlled human-reviewed pilot | Weeks 5–6 | Agreement, unsafe-outcome, and workload evidence |
| Evaluation and decision | Weeks 7–8 | Pilot report and **STOP / CONTINUE / PIVOT** decision |

## Boundary

This is a decision-support pilot using public synthetic data. It is not a
production clinical-decision system and does not authorise automated
eligibility or enrolment decisions.