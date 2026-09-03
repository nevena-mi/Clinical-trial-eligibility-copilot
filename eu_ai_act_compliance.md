# EU AI Act Compliance Assessment

## Clinical-Trial Eligibility Copilot

**Document status:** Client-facing preliminary assessment
**Assessment date:** 3 September 2026
**Prepared for:** HelixBridge Clinical Research Network GmbH
**Client status:** Fictional company created for this project
**Territorial scope:** Germany and potential later use in the European Union
**Commercial model:** Consulting-led implementation

> This is a project-level compliance assessment, not legal advice. HelixBridge must obtain qualified legal and regulatory confirmation before processing real patient data, starting assisted use or materially changing the intended purpose.

---

## 1. Executive Summary

The Clinical-Trial Eligibility Copilot supports clinical-research coordinators by comparing approved patient information with individual trial criteria. It generates a proposed criterion-level label, rationale and evidence references. Every output requires coordinator confirmation; uncertain and defined high-risk cases receive additional escalation.

### Preliminary classification

Under the restricted intended purpose assessed here, the system is preliminarily classified as:

> **A non-high-risk AI system under the EU AI Act, subject to applicable transparency, AI-literacy and general governance obligations.**

“Limited risk” may be used informally in a presentation, but it is not a general statutory classification in the AI Act. The legally clearer description is **non-high-risk**, with specific obligations assessed separately.

This conclusion is based on the following:

- the system is an AI system under Article 3;
- no Article 5 prohibited practice is part of the intended use;
- trial-recruitment support is not expressly listed in Annex III;
- the system is not currently intended for diagnosis, treatment, monitoring, prognosis or another medical purpose;
- it does not make final eligibility, exclusion, contact or enrolment decisions;
- qualified staff retain authority and must verify the source information.

The classification is conditional. Human review does not itself remove high-risk status. A new legal and regulatory assessment is mandatory if functionality, marketing, deployment or actual use changes.

### Compliance decision

The synthetic proof of concept may support planning and demonstration. It is not approved for real-patient use. A real-data pilot may proceed only after intended-purpose approval, MDR qualification, DPIA and lawful-basis confirmation, vendor and transfer review, security approval, local validation, AI-literacy training and technical enforcement of human control.

---

## 2. System and Intended Purpose

### 2.1 Intended use

The solution is intended to:

1. receive minimum-necessary, authorised patient information;
2. compare it with one controlled trial criterion at a time;
3. generate a proposed `MET`, `NOT_MET`, `UNKNOWN` or `NOT_APPLICABLE` label;
4. provide an AI-generated rationale and evidence references;
5. support coordinator preparation and documentation;
6. route uncertain or designated high-risk results for additional review.

### 2.2 Human decision model

Every result is confirmed by a coordinator in the ordinary prescreening workflow. `UNKNOWN`, `NOT_APPLICABLE`, conflicting and otherwise defined high-risk results receive an additional escalation to a senior reviewer or investigator.

Human review must be meaningful. Reviewers require adequate time, source access, training, authority to disagree, a usable override mechanism and protection from workload pressure that would turn confirmation into a rubber stamp.

### 2.3 Explicit prohibited uses

The system must not:

- determine final eligibility;
- automatically exclude, prioritise or deprioritise a patient;
- contact or enrol a candidate autonomously;
- diagnose, monitor, prognose or recommend treatment;
- make a solely automated decision with legal or similarly significant effect;
- infer emotion or protected characteristics;
- perform biometric identification or categorisation;
- use ground-truth evaluation labels in live operations;
- process patient information through unapproved systems or vendors.

### 2.4 Production boundary

The target production service runs in a client-controlled or client-approved EU environment. Approved clinical sources, protocol repositories and the CTMS remain authoritative. Direct identifiers stay within the client identity boundary wherever possible.

The Streamlit interface, n8n workflow, Notion queue and development tracing used in the synthetic MVP are demonstration components. They are not automatically approved for real-patient deployment.

---

## 3. Step-by-Step Risk Classification

### Step 1 — Is the solution an AI system?

**Yes.** It is a machine-based system that infers recommendations and generated text from patient and trial inputs. It therefore falls within the Article 3 definition.

### Step 2 — Does it involve an Article 5 prohibited practice?

**No, under the defined design.** It does not use manipulative, social-scoring, prohibited biometric, emotion-recognition or criminal-risk capabilities.

Article 5 remains part of change control. Prohibited functionality cannot be added through a feature request, model update or workflow integration.

### Step 3 — Is it high-risk under Article 6(1) as a regulated product or safety component?

