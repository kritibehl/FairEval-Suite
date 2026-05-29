import json
from pathlib import Path

DATA = Path("retail_ml_eval/personalization_eval_cases.json")
OUT = Path("retail_ml_eval/recommendation_quality_results.json")

data = json.loads(DATA.read_text())
rows = []

for case in data["cases"]:
    expected = set(case["expected_relevant_items"])
    recs = case["recommended_items"]

    hit_rate = int(any(item in expected for item in recs))
    precision = sum(item in expected for item in recs) / max(len(recs), 1)
    irrelevant_count = sum(item not in expected for item in recs)

    rows.append({
        "case_id": case["case_id"],
        "recommendation_hit": bool(hit_rate),
        "recommendation_precision": round(precision, 4),
        "irrelevant_recommendation_count": irrelevant_count,
        "quality_regression": precision < 0.5
    })

summary = {
    "total_cases": len(rows),
    "hit_rate": round(sum(r["recommendation_hit"] for r in rows) / len(rows), 4),
    "avg_recommendation_precision": round(sum(r["recommendation_precision"] for r in rows) / len(rows), 4),
    "quality_regressions": sum(r["quality_regression"] for r in rows)
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2))
print(json.dumps(summary, indent=2))
