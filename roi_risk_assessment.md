# ROI and Risk Assessment

## Clinical-Trial Eligibility Copilot

**Document status:** Client-facing planning assessment  
**Assessment date:** 3 September 2026  
**Prepared for:** HelixBridge Clinical Research Network GmbH  
**Client status:** Fictional company created for this project  
**Financial horizon:** 12 and 36 months  
**Currency:** EUR, excluding VAT

> The organisation profile, volumes, costs and benefits are hypothetical planning assumptions derived from a pre-proposal scenario. The readiness assessment will replace them with measured client data and supplier quotations before HelixBridge makes a pilot or deployment investment decision.

---

## 1. Executive Summary

The Clinical-Trial Eligibility Copilot is intended to reduce repetitive prescreening preparation, improve criterion-level documentation and strengthen escalation of uncertain cases while keeping all consequential decisions with qualified staff.

The base case assumes a four-site network completing approximately 600 unique patient–trial reviews per month. A controlled pilot covers one trial, two sites and four coordinators before any network-wide deployment.

### Base-case financial result

| Measure | Result |
|---|---:|
| Upfront all-in programme cost | €160,000 |
| Annual ongoing cost after deployment | €60,000 |
| Annual steady-state quantified value | €135,500 |
| Annual steady-state net benefit | €75,500 |
| 12-month ROI | **−75.0%** |
| 36-month ROI | **2.7%** |
| Indicative break-even | **Approximately month 35** |

The negative first-year ROI is expected because readiness, pilot and deployment costs occur before full benefits are available. The 36-month base case is only slightly positive and depends materially on whether faster and more systematic review produces attributable recruitment value.

Coordinator time savings alone do not justify the full investment. The commercial case requires recruitment or avoided-cost value in addition to efficiency. For this reason, HelixBridge should approve readiness and pilot as separate decisions and commit to full deployment only after measured evidence supports the business case.

Safety and patient protection are mandatory conditions, not financial benefits used to make an unfavourable ROI appear positive.

---

## 2. Scope and Operating Assumptions

| Attribute | Base assumption |
|---|---:|
| Research sites | 4 |
| Clinical research coordinators | 12 |
| Active recruiting trials | 8 |
| Patient–trial reviews | 600 per month / 7,200 per year |
| Current preparation time | 30 minutes per review |
| Current annual preparation effort | 3,600 hours |
| Pilot scope | 1 trial, 2 sites, 4 coordinators |
| Pilot volume | Approximately 150 reviews per month |
| Target net preparation-time reduction | 25% |
| Full rollout | Conditional; approximately months 7–11 |

A review is one patient–trial combination. A patient assessed against three trials counts as three reviews.

The target time reduction is net of the time needed to inspect AI evidence, confirm or override the assessment and complete additional escalations.

---

## 3. ROI Method

The assessment uses:

\[
\text{ROI} = \frac{\text{Net Benefit}}{\text{Total Cost}} \times 100
\]

where:

\[
\text{Net Benefit} = \text{Quantified Business Value} - \text{Total Cost}
\]

### Benefit timing

The implementation roadmap reaches conditional deployment late in the first year. The model therefore assumes:

- **12 months:** 35% of annual steady-state value and 50% of annual ongoing cost;
- **36 months:** 2.35 years of steady-state value and 2.5 years of ongoing cost.

This reflects limited benefit during readiness, shadow mode and staged rollout. It avoids treating the solution as fully deployed from day one.

---

## 4. Upfront Costs

### 4.1 Base-case all-in programme cost

| Cost item | Base estimate | Basis |
|---|---:|---|
| Readiness assessment | €12,500 | Midpoint of €10,000–€15,000 provider range |
| Controlled pilot | €45,000 | Midpoint of €35,000–€55,000 provider range |
| Full-deployment implementation | €70,000 | Midpoint of €50,000–€90,000 provider range |
| Client internal participation | €20,000 | Part-time clinical, operations, IT, privacy, security and quality input |
| Programme contingency | €12,500 | Approximately 10% of provider implementation fees |
| **Total upfront cost** | **€160,000** | All-in planning base case |

### 4.2 Cost coverage

The upfront estimate covers:

- workflow measurement and pilot design;
- data and interface assessment;
- model and prompt configuration;
- local evaluation and safety testing;
- limited pilot integration;
- privacy, security and regulatory readiness work;
- shadow and assisted pilot operation;
- training and change support;
- pilot evaluation and decision package;
- conditional production integration and staged four-site rollout.

### 4.3 Exclusions

The following require confirmation and may change the estimate:

- major CTMS or EHR vendor interface fees;
- remediation of poor source-data quality;
- procurement of new enterprise infrastructure;
- extensive legal, notified-body or medical-device work if the intended purpose changes;
- expansion to materially different protocols or therapeutic areas;
- client staff backfill;
- 24/7 support or unusually demanding service levels.

