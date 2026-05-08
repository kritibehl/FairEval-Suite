# FairEval ML Platform Upgrade

FairEval now includes ML-platform-style artifacts:

## Run lineage
Tracks:
- run_id
- parent_run_id
- model_name
- model_version
- prompt_version
- dataset_hash
- evaluator_version
- threshold_version
- timestamp

## Async eval workers
Long-running evaluation jobs can be queued and processed asynchronously with:
- queued/running/succeeded/failed status
- retry attempts
- failed job records

## Regression reports
Exports Promptfoo/DeepEval-style reports:
- prompt regression report
- schema breaks
- failed constraints CSV

## Dashboard exports
Exports dashboard-ready CSV, JSON, and screenshot artifacts for self-service benchmark review.
