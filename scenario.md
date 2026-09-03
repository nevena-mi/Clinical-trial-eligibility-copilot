# Client and Delivery Scenario

## Clinical-Trial Eligibility Copilot

**Document status:** Canonical planning scenario  
**Scenario date:** 3 September 2026  
**Client:** HelixBridge Clinical Research Network GmbH  
**Client status:** Fictional company created for this project  
**Primary market:** Germany and the European Union

> All company characteristics, operating volumes and discovery findings in this document are hypothetical planning assumptions. They provide a consistent basis for the business case, compliance assessment, deployment plan and presentation. They must not be presented as measured results from a real client.

---

## 1. Purpose of This Scenario

This document defines the common client and delivery scenario for the Clinical-Trial Eligibility Copilot project. It will be used as the reference when aligning the ROI and risk assessment, strategic deployment plan, GDPR documentation, EU AI Act assessment and client presentation.

The proposed solution supports criterion-level prescreening. It analyses available patient information against trial inclusion or exclusion criteria, produces a structured label and rationale, cites supporting evidence and routes uncertain cases for review.

The system is decision support only. A qualified human remains responsible for confirming every assessment and for all patient-contact, eligibility and enrolment decisions.

---

## 2. Client Profile

HelixBridge Clinical Research Network GmbH is a fictional mid-sized, multi-site clinical research organisation operating four research sites in Germany.

### 2.1 Operating profile

| Attribute | Planning assumption |
|---|---:|
| Research sites | 4 |
| Clinical research coordinators | 12 |
| Active recruiting trials | 8 |
| Patient–trial prescreening reviews | Approximately 600 unique patient–trial combinations per month |
| Average preparation and criteria-review time | Approximately 30 minutes per review |
| Current operating model | Predominantly manual prescreening |

The network recruits participants for sponsor-funded clinical trials across several therapeutic areas. Coordinators review structured and narrative patient information, locate the applicable protocol criteria, record their interpretation and raise uncertain cases with investigators or senior clinical reviewers.

### 2.2 Existing technology environment

For planning purposes, HelixBridge is assumed to have:

- a clinical trial management system (CTMS);
- approved access to relevant clinical source systems or an authorised clinical data repository;
- a controlled protocol and trial-document repository;
- organisational identity and access management;
- established privacy, information-security and clinical-quality functions;
- no production AI capability currently integrated into prescreening.

The exact products, interfaces, data availability and contractual restrictions remain to be confirmed during the readiness assessment.

---

## 3. Problem Statement

Patient–trial prescreening is clinically important but operationally repetitive. Coordinators must interpret complex protocol criteria while moving between patient records, trial documents and local tracking tools.

The current process creates three connected problems.

### 3.1 Coordinator capacity

At the assumed operating volume, 600 patient–trial combinations per month at 30 minutes each represent approximately 300 hours of preparation and criteria-review work every month. A patient assessed against three trials counts as three reviews. This work reduces the time available for patient communication, source verification, investigator coordination and trial delivery.

### 3.2 Consistency and traceability

Different coordinators may interpret or document the same criterion differently. Rationales and source references are not always captured in a uniform form, making review, handover and quality assurance more difficult.

### 3.3 Safety and recruitment quality

Missing information, ambiguous wording or complex exclusion criteria can be overlooked. This can result in inappropriate progression of a candidate, unnecessary review work or failure to identify a potentially suitable candidate.

The proposed AI support is intended to provide a structured second pass—not to replace clinical judgement. Expected value must therefore be assessed across efficiency, consistency and safety rather than model accuracy alone.

---

## 4. Pre-Proposal Discovery

The scenario assumes that a limited pre-proposal discovery has already been completed. Its purpose was to establish whether the problem is material enough to justify a controlled pilot. It was not a full technical, clinical, legal or security assessment.

### 4.1 Discovery activities

| Activity | Participants | Hypothetical finding |
|---|---|---|
| Executive interview | COO or Head of Clinical Operations | Recruitment capacity, cross-site consistency and responsible AI adoption are strategic priorities |
| Workflow interviews | Four coordinators from two sites | Prescreening preparation takes approximately 30 minutes per patient–trial review and involves repeated navigation between systems |
| Clinical review | Principal investigator or medical lead | Exclusion criteria, missing evidence and ambiguous cases require explicit escalation and must never be resolved autonomously |
| Technical interview | IT and data representative | CTMS and clinical-data integration appear feasible, but interfaces, data quality and identity matching require assessment |
| Privacy and compliance interview | DPO or compliance representative | Processing real patient information requires a documented legal basis, DPIA, data minimisation, approved processors and controlled access |
| Baseline process review | Operations and quality representatives | Variation in documentation and missing-data handling supports testing a standardised, evidence-linked workflow |

### 4.2 Initial discovery conclusion

The opportunity is credible enough to justify a paid readiness assessment and limited pilot. The discovery does not yet establish:

