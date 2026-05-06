import csv, json, glob
from pathlib import Path

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
gates = sorted(glob.glob("benchmark_public/instruction_following/gates/**/*.json", recursive=True))
variance_path = Path("benchmark_public/instruction_following/variance_summary.json")

exports = Path("exports")
exports.mkdir(exist_ok=True)

rows = []
for p in reports:
    data = json.load(open(p))
    s = data.get("summary", {})
    c = data.get("config", {})
    rows.append({
        "run_id": data.get("run_id"),
        "model_name": c.get("model_name"),
        "suite_name": c.get("suite_name"),
        "avg_score": s.get("avg_score"),
        "pass_rate": s.get("pass_rate"),
        "failed_case_count": s.get("failed_case_count"),
        "num_cases": s.get("num_cases"),
        "artifact_path": p,
    })

with open(exports / "faireval_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["run_id"])
    writer.writeheader()
    writer.writerows(rows)

latest_gate = json.load(open(gates[-1])) if gates else {}
variance = json.load(open(variance_path)) if variance_path.exists() else {}

summary = {
    "run_count": len(rows),
    "models": sorted({r["model_name"] for r in rows if r.get("model_name")}),
    "latest_gate": {
        "decision": latest_gate.get("decision"),
        "release_decision": latest_gate.get("release_decision"),
        "reason": latest_gate.get("reason"),
    },
    "variance": variance,
}

(exports / "faireval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
