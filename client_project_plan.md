# Client Project Plan

## Integrated Clinical-Trial Eligibility Copilot Pilot

## 1. Project overview

This plan describes a realistic client project for introducing the Clinical-Trial Eligibility Copilot into a controlled clinical-research workflow.

The target client is an illustrative mid-sized, multi-site clinical research organisation or clinical research site network managing several active clinical studies.

The project will integrate criterion-level AI prescreening into an authorised human-review workflow. The system will prepare structured assessments, identify uncertainty and present supporting evidence. It will not make final eligibility or enrolment decisions.

The proposed project covers discovery, governance, integration, validation and a controlled pilot over approximately 18 weeks. Broader production deployment would be a separate decision and implementation phase.

## 2. Product vision

Enable clinical-research teams to prepare and document patient–trial eligibility reviews more efficiently while preserving human clinical judgement, traceability, privacy and accountability.

## 3. Business problem

Clinical-trial coordinators manually compare patient information with detailed inclusion and exclusion criteria.

This process is:

- time-consuming;
- difficult to scale across multiple studies;
- dependent on manual interpretation;
- vulnerable to missing or contradictory information;
- difficult to document consistently;
- associated with operational and patient-safety risk when exclusions are overlooked.

The proposed solution should reduce preparation effort and improve review consistency without replacing authorised clinical decision-makers.

## 4. Project objective

Design, integrate and evaluate a controlled AI-assisted prescreening workflow that:

- compares authorised patient evidence with individual trial criteria;
- provides structured labels, rationales and evidence references;
- routes uncertain and exceptional cases for priority review;
- keeps all clinical decisions under authorised human control;
- records model, workflow and reviewer activity;
- demonstrates measurable operational value;
- provides evidence for a STOP, ADAPT or PROCEED decision.

## 5. Project assumptions

| Area | Assumption |
|---|---|
| Organisation | The client operates multiple clinical research sites |
| Pilot scope | One therapeutic area, a limited number of studies and selected sites |
| Users | A defined group of coordinators and authorised clinical reviewers |
| Source systems | The client has an approved EHR, clinical data warehouse, CTMS or controlled data-extract process |
| Trial criteria | Pilot protocols and criteria can be converted into a controlled structured format |
| Data access | Only authorised, minimum-necessary patient information is processed |
| Human control | No eligibility or enrolment action occurs without human confirmation |
| Governance | A product owner, clinical owner, data protection officer and information-security representative are available |
| Validation | The client can provide a controlled reference set and reviewer time |
| Integration | Required APIs, FHIR interfaces or controlled data exports are technically available |
| Delivery | Work is organised in two-week sprints with governance decision gates |
| Timeline | Discovery through pilot decision takes approximately 18 weeks |
| Production | Full deployment is outside this project and would require a separate 3–6 month or longer phase |

These assumptions must be validated during discovery. Material changes may affect scope, cost and timeline.

## 6. Project scope

### In scope

- discovery and mapping of the current prescreening workflow;
- selection of pilot sites, studies and users;
- definition of intended use and human responsibilities;
- approved patient and trial-data access;
- data minimisation and normalisation;
- criterion-level AI assessment;
- structured labels, rationale and evidence references;
- uncertainty and safety routing;
- authorised human review;
- reviewer confirmation or correction;
- model and prompt versioning;
- audit and monitoring records;
- limited EHR, data warehouse or CTMS integration;
- controlled user acceptance testing;
- controlled human-reviewed pilot;
- pilot KPI measurement;
- final pilot decision report.

### Out of scope

- autonomous eligibility decisions;
- automatic patient enrolment;
- diagnosis or treatment recommendations;
- patient-facing medical advice;
- autonomous exclusion of potential participants;
- replacement of coordinators or investigators;
- organisation-wide rollout;
- all therapeutic areas and studies;
- unrestricted access to complete patient records;
- unsupervised write-back to clinical systems;
- automated patient contact;
- full historical-data migration;
- full clinical validation;
- medical-device certification;
- production commercial rollout.

## 7. Intended production workflow

1. An authorised workflow identifies a patient–trial pair requiring prescreening.
2. Approved source systems provide minimum-necessary patient evidence and trial criteria.
3. The integration layer validates access, provenance, completeness and format.
4. Patient evidence is normalised and linked to individual trial criteria.
5. The AI service creates a structured criterion-level assessment.
6. Validation rules check the output schema and evidence references.
7. Uncertain, contradictory or exceptional cases enter a priority-review queue.
8. An authorised clinical reviewer inspects the AI assessment and original evidence.
9. The reviewer confirms, corrects or rejects the assessment.
10. Only the human-confirmed outcome may be written to the approved clinical workflow.
11. Model, workflow and reviewer events are recorded under an approved logging and retention policy.

