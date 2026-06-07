## Evaluation Operations Platform

FairEval includes evaluation-operations workflows that make model quality review look like a platform, not a one-off benchmark.

### Release Governance Board

Tracks release outcomes across model versions:

```json
{
  "approved": 7,
  "blocked": 3,
  "rolled_back": 1
}
Artifacts:

release_governance/release_governance_board.json
release_governance/release_governance_board.md
Evaluator Reliability Dashboard

Compares human reviewers, AI evaluators, and candidate self-evaluation across:

agreement score
false allow rate
escalation accuracy

Artifacts:

evaluator_reliability/evaluator_comparison.json
evaluator_reliability/evaluator_reliability_dashboard.md
Experiment Registry

Tracks:

dataset
model
release
score
latency
cost
release decision

Artifacts:

experiment_registry/experiment_registry.json
experiment_registry/experiment_registry_report.md
