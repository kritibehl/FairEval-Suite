# Regression Case Library

This library documents realistic cases where a release gate should block a candidate model update.

## Cases
- case_01_instruction_drop — instruction followed by baseline, ignored by candidate
- case_02_format_regression — required output structure breaks
- case_03_keyword_omission — critical expected term disappears
- case_04_length_violation — brevity constraint regresses
- case_05_json_contract_break — structured output becomes invalid
- case_06_code_signature_break — generated code breaks interface contract
- case_07_safety_style_shift — output control degrades
- case_08_multi_constraint_failure — one instruction followed, another ignored
- case_09_consistency_drop — stability drops across similar prompts
- case_10_regression_under_context — context-sensitive behavior regresses

## Why this matters
Most model regressions are not obvious quality collapses. They are subtle contract violations:
- formatting drift
- omission of required content
- instability under small prompt changes
- structured-output failures
- degraded behavior under context

FairEval is designed to catch these before deployment.
