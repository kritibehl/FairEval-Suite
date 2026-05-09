#!/usr/bin/env bash
set -euo pipefail

echo "== FairEval demo: prompt regression =="
python evals/prompt_regression/run_prompt_regression.py

echo "== Export dashboard reports =="
python scripts/export_dashboard_reports.py

echo "== Export regression reports =="
python scripts/export_regression_reports.py

echo "== Generate provider comparison report =="
python scripts/generate_provider_comparison_report.py

echo "== Generate run lineage =="
python scripts/generate_run_lineage.py

echo "== Demo complete =="
find exports reports artifacts/run_lineage -maxdepth 2 -type f | sort
