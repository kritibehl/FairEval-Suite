import csv
import glob
import json
from pathlib import Path

import pandas as pd

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
compares = sorted(glob.glob("benchmark_public/instruction_following/compares/**/*.json", recursive=True))

exports = Path("exports")
exports.mkdir(exist_ok=True)

rows = []
score_rows = []

for report_path in reports:
    data = json.load(open(report_path))
    summary = data.get("summary", {})
    config = data.get("config", {})

    rows.append({
        "run_id": data.get("run_id"),
        "suite_name": config.get("suite_name"),
        "model_name": config.get("model_name"),
        "dataset_version": config.get("dataset_version"),
        "avg_score": summary.get("avg_score"),
        "pass_rate": summary.get("pass_rate"),
        "failed_case_count": summary.get("failed_case_count"),
        "num_cases": summary.get("num_cases"),
        "artifact_path": report_path,
    })

    for result in data.get("results", []):
        details = result.get("details", {})
        score_rows.append({
            "run_id": data.get("run_id"),
            "model_name": config.get("model_name"),
            "case_id": result.get("case_id"),
            "score": result.get("score"),
            "passed": result.get("passed"),
            "scorer": details.get("scorer"),
            "model_output": details.get("model_output"),
        })

benchmark_df = pd.DataFrame(rows)
scores_df = pd.DataFrame(score_rows)

benchmark_df.to_parquet(exports / "benchmark_results.parquet", index=False)
benchmark_df.to_csv(exports / "benchmark_results.csv", index=False)
scores_df.to_csv(exports / "model_scores.csv", index=False)

comparison_rows = []
for compare_path in compares:
    data = json.load(open(compare_path))
    comparison_rows.append({
        "compare_artifact_path": compare_path,
        "baseline_model": data.get("baseline", {}).get("config", {}).get("model_name"),
        "candidate_model": data.get("candidate", {}).get("config", {}).get("model_name"),
        "avg_score_delta": data.get("delta", {}).get("avg_score"),
        "pass_rate_delta": data.get("delta", {}).get("pass_rate"),
        "regressed_case_count": data.get("regressed_case_count"),
        "rollback_recommendation": data.get("rollback_recommendation"),
    })

with open(exports / "model_comparison.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "compare_artifact_path",
            "baseline_model",
            "candidate_model",
            "avg_score_delta",
            "pass_rate_delta",
            "regressed_case_count",
            "rollback_recommendation",
        ],
    )
    writer.writeheader()
    writer.writerows(comparison_rows)

print("Wrote exports/benchmark_results.parquet")
print("Wrote exports/benchmark_results.csv")
print("Wrote exports/model_scores.csv")
print("Wrote exports/model_comparison.csv")