- verified transaction volumes or time savings;
- attributable improvement in recruitment;
- production data quality or integration effort;
- legal approval to process patient data;
- clinical safety or subgroup performance;
- a final implementation price or positive ROI.

These points remain formal validation requirements before full deployment.

---

## 5. Proposed Delivery Scenario

### 5.1 Phase 1: Readiness assessment

The first contracted phase validates the assumptions used in this scenario.

It will:

- map the current prescreening workflow and establish a measured baseline;
- confirm review volumes, handling time, rework and escalation rates;
- select one suitable recruiting trial;
- inspect source-data availability, quality and provenance;
- define the intended purpose and prohibited uses;
- confirm GDPR roles, legal basis, Article 9 condition and DPIA requirements;
- assess security, architecture and integration constraints;
- define pilot acceptance criteria and a final pilot design.

The readiness phase ends with a `STOP`, `PIVOT` or `CONTINUE` recommendation.

### 5.2 Phase 2: Controlled pilot

| Pilot dimension | Scope |
|---|---|
| Trials | 1 actively recruiting, moderate-complexity trial selected during readiness |
| Sites | 2 |
| Coordinators/reviewers | 4 |
| Expected review volume | Approximately 150 patient–trial reviews per month |
| Assisted-use period | 6–8 weeks after validation and training |
| Decision authority | Qualified human reviewer |

The pilot begins in shadow mode, in which AI outputs do not influence operational decisions. It may progress to assisted use only after clinical, privacy, security and technical approval.

Every AI result must be confirmed by a coordinator in the ordinary prescreening workflow and remain connected to its source evidence. `UNKNOWN`, `NOT_APPLICABLE`, conflicting and otherwise defined high-risk results receive an additional escalation to a senior reviewer or investigator. Manual processing remains available throughout the pilot.

### 5.3 Phase 3: Conditional deployment

Full deployment is not included automatically. It is considered only if the pilot demonstrates:

- no unresolved critical safety event and no automated eligibility or exclusion decision;
- acceptable unsafe-error rate and review-routing recall against thresholds approved before the pilot;
- useful and reliable evidence references;
- manageable review workload;
- at least 25% net preparation-time reduction after including human-review effort;
- at least 80% active-user adoption among assigned pilot users;
- approved privacy, security and regulatory controls;
- credible financial value at the verified operating volume.

If approved, deployment expands in stages to four sites and approximately 600 patient–trial reviews per month. Each additional trial or therapeutic area is subject to controlled validation.

### 5.4 Intended production workflow

The production design is expected to replace the demonstration interfaces with authorised operational systems:

1. Minimum-necessary, preferably pseudonymised patient data is retrieved from the client’s clinical source environment; direct identifiers remain in the source system wherever possible.
2. Trial criteria are obtained from a controlled protocol repository.
3. The AI service produces a structured criterion-level assessment, rationale and evidence references.
4. Uncertain or designated high-risk outputs enter a controlled clinical-review queue.
5. A qualified reviewer checks the source information, confirms or overrides the result and records the decision.
6. Approved outcomes are written to the appropriate CTMS or operational system with an audit trail.

The production solution is hosted in a client-controlled or client-approved EU cloud environment and integrated with the client’s identity, security and audit controls. The current synthetic Streamlit interface, n8n workflow and Notion queue demonstrate the interaction pattern only. They are not the proposed systems of record for real patient deployment.

---

## 6. Provider Team

The provider uses a small multidisciplinary team. Roles may be combined where competence and independence requirements allow; not every role is full-time.

| Provider role | Primary responsibility | Typical involvement |
|---|---|---|
| AI consultant and product lead | Business requirements, scope, value case, governance and stakeholder coordination | Throughout the engagement |
| AI/data engineer | Data preparation, model workflow, evaluation, monitoring and technical documentation | High during build and validation |
| Integration engineer | Interfaces with approved clinical systems, CTMS, identity management and review workflow | Part-time, concentrated around integration |
| Privacy/security specialist | Privacy-by-design, processor assessment, threat modelling and security controls | At readiness and formal gates |
| Clinical subject-matter adviser | Criterion interpretation, safety review, evaluation design and escalation rules | Part-time throughout validation and pilot |

The provider is responsible for professional implementation, transparent limitations, agreed safeguards and the supporting evidence package. It does not assume the client’s statutory controller responsibilities or make clinical decisions. Detailed responsibilities and liability boundaries must be defined contractually and cannot remove mandatory provider obligations.

---

## 7. Client Team

