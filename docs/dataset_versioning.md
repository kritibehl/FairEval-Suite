# Dataset Versioning

FairEval tracks lightweight dataset metadata for reproducible evaluation runs.

## Tracks
- dataset ID
- dataset hash
- number of cases
- task types
- downstream evaluation workflows

## Why this matters
AI evaluation results are only meaningful when tied to prompt, dataset, evaluator, and threshold versions.

## Safe scope
This is lightweight dataset-version metadata for reproducible evaluation artifacts, not a production DVC/MLflow deployment.
