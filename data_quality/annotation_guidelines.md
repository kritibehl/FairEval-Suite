# Annotation Guidelines

## Purpose
These guidelines standardize how evaluation cases, failed outputs, and regression findings are reviewed within FairEval.

## Annotation goals
- identify instruction-following failures
- detect schema violations
- identify hallucinated fields
- validate formatting constraints
- capture consistency regressions
- classify release-risk severity

## Reviewer rules
- evaluate outputs against explicit constraints only
- avoid subjective stylistic scoring
- flag missing required fields
- flag malformed JSON or invalid schema output
- record uncertainty explicitly

## Severity levels
- low: cosmetic issue
- medium: partial instruction failure
- high: schema break or failed contract
- critical: unsafe release candidate

## Required metadata
- case_id
- reviewer
- prompt_version
- model_name
- failed_constraint
- release_risk
- notes
