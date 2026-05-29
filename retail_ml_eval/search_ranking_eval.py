import json
from pathlib import Path

DATA = Path("retail_ml_eval/personalization_eval_cases.json")
OUT = Path("retail_ml_eval/search_ranking_results.json")

data = json.loads(DATA.read_text())
rows = []

def dcg(relevances):
    import math
    return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(relevances))

for case in data["cases"]:
    expected = set(case["expected_relevant_items"])
    ranked = case["ranked_results"]

    precision_at_3 = sum(item in expected for item in ranked[:3]) / 3
    recall_at_3 = sum(item in expected for item in ranked[:3]) / max(len(expected), 1)

    rels = [1 if item in expected else 0 for item in ranked[:3]]
    ideal = sorted(rels, reverse=True)
    ndcg_at_3 = dcg(rels) / max(dcg(ideal), 1e-9)

    rows.append({
        "case_id": case["case_id"],
        "precision_at_3": round(precision_at_3, 4),
        "recall_at_3": round(recall_at_3, 4),
        "ndcg_at_3": round(ndcg_at_3, 4),
        "ranking_regression": ndcg_at_3 < 0.8
    })

summary = {
    "total_cases": len(rows),
    "avg_precision_at_3": round(sum(r["precision_at_3"] for r in rows) / len(rows), 4),
    "avg_recall_at_3": round(sum(r["recall_at_3"] for r in rows) / len(rows), 4),
    "avg_ndcg_at_3": round(sum(r["ndcg_at_3"] for r in rows) / len(rows), 4),
    "ranking_regressions": sum(r["ranking_regression"] for r in rows)
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2))
print(json.dumps(summary, indent=2))
