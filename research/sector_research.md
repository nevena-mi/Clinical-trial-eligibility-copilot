# Sector Research: AI-Assisted Clinical-Trial Pre-Screening

## Client scenario

The hypothetical client is a medium-sized German contract research organisation (CRO) supporting pharmaceutical and biotechnology sponsors with clinical-trial operations. Its research coordinators and clinical-operations staff help sites identify potential participants and prepare the evidence required for investigator review.

The proposed product is not a replacement for investigators, research coordinators, trial protocols or formal screening. It is a transparent pre-screening assistant: it compares a patient summary with selected inclusion and exclusion criteria, identifies what is supported, contradicted or unknown, and prepares an evidence-linked review package for a human user.

For the capstone POC, all patient information is synthetic or de-identified public research data. A real deployment would require a lawful basis for processing health data, site and sponsor agreements, security controls, validation, and human oversight.

## Sector problem

Patient recruitment is a persistent operational bottleneck in clinical research. Eligibility criteria are often complex and information relevant to them may be distributed across structured fields, clinical notes, laboratory results and reports. Research coordinators must manually compare patient records with protocol criteria, document reasons for excluding or advancing a candidate, and escalate uncertain cases.

This work is repetitive but cannot be treated as a purely administrative task: a false positive may create unnecessary coordinator workload or inappropriate patient contact, while a false negative may cause a potentially suitable candidate to be missed. Missing or ambiguous information must therefore remain visible rather than being inferred by an automated system.

The operational need is not an autonomous eligibility decision. It is a reliable way to reduce manual first-pass review while preserving evidence, uncertainty, auditability and researcher accountability.

## Market evidence and real-world relevance

AI-supported patient–trial matching is already used and offered in the clinical-research market.

Deep 6 AI offers software that applies NLP and machine learning to structured and unstructured clinical data for patient–trial matching. Texas Medical Center Clinical Research Institute partnered with Deep 6 AI to make this capability available to member institutions, using a staged process from proof of concept and user training to KPI tracking and live-study deployment. [TMC Clinical Research Institute and Deep 6 AI](https://www.tmc.edu/clinical-research/wp-content/uploads/sites/5/2019/08/TMC-Clinical-Research-SuperSite-powered-by-Deep6.pdf)

WCG, a major clinical-research services organisation, partnered with Deep 6 AI to support sponsors, CROs and investigative sites with more targeted recruitment. The partnership combines research-operations expertise with AI-supported matching across structured and unstructured healthcare data. [WCG and Deep 6 AI partnership](https://www.wcgclinical.com/2022/05/02/wcg-and-deep-6-ai-announce-best-in-class-partnership-to-enable-faster-smarter-clinical-trial-patient-recruitment/)

Tempus offers AI-supported clinical-trial matching and pre-screening. Its published example describes using AI to identify patients for review from unstructured records, with registered-nurse review retained in the workflow. [Tempus clinical-trial matching](https://www.tempus.com/content/article/how-ai-impacts-clinical-trial-process-design-matching/)

TrialX offers EHR-supported patient–trial matching and pre-screening workflows for research teams and sponsors. Its product positioning highlights the same real-world challenge addressed in this capstone: patient information exists in healthcare records but does not map cleanly to detailed trial criteria. [TrialX clinical-trial matching](https://trialx.com/how-trialx-ai-powered-clinical-trial-matching-leverages-ehr-data-to-identify-eligible-patients-efficiently/)

Research evidence also supports the technical direction. TrialGPT, developed by the U.S. National Library of Medicine and collaborators, uses LLMs for retrieval, criterion-level matching and trial ranking. Its published evaluation used synthetic patients and explicitly positions the system as a research and discovery tool requiring professional review rather than a clinical decision system. [TrialGPT FAQ](https://www.ncbi.nlm.nih.gov/research/trialgpt/faq/), [TrialGPT publication](https://pubmed.ncbi.nlm.nih.gov/39557832/)

## Product position

The proposed product is a narrow, transparent pre-screening module for a CRO rather than an enterprise replacement for platforms such as Deep 6 AI, Tempus or TrialX.

It focuses on one operational unit of work: assessing a synthetic patient summary against selected trial criteria and returning, for every criterion:

- `MET`
- `NOT_MET`
- `UNKNOWN`
- supporting patient evidence
- a short rationale
- a mandatory human-review flag

The system must not infer absent clinical facts, decide that a patient is eligible for enrolment, contact patients, recommend treatment, or replace protocol-defined screening. A research coordinator or investigator verifies every result against the current protocol and local study context.

This positioning is realistic for a medium-sized CRO because it supports a pilot or vendor-evaluation decision: the organisation can assess model quality, unsafe false-positive risk, abstention behaviour, review workload, cost and governance requirements before considering a production integration.

## Public data sources for the POC

| Source | Use in the project | Why it is appropriate | Limitation |
|---|---|---|---|
| [TrialGPT](https://github.com/ncbi-nlp/TrialGPT) public code and research resources | Starting point for synthetic patient–trial matching examples and labelled evaluation design | Directly relevant public research resource for criterion-level matching | Research data and outputs are not real-world clinical records or a production benchmark |
| [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/api) | Selected study metadata and public inclusion/exclusion criteria | Official public registry with machine-readable trial records | Registry information may be updated; it is not a substitute for the currently approved local protocol |
| Manually curated synthetic patient cases | 30–50 controlled cases, including clear matches, exclusions, missing information and ambiguity | Allows reproducible labels and safe testing without personal data | Synthetic cases cannot demonstrate real clinical performance or represent all patient populations |

## Data and governance justification

The Round 1 POC uses no real patient data. Synthetic patient records allow the workflow, evaluation approach and dashboard to be demonstrated without processing special-category health data.

In production, the system would need clearly defined data-controller and processor roles, a lawful basis for health-data processing, access controls, retention rules, security review, audit logs and likely a data-protection impact assessment. The CRO would also need to validate performance in its intended context of use and determine the applicable regulatory classification before operational deployment.

## Research conclusion

There is a genuine market and operational need for AI-assisted trial pre-screening. Existing providers demonstrate that organisations already invest in AI/NLP-supported patient matching, but they also show that value depends on integration, data quality, workflow design and human review.

The capstone therefore tests a credible and bounded proposition: whether an evidence-linked LLM assistant can safely reduce first-pass manual review for selected criteria while escalating uncertainty instead of hiding it. Its value lies in transparent evaluation, human oversight, dashboard monitoring and a realistic pilot/governance recommendation—not in claiming autonomous trial eligibility decisions.