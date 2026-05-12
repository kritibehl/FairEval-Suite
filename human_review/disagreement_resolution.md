# Human Review and Disagreement Resolution

## Review states
- pending_review
- approved
- rejected
- needs_second_reviewer
- escalated

## Override policy
Annotation overrides must include:
- reviewer name or ID
- original label
- corrected label
- reason
- downstream impact
- timestamp

## Disagreement process
1. identify evaluator disagreement
2. compare against written expected behavior
3. classify severity
4. record override or escalation
5. update case library if ambiguity is recurring
