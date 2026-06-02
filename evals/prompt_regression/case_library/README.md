# Prompt Regression Case Library

This library documents prompt-level regressions that FairEval is designed to catch.

## Failure classes
- instruction drop
- hallucinated fields
- schema failure
- safety-style drift
- truncation
- formatting regression
- consistency failure
- multi-constraint failure

## Why this matters
Prompt regressions often preserve surface-level fluency while breaking product contracts. FairEval treats those as release risks, not cosmetic issues.
