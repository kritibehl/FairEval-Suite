import json
from pathlib import Path

DATA = Path("latency_cost_eval/latency_cost_samples.json")
OUT = Path("latency_cost_eval/latency_cost_gate_report.json")
MD = Path("latency_cost_eval/latency_cost_gate_report.md")

data = json.loads(DATA.read_text())
samples = data["samples"]
thresholds = data["thresholds"]

latencies = sorted(s["latency_ms"] for s in samples)
p95 = latencies[int(round(0.95 * (len(latencies) - 1)))]
avg_cost = sum(s["cost_usd"] for s in samples) / len(samples)
max_cost = max(s["cost_usd"] for s in samples)

latency_fail = p95 > thresholds["max_p95_latency_ms"]
cost_fail = max_cost > thresholds["max_cost_per_request_usd"]

summary = {
    "num_requests": len(samples),
    "p95_latency_ms": p95,
    "avg_cost_per_request_usd": round(avg_cost, 6),
    "max_cost_per_request_usd": max_cost,
    "latency_fail": latency_fail,
    "cost_fail": cost_fail,
    "release_decision": "block" if latency_fail or cost_fail else "ship"
}

OUT.write_text(json.dumps({"summary": summary, "samples": samples}, indent=2))

MD.write_text(
    "\n".join([
        "# Latency and Cost Gate Report",
        "",
        f"- requests: {summary['num_requests']}",
        f"- p95 latency ms: {summary['p95_latency_ms']}",
        f"- avg cost/request USD: {summary['avg_cost_per_request_usd']}",
        f"- max cost/request USD: {summary['max_cost_per_request_usd']}",
        f"- latency fail: {summary['latency_fail']}",
        f"- cost fail: {summary['cost_fail']}",
        f"- release decision: `{summary['release_decision']}`",
    ]) + "\n"
)

print(json.dumps(summary, indent=2))
