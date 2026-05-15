# Responsible AI Evaluation Service Contract

## Endpoints

### POST `/responsible-ai/evaluate`
Submit or retrieve a Responsible AI safety-evaluation summary.

### GET `/responsible-ai/runs/{run_id}`
Return safety-regression run details.

### GET `/responsible-ai/release-decision/{run_id}`
Return release-decision fields for automation.

## Returned fields
- run_id
- release_decision
- safety_regressions
- false_allows
- human_review_required
- triggered_risk_categories

## Safe scope
This is a lightweight service API around synthetic Responsible AI evaluation artifacts. It is not a production policy engine or deployed trust-and-safety system.
