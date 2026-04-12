# case_04_length_violation

## Summary
Candidate exceeds a strict brevity or length constraint.

## Baseline behavior
- Obeys the requested brevity bound.
- Example: under 20 words or exactly one sentence.

## Candidate regression
- Produces a longer response that violates product UX constraints.
- The answer may still be semantically good but operationally wrong.

## Why a naive check might miss it
- Traditional evaluation often rewards completeness and detail.
- It may fail to penalize instruction non-compliance.

## What FairEval detects
- Missing format-aligned success conditions.
- Case fails despite acceptable language quality.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
