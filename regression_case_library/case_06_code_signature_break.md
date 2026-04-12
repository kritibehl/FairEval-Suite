# case_06_code_signature_break

## Summary
Generated code misses the required function signature or interface contract.

## Baseline behavior
- Produces code with the requested function name and expected return path.
- Matches the minimal callable contract.

## Candidate regression
- Returns code that is syntactically plausible but interface-incompatible.
- Example: wrong function name, missing return, extra wrapper text.

## Why a naive check might miss it
- Code may still look “correct” on quick visual scan.
- Non-executable review misses interface-level breakage.

## What FairEval detects
- Expected signature tokens are absent.
- Candidate is marked regressed even when code quality appears reasonable.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
