import json
from pathlib import Path

DATA = Path("agent_eval/tool_call_correctness.json")
OUT = Path("agent_eval/retrieval_quality_results.json")

data = json.loads(DATA.read_text())
rows = []

for case in data["cases"]:
    tool_correct = case["expected_tool"] == case["observed_tool"]
    args_correct = case["expected_args"] == case["observed_args"]
    grounded = case["tool_result_grounded"]

    retrieval_quality_score = round(
        (int(tool_correct) + int(args_correct) + int(grounded)) / 3,
        4
    )

    rows.append({
        "case_id": case["case_id"],
        "tool_correct": tool_correct,
        "args_correct": args_correct,
        "tool_result_grounded": grounded,
        "retrieval_quality_score": retrieval_quality_score,
        "agent_regression": retrieval_quality_score < 0.8
    })

summary = {
    "total_cases": len(rows),
    "tool_selection_accuracy": round(sum(r["tool_correct"] for r in rows) / len(rows), 4),
    "argument_accuracy": round(sum(r["args_correct"] for r in rows) / len(rows), 4),
    "grounded_tool_result_rate": round(sum(r["tool_result_grounded"] for r in rows) / len(rows), 4),
    "avg_retrieval_quality_score": round(sum(r["retrieval_quality_score"] for r in rows) / len(rows), 4),
    "agent_regressions": sum(r["agent_regression"] for r in rows)
}

OUT.write_text(json.dumps({"summary": summary, "results": rows}, indent=2))
print(json.dumps(summary, indent=2))
