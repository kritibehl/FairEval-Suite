# FairEval Benchmark v1

FairEval Benchmark v1 is a public-facing release-safety benchmark page for AI evaluation, Responsible AI regression review, RAG groundedness, agentic workflow checks, latency/cost gates, and oversight reliability.

## Live Demo

- Live API docs: https://faireval-rai-api-126325674316.us-central1.run.app/docs
- Health endpoint: https://faireval-rai-api-126325674316.us-central1.run.app/rai/health
- React dashboard: `dashboard_frontend/`

## Headline metrics

- text_generation_regressions: `6`
- responsible_ai_false_allows: `6`
- weak_evaluator_false_allows: `16`
- composite_evaluator_false_allows: `0`
- agentic_release_decision: `block`
- p95_latency_ms: `950`

## Leaderboard-style comparison

| System | Pack | Avg / Recall | Regressions Detected | Groundedness Failures | Safety False Allows | Release Decision |
|---|---|---:|---:|---:|---:|---|
| baseline_mock_adapter | text_generation_v1 | 1.0 | 0 | 0 | 0 | ship |
| candidate_mock_adapter | text_generation_v1 | 0.7 | 6 | 1 | 6 | block |
| weak_surface_evaluator | oversight_reliability_v1 | 0.2727 | 6 | n/a | 16 | not_release_safe |
| composite_oversight_evaluator | oversight_reliability_v1 | 1.0 | 22 | n/a | 0 | review_pass |
| agentic_candidate_workflow | agentic_release_safety_v1 | n/a | 4 | 1 | n/a | block |

## What hiring teams can verify in 2 minutes

1. Open the live API docs.
2. Run `/rai/health`.
3. Try `/rai/evaluate-content` with the provided sample payload.
4. Open the React dashboard in `dashboard_frontend/`.
5. Inspect the release-gate JSON artifacts for Responsible AI, agentic workflows, and oversight reliability.

## Safe scope

Benchmark v1 uses synthetic evaluation artifacts and local/mock adapters unless explicitly marked as a live API. It is designed to demonstrate evaluation infrastructure, not claim frontier-model benchmarking coverage.
