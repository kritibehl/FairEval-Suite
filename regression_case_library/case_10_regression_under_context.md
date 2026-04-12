# case_10_regression_under_context

## Summary
Candidate degrades when lightweight context is present.

## Baseline behavior
- Correctly incorporates short contextual grounding.
- Uses provided context without drifting away from it.

## Candidate regression
- Ignores context or responds with generic prior knowledge.
- Looks fluent but loses groundedness.

## Why a naive check might miss it
- Ungrounded answers can still sound plausible.
- Reviewers may not compare output directly against provided context.

## What FairEval detects
- Lower context overlap on RAG-style cases.
- Clear regressions in context-sensitive evaluation mode.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
