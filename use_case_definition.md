# Use Case Definition

## 1. Use case overview

**Use case:** Human-reviewed AI support for criterion-level clinical-trial eligibility prescreening

**Sector:** Clinical research and pharmaceutical development

**Scenario client:** HelixBridge Clinical Research Network GmbH, a fictional mid-sized multi-site clinical research site network.

**System type:** Generative AI decision-support system with rule-based workflow routing, human review and model monitoring.

**Round 1 decision:** **KEEP**

The industry and use case remain unchanged after Round 1. Round 2 has deepened the original concept through a functional user-facing MVP, explicit human-review submission, model comparison, expanded business analysis, compliance documentation and a phased deployment plan.

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

This capstone uses HelixBridge Clinical Research Network GmbH, a clearly fictional company, to provide one consistent real-world planning scenario. All organisation characteristics and volumes remain assumptions requiring validation during readiness.

| Attribute | Target profile |
|---|---|
| Industry | Clinical research and pharmaceutical development |
| Organisation size | Four research sites, 12 coordinators and eight actively recruiting trials |
| Primary users | Clinical-trial coordinators, recruitment teams and authorised clinical reviewers |
| Current process | Manual comparison of patient summaries with trial inclusion and exclusion criteria |
| Work volume | Approximately 600 unique patient–trial combinations per month |
| Pilot scope | One moderate-complexity trial, two sites, four coordinators and approximately 150 reviews per month |
| Data environment | Approved clinical source environment, protocol repository, CTMS and organisational identity management |
| Main constraint | Clinical decisions require qualified human review and clear accountability |
| Main opportunity | Faster preparation, prioritisation and documentation of eligibility assessments |
| Technology maturity | Existing digital records and trial-management tools, but limited AI-supported criterion assessment |

The target organisation is assumed to have an approved clinical-data environment, defined user roles and an established clinical review process. These production capabilities are not implemented in the current POC.

The engagement is a consulting-led implementation. HelixBridge owns its data, operational records, production accounts and final decisions. Its Head of Clinical Operations owns the workflow; the provider implements and supports the technology but does not operate the clinical review queue.

Trial sponsors and CROs may act as funding partners or operational stakeholders, but they do not necessarily have direct access to patient records. Any production workflow must respect the data-access responsibilities of participating clinical sites.

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

A criterion-level `MET` means that the patient passes that individual criterion. It never establishes eligibility for the complete trial.

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
| Configured model service | GPT-4.1 powers the current MVP; GPT-5.6 Sol was evaluated as a candidate but performed worse on the locked synthetic cohort |
| n8n | Receives screening results and applies review-routing logic |
| n8n Data Table | Stores review-queue records in the POC |
| Notion | Provides a demonstration human-review queue |
| LangSmith | Provides development traces for synthetic evaluation; production observability requires separate approval |
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
5. An authorised coordinator examines every assessment against the original evidence and confirms or overrides it.
6. `UNKNOWN`, `NOT_APPLICABLE`, conflicting and otherwise designated high-risk cases receive additional escalation to a senior reviewer or investigator.
7. Technical and integration failures remain separate from clinical-review routing.
8. Only a human-confirmed outcome may be written back to an approved clinical system.
9. Model calls, routing events and reviewer actions are logged under an approved retention policy.

### Round 2 MVP status and boundary

The MVP implements user-facing criterion assessment, controlled error handling and explicit queue submission using public synthetic data.

The completed demonstration includes:

- structured screening output;
- n8n routing;
- review-queue creation;
- Notion records;
- LangSmith model monitoring.
- session-state protection against stale results and duplicate queue submission.

It does not implement live EHR, clinical data warehouse or CTMS integration. Notion is a demonstration queue rather than a validated clinical workflow system.

## 6. Human-review logic

Human confirmation and priority routing represent two different controls.

### Human confirmation

All AI-generated assessments must remain inspectable. No clinical action, final eligibility decision or enrolment decision may be based on an assessment without confirmation by an authorised human reviewer.

### Priority clinical-review routing

A case receives additional priority escalation when:

- the model returns `UNKNOWN`;
- the model returns `NOT_APPLICABLE`;
- missing or contradictory evidence results in an uncertain output;
- an exclusion-related concern meets a clinically approved escalation rule;
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
| Reliable escalation | `UNKNOWN`, `NOT_APPLICABLE`, invalid and failed results safely handled | 100% |
| Human control | Cases that trigger a clinical action without authorised human confirmation | 0 |
| Structured transparency | Valid outputs with complete evidence and configuration provenance | At least 95% |
| Review-routing performance | Recall for cases requiring additional review | Threshold approved clinically before pilot execution |
| Safety performance | Unsafe-error rate | Threshold approved clinically before pilot execution; every occurrence investigated |
| Safety governance | Unresolved critical safety events | 0 |