---

## 5. Ongoing Costs

### 5.1 Annual base case after deployment

| Cost item | Annual estimate | Basis |
|---|---:|---|
| Provider support and controlled maintenance | €27,000 | Midpoint of €18,000–€36,000 range |
| Cloud and model usage | €8,000 | Client-contracted EU environment and API consumption |
| Monitoring, security and backup tooling | €5,000 | Incremental operational tooling |
| Client product ownership and governance | €15,000 | Part-time operations, clinical, IT and control-owner effort |
| Training and periodic revalidation | €5,000 | Refresher training and scheduled quality review |
| **Total annual ongoing cost** | **€60,000** | Planning base case |

Model API expenditure is not expected to be the main cost driver. Human review, integration, governance, monitoring and controlled change account for most ongoing cost.

---

## 6. Quantified Business Value

### 6.1 Coordinator capacity released

Current annual preparation effort:

\[
600 \text{ reviews/month} \times 0.5 \text{ hours} \times 12 = 3{,}600 \text{ hours}
\]

At a 25% net reduction:

\[
3{,}600 \times 25\% = 900 \text{ hours released annually}
\]

At an illustrative loaded coordinator cost of €45 per hour:

\[
900 \times €45 = €40{,}500
\]

| Benefit | Annual value |
|---|---:|
| Coordinator capacity released | €40,500 |

This is capacity value, not automatically cash savings. It becomes financially real only if the time is redeployed to productive work, avoids overtime or external support, or delays additional hiring.

### 6.2 Attributable recruitment contribution

The base case assumes that more systematic and timely review contributes to 16 additional or recovered participant enrolments per year across the network. An illustrative net contribution of €5,000 per participant gives:

\[
16 \times €5{,}000 = €80{,}000
\]

| Benefit | Annual value |
|---|---:|
| Attributable recruitment contribution | €80,000 |

This is the most uncertain and influential assumption. Actual site payments differ by study, milestone and contract. The pilot must define an attribution method and use trial-specific finance data. Candidates identified by the tool must not automatically be counted as incremental enrolments.

### 6.3 Reduced rework and overflow

Standardised evidence capture and earlier identification of missing information are assumed to reduce repeat review, avoidable escalation preparation and limited overflow support.

| Benefit | Annual value |
|---|---:|
| Reduced rework and overflow | €15,000 |

### 6.4 Total steady-state value

| Value component | Annual value | Share |
|---|---:|---:|
| Coordinator capacity | €40,500 | 29.9% |
| Attributable recruitment contribution | €80,000 | 59.0% |
| Reduced rework and overflow | €15,000 | 11.1% |
| **Total annual business value** | **€135,500** | **100%** |

No monetary value is assigned to patient safety, regulatory compliance, auditability or avoided harm. These remain mandatory performance and governance requirements.

---

## 7. ROI Calculations

### 7.1 Twelve-month ROI

| Component | Calculation | Amount |
|---|---|---:|
| Realised value | €135,500 × 35% | €47,425 |
| Upfront cost | Base programme cost | €160,000 |
| Ongoing cost | €60,000 × 50% | €30,000 |
| **Total cost** | €160,000 + €30,000 | **€190,000** |
| **Net benefit** | €47,425 − €190,000 | **−€142,575** |

\[
\text{12-month ROI} = \frac{-€142{,}575}{€190{,}000} \times 100 = \mathbf{-75.0\%}
\]

### 7.2 Thirty-six-month ROI

| Component | Calculation | Amount |
|---|---|---:|
| Realised value | €135,500 × 2.35 | €318,425 |
| Upfront cost | Base programme cost | €160,000 |
| Ongoing cost | €60,000 × 2.5 | €150,000 |
| **Total cost** | €160,000 + €150,000 | **€310,000** |
| **Net benefit** | €318,425 − €310,000 | **€8,425** |

\[
\text{36-month ROI} = \frac{€8{,}425}{€310{,}000} \times 100 = \mathbf{2.7\%}
\]

### 7.3 Steady-state annual position

| Measure | Amount |
|---|---:|
| Annual business value | €135,500 |
| Annual ongoing cost | €60,000 |
| **Annual net benefit after stabilisation** | **€75,500** |

---

## 8. Sensitivity Analysis

The sensitivity analysis keeps programme costs constant and varies the three benefit drivers. This isolates the effect of operational performance and recruitment value.

### 8.1 Scenarios

| Assumption | Low | Base | High |
|---|---:|---:|---:|
| Net time reduction | 15% | 25% | 35% |
| Annual capacity value | €24,300 | €40,500 | €56,700 |
| Additional/recovered enrolments | 6 | 16 | 24 |
| Contribution per enrolment | €3,000 | €5,000 | €7,000 |
| Recruitment contribution | €18,000 | €80,000 | €168,000 |
| Rework/overflow value | €5,000 | €15,000 | €25,000 |
| **Annual value** | **€47,300** | **€135,500** | **€249,700** |

