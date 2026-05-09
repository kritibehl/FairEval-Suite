# Case Study 02 — Schema Break

## Failure class
Output contract regression

## Scenario
A model is expected to return structured JSON but produces malformed or incomplete fields.

## Why score-only evals miss it
The answer may look semantically correct while downstream parsers fail.

## FairEval signal
- schema break report
- failed constraint artifact
- gate review decision

## Release impact
Schema breaks can cause downstream automation failures even when text quality looks high.
