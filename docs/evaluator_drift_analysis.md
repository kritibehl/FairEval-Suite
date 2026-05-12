# Evaluator Drift Analysis

Evaluator drift analysis helps separate model regressions from evaluation-system changes.

FairEval checks:
- prompt version drift
- evaluator version drift
- threshold version drift
- dataset hash drift
- failed-case set changes

## Why this matters
A release regression may be caused by:
- the model changing
- the prompt changing
- the benchmark dataset changing
- the evaluator/scorer changing
- the gate threshold changing

FairEval records and compares these dimensions so release decisions remain reproducible and auditable.
