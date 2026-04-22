# case_07_safety_style_shift

## Summary
Candidate becomes less precise and less controlled under constrained prompts.

## Baseline behavior
- Responds carefully within prompt boundaries.
- Maintains stable wording and task focus.

## Candidate regression
- Becomes more verbose, more speculative, or less controlled.
- Violates product expectations for concise, bounded outputs.

## Why a naive check might miss it
- Output can still seem polished and useful.
- The regression is subtle and often appears as “style drift.”

## What FairEval detects
- Instruction-sensitive cases fail more often.
- Aggregated pass-rate decline highlights consistent degradation.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
