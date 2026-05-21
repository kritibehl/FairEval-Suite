import json
from pathlib import Path

rag = json.loads(Path("rag_groundedness_eval/rag_groundedness_report.json").read_text())["summary"]
latency = json.loads(Path("latency_cost_eval/latency_cost_gate_report.json").read_text())["summary"]

failures = []

if rag["unsupported_answer_count"] > 0:
    failures.append("unsupported_answers_detected")

if rag["hallucination_detected_count"] > 0:
    failures.append("hallucination_detected")

if latency["latency_fail"]:
    failures.append("latency_threshold_failed")

if latency["cost_fail"]:
    failures.append("cost_threshold_failed")

release_decision = "block" if failures else "ship"

summary = {
    "rag_groundedness_pass_count": rag["groundedness_pass_count"],
    "unsupported_answer_count": rag["unsupported_answer_count"],
    "hallucination_detected_count": rag["hallucination_detected_count"],
    "p95_latency_ms": latency["p95_latency_ms"],
    "max_cost_per_request_usd": latency["max_cost_per_request_usd"],
    "failures": failures,
    "release_decision": release_decision
}

Path("safety_release_gate/agentic_release_gate_summary.json").write_text(
    json.dumps(summary, indent=2)
)

Path("safety_release_gate/agentic_release_gate_report.md").write_text(
    "\n".join([
        "# Agentic System Release Gate Report",
        "",
        f"- RAG groundedness pass count: {summary['rag_groundedness_pass_count']}",
        f"- Unsupported answers: {summary['unsupported_answer_count']}",
        f"- Hallucinations detected: {summary['hallucination_detected_count']}",
        f"- p95 latency ms: {summary['p95_latency_ms']}",
        f"- max cost/request USD: {summary['max_cost_per_request_usd']}",
        f"- failures: {', '.join(failures) or '-'}",
        f"- release decision: `{release_decision}`",
    ]) + "\n"
)

print(json.dumps(summary, indent=2))