| Client role | Primary responsibility |
|---|---|
| Executive sponsor | Funding, strategic direction and final investment decision |
| Clinical operations owner | Workflow ownership, operational acceptance and benefit realisation |
| Principal investigator or medical lead | Clinical safety criteria, escalation rules and residual clinical-risk acceptance |
| Pilot coordinators | Workflow testing, human review, usability feedback and issue reporting |
| IT/data representative | Source-system access, data quality, architecture and integration support |
| DPO/compliance representative | GDPR assessment, legal basis, DPIA, transparency and processor review |
| Information-security representative | Security requirements, access controls, vendor assurance and incident readiness |
| Quality/regulatory representative | Quality-management alignment, change control and regulatory assessment |

Client specialists participate according to project phase. Their involvement is primarily part-time, but named decision owners must be available at each approval gate.

---

## 8. Provider–Client Working Model

The provider and client operate as one governed delivery team while retaining distinct accountabilities.

### 8.1 Provider responsibilities

- design, configure, test and document the proposed solution;
- make assumptions, limitations and known failure modes explicit;
- provide technical and evaluation evidence;
- implement agreed safeguards and monitoring;
- train users and support controlled rollout;
- escalate risks and refrain from deployment when mandatory conditions are unmet.

### 8.2 Client responsibilities

- define and approve the intended operational use;
- provide authorised access to systems, data and subject-matter experts;
- validate clinical workflows and source-data meaning;
- determine the lawful basis and approve privacy and security controls;
- assign qualified reviewers and maintain human decision authority;
- accept residual risks and make phase-gate decisions.

### 8.3 Joint responsibilities

- maintain the project risk and decision logs;
- agree acceptance criteria before testing;
- investigate disagreements and incidents;
- measure benefits against the documented baseline;
- control changes to models, prompts, data sources and workflows;
- decide whether to stop, narrow, repeat or expand the pilot.

### 8.4 Engagement, ownership and commercial model

The engagement is a consulting-led implementation rather than the sale of a mature standalone clinical SaaS product.

- Readiness and pilot are separately scoped fixed-price engagements.
- Production deployment requires a separate approval and contract after the pilot gate.
- Ongoing monitoring, maintenance and support may be provided through an optional support retainer.
- The client owns its patient data, operational records, final decisions, production accounts and client-specific configurations.
- Reusable provider methods and components remain provider intellectual property, subject to an agreed client usage licence.
- The client contracts directly for underlying cloud, model and operational services where practical, preserving control and commercial transparency.
- The Head of Clinical Operations owns the live process and review queue; the provider supports the technology but does not operate the clinical decision process.

### 8.5 Phase-gate authority

Readiness, pilot and deployment each end with a documented `STOP`, `PIVOT` or `CONTINUE` decision. Progression is never automatic. The steering committee considers clinical safety, privacy, security, operational performance, adoption and financial evidence together; a commercial benefit cannot override an unmet mandatory safety or compliance condition.

---

## 9. Expected Value and Evidence Standard

The business proposition has three value dimensions.

### 9.1 Efficiency

Reduce net coordinator preparation and documentation time without creating an equal or larger review burden.

### 9.2 Consistency

Provide standardised criterion-level outputs, explicit handling of missing information, evidence-linked rationales and auditable human decisions across sites.

### 9.3 Safety and recruitment quality

Provide a structured second-pass review that may help identify missed exclusion concerns, unsupported conclusions and potentially suitable candidates.

No safety or recruitment improvement is assumed to be proven. These claims require controlled pilot evidence. Safety benefits should primarily be reported through quality and risk indicators rather than converted into speculative financial savings.

---

## 10. Model and Prompt Status

The project currently retains the validated model-comparison results and existing prompt as the evidence baseline. Planned prompt improvement does not change the figures until a new version has been frozen, evaluated on the complete locked cohort and documented.

Future performance numbers must identify:

- model configuration;
- prompt version;
- evaluation cohort;
- exact agreement and label-level performance;
- unsafe-error count;
- review-routing performance and workload;
- latency and cost;
- comparison with the current baseline.

This prevents anticipated improvements from being presented as achieved results.

---

## 11. Non-Negotiable Boundaries

The proposed system must not:

- determine final trial eligibility;
- automatically exclude or deprioritise a patient;
- enrol a participant;
- contact a patient without an approved human-controlled workflow;
- make a diagnosis or treatment recommendation;
- use ground-truth evaluation labels in live operations;
- expose patient data to unapproved models, logs or external systems;
- replace investigator or coordinator accountability.

Human confirmation, source verification, access control, auditability and manual fallback remain mandatory at every deployment stage.

---

## 12. Scenario Governance

This scenario is the shared reference for subsequent project documents. Assumptions may be changed only when the change is documented and propagated consistently across:

- `roi_risk_assessment.md`;
- `strategic_plan.md`;
- `gdpr_documentation.md`;
- `eu_ai_act_compliance.md`;
- the presentation and management plan.

The following values must remain labelled as hypothetical until validated by client evidence:

- organisation and team size;
- number of active trials;
- monthly review volume;
- current handling time;
- expected time reduction;
- incremental recruitment value;
- integration effort;
- project cost and ROI.
