#!/usr/bin/env bash
set -euo pipefail

python -m evals.cli run \
  --suite classification_basic \
  --model distilbert-sst2 \
  --out-dir real_model_artifacts

REPORT_ID=$(ls real_model_artifacts/reports/*.json | head -n 1)
echo "Generated report: $REPORT_ID"
sed -n '1,240p' "$REPORT_ID"
