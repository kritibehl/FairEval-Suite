import json
from pathlib import Path

PACK = Path("agent_eval_packs/agent_eval_scenarios.json")
OUT = Path("rag_groundedness_eval/rag_groundedness_report.json")
MD = Path("rag_groundedness_eval/rag_groundedness_report.md")

data = json.loads(PACK.read_text())
rows = []

for s in data["scenarios"]:
    answer = s["candidate_answer"].lower()
    context = " ".join(s["retrieved_context"]).lower()

    missing_expected = [
        term for term in s["expected_terms"]
        if term.lower() not in answer
    ]
    hallucinated_terms = [
        term for term in s["forbidden_terms"]
        if term.lower() in answer and term.lower() not in context
    ]

    unsupported_answer = bool(hallucinated_terms)
    groundedness_pass = not missing_expected and not hallucinated_terms

    rows.append({
        "scenario_id": s["scenario_id"],
        "task_type": s["task_type"],
        "groundedness_pass": groundedness_pass,
        "unsupported_answer": unsupported_answer,
        "missing_expected_terms": missing_expected,
        "hallucinated_terms": hallucinated_terms
    })

summary = {
    "total_scenarios": len(rows),
    "groundedness_pass_count": sum(r["groundedness_pass"] for r in rows),
    "unsupported_answer_count": sum(r["unsupported_answer"] for r in rows),
    "hallucination_detected_count": sum(bool(r["hallucinated_terms"]) for r in rows),
    "release_risk": "block" if any(r["unsupported_answer"] for r in rows) else "ship"
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2))

md = [
    "# RAG Groundedness Evaluation Report",
    "",
    f"- total scenarios: {summary['total_scenarios']}",
    f"- groundedness pass count: {summary['groundedness_pass_count']}",
    f"- unsupported answer count: {summary['unsupported_answer_count']}",
    f"- hallucination detected count: {summary['hallucination_detected_count']}",
    f"- release risk: `{summary['release_risk']}`",
    "",
    "| Scenario | Task | Grounded | Unsupported | Missing Expected | Hallucinated Terms |",
    "|---|---|---:|---:|---|---|",
]

for r in rows:
    md.append(
        f"| {r['scenario_id']} | {r['task_type']} | {r['groundedness_pass']} | {r['unsupported_answer']} | {', '.join(r['missing_expected_terms']) or '-'} | {', '.join(r['hallucinated_terms']) or '-'} |"
    )

MD.write_text("\n".join(md) + "\n")
print(json.dumps(summary, indent=2))