**Not under the present intended purpose, subject to formal MDR review.**

The system is positioned as operational support for clinical-trial recruitment, not as software intended to diagnose, prevent, monitor, predict, prognose, treat or alleviate disease. It is not currently presented as a medical device or a safety component of one.

Healthcare context alone does not automatically make software a medical device. Qualification depends on the intended purpose expressed through functionality, instructions, claims and foreseeable use. Before a real-data pilot, the client and provider must document an MDR qualification assessment using current MDCG guidance.

If the purpose changes to clinical decision support or another medical purpose, Article 6(1), MDR classification, conformity assessment and the later application date for product-related high-risk requirements must be reassessed.

### Step 4 — Is the use listed in Annex III?

**Not expressly under the current private trial-recruitment use case.**

Annex III covers specified areas such as biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration and administration of justice. Recruiting participants for clinical trials is not employment recruitment, and the defined system does not determine access to healthcare.

Reassessment is required if the system is used by or for a public authority, determines access to an essential service, is repurposed for patient-care allocation or falls within a later amendment or authoritative interpretation.

### Step 5 — Does human review determine classification?

**No.** Classification depends on intended purpose, functionality and deployment context. Human oversight is an essential risk control but does not convert an otherwise high-risk system into a non-high-risk one.

### Step 6 — Do specific transparency duties apply?

**A conservative transparency approach is required.**

Coordinators must be clearly informed that:

- they are using an AI-assisted system;
- labels and rationales are generated by AI and may be wrong or incomplete;
- source verification and human confirmation are mandatory;
- outputs and overrides are logged under approved governance.

Patients do not interact directly with the AI in the defined workflow. If direct AI interaction is introduced, Article 50 disclosure duties must be reassessed. The provider must also assess with the underlying model provider whether machine-readable identification requirements for generated text apply to these internal outputs and how responsibilities are divided.

Public-facing GDPR information remains necessary even where Article 50 does not require a chatbot-style notice.

### Classification conclusion

The current intended use is preliminarily **non-high-risk** under the AI Act. This does not mean low operational or privacy risk. Health data, potential recruitment consequences and automation bias justify controls broadly aligned with high-risk system practices even where those practices are not legally mandatory.

---

## 4. Roles and Accountability

| Party | Preliminary role | Core responsibility |
|---|---|---|
| Consulting and integration provider | Likely AI-system provider or integrator, depending on branding and contract | Intended-purpose implementation, documentation, testing, instructions, controls and change support |
| HelixBridge | Deployer and GDPR controller; provider status remains possible depending on commissioning and branding | Approved use, human oversight, data access, local validation, monitoring and operational decisions |
| General-purpose model supplier | GPAI model provider and service supplier | Model-level documentation, contractual controls and applicable GPAI duties |
| Hosting and workflow suppliers | Technology suppliers/processors as applicable | Security, availability and contracted data handling |
| Coordinators and investigators | Human reviewers | Source verification, confirmation, override and escalation |
| DPO, security and quality functions | Independent control functions | Legal, privacy, security, quality and audit oversight |

Legal roles follow actual facts, not project labels. An organisation that substantially modifies, rebrands or changes the intended purpose of a system may acquire additional provider obligations. Contracts must define roles, but cannot contract out statutory responsibility.

---

## 5. Requirements for the Current Classification

### 5.1 AI literacy

Staff who operate, supervise or govern the system require role-appropriate AI literacy. Training must cover:

- intended and prohibited use;
- known error types and current evaluation results;
- uncertainty and non-applicability;
- source verification and evidence limitations;
- automation bias and effective override;
- privacy, security and incident reporting;
- when to stop processing and escalate.

Completion and refresher training should be recorded.

### 5.2 Transparency and instructions

The interface and user instructions must identify AI-generated outputs, describe limitations, require human confirmation and explain escalation and correction. Marketing, contracts, training and interface language must remain consistent with the restricted intended purpose.

### 5.3 Prohibited-practice controls

Change control must screen new capabilities and vendors against Article 5. Emotion recognition, manipulative patient interaction, prohibited biometric categorisation and other prohibited uses are outside scope.

### 5.4 General legal and governance duties

Non-high-risk classification does not displace:

- GDPR and national health-data requirements;
- confidentiality and clinical-trial obligations;
- information-security and processor requirements;
- contractual and professional responsibilities;
- MDR qualification when the intended purpose may be medical;
- workplace consultation or employment requirements where applicable.

### 5.5 Voluntary high-risk-style safeguards

