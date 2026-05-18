# Monitoring Endpoint Plan

FairEval currently exposes:
- `/rai/health`
- `/rai/release-decision/{run_id}`

These provide lightweight service-health and release-governance signals.

## Future monitoring endpoint
A future `/rai/monitoring/summary` endpoint could expose:
- total evaluations
- release blocks
- false allows
- human-review actions
- high-risk categories
- service-readiness metrics

## Safe scope
Current monitoring is lightweight and endpoint-based. This is not production observability infrastructure.
