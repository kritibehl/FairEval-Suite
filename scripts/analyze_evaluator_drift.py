import glob
import json
from pathlib import Path
from collections import defaultdict

lineage_files = sorted(glob.glob("artifacts/run_lineage/*.json"))
report_files = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))

lineage_by_run = {}
for p in lineage_files:
    data = json.load(open(p))
    lineage_by_run[data.get("run_id")] = data

report_by_run = {}
for p in report_files:
    data = json.load(open(p))
    report_by_run[data.get("run_id")] = data

rows = []

for run_id, report in report_by_run.items():
    lineage = lineage_by_run.get(run_id, {})
    summary = report.get("summary", {})
    failed_cases = sorted([
        r.get("case_id")
        for r in report.get("results", [])
        if not r.get("passed", False)
    ])

    rows.append({
        "run_id": run_id,
        "model_name": report.get("config", {}).get("model_name"),
        "prompt_version": lineage.get("prompt_version", "unknown"),
        "dataset_hash": lineage.get("dataset_hash", "unknown"),
        "evaluator_version": lineage.get("evaluator_version", "unknown"),
        "threshold_version": lineage.get("threshold_version", "unknown"),
        "avg_score": summary.get("avg_score"),
        "pass_rate": summary.get("pass_rate"),
        "failed_case_count": summary.get("failed_case_count"),
        "failed_cases": failed_cases,
    })

drift_groups = defaultdict(list)
for row in rows:
    key = (
        row["prompt_version"],
        row["evaluator_version"],
        row["threshold_version"],
        row["dataset_hash"],
    )
    drift_groups[key].append(row)

comparisons = []
for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]

    prev_failed = set(prev["failed_cases"])
    curr_failed = set(curr["failed_cases"])

    comparisons.append({
        "baseline_run_id": prev["run_id"],
        "candidate_run_id": curr["run_id"],
        "prompt_version_changed": prev["prompt_version"] != curr["prompt_version"],
        "evaluator_version_changed": prev["evaluator_version"] != curr["evaluator_version"],
        "threshold_version_changed": prev["threshold_version"] != curr["threshold_version"],
        "dataset_hash_changed": prev["dataset_hash"] != curr["dataset_hash"],
        "avg_score_delta": round((curr["avg_score"] or 0) - (prev["avg_score"] or 0), 4),
        "pass_rate_delta": round((curr["pass_rate"] or 0) - (prev["pass_rate"] or 0), 4),
        "new_failed_cases": sorted(curr_failed - prev_failed),
        "resolved_failed_cases": sorted(prev_failed - curr_failed),
        "shared_failed_cases": sorted(prev_failed & curr_failed),
    })

audit = {
    "num_runs_analyzed": len(rows),
    "num_lineage_records": len(lineage_by_run),
    "drift_dimensions": [
        "prompt_version",
        "evaluator_version",
        "threshold_version",
        "dataset_hash",
        "failed_case_set",
    ],
    "runs": rows,
    "comparisons": comparisons,
}

Path("reports/evaluator_drift_analysis.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

md = [
    "# Evaluator Drift Analysis",
    "",
    "FairEval compares prompt, evaluator, threshold, dataset, and failed-case changes across benchmark runs.",
    "",
    f"- runs analyzed: {len(rows)}",
    f"- lineage records: {len(lineage_by_run)}",
    "",
    "## Drift dimensions",
    "- prompt version drift",
    "- evaluator version drift",
    "- threshold version drift",
    "- dataset hash drift",
    "- failed-case set changes",
    "",
    "## Run summary",
    "",
    "| Run ID | Model | Prompt | Evaluator | Threshold | Avg Score | Pass Rate | Failed |",
    "|---|---|---|---|---|---:|---:|---:|",
]

for r in rows:
    md.append(
        f"| `{r['run_id']}` | {r['model_name']} | {r['prompt_version']} | {r['evaluator_version']} | {r['threshold_version']} | {r['avg_score']} | {r['pass_rate']} | {r['failed_case_count']} |"
    )

md += [
    "",
    "## Pairwise drift comparisons",
    "",
    "| Baseline | Candidate | Prompt drift | Evaluator drift | Threshold drift | Dataset drift | Avg Δ | Pass Δ | New failures | Resolved failures |",
    "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
]

for c in comparisons:
    md.append(
        f"| `{c['baseline_run_id']}` | `{c['candidate_run_id']}` | {c['prompt_version_changed']} | {c['evaluator_version_changed']} | {c['threshold_version_changed']} | {c['dataset_hash_changed']} | {c['avg_score_delta']} | {c['pass_rate_delta']} | {', '.join(c['new_failed_cases']) or '-'} | {', '.join(c['resolved_failed_cases']) or '-'} |"
    )

Path("reports/evaluator_drift_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print("Wrote reports/evaluator_drift_analysis.json")
print("Wrote reports/evaluator_drift_analysis.md")
