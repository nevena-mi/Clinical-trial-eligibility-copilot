# Use Case Proposals: AI for Clinical-Trial Operations

## Client context

The hypothetical client is a medium-sized German CRO supporting pharmaceutical and biotechnology sponsors with clinical-trial operations. The use cases below are decision-support tools: qualified research staff retain responsibility for protocol interpretation, formal screening, patient contact and enrolment decisions.

| Use case | Primary users | Business value | Exact output | Scope and limitation |
|---|---|---|---|---|
| **1. Transparent clinical-trial eligibility pre-screening copilot** **(selected capstone use case)** | Research coordinators, clinical-research associates and site study teams | Reduces repetitive first-pass chart review; makes missing information and reasons for exclusion explicit; creates a consistent review record | For each patient–criterion pair: `MET`, `NOT_MET` or `UNKNOWN`; supporting evidence from the patient summary; concise rationale; mandatory human-review flag. At patient level: “potentially suitable for further review” or “not suitable based on documented criteria.” | Uses synthetic patient summaries and selected public trial criteria. It does not determine final eligibility, enrol a participant, contact patients or infer missing clinical facts. |
| **2. Protocol feasibility and recruitment-risk assessment** | Feasibility leads, study-start-up managers and sponsor-facing clinical-operations managers | Helps assess whether a proposed protocol is likely to find sufficient potential participants at available sites before a study opens; identifies overly restrictive or data-dependent criteria | Trial-level feasibility briefing: number and proportion of synthetic records that are potentially compatible, excluded or unknown for each criterion; criteria with the highest exclusion or missing-information rate; a human-review recommendation. | A POC can use a synthetic cohort only. A real decision would require representative local patient data, validated cohort definitions and site-level recruitment context. |
| **3. Screening exception and evidence-quality review** | Senior research coordinators, quality managers and clinical-operations leads | Focuses human effort on the most uncertain or risky AI outputs; supports quality assurance and audit readiness | Exception queue containing records with `UNKNOWN`, conflicting evidence, missing required data or low-confidence rationale; criterion, evidence, reason for escalation, reviewer decision and timestamp. Dashboard metrics show exception volume and recurring data gaps. | Does not resolve clinical uncertainty automatically. Reviewers verify the original record and the current approved protocol. |

## Selected use case

The capstone will implement **Use Case 1: Transparent clinical-trial eligibility pre-screening copilot**.

It provides the strongest balance of meaningful LLM use, measurable quality and a realistic CRO workflow. The AI must interpret free-text patient summaries against free-text eligibility criteria, cite the available evidence and abstain where the information is insufficient. This cannot be replaced reliably by a simple dashboard or fixed keyword rules.

Uses Cases 2 and 3 remain realistic future extensions. Use Case 2 builds on the same criterion-level output for study feasibility; Use Case 3 uses the same outputs to create a governed human-review and quality-monitoring workflow.