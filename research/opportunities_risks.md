# Opportunities and Risks: AI-Assisted Clinical-Trial Pre-Screening

## Opportunities

| Opportunity | Value for a medium-sized CRO | How the capstone demonstrates it |
|---|---|---|
| Reduce first-pass review effort | Coordinators can focus on records likely to require action rather than repeatedly comparing every record with every criterion | Measures review volume, model latency and estimated cost per assessment |
| Make screening more consistent | A structured criterion-level format reduces variation in how coordinators document preliminary findings | Requires `MET`, `NOT_MET` or `UNKNOWN`, evidence and rationale for every criterion |
| Surface missing information early | Identifies which data are required before formal screening can continue | Tracks `UNKNOWN` outcomes and the criteria most frequently blocked by missing information |
| Improve transparency and auditability | Creates a reviewable record of what the AI assessed and why the case was escalated | Stores criteria, model output, evidence, human-review flag and final reviewer decision |
| Support a controlled build/buy/integrate decision | Gives the CRO evidence before investing in an enterprise platform or production integration | Dashboard compares accuracy, unsafe results, abstention, review burden, latency and cost |
| Create a foundation for future workflow tools | The same structured outputs could later support feasibility analysis, exception queues and monitoring | Uses a reusable patient–criterion assessment schema |

## Risks and mitigations

| Risk | Why it matters | Mitigation in the capstone | Requirement for a real deployment |
|---|---|---|---|
| Unsafe false positive | A patient may be marked `MET` despite an exclusion or missing requirement | Evaluate and highlight unsafe `MET` results; require human review for every output | Clinical validation, risk thresholds, escalation rules and continuous monitoring |
| Unsupported or invented evidence | An LLM may claim a fact that is not in the record | Require evidence snippets; evaluate evidence grounding; use `UNKNOWN` when information is absent | Retrieval controls, source citations, audit logs and routine quality review |
| Failure to abstain | The model may guess instead of recognising insufficient information | Include ambiguous and missing-data cases; track `UNKNOWN` behaviour | Clear abstention policy, staff training and monitoring by criterion type |
| Protocol misinterpretation | Eligibility wording can be complex and protocol versions change | Use selected static public criteria and make scope explicit | Approved protocol source, version control, clinical review and change management |
| Data protection and confidentiality | Real patient records are special-category personal data under GDPR | Use synthetic records only; no personal data in the POC | Lawful basis, DPIA, role-based access, data-minimisation, retention rules and processor agreements |
| Bias and unequal access | Biased or incomplete data may systematically overlook suitable participants | Use varied synthetic cases and document dataset limits | Fairness evaluation across relevant groups, representative validation data and governance oversight |
| Automation bias | Users may accept an AI recommendation without sufficient verification | Mandatory human-review flag and visible evidence/uncertainty | Training, SOPs, sign-off responsibility and audit sampling |
| Integration complexity | Real value depends on access to current EHR and protocol data, not only model quality | POC uses standardised files to isolate the decision-support workflow | Secure integration, identity/access management, source-system validation and operational support |
| Cost or vendor lock-in | A model or platform may become expensive or difficult to replace | Estimate cost per assessment and keep the assessment schema model-independent | Procurement review, service-level agreements, exit strategy and periodic vendor comparison |
| Regulatory classification | The intended use may trigger medical-device or other regulatory obligations | Do not claim clinical decision-making or autonomous eligibility decisions | Formal legal, quality and regulatory assessment before deployment |

## Opportunity–risk conclusion

The strongest near-term value is not autonomous screening. It is a transparent first-pass assistant that helps coordinators prioritise work, identify missing information and document preliminary reasoning consistently.

The product should progress only if it demonstrates acceptable criterion-level quality, a very low unsafe false-positive rate, evidence-grounded explanations, useful `UNKNOWN` behaviour and a measurable reduction in manual first-pass workload. Final eligibility, patient contact and enrolment remain human clinical-research responsibilities.