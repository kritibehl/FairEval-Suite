#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${VIRTUAL_ENV:+$VIRTUAL_ENV/bin/python}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "=== FairEval AI Reliability Demo ==="

mkdir -p demo

cat > demo/baseline_report.json <<'JSON'
{
  "run_id": "baseline-demo",
  "config": {"suite_name": "demo", "model_name": "mock"},
  "summary": {"num_cases": 2, "avg_score": 0.90, "pass_rate": 1.0},
  "results": [
    {"case_id": "case-1", "score": 0.92, "passed": true, "details": {"model_output": "baseline ok", "latency_ms": 41.2, "cost_usd": 0.0}},
    {"case_id": "case-2", "score": 0.88, "passed": true, "details": {"model_output": "baseline ok", "latency_ms": 44.8, "cost_usd": 0.0}}
  ]
}
JSON

cat > demo/candidate_report.json <<'JSON'
{
  "run_id": "candidate-demo",
  "config": {"suite_name": "demo", "model_name": "mock"},
  "summary": {"num_cases": 2, "avg_score": 0.70, "pass_rate": 0.5},
  "results": [
    {"case_id": "case-1", "score": 0.75, "passed": true, "details": {"model_output": "candidate weaker", "latency_ms": 73.2, "cost_usd": 0.0}},
    {"case_id": "case-2", "score": 0.65, "passed": false, "details": {"model_output": "candidate failed", "latency_ms": 85.1, "cost_usd": 0.0}}
  ]
}
JSON

"$PYTHON_BIN" -m uvicorn api.main:app --host 127.0.0.1 --port 8000 &
UV_PID=$!
sleep 3

echo
echo "Health:"
curl -s http://localhost:8000/health
echo

echo
echo "Compare:"
curl -s -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "baseline_report_path": "demo/baseline_report.json",
    "candidate_report_path": "demo/candidate_report.json",
    "top_k": 5
  }'
echo

COMPARE_FILE=$(ls compare/*.json | tail -n 1)

echo
echo "Gate:"
curl -s -X POST "http://localhost:8000/gate" \
  -H "Content-Type: application/json" \
  -d "{
    \"compare_artifact_path\": \"$COMPARE_FILE\",
    \"max_avg_score_drop\": 0.05,
    \"max_pass_rate_drop\": 0.10,
    \"fail_on_any_regression_case\": true
  }"
echo

echo
echo "Traces:"
curl -s http://localhost:8000/traces
echo

kill $UV_PID
