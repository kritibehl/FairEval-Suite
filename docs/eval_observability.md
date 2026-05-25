# Evaluation Observability

FairEval includes Langfuse/LangSmith-style trace export artifacts for AI release evaluation.

## Captured signals
- retrieval steps
- generation latency
- token counts
- estimated cost/request
- groundedness checks
- hallucination / unsupported-answer detection
- release-gate decisions

## Artifacts
- `observability/eval_trace_export.json`
- `observability/token_cost_report.json`

## Safe scope
These are portable trace artifacts for evaluation observability. They are not a hosted Langfuse, LangSmith, or production observability deployment.
