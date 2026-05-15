# Responsible AI Risk Evaluation Service Contract

## Purpose
FairEval exposes a lightweight Responsible AI risk-evaluation API for synthetic text-content scenarios.

## Endpoints
- `POST /rai/evaluate-content`
- `POST /rai/evaluate-batch`
- `GET /rai/runs/{run_id}`
- `GET /rai/release-decision/{run_id}`
- `GET /rai/health`

## Output signals
- risk categories
- risk severity
- recommended mitigation action
- review reason
- telemetry tags
- release recommendation

## Safe claim boundary
This is a Responsible AI risk evaluation service and synthetic risk-review workflow. It is not a production moderation API, content-safety classifier, or Azure AI Content Safety replacement.