HelixBridge should adopt proportionate controls associated with trustworthy high-risk systems:

- documented risk management;
- data-quality and provenance controls;
- technical documentation and versioning;
- event and decision logging;
- human-oversight design;
- measured accuracy, robustness and cybersecurity;
- post-deployment monitoring and incident handling;
- controlled change and rollback.

This is justified by the sensitivity and possible consequences of the use case, even if the statutory high-risk regime does not currently apply.

---

## 6. Reclassification Triggers

A documented reassessment is mandatory before any of the following:

| Trigger | Possible consequence |
|---|---|
| Final eligibility, exclusion or prioritisation becomes automated | Annex III, fundamental-rights and automated-decision assessment |
| Output materially determines access to healthcare | Possible essential-service/high-risk classification |
| Diagnosis, prognosis, monitoring or treatment functionality is added | Possible MDR and Article 6(1) high-risk classification |
| System is marketed with a medical intended purpose | MDR qualification and conformity assessment |
| Patient-facing conversational interface is introduced | Additional Article 50 transparency duties |
| Public-authority deployment is introduced | Annex III and fundamental-rights reassessment |
| Emotion, biometric or protected-trait inference is proposed | Article 5 and high-risk reassessment |
| Model, prompt, data source or routing changes materially | Performance, safety and substantial-modification assessment |
| Provider, branding or placing-on-market model changes | Provider-role and documentation reassessment |
| EU AI Act, Annex III or authoritative guidance changes | Classification and implementation update |

No material change may enter assisted or production use until the assessment and required validation are approved.

---

## 7. High-Risk Contingency Requirements

If later classified as high-risk, the programme must not rely on the present non-high-risk assessment. Before applicable placement on the market or use, the responsible parties would need to address, as applicable:

- continuous risk management;
- data and data-governance requirements;
- complete technical documentation;
- automatic record keeping and logs;
- instructions and information for deployers;
- effective human oversight;
- accuracy, robustness and cybersecurity;
- quality-management system;
- conformity assessment and declaration obligations;
- registration where required;
- post-market monitoring and serious-incident procedures;
- deployer monitoring, log retention and impact-assessment duties where applicable.

The precise obligations and application date depend on whether classification arises from Annex III or from integration into a regulated Annex I product.

---

## 8. Conformity Assessment Summary

### 8.1 Purpose

This section provides a proportionate internal conformity-readiness review. It is not an EU declaration of conformity, CE marking or notified-body assessment.

### 8.2 Current conclusion

| Question | Assessment |
|---|---|
| Is formal high-risk conformity assessment currently required? | Not under the present preliminary non-high-risk classification |
| Is the system approved for real-patient production use? | No |
| Can the synthetic POC support readiness planning? | Yes |
| Can a real-data pilot start immediately? | No; mandatory readiness conditions remain |
| Is MDR qualification complete? | No; required before real-data pilot |
| Are provider/deployer roles contractually finalised? | No |

### 8.3 Evidence available

- documented intended purpose and prohibited uses;
- synthetic-data architecture and user workflow;
- structured outputs and review routing;
- locked synthetic evaluation cohort;
- baseline and candidate model comparison;
- evidence that higher model cost did not improve agreement;
- explicit human-confirmation messaging;
- preliminary risk, GDPR and AI Act assessments.

### 8.4 Material gaps

- no client-specific data-flow and architecture approval;
- no completed MDR qualification;
- no final provider/deployer role allocation;
- no client-approved DPIA or lawful-basis decision;
- no vendor, subprocessor and transfer approval;
- no production security assessment;
- no independently adjudicated local clinical evaluation;
- no subgroup or site-level validation;
- no operational monitoring, incident and rollback evidence;
- no validated user training or human-factors assessment.

### 8.5 Readiness decision

> **Conditional pass for a readiness assessment only. No approval for assisted real-patient use or full deployment.**

### 8.6 Conditions before shadow mode

- intended use and prohibited uses signed by client and provider;
- MDR qualification documented;
- DPIA, legal basis and Article 9 condition approved;
- provider, deployer, controller and processor roles confirmed;
- suppliers, subprocessors and transfers approved;
- production-like security and access controls tested;
- minimum dataset and retention approved;
- local evaluation set and clinical thresholds approved;
- human confirmation and manual fallback technically enforced;
- all pilot users trained;
- no unresolved critical clinical, privacy or security finding.

### 8.7 Conditions before assisted mode

