import json
from pathlib import Path

baseline = json.loads(Path("ci_eval_gate/baseline_outputs.json").read_text())["outputs"]
candidate = json.loads(Path("ci_eval_gate/candidate_outputs.json").read_text())["outputs"]

base_by_id = {x["case_id"]: x for x in baseline}
rows = []

for c in candidate:
    b = base_by_id[c["case_id"]]
    rows.append({
        "case_id": c["case_id"],
        "groundedness_regression": b["grounded"] and not c["grounded"],
        "format_failure": not c["format_pass"],
        "false_allow": c["false_allow"]
    })

summary = {
    "candidate": "blocked" if any(
        r["groundedness_regression"] or r["format_failure"] or r["false_allow"]
        for r in rows
    ) else "ship",
    "groundedness_regressions": sum(r["groundedness_regression"] for r in rows),
    "format_failures": sum(r["format_failure"] for r in rows),
    "false_allows": sum(r["false_allow"] for r in rows),
    "results": rows
}

Path("ci_eval_gate/regression_gate_report.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))

if summary["candidate"] == "blocked":
    raise SystemExit(1)