## 8. Delivery approach

The project uses a hybrid agile approach:

- two-week delivery sprints;
- prioritised user stories;
- testable acceptance criteria;
- sprint reviews with client representatives;
- documented risks, decisions and dependencies;
- formal governance gates before real patient data or broader use;
- a controlled pilot before any production recommendation.

Agile delivery does not override clinical, security, privacy or regulatory approval requirements.

## 9. Governance and responsibilities

| Role | Main responsibility |
|---|---|
| Executive sponsor | Funding, strategic direction and escalation |
| Product owner | Scope, backlog priorities and business acceptance |
| Clinical owner | Intended use, clinical rules, safety boundaries and reviewer authority |
| Clinical-trial coordinators | Workflow discovery, user testing and operational feedback |
| Principal investigator or clinical reviewer | Clinical validation and final decision authority |
| Project manager | Planning, dependencies, risks, milestones and communication |
| AI lead | Model, prompt, evaluation and monitoring design |
| Data engineer | Source integration, transformation and data quality |
| Application engineer | User interface, workflow and system integration |
| Quality and regulatory lead | Validation, change control and audit readiness |
| Data protection officer | GDPR assessment, DPIA and processing controls |
| Information-security lead | Security architecture, access control and incident requirements |
| System owners | EHR, data warehouse, CTMS and interface approvals |

## 10. Jobs-to-be-Done

### Clinical-trial coordinator

**Functional job:** Prepare an accurate patient–trial review without manually reconstructing every criterion assessment.

**Emotional job:** Feel confident that uncertainty and important evidence are visible.

**Social job:** Be seen as reliable, efficient and accountable.

### Authorised clinical reviewer

**Functional job:** Review AI-supported assessments against original evidence and retain final decision authority.

**Emotional job:** Trust that the system supports rather than obscures clinical judgement.

**Social job:** Demonstrate responsible and traceable oversight.

### Clinical operations lead

**Functional job:** Understand whether the workflow improves throughput without increasing safety or review risk.

**Emotional job:** Feel confident that operational improvements are measurable and governed.

**Social job:** Demonstrate responsible innovation to leadership, sponsors and regulators.

### Quality, privacy and security stakeholders

**Functional job:** Verify that the system operates within approved controls and produces sufficient evidence for review and audit.

**Emotional job:** Avoid hidden processing, uncontrolled model behaviour and unclear accountability.

**Social job:** Demonstrate that innovation is introduced through a controlled process.

## 11. User stories and acceptance criteria

### US-01 — Select a patient–trial assessment

**As a clinical-trial coordinator, I want to open an authorised patient–trial case so that I can review the relevant eligibility criteria.**

#### Acceptance criteria

- The user is authenticated and authorised.
- Only approved studies and patient records are available.
- The system displays the correct patient, trial and criterion identifiers.
- The source and timestamp of the supplied information are recorded.
- Unauthorised users cannot access the case.
- Access is logged.

### US-02 — Review patient evidence and criterion text

**As a clinical-trial coordinator, I want to see the relevant patient evidence beside the trial criterion so that I can understand the basis of the assessment.**

#### Acceptance criteria

- The criterion text and type are displayed.
- Minimum-necessary patient evidence is displayed.
- Evidence provenance is available.
- Missing required information is identified.
- The interface does not expose unrelated patient information.

### US-03 — Generate a criterion-level assessment

**As a clinical-trial coordinator, I want the system to prepare a structured criterion-level assessment so that I can reduce manual preparation work.**

#### Acceptance criteria

- The output uses an approved label.
- The output contains a concise rationale.
- The output contains valid evidence references.
- The model and prompt versions are recorded.
- Ground-truth or reviewer-reference labels are not supplied to the model.
- Invalid outputs fail safely and are not presented as valid assessments.

### US-04 — Identify uncertainty

**As an authorised clinical reviewer, I want missing and contradictory evidence to be visible so that uncertainty is not converted into an unsupported conclusion.**

#### Acceptance criteria

- Insufficient evidence produces `UNKNOWN`.
- Non-applicable criteria produce `NOT_APPLICABLE`.
- Contradictory evidence is visibly flagged.
- The system does not invent missing patient facts.
- Uncertainty triggers the approved priority-review route.

