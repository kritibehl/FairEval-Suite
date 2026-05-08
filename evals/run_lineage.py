from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def sha256_file(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return "missing"
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build_run_lineage(
    *,
    run_id: str,
    dataset_path: str,
    model_name: str,
    parent_run_id: str | None = None,
    model_version: str | None = None,
    prompt_version: str | None = None,
    evaluator_version: str | None = None,
    threshold_version: str | None = None,
) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "parent_run_id": parent_run_id,
        "model_name": model_name,
        "model_version": model_version or os.getenv("MODEL_VERSION", "unknown"),
        "prompt_version": prompt_version or os.getenv("PROMPT_VERSION", "prompt_v1"),
        "dataset_hash": sha256_file(dataset_path),
        "evaluator_version": evaluator_version or os.getenv("EVALUATOR_VERSION", "evaluator_v1"),
        "threshold_version": threshold_version or os.getenv("THRESHOLD_VERSION", "threshold_v1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def write_run_lineage(lineage: Dict[str, Any], out_dir: str = "artifacts/run_lineage") -> str:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    out = path / f"{lineage['run_id']}.lineage.json"
    out.write_text(json.dumps(lineage, indent=2), encoding="utf-8")
    return str(out)
