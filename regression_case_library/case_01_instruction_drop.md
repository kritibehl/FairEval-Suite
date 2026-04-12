# case_01_instruction_drop

## Summary
Instruction dropped despite an otherwise fluent answer.

## Baseline behavior
- Follows the requested instruction exactly.
- Produces a response that satisfies both content and formatting constraints.

## Candidate regression
- Answers the general question correctly but ignores the explicit instruction.
- Example: asked for one sentence, returns a paragraph.

## Why a naive check might miss it
- Surface-level quality still appears strong.
- Human reviewer may read the answer as “good enough” and overlook instruction non-compliance.

## What FairEval detects
- Missing required expected terms or format-aligned content.
- Reduced pass rate even when language quality appears acceptable.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
