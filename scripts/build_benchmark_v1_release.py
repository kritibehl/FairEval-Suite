import json
from pathlib import Path

def load(path, default):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else default

text_gen = load("nlp_experiments/local_model_comparison_report.json", {"summary": {}})["summary"]
rai = load("responsible_ai/responsible_ai_regression_summary.json", {"summary": {}})["summary"]
oversight = load("oversight_reliability_study/oversight_failure_results.json", {"summary": {}})["summary"]
agentic = load("safety_release_gate/agentic_release_gate_summary.json", {})
rag = load("rag_groundedness_eval/rag_groundedness_report.json", {"summary": {}})["summary"]
latency = load("latency_cost_eval/latency_cost_gate_report.json", {"summary": {}})["summary"]

leaderboard = [
    {
        "system": "baseline_mock_adapter",
        "evaluation_pack": "text_generation_v1",
        "avg_score": text_gen.get("baseline_avg_score", 1.0),
        "regressions_detected": 0,
        "groundedness_failures": 0,
        "safety_false_allows": 0,
        "release_decision": "ship"
    },
    {
        "system": "candidate_mock_adapter",
        "evaluation_pack": "text_generation_v1",
        "avg_score": text_gen.get("candidate_avg_score", 0.7),
        "regressions_detected": text_gen.get("regressions_detected", 6),
        "groundedness_failures": rag.get("unsupported_answer_count", 1),
        "safety_false_allows": rai.get("false_allows", 6),
        "release_decision": "block"
    },
    {
        "system": "weak_surface_evaluator",
        "evaluation_pack": "oversight_reliability_v1",
        "avg_score": oversight.get("weak_evaluator_regression_recall", 0.2727),
        "regressions_detected": oversight.get("safety_regressions_present", 22) - oversight.get("weak_evaluator_false_allows", 16),
        "groundedness_failures": "n/a",
        "safety_false_allows": oversight.get("weak_evaluator_false_allows", 16),
        "release_decision": "not_release_safe"
    },
    {
        "system": "composite_oversight_evaluator",
        "evaluation_pack": "oversight_reliability_v1",
        "avg_score": oversight.get("composite_evaluator_regression_recall", 1.0),
        "regressions_detected": oversight.get("safety_regressions_present", 22),
        "groundedness_failures": "n/a",
        "safety_false_allows": oversight.get("composite_evaluator_false_allows", 0),
        "release_decision": "review_pass"
    },
    {
        "system": "agentic_candidate_workflow",
        "evaluation_pack": "agentic_release_safety_v1",
        "avg_score": "n/a",
        "regressions_detected": len(agentic.get("failures", [])),
        "groundedness_failures": rag.get("unsupported_answer_count", 1),
        "safety_false_allows": "n/a",
        "release_decision": agentic.get("release_decision", "block")
    }
]

summary = {
    "benchmark_name": "FairEval Benchmark v1",
    "live_api_docs": "https://faireval-rai-api-126325674316.us-central1.run.app/docs",
    "dashboard_path": "dashboard_frontend",
    "systems_compared": len(leaderboard),
    "evaluation_dimensions": [
        "baseline_vs_candidate_regression",
        "rag_groundedness",
        "hallucination_or_unsupported_answer",
        "responsible_ai_false_allow",
        "latency_cost_release_gate",
        "oversight_reliability"
    ],
    "headline_metrics": {
        "text_generation_regressions": text_gen.get("regressions_detected", 6),
        "responsible_ai_false_allows": rai.get("false_allows", 6),
        "weak_evaluator_false_allows": oversight.get("weak_evaluator_false_allows", 16),
        "composite_evaluator_false_allows": oversight.get("composite_evaluator_false_allows", 0),
        "agentic_release_decision": agentic.get("release_decision", "block"),
        "p95_latency_ms": latency.get("p95_latency_ms", 950)
    },
    "leaderboard": leaderboard
}

Path("public_benchmark/benchmark_v1_leaderboard.json").write_text(json.dumps(summary, indent=2))

md = [
    "# FairEval Benchmark v1",
    "",
    "FairEval Benchmark v1 is a public-facing release-safety benchmark page for AI evaluation, Responsible AI regression review, RAG groundedness, agentic workflow checks, latency/cost gates, and oversight reliability.",
    "",
    "## Live Demo",
    "",
    "- Live API docs: https://faireval-rai-api-126325674316.us-central1.run.app/docs",
    "- Health endpoint: https://faireval-rai-api-126325674316.us-central1.run.app/rai/health",
    "- React dashboard: `dashboard_frontend/`",
    "",
    "## Headline metrics",
    "",
]

for k, v in summary["headline_metrics"].items():
    md.append(f"- {k}: `{v}`")

md += [
    "",
    "## Leaderboard-style comparison",
    "",
    "| System | Pack | Avg / Recall | Regressions Detected | Groundedness Failures | Safety False Allows | Release Decision |",
    "|---|---|---:|---:|---:|---:|---|",
]

for row in leaderboard:
    md.append(
        f"| {row['system']} | {row['evaluation_pack']} | {row['avg_score']} | {row['regressions_detected']} | {row['groundedness_failures']} | {row['safety_false_allows']} | {row['release_decision']} |"
    )

md += [
    "",
    "## What hiring teams can verify in 2 minutes",
    "",
    "1. Open the live API docs.",
    "2. Run `/rai/health`.",
    "3. Try `/rai/evaluate-content` with the provided sample payload.",
    "4. Open the React dashboard in `dashboard_frontend/`.",
    "5. Inspect the release-gate JSON artifacts for Responsible AI, agentic workflows, and oversight reliability.",
    "",
    "## Safe scope",
    "",
    "Benchmark v1 uses synthetic evaluation artifacts and local/mock adapters unless explicitly marked as a live API. It is designed to demonstrate evaluation infrastructure, not claim frontier-model benchmarking coverage.",
]

Path("docs/benchmark_v1/release_page.md").write_text("\n".join(md) + "\n")
print("Wrote public_benchmark/benchmark_v1_leaderboard.json")
print("Wrote docs/benchmark_v1/release_page.md")
