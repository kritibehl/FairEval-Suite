import glob
import json
from pathlib import Path

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*gemini_real*.json"))
if not reports:
    raise SystemExit("No benchmark reports found")

p = reports[-1]
data = json.load(open(p))

failed = [r for r in data.get("results", []) if not r.get("passed", False)]

artifact = {
    "scenario": "llm_instruction_following_benchmark",
    "failure_class": "ai_quality_regression",
    "metrics": {
        "avg_score": data.get("summary", {}).get("avg_score"),
        "pass_rate": data.get("summary", {}).get("pass_rate"),
        "failed_case_count": data.get("summary", {}).get("failed_case_count"),
        "num_cases": data.get("summary", {}).get("num_cases"),
    },
    "recommendation": "review_before_release" if failed else "safe_to_release",
    "safe": False if failed else True,
    "operator_summary": {
        "top_failed_cases": [r.get("case_id") for r in failed[:5]],
        "benchmark_run_id": data.get("run_id"),
        "model_name": data.get("config", {}).get("model_name"),
    },
}

out = Path("benchmark_public/instruction_following/autoops_signal.json")
out.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
print(json.dumps(artifact, indent=2))
print(f"\nWrote {out}")
