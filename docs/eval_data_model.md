# FairEval Evaluation Data Model

FairEval stores model-release evidence as structured evaluation artifacts.

## Tables

### benchmark_runs
Stores one row per benchmark execution.

Fields:
- run_id
- suite_name
- model_name
- dataset_version
- avg_score
- pass_rate
- failed_case_count
- num_cases

### model_scores
Stores case-level model behavior.

Fields:
- run_id
- case_id
- score
- passed
- model_output
- scorer

### regression_cases
Stores documented model failure cases.

Fields:
- case_id
- category
- expected_behavior
- regression_type
- release_risk

### gate_decisions
Stores release decisions.

Fields:
- decision
- release_decision
- reason
- avg_score_delta
- pass_rate_delta
- regressed_case_count

## Exports

FairEval exports:
- `exports/benchmark_results.parquet`
- `exports/benchmark_results.csv`
- `exports/model_scores.csv`
- `exports/model_comparison.csv`

## Why this matters

This turns FairEval into an evaluation data pipeline, not just a benchmark script.

It supports:
- reproducible model release analysis
- model-quality scorecards
- CI-ready regression artifacts
- historical tracking of model behavior
