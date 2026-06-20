# Data Quality Audit Report

## Audit scope
FairEval benchmark and regression-review workflows.

## Sample size
- reviewed cases: 10
- failed cases: 6
- repeated-run evaluations reviewed: 3

## Labeling disagreement
- disagreement cases identified: 2
- common issue: partial instruction completion ambiguity

## Schema issues
- malformed JSON outputs detected
- missing required fields detected
- formatting drift observed in structured-output cases

## Missing fields
- omitted required constraints
- incomplete schema responses
- missing metadata in failed-case exports

## Recommended corrections
- enforce stricter schema validation
- require explicit constraint tagging
- standardize failed-case severity levels
- expand evaluator review guidance

## Operational impact
Undetected schema failures and instruction drops can produce incorrect release decisions or downstream automation failures.

## Recommended release action
review_before_release
