import csv
import glob
import json
from pathlib import Path

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
if not reports:
    raise SystemExit("No benchmark reports found.")

latest = reports[-1]
data = json.load(open(latest))
results = data.get("results", [])

out_dir = Path("reports")
out_dir.mkdir(exist_ok=True)

failed = [r for r in results if not r.get("passed", False)]

prompt_report = {
    "run_id": data.get("run_id"),
    "model_name": data.get("config", {}).get("model_name"),
    "summary": data.get("summary"),
    "failure_categories": {
        "instruction_drops": [r["case_id"] for r in failed if "instruction" in r["case_id"].lower() or r["score"] < 0.5],
        "format_failures": [r["case_id"] for r in failed if "format" in str(r.get("details", {})).lower()],
        "consistency_drops": [r["case_id"] for r in failed if "variance" in str(r.get("details", {})).lower()],
    },
    "failed_cases": failed,
}

schema_breaks = {
    "run_id": data.get("run_id"),
    "schema_breaks": [
        {
            "case_id": r["case_id"],
            "reason": "failed_required_output_contract",
            "score": r.get("score"),
        }
        for r in failed
    ],
}

(out_dir / "prompt_regression_report.json").write_text(json.dumps(prompt_report, indent=2), encoding="utf-8")
(out_dir / "schema_breaks.json").write_text(json.dumps(schema_breaks, indent=2), encoding="utf-8")

with open(out_dir / "failed_constraints.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["case_id", "score", "passed", "failure_type"])
    writer.writeheader()
    for r in failed:
        writer.writerow({
            "case_id": r.get("case_id"),
            "score": r.get("score"),
            "passed": r.get("passed"),
            "failure_type": "constraint_or_quality_failure",
        })

print("Wrote reports/prompt_regression_report.json")
print("Wrote reports/schema_breaks.json")
print("Wrote reports/failed_constraints.csv")
