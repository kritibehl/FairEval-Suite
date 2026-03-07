from pathlib import Path
from typing import Any, Dict

from .runner import run_suite
from .compare.diff import compare_reports
from .gate import apply_gate


def run_release_gate(
    suite_name: str,
    baseline_run_id: str,
    dataset_path: str,
    model_name: str = "mock",
    out_dir: str = ".",
    max_workers: int = 1,
    timeout_seconds: float = 10.0,
    reports_dir: str | None = None,
    max_avg_score_drop: float = 0.05,
    max_pass_rate_drop: float = 0.10,
    fail_on_any_regression_case: bool = False,
) -> Dict[str, Any]:
    run_res = run_suite(
        suite_name=suite_name,
        dataset_path=dataset_path,
        model_name=model_name,
        out_dir=out_dir,
        max_workers=max_workers,
        timeout_seconds=timeout_seconds,
    )

    candidate_run_id = run_res["run_id"]
    reports_root = Path(reports_dir) if reports_dir else Path(out_dir) / "reports"

    baseline_report_path = reports_root / f"{baseline_run_id}.json"
    candidate_report_path = reports_root / f"{candidate_run_id}.json"

    compare_res = compare_reports(
        baseline_report_path=str(baseline_report_path),
        candidate_report_path=str(candidate_report_path),
        out_dir=out_dir,
    )

    gate_res = apply_gate(
        compare_artifact_path=compare_res["output_path"],
        out_dir=out_dir,
        max_avg_score_drop=max_avg_score_drop,
        max_pass_rate_drop=max_pass_rate_drop,
        fail_on_any_regression_case=fail_on_any_regression_case,
    )

    return {
        "baseline_run_id": baseline_run_id,
        "candidate_run_id": candidate_run_id,
        "run": run_res,
        "compare": compare_res,
        "gate": gate_res,
    }
