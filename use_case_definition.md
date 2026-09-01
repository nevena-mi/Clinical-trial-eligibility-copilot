# Use Case Definition

## 1. Use case overview

**Use case:** Human-reviewed AI support for criterion-level clinical-trial eligibility prescreening

**Sector:** Clinical research and pharmaceutical development

**Target organisation:** A mid-sized multi-site clinical research organisation or clinical research site network managing multiple active studies with a relatively lean recruitment and trial-coordination team.

**System type:** Generative AI decision-support system with rule-based workflow routing, human review and model monitoring.

**Round 1 decision:** **KEEP**

The industry and use case remain unchanged after Round 1. Round 2 deepens the original concept through a user-facing MVP, expanded business analysis, compliance documentation and a phased deployment plan.

## 2. Business problem statement

Clinical-trial coordinators must compare patient information with detailed inclusion and exclusion criteria before a patient can progress towards enrolment.

Patient information is often narrative, incomplete or distributed across different records. Trial protocols may contain many criteria that depend on diagnoses, medications, laboratory values, medical history, dates and contextual details.

The current prescreening process is therefore:

- repetitive and time-consuming;
- difficult to scale across multiple active trials;
- dependent on manual interpretation;
- difficult to document consistently;
- vulnerable to missing information and overlooked exclusion criteria.

An incorrect positive match may create operational and patient-safety risk. At the same time, overly cautious screening may exclude potentially suitable patients or generate an unmanageable review workload.

The business need is to reduce the administrative preparation and prioritisation burden while preserving traceability, escalation of uncertainty and mandatory human clinical review.

## 3. Representative company profile

This capstone uses an illustrative mid-sized multi-site clinical research organisation or clinical research site network rather than a named real company.

| Attribute | Target profile |
|---|---|
| Industry | Clinical research and pharmaceutical development |
| Organisation size | Mid-sized organisation operating multiple research sites and managing several active clinical studies |
| Primary users | Clinical-trial coordinators, recruitment teams and authorised clinical reviewers |
| Current process | Manual comparison of patient summaries with trial inclusion and exclusion criteria |
| Data environment | Patient information, trial protocols and operational data held in separate systems or documents |
| Main constraint | Clinical decisions require qualified human review and clear accountability |
| Main opportunity | Faster preparation, prioritisation and documentation of eligibility assessments |
| Technology maturity | Existing digital records and trial-management tools, but limited AI-supported criterion assessment |

The target organisation is assumed to have an approved clinical-data environment, defined user roles and an established clinical review process. These production capabilities are not implemented in the current POC.

Trial sponsors and CROs may act as buyers, implementation partners or operational stakeholders, but they do not necessarily have direct access to patient records. Any production workflow must respect the data-access responsibilities of the participating clinical sites.

## 4. Proposed AI solution

The Clinical-Trial Eligibility Copilot performs an initial criterion-level comparison between a supplied patient summary and an individual clinical-trial criterion.

For each criterion, the system produces one of four structured labels:

| Label | Meaning |
|---|---|
| `MET` | The supplied evidence supports that the patient passes this criterion |
| `NOT_MET` | The supplied evidence supports that the patient does not pass this criterion |
| `UNKNOWN` | The available evidence is insufficient to determine whether the patient passes the criterion |
| `NOT_APPLICABLE` | The criterion clearly does not apply in the supplied patient–trial context |

For inclusion criteria, `MET` means that the required condition is supported. For exclusion criteria, MET means the evidence explicitly shows that the stated exclusion does not apply; NOT_MET means that the exclusion applies. A criterion-level `MET` result does not mean that the patient is eligible for the complete trial.

Example:

Exclusion criterion: History of severe psychiatric illness

- Explicitly no such history → `MET`
- Such history documented → `NOT_MET`
- No information available → `UNKNOWN`

So `MET` always means “passes this individual criterion,” regardless of whether it is an inclusion or exclusion criterion.

