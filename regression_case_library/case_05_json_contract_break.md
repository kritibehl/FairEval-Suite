# case_05_json_contract_break

## Summary
Candidate returns invalid or incomplete JSON, breaking downstream parsing.

## Baseline behavior
- Produces valid JSON with all required keys.
- Supports downstream automation without manual repair.

## Candidate regression
- Omits required keys or returns malformed JSON-like text.
- Causes runtime failures in consumers that rely on schema stability.

## Why a naive check might miss it
- The response may “look like JSON” at a glance.
- Human readers may not verify strict schema compliance.

## What FairEval detects
- Required keys or expected fields are missing.
- Pass-rate drops on cases with structured-output requirements.

## Expected release decision
- BLOCK

## Notes
- Synthetic but production-plausible case.
