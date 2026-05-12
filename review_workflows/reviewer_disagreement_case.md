# Reviewer Disagreement Case

## Case
`pr-003`

## Prompt
Return valid JSON with keys `decision` and `reason`.

## Reviewer A
Marked as pass because the output included a decision field.

## Reviewer B
Marked as fail because the `reason` field was missing.

## Resolution
Required schema fields are mandatory. The case remains failed.

## Governance rule
When a prompt specifies explicit output fields, all required fields must be present for the case to pass.

## Release impact
Missing required fields can break downstream automation, so this should trigger review-before-release or block-until-resolved depending on severity.