A `MET` label does not by itself mean that a patient is eligible. For example, meeting an exclusion criterion may indicate a potential reason for exclusion.

The output also contains:

- a short rationale;
- references to supporting evidence sentences;
- patient, trial and criterion identifiers;
- model and prompt-version metadata;
- latency and token-usage information.

The system does not make a final eligibility or enrolment decision. It prepares a structured assessment that an authorised clinical reviewer can inspect, challenge and confirm.

The MVP evaluates a supplied patient–trial–criterion combination. It does not search health records for potential participants, recommend trials or rank candidates.

### Solution components

| Component | Role |
|---|---|
| Python screening service | Validates the input and prepares criterion-level model requests |
| GPT-4.1 | Produces the structured criterion assessment, rationale and evidence references |
| n8n | Receives screening results and applies review-routing logic |
| n8n Data Table | Stores review-queue records in the POC |
| Notion | Provides a demonstration human-review queue |
| LangSmith | Records model traces, prompt metadata, outputs, latency and token usage |
| User-facing MVP | Allows a user to submit or select a screening case and inspect the result |

### System classification by function

The proposed solution combines:

- **generative AI**, for interpreting narrative patient information and criterion text;
- **decision support**, because it prepares evidence for an authorised reviewer;
- **workflow automation**, for routing uncertain cases;
- **human-in-the-loop control**, because clinical decisions remain with authorised personnel;
- **monitoring and observability**, for inspecting model behaviour and performance.

## 5. Intended workflow

1. Minimum-necessary authorised patient information and trial criteria are provided to the system.
2. Required input fields are validated and normalised.
3. The AI compares the supplied patient evidence with one criterion.
4. The model returns a structured label, rationale and evidence references.
5. The workflow checks whether the case requires priority review.
6. `UNKNOWN` and `NOT_APPLICABLE` results are routed to the review queue.
7. An authorised clinical reviewer examines the assessment and original evidence.
8. Only a human-confirmed outcome may be written back to an approved clinical system.
9. Model calls, routing events and reviewer actions are logged under an approved retention policy.

### Round 2 MVP boundary

The MVP will implement the user-facing criterion assessment and basic error handling using public synthetic data.

The existing POC demonstrates:

- structured screening output;
- n8n routing;
- review-queue creation;
- Notion records;
- LangSmith model monitoring.

It does not implement live EHR, clinical data warehouse or CTMS integration. Notion is a demonstration queue rather than a validated clinical workflow system.

## 6. Human-review logic

Human confirmation and priority routing represent two different controls.

### Human confirmation

All AI-generated assessments must remain inspectable. No clinical action, final eligibility decision or enrolment decision may be based on an assessment without confirmation by an authorised human reviewer.

### Priority clinical-review routing

A case must be routed to a priority clinical-review queue when:

- the model returns `UNKNOWN`;
- the model returns `NOT_APPLICABLE`;
- relevant patient evidence is missing;
- patient information is contradictory;
- an exclusion-related concern requires clinical interpretation;
- configured safety or uncertainty rules are triggered.

### Validation and technical failures

The following conditions must produce a visible error or technical-review state rather than a normal clinical result:

- the output does not follow the required schema;
- evidence references are invalid;
- the model call fails;
- the workflow or queue integration fails.

A technical failure must not be presented as a successful assessment or successful queue submission.

During evaluation, a reference label may be used to detect unsafe model outcomes. This is evaluation-only logic because ground-truth labels are not available during live production use.

The production workflow must therefore use missing evidence, uncertainty, validation failures and clinically approved rules rather than reference labels.

## 7. Key stakeholders and interests

