# LangSmith Monitoring Sample

## Purpose

LangSmith provides trace-level observability for the criterion-level screening
POC. It records how each screening call was made and supports investigation of
model behaviour without storing real patient data.

## What was monitored

The monitoring sample captures:

- model name;
- prompt version;
- input and output payloads for the public synthetic test cases;
- structured predicted label;
- rationale and evidence-sentence references;
- response ID;
- token usage;
- latency;
- run metadata identifying the application as a public-synthetic,
  human-review-required POC.

## Evidence

The screenshots in `langsmith/screenshots/` show:

- `langsmith_trace_list.png` — the trace list for screening runs;
- `langsmith_model_call_metadata.png` — model-call metadata for an individual
  trace.

## What this demonstrates

The traces make a screening output inspectable rather than a black-box result.
A reviewer can connect a prediction to its model, prompt version, timing,
token usage, rationale, and evidence references. This supports transparency,
debugging, cost monitoring, and investigation of unexpected outputs.

## Limitations

- The sample contains public synthetic data only.
- LangSmith observability does not itself establish clinical validity,
  accuracy, regulatory compliance, or production readiness.
- A production deployment would require an approved logging policy, access
  controls, retention rules, and explicit safeguards for health data.