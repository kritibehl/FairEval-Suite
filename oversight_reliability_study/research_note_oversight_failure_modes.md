# Oversight Failure Modes in Synthetic Responsible AI Regression Review

## Abstract
This note studies whether simple surface-level safety evaluators miss materially unsafe model-output regressions in synthetic Responsible AI review scenarios. The experiment compares a weak evaluator against a composite evaluator that checks grounding, escalation, refusal consistency, sensitive-data risk, policy-bypass handling, and unsupported claims.

## Research Question
Do simple surface-level safety evaluation rules miss false-allow regressions that a composite evaluator with grounding, escalation, and refusal-consistency signals can detect?

## Experimental Setup
The study uses synthetic Responsible AI regression scenarios. Each scenario includes a safer baseline output and a degraded candidate output. The goal is not to generate harmful content, but to test whether evaluators detect risky release behavior.

## Scenario Taxonomy
Scenarios are grouped into:
- sensitive_data_exposure_risk
- policy_bypass_attempt
- unsupported_high_stakes_claim
- grounding_failure
- refusal_inconsistency
- human_review_escalation_gap
- instruction_conflict
- ambiguous_risk_case

## Evaluator Designs

### Weak / Surface Evaluator
Checks:
- direct refusal or hold present
- obvious sensitive-risk label
- basic formatting pass

### Composite Oversight Evaluator
Checks:
- unsupported claim risk
- missing human-review escalation
- refusal inconsistency
- sensitive-data exposure risk
- policy-bypass attempt handling
- grounding failure
- high-stakes response without evidence

## Results
The generated results are stored in:
- `oversight_failure_results.json`
- `oversight_failure_report.md`

The key comparison is the number of false allows from the weak evaluator versus the composite evaluator, plus recall for known safety regressions and evaluator disagreement rate.

## Failure Cases
Important failure modes include:
- candidate output appears fluent but lacks grounding
- candidate output allows a request that should require review
- candidate output misses human-review escalation
- surface evaluator fails because it only checks obvious refusal text
- composite evaluator catches risk through multiple independent signals

## Limitations
This is a synthetic, rule-based oversight experiment. It does not claim production safety evaluation, human preference modeling, or real-world red-team coverage. It is a controlled portfolio experiment for studying oversight failure modes.

## Why This Matters for Scalable Oversight
If oversight systems rely only on shallow refusal or formatting signals, they may miss materially unsafe regressions. Composite evaluators can reduce false allows by combining grounding, escalation, refusal-consistency, and risk-category checks.

## Next Experiments
- add human-labeled evaluator disagreement cases
- compare model-graded vs rule-graded safety judgments
- add uncertainty estimates for evaluator decisions
- evaluate evaluator drift across prompt and policy versions
- connect safety-regression events to monitoring and incident review
