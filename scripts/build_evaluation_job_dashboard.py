import json
from pathlib import Path

import matplotlib.pyplot as plt

summary_path = Path("reports/async_eval_worker_summary.json")
if not summary_path.exists():
    raise SystemExit("Missing reports/async_eval_worker_summary.json")

summary = json.loads(summary_path.read_text())
jobs = summary.get("processed_jobs", [])

queued = summary.get("jobs_received", 0)
completed = summary.get("jobs_succeeded", 0)
failed = summary.get("jobs_failed", 0)
retries = summary.get("retry_jobs", 0)
review_before_release = sum(
    1
    for job in jobs
    if job.get("result", {}).get("release_recommendation") == "review_before_release"
)

out_json = {
    "queued_jobs": queued,
    "completed_jobs": completed,
    "failed_evaluations": failed,
    "retry_jobs": retries,
    "review_before_release_count": review_before_release,
    "source": str(summary_path),
    "note": "Dashboard summary for async evaluation workflow; not production monitoring."
}

Path("dashboard/queued_vs_completed.json").write_text(json.dumps(out_json, indent=2), encoding="utf-8")

labels = [
    "Queued",
    "Completed",
    "Failed",
    "Retries",
    "Review Before Release"
]
values = [
    queued,
    completed,
    failed,
    retries,
    review_before_release
]

plt.figure(figsize=(9, 5))
plt.bar(labels, values)
plt.title("FairEval Evaluation Job Dashboard")
plt.ylabel("Job Count")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("dashboard/evaluation_jobs_dashboard.png")

print(json.dumps(out_json, indent=2))
print("Wrote dashboard/evaluation_jobs_dashboard.png")