| Stakeholder | Primary interests |
|---|---|
| Clinical-trial coordinator | Faster preparation, clear evidence, manageable review workload and easy documentation |
| Principal investigator or authorised clinical reviewer | Patient safety, correct interpretation and final clinical authority |
| Clinical operations lead | Recruitment speed, workload, throughput, quality and operational KPIs |
| Trial sponsor or CRO leadership | Shorter recruitment timelines, controlled costs and scalable processes |
| Quality and regulatory team | Traceability, validation, documented controls and audit readiness |
| Data protection officer | Lawful processing, data minimisation, retention controls and patient rights |
| IT and information-security team | Secure integration, identity management, access control and system reliability |
| Patients and trial candidates | Privacy, fair treatment, understandable processes and protection from inappropriate automated decisions |

## 8. Success criteria

The following targets are proposed for a controlled pilot. They are not claims about current production performance.

### Safety and model quality

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Reliable escalation | `UNKNOWN` and `NOT_APPLICABLE` cases correctly routed to human review | 100% |
| Human control | Cases that trigger a clinical action without authorised human confirmation | 0 |
| Structured transparency | Completed assessments containing a valid label, rationale, evidence references, model and prompt metadata | 100% |
| Uncertainty recognition | Recall for reference `UNKNOWN` cases on the controlled evaluation dataset | At least 90% |
| Safety performance | Unsafe positive matches on the Round 2 holdout dataset | 0 before pilot recommendation; every occurrence must be investigated |

The Round 2 holdout is an internal comparison set rather than a completely untouched external validation dataset.

### Workflow reliability

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Request reliability | Valid requests completed without unhandled system or integration errors | At least 99% |
| Failure visibility | Detected failures presented as successful assessments or successful queue submissions | 0 |
| Routing reliability | Review-required cases that create or clearly fail to create the expected queue event | 100% |

### Reviewer usefulness

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Reviewer usefulness | Assessments rated useful or very useful on a defined reviewer survey scale | At least 80% |
| Evidence usefulness | Reviewers able to locate the cited evidence without re-reading the complete patient summary | To be established during pilot discovery |

The reviewer sample size and rating scale must be defined before the controlled pilot begins.

### Business value

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Screening efficiency | Median coordinator preparation time for a complete patient–trial prescreening review compared with the manual baseline | At least 25% reduction |
| Review workload | Time spent reviewing routed cases and correcting model outputs | Measured and reported alongside time savings |

### Pilot decision principle

A pilot should proceed towards broader deployment only if it demonstrates measurable time savings without weakening safety, traceability or human accountability.

A fast model response alone is not sufficient evidence of business value. The pilot must measure the complete coordinator workflow, including review-queue effort and correction of model outputs.

## 9. Round 1 evidence

Round 1 evaluated GPT-4.1 on 120 locked criterion-level assessments derived from public synthetic TrialGPT data.

| Metric | Round 1 result |
|---|---:|
| Exact agreement with reference labels | 72.5% |
| Unsafe `MET` rate | 5.9% (1 of 17 reference `NOT_MET` cases) |
| `UNKNOWN` recall | 92.3% (48 of 52 cases) |
| Human-review routing rate | 59.2% |
| Median model latency | 1.01 seconds |
| Estimated model cost per assessment | Approximately $0.0021 |

The estimated model cost reflects the token-pricing assumptions used at the time of the Round 1 calculation.

These results indicate that the model can recognise many cases with insufficient evidence and can produce structured, inspectable outputs.

However, the unsafe positive result and substantial review rate show that the system is not suitable for autonomous eligibility decisions. Human review, safety-focused evaluation and workflow-level validation remain mandatory.

The unsafe `MET` result was calculated from only 17 reference `NOT_MET` cases. The observed 5.9% should therefore not be interpreted as a stable estimate of production safety performance.

## 10. Out-of-scope boundaries

The following capabilities are outside the current project scope:

