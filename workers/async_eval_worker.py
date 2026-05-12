import json
import time
from pathlib import Path
from datetime import datetime, timezone

QUEUE_PATH = Path("workers/queue_retry_examples.json")
REPORT_PATH = Path("reports/async_eval_worker_summary.json")


def now():
    return datetime.now(timezone.utc).isoformat()


def run_job(job):
    job = dict(job)
    job["started_at"] = now()

    try:
        if job["status"] == "retry_pending" and job["attempt"] < job["max_retries"]:
            job["attempt"] += 1
            job["status"] = "succeeded_after_retry"
            job["result"] = {
                "regression_summary_exported": True,
                "failed_cases": 1,
                "release_recommendation": "review_before_release"
            }
        else:
            job["status"] = "succeeded"
            job["result"] = {
                "regression_summary_exported": True,
                "failed_cases": 0,
                "release_recommendation": "ship"
            }

        time.sleep(0.05)
        job["finished_at"] = now()
        return job

    except Exception as exc:
        job["status"] = "failed"
        job["error"] = str(exc)
        job["finished_at"] = now()
        return job


def main():
    jobs = json.loads(QUEUE_PATH.read_text())
    processed = [run_job(job) for job in jobs]

    summary = {
        "worker": "async_eval_worker",
        "jobs_received": len(jobs),
        "jobs_succeeded": sum(j["status"] in {"succeeded", "succeeded_after_retry"} for j in processed),
        "jobs_failed": sum(j["status"] == "failed" for j in processed),
        "retry_jobs": sum(j.get("attempt", 0) > 0 for j in processed),
        "processed_jobs": processed,
        "note": "Demo async evaluation worker queue for FairEval; not a distributed job scheduler."
    }

    REPORT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
