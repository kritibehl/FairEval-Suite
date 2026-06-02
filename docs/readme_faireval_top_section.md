# FairEval-Suite

**AI Evaluation & Responsible AI Release-Safety Platform**

FairEval is a portfolio-grade AI evaluation platform for testing model-output quality, RAG groundedness, Responsible AI regressions, agent workflow safety, retail search/recommendation quality, dataset drift, reviewer agreement, and release-readiness decisions.

## What it proves

- Baseline-vs-candidate model evaluation
- CI regression gates for GenAI outputs
- Responsible AI false-allow detection
- RAG groundedness and hallucination checks
- Agent tool-call correctness and unsupported-action detection
- Retail search/recommendation evaluation with Precision@K, Recall@K, and NDCG
- Evaluation warehouse for model, prompt, dataset, score, failure, latency, cost, and release-decision tracking
- Dataset drift monitoring
- Human reviewer agreement analysis
- Release history explorer
- Live Responsible AI API deployed on Cloud Run
- React dashboard and leaderboard-ready artifacts

## Live API

Swagger docs:

```text
https://faireval-rai-api-126325674316.us-central1.run.app/docs
Health:

https://faireval-rai-api-126325674316.us-central1.run.app/rai/health
Verify in 2 minutes
Open the live API docs.
Inspect docs/diagrams/faireval_architecture_mermaid.md.
Open leaderboard/leaderboard.html.
Run python ci_eval_gate/regression_gate.py || true.
Inspect eval_warehouse/weekly_eval_report.md.
Inspect dataset_drift/dataset_drift_report.json.
Inspect release_history/release_history_explorer.md.
Safe scope

FairEval uses synthetic evaluation data and local/provider-style artifacts unless a file explicitly states real API outputs were successfully generated. It does not claim production deployment, private customer data, or live Apple/OpenAI/Anthropic/Google benchmark results.
