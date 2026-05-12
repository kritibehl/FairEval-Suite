# Local Inference API Example

This demo shows a tiny local inference-style workflow for FairEval.

## Example request

```json
{
  "request_id": "req-001",
  "prompt": "Return JSON with decision and reason.",
  "batch_size": 1
}
Example response
{
  "decision": "review",
  "reason": "schema-sensitive output requires validation"
}
Captured fields
request ID
prompt
response
latency
batch size
token count estimate
Safe scope

This demonstrates inference workflow familiarity and latency measurement. It does not claim production model serving or distributed inference infrastructure.