- shadow-mode safety and routing results meet approved thresholds;
- every safety-significant disagreement is clinically adjudicated;
- review workload permits meaningful human oversight;
- no material privacy, security or subgroup concern remains unresolved;
- clinical, quality, DPO, security and operational owners approve progression.

---

## 9. Technical Documentation Outline

The following structure should be maintained in the client’s governed repository.

1. **Document control**
   - owner, version, approvals, review date and change history
2. **System identification**
   - product name, configuration IDs, components, environments and suppliers
3. **Intended purpose and users**
   - intended use, prohibited use, users, populations, sites and trial scope
4. **Roles and legal classification**
   - provider/deployer analysis, AI Act classification and MDR qualification
5. **Architecture and integrations**
   - data sources, protocol repository, CTMS, identity, model, review and audit services
6. **Data governance**
   - field definitions, provenance, minimisation, quality, pseudonymisation and retention
7. **Model and prompt configuration**
   - model, prompt, parameters, structured schema, routing rules and version control
8. **Development and validation**
   - requirements, datasets, test design, results, errors, subgroup analysis and acceptance decisions
9. **Human oversight**
   - confirmation, escalation, override, training, workload and automation-bias controls
10. **Risk management**
    - hazards, likelihood, impact, controls, residual risk and phase gates
11. **Accuracy, robustness and cybersecurity**
    - performance metrics, failure modes, threat model, access, secrets, resilience and recovery
12. **Logging and traceability**
    - inputs, outputs, evidence, versions, reviewer actions, retention and audit access
13. **User instructions and transparency**
    - interface notices, limitations, operating procedure, patient information and support
14. **Monitoring and incidents**
    - KPIs, drift, complaints, incidents, suspension, investigation and notification
15. **Change and release control**
    - impact assessment, regression testing, approvals, deployment and rollback
16. **Third-party assurance**
    - contracts, subprocessors, locations, security evidence and transfer safeguards
17. **Compliance evidence**
    - DPIA, AI Act assessment, MDR decision, policies, approvals and audit records
18. **Decommissioning**
    - termination, data return/deletion, record retention and continuity plan

---

## 10. Implementation Responsibilities

| Action | Accountable owner | Timing |
|---|---|---|
| Approve intended purpose and boundaries | Executive sponsor and clinical owner | Readiness |
| Confirm AI Act and MDR classification | Quality/regulatory with legal counsel | Before real-data access |
| Confirm provider/deployer allocation | Legal and procurement | Before pilot contract |
| Complete DPIA and lawful-basis decision | Client DPO/controller | Before real-data access |
| Approve vendors and transfers | DPO, security and procurement | Before configuration |
| Define local validation and safety thresholds | Clinical and quality owners | Before offline validation |
| Implement and test technical controls | Provider and client IT | Before shadow mode |
| Train users and verify competence | Clinical Operations and provider | Before shadow mode |
| Approve shadow-to-assisted progression | Clinical, quality, DPO and security owners | Pilot gate |
| Reassess material changes | Product owner with all control functions | Before release |

---

## 11. Application Timeline

The EU AI Act entered into force on 1 August 2024 and became generally applicable on 2 August 2026. Prohibited-practice and AI-literacy provisions applied earlier, from 2 February 2025, and GPAI obligations began applying from 2 August 2025.

Following the 2026 AI Omnibus changes, official Commission information states that the rules for Annex III high-risk systems apply from 2 December 2027 and rules for high-risk AI embedded in regulated products apply from 2 August 2028.

The programme must monitor further Commission guidance, harmonised standards and German authority practice. A later legal deadline is not a reason to postpone safeguards needed for safe pilot operation.

---

## 12. Final Recommendation

Maintain the narrow recruitment-support purpose and consulting-led deployment model. Proceed only to the four-week readiness assessment.

Before any real-data pilot, HelixBridge should obtain a written AI Act and MDR classification decision, approve the GDPR and security controls, establish contractual roles and validate the system locally. Human confirmation, additional escalation, manual fallback and controlled change are mandatory throughout.

If the system’s purpose expands toward clinical decision-making, access to healthcare or autonomous recruitment decisions, suspend expansion and perform a new classification and conformity assessment before use.

---

## 13. Authoritative References

- [Regulation (EU) 2024/1689 — Artificial Intelligence Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [European Commission — AI Act regulatory framework and application timeline](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [European Commission — Navigating the AI Act](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act)
- [European Commission — High-risk AI-system classification guidance](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems)
- [MDCG 2019-11 rev.1 — Qualification and classification of software under the MDR and IVDR](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en)
- [European Commission — MDCG guidance catalogue](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)