### 8.2 Results

| Scenario | 12-month ROI | 36-month ROI | Indicative break-even |
|---|---:|---:|---|
| Low | −91.3% | −64.1% | No break-even while annual value remains below annual cost |
| Base | −75.0% | 2.7% | Approximately month 35 |
| High | −54.0% | 89.3% | Approximately month 19 |

### 8.3 Interpretation

The investment is highly sensitive to attributable recruitment value. The low scenario does not cover annual operating cost and should trigger a stop or material scope and cost revision. The base scenario produces only a marginal 36-month return. The high scenario is attractive but must not be used as the primary forecast without client evidence.

---

## 9. Assumptions Register

| Assumption | Base value | Validation source | Owner |
|---|---:|---|---|
| Patient–trial review volume | 600/month | CTMS and workflow sampling | Clinical Operations |
| Current preparation time | 30 minutes | Time-and-motion baseline | Clinical Operations |
| Net time reduction | 25% | Shadow and assisted pilot | Pilot product owner |
| Loaded coordinator cost | €45/hour | HR and Finance | Finance |
| Additional/recovered enrolments | 16/year | Predefined attribution analysis | Clinical Operations and Finance |
| Net contribution per enrolment | €5,000 | Trial contracts and finance records | Finance |
| Rework/overflow value | €15,000/year | Overtime, vendor and rework records | Operations and Finance |
| Upfront cost | €160,000 | Readiness, supplier quote and internal resource plan | Sponsor and Procurement |
| Annual ongoing cost | €60,000 | Vendor, infrastructure and governance estimates | IT and Operations |
| First-year value realisation | 35% | Final delivery schedule | Programme lead |
| First-year ongoing-cost exposure | 50% | Contract and deployment schedule | Finance |

No assumption becomes a committed benefit until its measurement method, source and accountable owner are agreed.

---

## 10. Break-Even Note

Under the base case, the first 12 months end with a cumulative deficit of €142,575. After stabilisation, annual net benefit is €75,500.

\[
€142{,}575 \div €75{,}500 = 1.89 \text{ additional years}
\]

This gives an indicative break-even around month 35.

Break-even is not guaranteed. It moves later if integration costs increase, review volume is lower, time savings are not redeployed or recruitment value cannot be attributed. HelixBridge should update the forecast at readiness completion, the end of shadow mode and the final pilot gate.

---

## 11. Risk Scoring Method

### Likelihood

| Score | Meaning |
|---:|---|
| 1 | Rare |
| 2 | Unlikely |
| 3 | Possible |
| 4 | Likely |
| 5 | Almost certain |

### Impact

| Score | Meaning |
|---:|---|
| 1 | Negligible |
| 2 | Minor |
| 3 | Moderate |
| 4 | Major |
| 5 | Critical |

Risk score equals likelihood multiplied by impact.

| Score | Rating |
|---:|---|
| 1–5 | Low |
| 6–10 | Medium |
| 11–15 | High |
| 16–25 | Critical |

Scores describe risk before the listed mitigation. Residual risks require reassessment by the accountable owner before each phase gate.

---

## 12. Risk Matrix

