#!/usr/bin/env bash
set -euo pipefail

echo "Starting FairEval API locally..."
echo "Run this in a separate terminal:"
echo "uvicorn api.main:app --reload"
echo
echo "Then open:"
echo "http://localhost:8000/docs"
echo
echo "Example evaluate call:"
cat <<'CMD'
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "suite_name": "rag_basic",
    "dataset_path": "demo/rag_demo_cases.jsonl",
    "model_name": "mock",
    "max_workers": 1,
    "timeout_seconds": 5.0
  }'
CMD
