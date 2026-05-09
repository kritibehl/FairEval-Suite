## FairEval — ML Release-Gating Platform

FairEval blocks bad AI model releases using regression-aware evaluation pipelines, reproducible benchmark artifacts, and CI-ready release signals.

### What it does

```text
run → compare → gate → export
FairEval evaluates model behavior, compares benchmark runs, detects regressions, and produces release decisions.

Verified benchmark result
Model	Avg Score	Pass Rate	Failed Cases
Gemini	0.367	40%	6 / 10
Platform artifacts
Run lineage with dataset hashes, prompt versions, evaluator versions, and threshold versions
Async eval workers with queue, run status, and failed-job tracking
Regression reports for schema breaks, failed constraints, and prompt regressions
Dashboard-ready CSV, JSON, Parquet, and screenshot exports
CI-ready release-gate workflow
Prometheus-style metrics endpoint
Kubernetes deployment manifest
Why score-only evals fail

Average scores can hide output-contract breaks, instruction drops, formatting drift, instability across repeated runs, and high-risk subset regressions. FairEval treats those as release risks, not cosmetic failures.
