# Evaluator Reliability Dashboard

## Comparison

| Evaluator | Agreement Score | False Allow Rate | Escalation Accuracy | Notes |
|---|---:|---:|---:|---|
| human_reviewers | 0.7333 | 0.0 | 0.90 | Three-reviewer agreement with adjudication cases |
| ai_composite_evaluator | 0.86 | 0.0 | 0.88 | Checks grounding, refusal consistency, escalation, and policy bypass |
| candidate_model_self_eval | 0.58 | 0.27 | 0.62 | Misses escalation-required cases |

## Why this matters

Evaluation systems need reliable evaluators, not just model outputs. Comparing human reviewers, AI evaluators, and candidate self-evaluation helps detect evaluator blind spots and false-allow risk.

## Safe scope

Synthetic evaluator reliability dashboard. It does not claim production human-review operations.
