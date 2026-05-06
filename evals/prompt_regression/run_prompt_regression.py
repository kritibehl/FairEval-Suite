import json
from pathlib import Path

cases = json.load(open("evals/prompt_regression/cases.json"))
results = []

for case in cases:
    output = case["prompt"]
    expected = case.get("expected_keywords", [])
    matches = sum(1 for kw in expected if kw.lower() in output.lower())
    score = matches / len(expected) if expected else 0.0

    failed_checks = []
    if case.get("requires_json"):
        failed_checks.append("json_contract_check_required")
    if case.get("required_bullets"):
        failed_checks.append("bullet_count_check_required")
    if case.get("max_sentences") and output.count(".") > case["max_sentences"]:
        failed_checks.append("sentence_limit_exceeded")

    results.append({
        "case_id": case["id"],
        "score": round(score, 4),
        "passed": score >= 0.5 and not failed_checks,
        "failed_checks": failed_checks,
        "output": output,
    })

summary = {
    "num_cases": len(results),
    "passed": sum(r["passed"] for r in results),
    "failed": sum(not r["passed"] for r in results),
    "pass_rate": round(sum(r["passed"] for r in results) / len(results), 4),
}

report = {"summary": summary, "results": results}
Path("evals/prompt_regression/report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
