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
