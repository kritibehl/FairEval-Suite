from pathlib import Path
import json

required = [
    "exports/faireval_results.csv",
    "exports/faireval_summary.json",
    "exports/dashboard_screenshot.png",
    "reports/prompt_regression_report.json",
    "reports/schema_breaks.json",
    "reports/failed_constraints.csv",
    "reports/provider_comparison.md",
    "benchmark_public/benchmark_card.md",
    "docs/ml_platform_upgrade.md",
    "docs/why_score_only_evals_fail.md",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    raise SystemExit(f"Missing required artifacts: {missing}")

summary = json.loads(Path("exports/faireval_summary.json").read_text())
print("Artifact validation passed")
print(json.dumps({
    "run_count": summary.get("run_count"),
    "models": summary.get("models"),
    "latest_gate": summary.get("latest_gate"),
}, indent=2))