### US-05 — Review supporting evidence

**As an authorised clinical reviewer, I want to inspect the evidence supporting an AI assessment so that I can verify or challenge it.**

#### Acceptance criteria

- Evidence references correspond to supplied patient information.
- Invalid evidence references are rejected.
- The reviewer can access the original authorised evidence.
- The rationale does not replace the underlying evidence.
- The assessment remains identifiable by patient, trial, criterion, model and prompt version.

### US-06 — Confirm or correct an assessment

**As an authorised clinical reviewer, I want to confirm, correct or reject an AI assessment so that final authority remains with a qualified person.**

#### Acceptance criteria

- The reviewer can confirm, correct or reject the assessment.
- Corrections require a reason or reviewer note.
- The original AI output remains preserved.
- The reviewer identity and timestamp are recorded.
- No clinical workflow update occurs before reviewer confirmation.

### US-07 — Route priority-review cases

**As a clinical-trial coordinator, I want uncertain or exceptional cases to enter a priority queue so that they receive appropriate attention.**

#### Acceptance criteria

- `UNKNOWN` and `NOT_APPLICABLE` results are routed.
- Clinically approved safety conditions are routed.
- Technical failures use an error state rather than a normal clinical result.
- Queue success or failure is visible.
- Failed queue submissions are not reported as successful.
- Duplicate queue records are prevented or visibly identified.

### US-08 — Monitor model and workflow behaviour

**As an AI or quality lead, I want model and workflow events to be inspectable so that errors and changes can be investigated.**

#### Acceptance criteria

- Model, prompt and application versions are recorded.
- Input and output metadata are recorded under approved controls.
- Latency, token usage and failures are measurable.
- Workflow and queue events can be correlated with the assessment.
- Monitoring access is restricted.
- Logging follows approved retention and minimisation rules.

### US-09 — Monitor pilot performance

**As a clinical operations lead, I want a pilot dashboard so that I can evaluate value, safety, workload and reliability.**

#### Acceptance criteria

- The dashboard reports agreed pilot KPIs.
- Model-quality and workflow metrics are distinguished.
- Time savings include review and correction effort.
- Unsafe outcomes are individually reviewable.
- Metric definitions, sources and periods are documented.
- Results can be filtered by approved pilot dimensions without exposing unnecessary patient data.

### US-10 — Exercise data-governance controls

**As a data protection or security stakeholder, I want processing controls to be documented and testable so that patient information is handled lawfully and securely.**

#### Acceptance criteria

- Controller and processor responsibilities are documented.
- The legal basis and Article 9 condition are assessed.
- A DPIA is completed before patient-data processing.
- Role-based access is tested.
- Data minimisation and retention rules are implemented.
- Processor, subprocessor and transfer arrangements are reviewed.
- Security and privacy incidents have defined escalation paths.

### US-11 — Make a pilot decision

**As the product owner and executive sponsor, we want a documented pilot evaluation so that we can decide whether to stop, adapt or proceed.**

#### Acceptance criteria

- All agreed KPIs are reported.
- Safety events and technical failures are investigated.
- Reviewer feedback is summarised.
- Actual costs and resource use are compared with assumptions.
- Compliance and security conditions are reviewed.
- Remaining risks and limitations are explicit.
- The decision and rationale are documented.

## 12. Non-functional requirements

### Safety

- No clinical action without authorised human confirmation.
- Invalid or incomplete outputs fail safely.
- Uncertainty is visible and routed appropriately.
- Ground truth is never used as a live production routing signal.

### Privacy

- Only minimum-necessary patient information is processed.
- Access is role-based.
- Data use, retention and deletion rules are documented.
- Monitoring does not create an uncontrolled copy of patient data.

### Security

- Data is encrypted in transit and at rest.
- Credentials are stored in approved secret-management systems.
- Access and administrative activity are logged.
- Security incidents have defined escalation procedures.

### Reliability

- Valid requests have a target completion rate of at least 99%.
- All detected failures are visibly reported.
- Integration failures do not erase completed assessments.
- Queue failures are not presented as successful submissions.

### Traceability

- Every assessment records the case, model, prompt and application version.
- Original AI outputs remain available after reviewer correction.
- Evidence references can be checked against their authorised source.
- Material configuration changes follow change control.

### Usability

- Coordinators can understand the result without interpreting raw model output.
- Clinical reviewers can access the supporting evidence.
- Error messages provide an appropriate next action.
- Pilot users receive training before live use.

## 13. Definition of Ready

