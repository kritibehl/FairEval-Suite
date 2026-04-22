# case_02_format_regression

## Summary
Required output format violated after a model update.

## Baseline behavior
- Produces output in the exact requested structure.
- Example: valid JSON or exact bullet count.

## Candidate regression
- Returns natural language prose instead of the required structure.
- Breaks downstream consumers expecting machine-readable output.

## Why a naive check might miss it
- The semantic content can still look correct to a human.
- Basic quality scoring may overrate the answer even though it is operationally unusable.

## What FairEval detects
- Expected structure-related keywords or fields are missing.
- Regression appears in pass-rate drop and case-level failure.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
