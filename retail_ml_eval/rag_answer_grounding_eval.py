import json
from pathlib import Path

DATA = Path("retail_ml_eval/personalization_eval_cases.json")
OUT = Path("retail_ml_eval/rag_answer_grounding_results.json")

data = json.loads(DATA.read_text())
rows = []

for case in data["cases"]:
    answer = case["rag_answer"].lower()
    context = " ".join(case["grounding_context"]).lower()

    expected_mentions = [
        item for item in case["expected_relevant_items"]
        if item.replace("_", " ").split()[0] in answer or item in answer
    ]

    unsupported_terms = []
    for term in ["best", "guaranteed", "cheapest", "fastest"]:
        if term in answer and term not in context:
            unsupported_terms.append(term)

    groundedness_pass = bool(expected_mentions) and not unsupported_terms

    rows.append({
        "case_id": case["case_id"],
        "expected_mentions_found": expected_mentions,
        "unsupported_terms": unsupported_terms,
        "groundedness_pass": groundedness_pass
    })

summary = {
    "total_cases": len(rows),
    "groundedness_pass_rate": round(sum(r["groundedness_pass"] for r in rows) / len(rows), 4),
    "unsupported_answer_count": sum(bool(r["unsupported_terms"]) for r in rows)
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2))
print(json.dumps(summary, indent=2))