A user story is ready for implementation when:

- the business purpose is clear;
- the intended user is identified;
- acceptance criteria are testable;
- required data and interfaces are identified;
- clinical and safety implications have been reviewed;
- privacy and security dependencies are known;
- responsible stakeholders are available;
- unresolved decisions do not prevent implementation;
- the product owner has prioritised the story.

A story involving patient data is not ready until the required data-access, privacy and security approvals are confirmed.

## 14. Definition of Done

### User-story Definition of Done

A user story is complete when:

- all acceptance criteria are satisfied;
- automated and manual tests pass;
- clinical review is completed where relevant;
- privacy and security controls are verified;
- monitoring and error handling are included;
- documentation is updated;
- no unresolved critical defect remains;
- the product owner accepts the result.

### Sprint Definition of Done

A sprint is complete when:

- accepted stories meet their Definition of Done;
- the integrated increment is demonstrated;
- tests and validation evidence are recorded;
- risks, decisions and dependencies are updated;
- documentation is current;
- unfinished work returns to the backlog;
- the sprint review is completed.

### Pilot Definition of Done

The controlled pilot is complete when:

- the agreed pilot population and period are completed;
- all planned KPI data are available;
- safety events and failures are investigated;
- reviewer feedback is documented;
- actual cost and effort are reported;
- privacy, security and compliance observations are reviewed;
- the pilot report is approved;
- a STOP, ADAPT or PROCEED decision is documented.

## 15. Prioritised backlog

### Must have

- approved intended use and pilot scope;
- authorised source-data access;
- minimum-necessary data extraction;
- criterion-level AI assessment;
- structured labels, rationale and evidence;
- uncertainty and error handling;
- human-review workflow;
- reviewer confirmation and correction;
- role-based access;
- model and prompt versioning;
- audit and monitoring records;
- controlled validation dataset;
- pilot KPIs;
- DPIA and security review;
- user training;
- controlled pilot;
- final pilot report and decision.

### Should have

- integration with the existing coordinator worklist;
- controlled write-back of human-confirmed outcomes;
- duplicate-case detection;
- workload and SLA monitoring;
- configurable clinical-routing rules;
- pilot dashboard;
- reviewer feedback capture in the workflow.

### Could have

- additional therapeutic areas;
- trial ranking;
- candidate-retrieval support;
- richer analytics;
- automated reminder notifications;
- advanced explanation visualisation.

### Will not have in this project

- autonomous eligibility decisions;
- automated enrolment;
- patient-facing medical advice;
- organisation-wide deployment;
- full clinical-system replacement;
- unrestricted use across all studies.

## 16. Sprint plan and timeline

The proposed timeline assumes two-week sprints. Detailed dates and staffing will be confirmed after discovery.

| Sprint | Weeks | Main objective | Principal outputs |
|---|---:|---|---|
| Sprint 1 | 1–2 | Discovery and scope | Current-state map, intended use, pilot scope, stakeholders, baseline KPIs |
| Sprint 2 | 3–4 | Governance and solution design | Data-flow design, architecture, DPIA initiation, security requirements, validation plan |
| Sprint 3 | 5–6 | Data integration | Approved data extract, data-quality rules, provenance and normalisation |
| Sprint 4 | 7–8 | AI and workflow integration | Criterion assessment, structured output, review routing, monitoring |
| Sprint 5 | 9–10 | Validation and user acceptance | Model evaluation, integration testing, security testing, UAT and training |
| Sprint 6 | 11–12 | Controlled pilot launch | Approved release, initial pilot operation and incident monitoring |
| Sprint 7 | 13–14 | Pilot operation | Workflow measurement, reviewer feedback and issue correction |
| Sprint 8 | 15–16 | Pilot completion | Completed pilot cohort, KPI collection and preliminary findings |
| Sprint 9 | 17–18 | Evaluation and decision | Final report, risk review and STOP / ADAPT / PROCEED decision |

## 17. Decision gates

### Gate 1 — Scope and feasibility

**Timing:** End of Week 2

Proceed only if:

- intended use is approved;
- pilot users, sites and studies are identified;
- source-data access appears feasible;
- baseline measures can be collected;
- no fundamental legal or operational blocker is identified.

### Gate 2 — Governance and design approval

**Timing:** End of Week 4

Proceed only if:

- target architecture is approved;
- privacy and security requirements are defined;
- DPIA work is sufficiently advanced;
- validation and human-review responsibilities are clear;
- integration dependencies are accepted.

### Gate 3 — Technical readiness

