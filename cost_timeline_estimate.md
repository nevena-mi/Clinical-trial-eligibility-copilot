# Cost and Timeline Estimate

## Cost basis

The completed synthetic evaluation processed 120 criterion-level assessments using GPT-4.1.

| Metric | Observed value |
|---|---:|
| Assessments | 120 |
| Total model cost | $0.2556 |
| Average cost per assessment | $0.0021 |
| Median latency | 1.01 seconds |

## Illustrative pilot operating cost

Assumption: 100 synthetic or approved pilot patient summaries per month,
screened against 3 candidate trials with 20 criteria each.

100 patients × 3 trials × 20 criteria = 6,000 assessments/month

| Item | Estimate |
|---|---:|
| Model/API assessments | 6,000/month |
| Estimated model/API cost | ~$12.60/month |
| n8n, Notion, LangSmith | Existing/free-tier POC tooling; production licensing not estimated |
| Human review | Required; effort depends on routed-case volume and clinical workflow |

This model/API estimate is directional only. It excludes production integration,
clinical validation, information-security review, user training, and any
enterprise platform licences. These, rather than raw LLM usage, would dominate
a real deployment budget.

## Indicative pilot timeline

| Phase | Duration | Output |
|---|---:|---|
| Scope and clinical-rule review | Week 1 | Approved pilot scope and escalation rules |
| Data mapping and controlled integration | Weeks 2–3 | Approved input format and secure test workflow |
| Workflow, monitoring, and reviewer-queue configuration | Weeks 3–4 | Review routing, audit trail, dashboard |
| Controlled human-reviewed pilot | Weeks 5–6 | Agreement, unsafe-outcome, and workload evidence |
| Evaluation and decision | Weeks 7–8 | Pilot report and STOP / CONTINUE / PIVOT decision |

## Boundary

This is a decision-support pilot using public synthetic data. It is not a
production clinical-decision system and does not authorise automated eligibility
or enrolment decisions.