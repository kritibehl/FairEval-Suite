# case_09_consistency_drop

## Summary
Candidate becomes inconsistent across closely related prompts.

## Baseline behavior
- Produces stable answers across minor prompt variations.
- Maintains predictable behavior under repeated evaluation.

## Candidate regression
- Gives uneven quality across near-identical tasks.
- Some cases pass while adjacent ones degrade sharply.

## Why a naive check might miss it
- Single-case spot checks may pass.
- Inconsistency only appears across a grouped evaluation pack.

## What FairEval detects
- Pack-level pass-rate degradation.
- Higher regressed-case count across a benchmark slice.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
