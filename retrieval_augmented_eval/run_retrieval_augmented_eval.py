import json
from pathlib import Path

DATA = Path("retrieval_augmented_eval/retrieval_eval_cases.json")
OUT = Path("retrieval_augmented_eval/retrieval_augmented_eval_report.json")
MD = Path("retrieval_augmented_eval/retrieval_augmented_eval_report.md")

data = json.loads(DATA.read_text())
rows = []

for case in data["cases"]:
    answer = case["candidate_answer"].lower()
    context = " ".join(case["retrieved_context"]).lower()

    expected_hits = [
        term for term in case["expected_context_terms"]
        if term.lower() in answer
    ]

    unsupported_hits = [
        term for term in case["unsupported_context_terms"]
        if term.lower() in answer and term.lower() not in context
    ]

    retrieval_precision = len(expected_hits) / max(len(case["expected_context_terms"]), 1)
    context_recall = len(expected_hits) / max(len(case["expected_context_terms"]), 1)

    rows.append({
        "case_id": case["case_id"],
        "retrieval_precision": round(retrieval_precision, 4),
        "context_recall": round(context_recall, 4),
        "citation_coverage": case["citations_present"],
        "unsupported_context_detected": bool(unsupported_hits),
        "unsupported_terms": unsupported_hits,
        "groundedness_pass": not unsupported_hits and retrieval_precision >= 0.8
    })

summary = {
    "total_cases": len(rows),
    "avg_retrieval_precision": round(sum(r["retrieval_precision"] for r in rows) / len(rows), 4),
    "avg_context_recall": round(sum(r["context_recall"] for r in rows) / len(rows), 4),
    "citation_coverage_rate": round(sum(r["citation_coverage"] for r in rows) / len(rows), 4),
    "unsupported_context_cases": sum(r["unsupported_context_detected"] for r in rows),
    "groundedness_pass_rate": round(sum(r["groundedness_pass"] for r in rows) / len(rows), 4)
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2), encoding="utf-8")

md = [
    "# Retrieval-Augmented Evaluation Report",
    "",
    f"- total cases: {summary['total_cases']}",
    f"- avg retrieval precision: {summary['avg_retrieval_precision']}",
    f"- avg context recall: {summary['avg_context_recall']}",
    f"- citation coverage rate: {summary['citation_coverage_rate']}",
    f"- unsupported context cases: {summary['unsupported_context_cases']}",
    f"- groundedness pass rate: {summary['groundedness_pass_rate']}",
    "",
    "| Case | Precision | Recall | Citation Coverage | Unsupported Context | Groundedness Pass |",
    "|---|---:|---:|---:|---:|---:|",
]

for r in rows:
    md.append(
        f"| {r['case_id']} | {r['retrieval_precision']} | {r['context_recall']} | {r['citation_coverage']} | {r['unsupported_context_detected']} | {r['groundedness_pass']} |"
    )

MD.write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
