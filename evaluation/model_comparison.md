# Model Comparison

## Status

Phase 4 Increment 1 infrastructure is complete. The GPT-5.6 Sol smoke run is
complete; the full 120-assessment candidate run and final comparison have not
yet been generated.

## Configurations

| Configuration ID | Model | Reasoning effort | Prompt |
| --- | --- | --- | --- |
| `gpt41-v2` | `gpt-4.1` | None | `v2_abstention_rules` |
| `gpt56sol-medium-v2` | `gpt-5.6-sol` | `medium` | `v2_abstention_rules` |

The candidate configuration checks that the active `PROMPT_VERSION` is
`v2_abstention_rules` before making a model call. Legacy runs without
`--configuration-id` retain the existing flexible prompt behaviour.

## Execution

The candidate requires an explicit output path and must not use the protected
baseline path:

```bash
python -m src.run_screening \
  --configuration-id gpt56sol-medium-v2 \
  --output data/processed/llm_predictions_gpt56sol_medium_v2.csv \
  --overwrite
```

This command is documented for a later explicitly authorised run and has not
been executed as part of this increment. The existing GPT-4.1 baseline file
`data/processed/llm_predictions_gpt41_v2.csv` remains unchanged.

## Request Parameters and Metadata

GPT-4.1 retains `temperature=0`. The reasoning candidate sends
`reasoning={"effort": "medium"}` and omits temperature. Each new prediction
row records configuration ID, reasoning effort, model, prompt version, response
ID, latency, token usage, status and error message.

## Pricing

Pricing is model-specific and unknown models fail rather than inheriting GPT-4.1
prices. Rates checked on `2026-09-01`:

| Model | Input / 1M tokens | Output / 1M tokens | Source |
| --- | ---: | ---: | --- |
| `gpt-4.1` | $2.00 | $8.00 | [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-4.1) |
| `gpt-5.6-sol` | $4.00 | $20.00 | [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |

Full-cohort execution, comparison CSV generation, metrics analysis, and model
selection remain later phases. All evaluation data is public synthetic data and
all model calls require explicit authorisation.

## Deterministic Smoke Manifest

The 15-case smoke sample is tracked in
`evaluation/model_comparison_smoke_manifest.csv`. Regenerate it safely from the
repository root with:

```bash
python -m scripts.create_smoke_manifest
```

Generation validates that the GPT-4.1 baseline covers the same 120 unique
locked annotation IDs, completed successfully with `gpt-4.1` and
`v2_abstention_rules`, contains valid labels and evidence JSON, and matches the
locked ground-truth labels. It refuses to overwrite an existing manifest
unless `--overwrite` is supplied.

The exact 15-case manifest must meet these minimum quotas:

| Category | Minimum |
| --- | ---: |
| Inclusion criteria | 5 |
| Exclusion criteria | 5 |
| Each ground-truth label | 2 |
| Baseline agreements | 4 |
| Baseline disagreements | 4 |
| Review outcomes | 5 |
| No-routine-queue outcomes | 5 |
| Evidence present | 3 |
| Evidence absent | 3 |
| Unique patients | 12 |
| Unique trials | 12 |

Every baseline unsafe case is mandatory. If mandatory unsafe cases exceed 15,
or if the deterministic selector cannot satisfy all quotas within 15 rows,
generation fails and reports the unmet targets. Each candidate reduces at most
one remaining slot per applicable category, but may reduce slots in several
different categories. Candidates are ranked by quota reduction, then new
patient, new trial, and lowest annotation ID.

The manifest contains all four reference labels, both criterion types,
agreement and disagreement cases, review and no-routine-queue outcomes, empty
and non-empty evidence cases where available, and every baseline unsafe `MET`
case. Selection is deterministic and uses coverage first, then new-patient
and new-trial diversity, then the lowest annotation ID.

The candidate smoke command is:

```bash
python -m src.run_screening \
  --configuration-id gpt56sol-medium-v2 \
  --annotation-manifest evaluation/model_comparison_smoke_manifest.csv \
  --output data/processed/llm_predictions_gpt56sol_medium_v2_smoke.csv \
  --overwrite
```

This 15-case run is a technical compatibility and obvious-safety gate. Its
metrics must not be presented as comparative model performance; only the
complete 120-case locked-cohort run supports the final model comparison.

## Completed Smoke Run

The GPT-5.6 Sol smoke run used configuration `gpt56sol-medium-v2` and the
tracked 15-case manifest. All 15/15 responses completed successfully with zero
technical errors. The run verified the expected model, prompt
`v2_abstention_rules`, reasoning effort `medium`, and manifest output order.

The following are smoke observations only, not final performance estimates:

| Metric | GPT-5.6 Sol candidate | GPT-4.1 baseline |
| --- | ---: | ---: |
| Exact agreement | 9/15 | 9/15 |
| Review cases | 9/15 | 5/15 |
| Unsafe `MET` cases | 0 | 1 known case |

The known baseline unsafe case `977` changed from `MET` to candidate `UNKNOWN`.
The candidate used 11,037 input tokens and 2,029 output tokens, with median
latency of 3.3 seconds and estimated cost of $0.0847.

### Smoke Routing Observations

There were 6 reference review cases. The candidate correctly routed 5 of them
to review and missed 1, giving smoke review-routing recall of 5/6 (83.3%). The
candidate exact `NOT_APPLICABLE` recall was 0/2. The baseline routed both of
those `NOT_APPLICABLE` cases to review as `UNKNOWN` (2/2).

Source annotation `479` is a review-routing disagreement:

- Reference: `NOT_APPLICABLE`.
- Baseline: `UNKNOWN`.
- Candidate: `MET`.
- Candidate rationale: the patient was alive on arrival, so the dead-on-arrival exclusion was not triggered.

The rationale appears logically plausible, but the locked reference remains
authoritative for reported evaluation metrics. This case is flagged for
possible annotation or label-semantics review.

### Smoke Decision

Decision: **PASS for full-cohort execution**. Technical compatibility and the
obvious-safety gate passed. The smoke sample does not demonstrate superior
performance and must not be presented as a performance estimate.

The full-cohort comparison will additionally report missed-review count and
rate, review-routing recall (reference `UNKNOWN` or `NOT_APPLICABLE` requiring
review), exact `NOT_APPLICABLE` recall, and the difference in review workload.
Only the complete 120-case locked-cohort run supports final comparative model
conclusions.


## GPT-4.1 v3 prompt evaluation

The safety-focused `v3_safety_and_label_rules` prompt was evaluated on the same locked 120-assessment synthetic cohort.

| Metric | GPT-4.1 v2 | GPT-4.1 v3 |
|---|---:|---:|
| Exact agreement | 87/120 (72.5%) | 93/120 (77.5%) |
| Review-routing recall | 60/71 (84.5%) | 67/71 (94.4%) |
| Missed-review cases | 11 | 4 |
| `NOT_APPLICABLE` recall | 3/19 (15.8%) | 8/19 (42.1%) |
| Review workload | 71/120 (59.2%) | 79/120 (65.8%) |
| Unsafe `MET` cases | 1/17 | 0/17 |
| Median latency | 1.01 seconds | 1.295 seconds |
| Estimated cost | $0.2556 | $0.3448 |

The v3 prompt produced the strongest tested quality result. It removed the observed unsafe `MET`, improved exact agreement and substantially reduced missed-review cases, at the cost of moderately higher review workload, latency and token usage.

Residual failures remain. Cases 481 and 783 incorrectly treated missing residency information as decisive evidence. The result therefore supports further controlled development, not autonomous eligibility or enrolment decisions.