The locked synthetic evaluation cohort is an internal comparison set rather than a completely untouched external validation dataset.

### Workflow reliability

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Request reliability | Valid requests completed without unhandled system or integration errors | At least 95% |
| Failure visibility | Detected failures presented as successful assessments or successful queue submissions | 0 |
| Routing reliability | Review-required cases that create or clearly fail to create the expected queue event | 100% |

### Reviewer usefulness

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Reviewer usefulness | Assessments rated useful or very useful on a defined reviewer survey scale | At least 80% |
| Evidence usefulness | Reviewers able to locate the cited evidence without re-reading the complete patient summary | To be established during pilot discovery |
| Adoption | Assigned trained users actively following the workflow | At least 80% |

The reviewer sample size and rating scale must be defined before the controlled pilot begins.

### Business value

| Outcome | Measure | Proposed pilot target |
|---|---|---:|
| Screening efficiency | Median coordinator preparation time for a complete patient–trial prescreening review compared with the manual baseline | At least 25% reduction |
| Review workload | Time spent reviewing routed cases and correcting model outputs | Measured and reported alongside time savings |
| Privacy and security | Material breach or unresolved critical finding | 0 |

### Pilot decision principle

A pilot should proceed towards broader deployment only if it demonstrates measurable time savings without weakening safety, traceability or human accountability.

A fast model response alone is not sufficient evidence of business value. The pilot must measure the complete coordinator workflow, including review-queue effort and correction of model outputs.

## 9. Current synthetic evaluation evidence

The project evaluated GPT-4.1 and GPT-5.6 Sol on the same 120 locked criterion-level assessments derived from public synthetic TrialGPT data.

| Metric | GPT-4.1 baseline | GPT-5.6 Sol candidate |
|---|---:|---:|
| Exact agreement with reference labels | 72.5% | 65.0% |
| Unsafe `MET` cases among 17 reference `NOT_MET` cases | 1 | 1 |
| `UNKNOWN` recall | 48/52 | 51/52 |
| Human-review routing rate | 59.2% | 72.5% |
| Median model latency | 1.01 seconds | 2.48 seconds |
| Estimated cost for 120 assessments | $0.2556 | $0.5957 |

The estimated model cost reflects the token-pricing assumptions used at the time of the Round 1 calculation.

These results show that both models can produce structured, inspectable outputs and recognise many cases with insufficient evidence. They also show that selecting a more expensive model did not improve overall agreement or remove unsafe errors.

However, the unsafe positive result and substantial review rate show that the system is not suitable for autonomous eligibility decisions. Human review, safety-focused evaluation and workflow-level validation remain mandatory.

Each unsafe result was calculated from only 17 reference `NOT_MET` cases. The observed rate must not be interpreted as a stable estimate of production safety performance.

GPT-4.1 remains the configured MVP model. Prompt improvement is planned, but no improved figure will be reported until a new frozen prompt has been evaluated on the complete locked cohort. Because this cohort has been used repeatedly during development, it is a locked synthetic evaluation cohort rather than a fully untouched holdout. The pilot requires a separate, independently adjudicated local validation set.

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

The capstone MVP and model evaluations use public synthetic TrialGPT-derived data.

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
7. a phased POC-to-pilot-to-production strategy defining stakeholders, KPIs and commercialisation options.

The objective is not to claim clinical readiness. It is to determine whether the use case is sufficiently valuable, safe, transparent and governable to justify a controlled pilot.

## 13. Final use-case statement

The Clinical-Trial Eligibility Copilot is a human-reviewed AI decision-support system proposed for HelixBridge Clinical Research Network GmbH. It compares a supplied patient summary with an individual clinical-trial criterion.

The current MVP processes public synthetic information only. It produces structured labels, rationales and evidence references. Every result requires human confirmation; uncertain and designated high-risk cases receive additional escalation.

A future production deployment could process minimum-necessary, preferably pseudonymised patient information in a client-controlled or client-approved EU environment only after the required governance, legal, security, integration and validation conditions are met.

Its purpose is to help clinical-research teams prepare, prioritise and document criterion-level eligibility reviews more efficiently while preserving human clinical judgement, traceability and accountability.
