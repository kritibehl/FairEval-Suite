from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

QUEUE_DIR = Path("evals/async_jobs/queue")
STATUS_PATH = Path("evals/async_jobs/run_status.json")
FAILED_PATH = Path("evals/async_jobs/failed_jobs.json")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def enqueue_eval_job(suite: str, model: str, out_dir: str) -> Dict[str, Any]:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    job_id = f"eval_{uuid.uuid4().hex[:12]}"
    job = {
        "job_id": job_id,
        "suite": suite,
        "model": model,
        "out_dir": out_dir,
        "status": "queued",
        "attempts": 0,
        "created_at": _now(),
    }
    _write_json(QUEUE_DIR / f"{job_id}.json", job)

    status = _read_json(STATUS_PATH, {})
    status[job_id] = job
    _write_json(STATUS_PATH, status)

    return job


def update_status(job_id: str, patch: Dict[str, Any]) -> None:
    status = _read_json(STATUS_PATH, {})
    current = status.get(job_id, {"job_id": job_id})
    current.update(patch)
    current["updated_at"] = _now()
    status[job_id] = current
    _write_json(STATUS_PATH, status)


def record_failed_job(job: Dict[str, Any], error: str) -> None:
    failed = _read_json(FAILED_PATH, [])
    failed.append({
        **job,
        "status": "failed",
        "error": error,
        "failed_at": _now(),
    })
    _write_json(FAILED_PATH, failed)
