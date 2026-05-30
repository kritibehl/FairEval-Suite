# Model Lifecycle Regression Summary

```text
baseline_run
    ↓
candidate_run
    ↓
regression analysis
    ↓
release decision = block
    ↓
recommended action = rollback to baseline + human review
Baseline
avg score: 1.0
regressions: 0
groundedness pass rate: 1.0
release decision: reference
Candidate
avg score: 0.7
regressions: 6
groundedness pass rate: 0.6667
Responsible AI false allows: 6
agent regressions: 1
release decision: block
Why this matters

Model lifecycle review connects evaluation results to release decisions. This supports continuous improvement by making candidate regressions, rollback decisions, and human-review requirements explicit.

Safe scope

This is synthetic evaluation lineage for model-release review, not a production MLOps deployment system.
