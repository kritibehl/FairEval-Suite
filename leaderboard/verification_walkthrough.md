# Leaderboard Verification Walkthrough

## What this leaderboard shows
- groundedness
- hallucination risk
- instruction adherence
- p95 latency
- cost/request
- release readiness

## Verify locally
Open:

```text
leaderboard/leaderboard.html
Inspect:

leaderboard/model_comparison.json
Safe scope

This leaderboard combines local/mock and provider-style artifacts. It should not be described as a live frontier-model leaderboard unless real provider runs succeed with stored raw responses.
