# Async Evaluation Worker Queue

FairEval includes a lightweight async evaluation worker demo for queue-based model evaluation processing.

## What it demonstrates
- queued evaluation jobs
- retry state handling
- succeeded-after-retry outcomes
- regression summary export
- separation between job submission and report generation

## Why this matters
Long-running model evaluations should not block API or CLI workflows. Queue-based processing makes FairEval closer to an AI platform service.

## Safe scope
This is a lightweight local worker demo, not a distributed job scheduler or production queue system.
