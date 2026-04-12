# case_03_keyword_omission

## Summary
Critical expected term disappears in the candidate response.

## Baseline behavior
- Includes required terms needed for completeness or correctness.
- Preserves important product, safety, or technical language.

## Candidate regression
- Omits one or more critical terms while still sounding coherent.
- Example: explains retrieval-augmented generation without mentioning retrieval context.

## Why a naive check might miss it
- The answer may remain fluent and superficially relevant.
- Reviewers may notice style quality before factual completeness.

## What FairEval detects
- Missing expected keywords directly lower case score.
- Regressed-case count rises even if overall fluency is high.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
