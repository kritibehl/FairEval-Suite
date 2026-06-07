import json
from pathlib import Path

DATA = Path("experiment_registry/experiment_registry.json")
OUT = Path("experiment_registry/experiment_registry_report.md")

data = json.loads(DATA.read_text())
experiments = data["experiments"]

blocked = [e for e in experiments if e["decision"] in {"blocked", "rolled_back"}]
avg_score = sum(e["score"] for e in experiments) / len(experiments)
avg_latency = sum(e["latency_ms"] for e in experiments) / len(experiments)
avg_cost = sum(e["cost_usd"] for e in experiments) / len(experiments)

summary = {
    "total_experiments": len(experiments),
    "blocked_or_rolled_back": len(blocked),
    "avg_score": round(avg_score, 4),
    "avg_latency_ms": round(avg_latency, 4),
    "avg_cost_usd": round(avg_cost, 6)
}

Path("experiment_registry/experiment_registry_summary.json").write_text(
    json.dumps(summary, indent=2)
)

md = [
    "# Experiment Registry Report",
    "",
    f"- total experiments: {summary['total_experiments']}",
    f"- blocked or rolled back: {summary['blocked_or_rolled_back']}",
    f"- avg score: {summary['avg_score']}",
    f"- avg latency ms: {summary['avg_latency_ms']}",
    f"- avg cost USD: {summary['avg_cost_usd']}",
    "",
    "| Experiment | Dataset | Model | Release | Score | Latency ms | Cost USD | Decision |",
    "|---|---|---|---|---:|---:|---:|---|",
]

for e in experiments:
    md.append(
        f"| {e['experiment_id']} | {e['dataset']} | {e['model']} | {e['release']} | {e['score']} | {e['latency_ms']} | {e['cost_usd']} | {e['decision']} |"
    )

OUT.write_text("\n".join(md) + "\n")
print(json.dumps(summary, indent=2))
