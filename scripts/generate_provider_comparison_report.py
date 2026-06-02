import glob
import json
from pathlib import Path

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
compares = sorted(glob.glob("benchmark_public/instruction_following/compares/**/*.json", recursive=True))
gates = sorted(glob.glob("benchmark_public/instruction_following/gates/**/*.json", recursive=True))

latest_by_model = {}
for p in reports:
    data = json.load(open(p))
    model = data.get("config", {}).get("model_name", "unknown")
    latest_by_model[model] = {
        "path": p,
        "run_id": data.get("run_id"),
        "summary": data.get("summary", {}),
    }

comparison = {
    "models": latest_by_model,
    "latest_compare_artifact": compares[-1] if compares else None,
    "latest_gate_artifact": gates[-1] if gates else None,
}

Path("reports/provider_comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")

lines = [
    "# Provider Comparison Report",
    "",
    "FairEval compares provider behavior through benchmark summaries, compare artifacts, and gate outcomes.",
    "",
    "## Latest model runs",
    "",
    "| Model | Avg Score | Pass Rate | Failed Cases | Run ID |",
    "|---|---:|---:|---:|---|",
]

for model, row in sorted(latest_by_model.items()):
    s = row["summary"]
    lines.append(
        f"| {model} | {s.get('avg_score')} | {s.get('pass_rate')} | {s.get('failed_case_count')} | `{row.get('run_id')}` |"
    )

lines += [
    "",
    "## Latest artifacts",
    f"- Compare artifact: `{comparison['latest_compare_artifact']}`",
    f"- Gate artifact: `{comparison['latest_gate_artifact']}`",
    "",
    "## Release-gating interpretation",
    "Provider comparison is used to identify score deltas, pass-rate deltas, failed-case overlap, and deployment risk before model release.",
]

Path("reports/provider_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote reports/provider_comparison.json")
print("Wrote reports/provider_comparison.md")