**Timing:** End of Week 8

Proceed only if:

- authorised data can be processed correctly;
- structured assessments pass validation;
- review routing works;
- monitoring and audit records are available;
- critical technical defects are resolved.

### Gate 4 — Pilot go/no-go

**Timing:** End of Week 10

Proceed only if:

- validation and UAT criteria are met;
- safety and failure handling are accepted;
- privacy, security and quality approvals are complete;
- pilot users are trained;
- rollback and incident procedures are available.

### Gate 5 — Deployment recommendation

**Timing:** End of Week 18

Decide:

- **STOP** — value, safety or feasibility is insufficient;
- **ADAPT** — revise scope, model, workflow or controls and repeat a limited pilot;
- **PROCEED** — prepare a separately approved production-deployment phase.

## 18. Pilot KPIs

### Business value

- median preparation time per complete patient–trial review;
- coordinator time saved;
- number of assessments processed;
- review and correction effort;
- cost per completed assessment.

### Model and safety quality

- unsafe positive outcomes;
- `UNKNOWN` recall;
- exact agreement;
- invalid-output rate;
- evidence-reference validity;
- reviewer correction rate.

### Workflow performance

- priority-review routing accuracy;
- queue completion time;
- failed integration requests;
- duplicate records;
- unhandled errors.

### User value

- reviewer usefulness rating;
- coordinator adoption;
- user-reported confidence;
- training and support issues.

### Governance

- unauthorised-access events;
- unresolved audit-log gaps;
- retention or deletion failures;
- privacy or security incidents;
- unapproved model or prompt changes.

## 19. Pilot success criteria

A recommendation to proceed requires:

- at least 25% reduction in median coordinator preparation time;
- 100% routing of `UNKNOWN` and `NOT_APPLICABLE` cases;
- zero clinical actions without authorised human confirmation;
- zero unresolved unsafe positive outcomes;
- 100% of completed assessments containing the required structured fields;
- at least 99% of valid requests completing without an unhandled error;
- 100% of detected failures reported visibly;
- at least 80% of reviewers rating assessments useful or very useful;
- no unresolved critical privacy, security or regulatory issue;
- evidence that benefits remain after review and correction effort is included.

Failure to meet one criterion does not automatically require project cancellation, but it must prevent an unconditional production recommendation.

## 20. Dependencies

- availability of clinical and operational subject-matter experts;
- access to approved source systems and interfaces;
- quality and structure of patient and protocol data;
- availability of a controlled reference dataset;
- reviewer capacity;
- information-security approval;
- completion of privacy and regulatory assessments;
- vendor and processor agreements;
- availability and stability of the selected model service;
- agreement on pilot KPI definitions.

## 21. Project risks

Detailed risks will be maintained in `roi_risk_assessment.md`.

Primary project risks include:

- delayed data access;
- incomplete or inconsistent source data;
- insufficient reviewer capacity;
- unsupported model conclusions;
- unsafe positive assessments;
- excessive review workload;
- workflow integration failure;
- privacy or security non-compliance;
- unclear regulatory classification;
- user resistance;
- vendor dependency;
- schedule expansion caused by governance or integration requirements.

## 22. Change and decision management

The project will maintain:

- a prioritised backlog;
- sprint review notes;
- a decision log;
- an assumptions register;
- a risk and issue register;
- versioned model and prompt records;
- documented acceptance evidence.

A material change to intended use, data scope, autonomy, user group or system integration requires renewed clinical, privacy, security and regulatory review.

## 23. Project deliverables

- approved use-case and intended-purpose statement;
- current-state workflow map;
- target architecture and data-flow design;
- data dictionary and data-quality rules;
- DPIA and processing documentation;
- security and access-control requirements;
- integrated criterion-assessment service;
- human-review workflow;
- model and prompt evaluation report;
- monitoring and audit design;
- user-acceptance evidence;
- training materials;
- pilot dashboard;
- pilot KPI report;
- risk and issue register;
- final STOP / ADAPT / PROCEED recommendation.

## 24. Post-pilot production phase

A decision to proceed does not mean immediate organisation-wide deployment.

A separate production phase would likely require an additional three to six months or longer for:

- broader system integration;
- additional studies and sites;
- production infrastructure;
- operational support;
- formal validation;
- expanded security testing;
- regulatory and quality-management activities;
- change management;
- service-level agreements;
- production monitoring;
- controlled rollout.

The production timeline would be estimated after the pilot confirms the final scope, architecture, value and regulatory requirements.