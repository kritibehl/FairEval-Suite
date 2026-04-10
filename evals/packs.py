from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .compare.diff import compare_reports
from .io import ensure_dir, write_json
from .runner import run_suite
from .stats import chi_squared_pass_fail, confidence_interval, welch_t_test
from .storage import ArtifactStore


def _stable_pack_run_id(suite_name: str, model_name: str, repeat_count: int) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    h = hashlib.sha256(f"{suite_name}|{model_name}|{repeat_count}".encode("utf-8")).hexdigest()[:10]
    return f"{ts}_{suite_name}_{model_name}_pack_{h}"


def run_pack(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    out_dir: str = ".",
    repeat_count: int = 5,
    max_workers: int = 1,
    timeout_seconds: float = 10.0,
) -> Dict[str, Any]:
    if repeat_count < 2:
        raise RuntimeError("repeat_count must be >= 2")
    runs: List[Dict[str, Any]] = []
    for _ in range(repeat_count):
        runs.append(
            run_suite(
                suite_name=suite_name,
                dataset_path=dataset_path,
                model_name=model_name,
                out_dir=out_dir,
                max_workers=max_workers,
                timeout_seconds=timeout_seconds,
            )
        )

    avg_scores = [float(r["avg_score"]) for r in runs]
    pass_rates = [float(r["pass_rate"]) for r in runs]
    avg_ci = confidence_interval(avg_scores)
    pass_ci = confidence_interval(pass_rates)
    pack_run_id = _stable_pack_run_id(suite_name, model_name, repeat_count)
    artifact = {
        "pack_run_id": pack_run_id,
        "suite_name": suite_name,
        "model_name": model_name,
        "repeat_count": repeat_count,
        "runs": runs,
        "avg_score_confidence_interval": avg_ci,
        "pass_rate_confidence_interval": pass_ci,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    out_path = Path(out_dir) / "packs" / f"{pack_run_id}.json"
    write_json(out_path, artifact)

    ArtifactStore(out_dir).index_pack_run(
        {
            "pack_run_id": pack_run_id,
            "suite_name": suite_name,
            "model_name": model_name,
            "created_at": artifact["created_at"],
            "repeat_count": repeat_count,
            "avg_score_mean": avg_ci["mean"],
            "avg_score_ci_low": avg_ci["lower"],
            "avg_score_ci_high": avg_ci["upper"],
            "pass_rate_mean": pass_ci["mean"],
            "pass_rate_ci_low": pass_ci["lower"],
            "pass_rate_ci_high": pass_ci["upper"],
            "pack_artifact_path": str(out_path),
        }
    )
    return {"output_path": str(out_path), **artifact}


def compare_pack_artifacts(baseline_pack_path: str, candidate_pack_path: str, out_dir: str = ".") -> Dict[str, Any]:
    baseline = json.loads(Path(baseline_pack_path).read_text(encoding="utf-8"))
    candidate = json.loads(Path(candidate_pack_path).read_text(encoding="utf-8"))

    baseline_scores = [float(r["avg_score"]) for r in baseline["runs"]]
    candidate_scores = [float(r["avg_score"]) for r in candidate["runs"]]
    baseline_passes = [float(r["pass_rate"]) for r in baseline["runs"]]
    candidate_passes = [float(r["pass_rate"]) for r in candidate["runs"]]

    total_cases_b = sum(int(r["num_cases"]) for r in baseline["runs"])
    total_cases_c = sum(int(r["num_cases"]) for r in candidate["runs"])
    pass_count_b = sum(round(float(r["pass_rate"]) * int(r["num_cases"])) for r in baseline["runs"])
    pass_count_c = sum(round(float(r["pass_rate"]) * int(r["num_cases"])) for r in candidate["runs"])

    score_t = welch_t_test(baseline_scores, candidate_scores)
    chi2 = chi_squared_pass_fail(
        int(pass_count_b), int(total_cases_b - pass_count_b), int(pass_count_c), int(total_cases_c - pass_count_c)
    )

    artifact = {
        "baseline_pack_path": baseline_pack_path,
        "candidate_pack_path": candidate_pack_path,
        "baseline_avg_score_ci": confidence_interval(baseline_scores),
        "candidate_avg_score_ci": confidence_interval(candidate_scores),
        "baseline_pass_rate_ci": confidence_interval(baseline_passes),
        "candidate_pass_rate_ci": confidence_interval(candidate_passes),
        "score_change_test": score_t,
        "pass_fail_distribution_test": chi2,
        "drift_significant": bool(score_t.get("supported") and score_t.get("p_value", 1.0) < 0.05),
    }
    out_path = Path(out_dir) / "packs" / f"{Path(candidate_pack_path).stem}_vs_{Path(baseline_pack_path).stem}.json"
    write_json(out_path, artifact)
    return {"output_path": str(out_path), **artifact}
