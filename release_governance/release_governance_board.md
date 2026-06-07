# Release Governance Board

## Summary

```json
{
  "approved": 7,
  "blocked": 3,
  "rolled_back": 1,
  "needs_review": 2
}
Governance Signals
Signal	Why it matters
approved	Candidate met release-readiness criteria
blocked	Candidate introduced quality or safety regressions
rolled_back	Candidate required rollback after evaluation failure
needs_review	Candidate required human-review escalation
Example Decisions
Release	Model	Decision	Reason
rel-v1	baseline_mock_adapter	approved	Passed groundedness, formatting, and Responsible AI checks
rel-v2	candidate_mock_adapter	blocked	False allows, groundedness regressions, and ranking regressions detected
rel-v3	candidate_recommender_v2	needs_review	Hit rate preserved but recommendation precision dropped
rel-v4	agentic_candidate_workflow	rolled_back	Unsupported action attempted during blocked-release approval workflow
Safe scope

Synthetic release-governance artifact for AI evaluation operations.
