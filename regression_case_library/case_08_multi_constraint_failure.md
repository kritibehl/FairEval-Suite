# case_08_multi_constraint_failure

## Summary
Model satisfies one instruction but ignores another.

## Baseline behavior
- Correctly balances multiple simultaneous constraints.
- Example: one sentence plus required keyword inclusion.

## Candidate regression
- Follows only the easiest or most obvious instruction.
- Appears partially correct but fails the true task contract.

## Why a naive check might miss it
- Reviewers may reward partial correctness.
- Loose evaluation may not capture multi-constraint failure.

## What FairEval detects
- Missing expected tokens plus degraded pass/fail outcome.
- Candidate is flagged at case level as regressed.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
