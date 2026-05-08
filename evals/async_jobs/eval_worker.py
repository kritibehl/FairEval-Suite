from __future__ import annotations

import json
import subprocess
from pathlib import Path

from evals.async_jobs.job_queue import QUEUE_DIR, record_failed_job, update_status


def run_next_job() -> None:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    jobs = sorted(QUEUE_DIR.glob("*.json"))
    if not jobs:
        print("No queued eval jobs.")
        return

    job_path = jobs[0]
    job = json.loads(job_path.read_text())
    job_id = job["job_id"]

    update_status(job_id, {"status": "running", "attempts": job.get("attempts", 0) + 1})

    cmd = [
        "python",
        "-m",
        "evals.cli",
        "run",
        "--suite",
        job["suite"],
        "--model",
        job["model"],
        "--out-dir",
        job["out_dir"],
    ]

    try:
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
        update_status(job_id, {
            "status": "succeeded",
            "stdout": completed.stdout[-2000:],
            "stderr": completed.stderr[-2000:],
        })
        job_path.unlink()
        print(f"Completed {job_id}")
    except Exception as exc:
        record_failed_job(job, str(exc))
        update_status(job_id, {"status": "failed", "error": str(exc)})
        print(f"Failed {job_id}: {exc}")


if __name__ == "__main__":
    run_next_job()