| ID | Category | Risk | L | I | Score | Rating | Principal mitigation | Owner |
|---|---|---|---:|---:|---:|---|---|---|
| R1 | Regulatory/privacy | No valid lawful basis or Article 9 condition is established for prescreening | 3 | 5 | 15 | High | DPO/legal approval before real-data access; document purpose, roles, national-law basis, DPIA and transparency; stop if unresolved | Client DPO/legal |
| R2 | Regulatory | Intended use changes and triggers medical-device or higher-risk AI obligations | 2 | 5 | 10 | Medium | Freeze intended purpose and prohibited uses; reassess AI Act and MDR status before every material change | Quality/regulatory lead |
| R3 | Regulatory/privacy | Processor or international-transfer arrangements are inadequate | 3 | 5 | 15 | High | Approved vendor register, Article 28 terms, transfer mapping, adequacy/SCC assessment and supplementary controls | DPO/procurement |
| R4 | Technical/safety | Incorrect positive assessment overlooks an exclusion concern | 3 | 5 | 15 | High | Human confirmation, source review, safety test set, fail-safe routing, incident process and rollback | Clinical owner/AI lead |
| R5 | Technical | Incomplete or inconsistent source data produces misleading assessments | 4 | 4 | 16 | Critical | Minimum data contract, provenance, validation, missing-data flags, site testing and `UNKNOWN` handling | Client IT/data owner |
| R6 | Technical | Model or prompt changes degrade performance | 3 | 4 | 12 | High | Frozen versions, full regression evaluation, release approval, monitoring and rollback | Product/AI owner |
| R7 | Security | Patient information is exposed through an integration, log, model or queue | 3 | 5 | 15 | High | Minimisation, pseudonymisation, EU hosting, RBAC, MFA, encryption, secrets management, approved logging and security testing | Security owner |
| R8 | Ethical | Performance differs materially across demographic or clinical groups | 3 | 5 | 15 | High | Representative local validation, subgroup monitoring, clinical investigation and deployment restriction where evidence is insufficient | Clinical/quality owner |
| R9 | Ethical/human factors | Reviewers over-trust the AI and confirmation becomes a rubber stamp | 4 | 4 | 16 | Critical | Source-first review, training, override authority, sampled audits, workload limits and reviewer accountability | Clinical Operations |
| R10 | Ethical/safety | Suitable patients are silently excluded or deprioritised | 3 | 5 | 15 | High | No automatic suppression; monitor unsafe and missed-review cases; retain manual fallback and correction route | Clinical owner |
| R11 | Operational | Escalation and confirmation workload offsets preparation savings | 4 | 4 | 16 | Critical | Measure end-to-end time and queue ageing; include review effort in ROI; narrow or stop if net burden rises | Clinical Operations/product owner |
| R12 | Operational | Coordinators do not adopt or consistently use the workflow | 3 | 3 | 9 | Medium | Co-design, training, site champions, usability testing and adoption monitoring | Change lead/site managers |
| R13 | Operational | Integration, privacy, procurement or clinical approvals delay delivery | 4 | 3 | 12 | High | Named decision owners, four-week readiness gate, dependency plan, weekly escalation and schedule contingency | Programme lead |
| R14 | Operational | Service outage interrupts recruitment work | 3 | 3 | 9 | Medium | Manual fallback, monitoring, backup, recovery testing and support targets | Client IT/provider support |
| R15 | Financial | Volume or attributable recruitment value is insufficient to recover cost | 4 | 4 | 16 | Critical | Validate volume and value during readiness; low/base/high forecast; separate pilot and deployment decisions | Executive sponsor/Finance |
| R16 | Commercial/technical | Client-specific integration prevents repeatable or maintainable delivery | 3 | 4 | 12 | High | Standard data contracts and connectors; price custom work separately; architecture review before commitment | Provider lead/client IT |

---

## 13. Priority Risk Interpretation

Four risks are rated critical:

1. **Source-data quality:** AI cannot correct missing, outdated or incorrectly mapped clinical information.
2. **Automation bias:** Human confirmation is ineffective if reviewers do not critically inspect evidence.
3. **Review workload:** Conservative routing may improve caution while eliminating the expected time saving.
4. **Insufficient financial value:** The narrow use case may not justify integration and governance cost at the client’s actual volume.

These risks are linked. Poor data increases uncertain outputs; uncertainty increases review workload; higher workload reduces value; time pressure can increase automation bias. They should therefore be reviewed together rather than as isolated technical problems.

---

## 14. Risk Governance

| Phase | Required review |
|---|---|
| Readiness | Validate assumptions, legal basis, intended purpose, data quality and architecture |
| Build and offline validation | Weekly technical risk review and formal clinical, privacy and security gates |
| Shadow mode | Weekly disagreement, subgroup, data-quality and routing review |
| Assisted mode | Weekly safety, workload, adoption and incident review |
| Deployment | Review at every site/trial activation wave |
| Operations | Monthly performance review and quarterly governance review |

Processing is suspended or prevented from advancing if:

- mandatory human-confirmation controls fail;
- a suspected personal-data breach occurs;
- an unsafe automated action is detected;
- source-data integrity cannot be established;
- a material model, prompt or workflow change has not been validated;
- a critical privacy, security, regulatory or clinical finding remains unresolved;
- review backlog prevents meaningful human oversight.

The clinical owner accepts clinical residual risk; the DPO/legal team assesses privacy lawfulness; the security owner assesses security residual risk; Finance validates the business case; and the steering committee makes the final `STOP / PIVOT / CONTINUE` decision.

---

## 15. Investment Recommendation

Approve the four-week readiness assessment as the next bounded investment. Use it to verify volumes, handling time, integration constraints, compliance conditions and trial-specific recruitment economics.

If readiness supports continuation, proceed with one controlled pilot for one trial across two sites. Do not commit to full deployment before the pilot demonstrates:

- mandatory human control and acceptable safety performance;
- reliable source evidence and manageable review workload;
- at least 25% net preparation-time reduction;
- at least 80% active-user adoption;
- approved privacy, security and regulatory controls;
- a credible 36-month return using measured client data.

The base case reaches only 2.7% ROI over 36 months. Modest underperformance would make the investment negative. HelixBridge should therefore treat the pilot as an evidence-generating decision gate and not as the first instalment of an already-approved full rollout.