- final clinical-trial eligibility decisions;
- automatic patient enrolment;
- replacement of clinical-trial coordinators, investigators or medical reviewers;
- diagnosis, treatment or medical advice;
- autonomous exclusion of patients from clinical-trial opportunities;
- use of real identifiable patient data in the capstone;
- candidate retrieval from health records;
- trial recommendation or ranking;
- population-level patient–trial matching;
- production EHR, clinical data warehouse or CTMS integration;
- production identity and access management;
- automated write-back to clinical systems;
- full clinical validation or medical-device certification;
- production-scale cybersecurity, availability and disaster-recovery controls;
- guarantee that all eligible patients or relevant trials will be identified;
- use of evaluation ground truth as a live production routing signal.

The MVP is a decision-support demonstration using public synthetic data. It must not be used for real clinical or enrolment decisions.

## 11. Data boundaries

Round 1 and the initial Round 2 MVP use public synthetic TrialGPT-derived data.

The project does not require or authorise:

- names;
- contact details;
- insurance identifiers;
- medical-record numbers;
- directly identifiable health information;
- live hospital or sponsor-system access.

A real pilot involving patient data would require:

- confirmed controller and processor responsibilities;
- an identified GDPR Article 6 legal basis and Article 9 condition;
- data minimisation;
- access and security controls;
- documented retention rules;
- processor and subprocessor assessment;
- international-transfer assessment where relevant;
- a Data Protection Impact Assessment before patient data is processed.

The applicable legal basis and safeguards would require confirmation by the organisation's data protection officer and legal advisers. This project does not provide formal legal advice.

## 12. Evolution from Round 1

### Decision

**KEEP — clinical research sector and criterion-level eligibility prescreening use case**

No substantive teaching-staff feedback requiring a sector or use-case change was recorded. The KEEP decision was based on the demonstrated relevance of the business problem, feasibility of the criterion-level prototype and the identified need for deeper safety, business and compliance analysis.

An additional market-evidence dashboard was identified as a useful extension. It should use cited real-world evidence to examine:

- existing AI-supported patient–trial matching and prescreening products;
- when relevant solutions entered the market;
- organisations using or partnering around these solutions;
- reported operational or recruitment benefits;
- remaining market and implementation gaps.

This dashboard will be developed after the core MVP and required Round 2 deliverables are verified.

### Round 1 evidence demonstrated

- a relevant business problem;
- existing market activity in AI-supported patient–trial matching;
- a criterion-level GPT-4.1 evaluation;
- a stakeholder dashboard;
- n8n review routing;
- a Notion demonstration queue;
- LangSmith monitoring;
- an indicative pilot cost and timeline.

### Round 2 development

Round 2 retains the same industry and use case but deepens the project through:

1. a functional user-facing MVP that makes the core AI capability directly testable;
2. reproducible model and prompt comparison;
3. ROI calculations over 12 and 36 months using explicit operational assumptions;
4. systematic assessment of regulatory, technical, ethical and operational risks;
5. EU AI Act and GDPR analysis based on the proposed intended use and production data flow;
6. a realistic AI product-management and client-pilot plan with user stories, acceptance criteria, decision gates and a Definition of Done;
7. a phased POC-to-pilot-to-production strategy defining stakeholders, KPIs and commercialisation options;
8. a cited market-evidence dashboard after the core deliverables are complete.

The objective is not to claim clinical readiness. It is to determine whether the use case is sufficiently valuable, safe, transparent and governable to justify a controlled pilot.

## 13. Final use-case statement

The Clinical-Trial Eligibility Copilot is a human-reviewed AI decision-support system that compares a supplied patient summary with an individual clinical-trial criterion.

The current MVP processes public synthetic information only. It produces structured labels, rationales and evidence references, routes uncertain cases to authorised reviewers and records model behaviour for inspection.

A future production deployment could process minimum-necessary authorised patient information only after the required governance, legal, security, integration and validation conditions are met.

Its purpose is to help clinical-research teams prepare, prioritise and document criterion-level eligibility reviews more efficiently while preserving human clinical judgement, traceability and accountability.