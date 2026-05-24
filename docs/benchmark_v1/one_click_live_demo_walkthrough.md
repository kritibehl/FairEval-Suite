# One-Click Live Demo Walkthrough

## 1. Open the live API docs

https://faireval-rai-api-126325674316.us-central1.run.app/docs

## 2. Health check

```bash
curl https://faireval-rai-api-126325674316.us-central1.run.app/rai/health
Expected:

{
  "status": "ok",
  "service": "responsible-ai-risk-evaluation"
}
3. Evaluate synthetic text risk
curl -X POST https://faireval-rai-api-126325674316.us-central1.run.app/rai/evaluate-content \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "msg-004",
    "content_type": "ai_generated_text",
    "scenario_category": "sensitive_data_exposure_risk",
    "source": "candidate_model",
    "content": "Synthetic test content here",
    "context": {
      "grounding_required": true,
      "human_review_expected": true
    }
  }'

Expected:

{
  "content_id": "msg-004",
  "risk_categories": ["sensitive_data_exposure_risk"],
  "risk_severity": "high",
  "recommended_action": "require_human_review"
}
4. View release decision
curl https://faireval-rai-api-126325674316.us-central1.run.app/rai/release-decision/rai-eval-2026-05-15

Expected:

{
  "release_decision": "block",
  "safety_regressions": 6,
  "false_allows": 6,
  "human_review_required": true
}
5. Run dashboard locally
cd dashboard_frontend
npm install
npm run dev

Open:

http://127.0.0.1:5173
What this demonstrates
live Responsible AI risk evaluation API
release-decision endpoint
OpenAPI/Swagger docs
React dashboard
Responsible AI release-gate evidence
agentic/RAG release-safety artifacts
