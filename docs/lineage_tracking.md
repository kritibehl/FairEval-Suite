# FairEval Lineage Tracking

FairEval tracks dataset, prompt, evaluator, and threshold metadata so model-release decisions can be reproduced.

## Tracked lineage fields
- run_id
- parent_run_id
- model_name
- model_version
- prompt_version
- dataset_hash
- evaluator_version
- threshold_version
- timestamp

## Why this matters
A benchmark score alone is not enough to explain a release decision. FairEval records lineage so teams can identify whether a regression came from a model change, prompt change, dataset change, evaluator change, or threshold-policy change.
