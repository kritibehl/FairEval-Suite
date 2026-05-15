# Deploy FairEval Responsible AI Risk Evaluation API to Cloud Run

## Endpoints
- `GET /rai/health`
- `POST /rai/evaluate-content`
- `POST /rai/evaluate-batch`
- `GET /rai/release-decision/{run_id}`

## Deploy using source

```bash
gcloud run deploy faireval-rai-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
Smoke test
LIVE_URL="PASTE_REAL_CLOUD_RUN_URL"

curl "$LIVE_URL/rai/health"

curl -X POST "$LIVE_URL/rai/evaluate-content" \
  -H "Content-Type: application/json" \
  -d @responsible_ai_service/sample_text_risk_request.json
Safe scope

Lightweight deployed Responsible AI risk-evaluation service for synthetic risk-review workflows. Not a production moderation system.
