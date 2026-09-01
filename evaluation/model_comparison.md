# Model Comparison

## Status

Phase 4 Increment 1 adds reproducible execution infrastructure only. Candidate
predictions have **not yet been generated**. No smoke run or full comparison
run is included in this increment.

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

Smoke and full-cohort execution, comparison CSV generation, metrics analysis,
and model selection remain later phases. All evaluation data is public
synthetic data and all model calls require explicit authorisation.

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
