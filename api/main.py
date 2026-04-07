from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from evals.compare.diff import compare_reports
from evals.gate import apply_gate
from evals.runner import run_suite

app = FastAPI(title="FairEval API", version="1.0.0")


class EvaluateRequest(BaseModel):
    suite_name: str
    dataset_path: str
    model_name: str = "mock"
    scorer_name: str | None = None
    max_workers: int = 1
    timeout_seconds: float = 10.0
    out_dir: str = "."


class CompareRequest(BaseModel):
    baseline_report_path: str
    candidate_report_path: str
    out_dir: str = "."
    top_k: int = 5


class GateRequest(BaseModel):
    compare_artifact_path: str
    out_dir: str = "."
    max_avg_score_drop: float = 0.05
    max_pass_rate_drop: float = 0.10
    fail_on_any_regression_case: bool = False
    estimated_affected_query_pct: float | None = None
    max_affected_query_pct: float = 0.10
    daily_query_volume: int | None = None
    downstream_risk: str | None = None
    block_on_high_downstream_risk: bool = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    result = run_suite(
        suite_name=req.suite_name,
        dataset_path=req.dataset_path,
        model_name=req.model_name,
        scorer_name=req.scorer_name,
        out_dir=req.out_dir,
        max_workers=req.max_workers,
        timeout_seconds=req.timeout_seconds,
    )
    report_path = str(Path(req.out_dir) / "reports" / f'{result["run_id"]}.json')
    return {
        "run_id": result["run_id"],
        "summary": {
            "num_cases": result["num_cases"],
            "avg_score": result["avg_score"],
            "pass_rate": result["pass_rate"],
            "failed_case_count": result["failed_case_count"],
            "integrity": result.get("integrity"),
        },
        "report": report_path,
        "report_path": report_path,
        "report_artifact_path": report_path,
        "run_artifact": result,
    }


@app.post("/compare")
def compare(req: CompareRequest):
    result = compare_reports(
        baseline_report_path=req.baseline_report_path,
        candidate_report_path=req.candidate_report_path,
        out_dir=req.out_dir,
        top_k=req.top_k,
    )
    artifact_path = result["output_path"]
    artifact_text = Path(artifact_path).read_text(encoding="utf-8")

    return {
        "compare_artifact": artifact_text,
        "compare_artifact_path": artifact_path,
        "summary": {
            "avg_score": result.get("avg_score"),
            "pass_rate": result.get("pass_rate"),
            "regressed_case_count": result.get("regressed_case_count"),
            "rollback_recommendation": result.get("rollback_recommendation"),
        },
        "output_path": artifact_path,
        "compare_details": result,
    }


@app.post("/gate")
def gate(req: GateRequest):
    result = apply_gate(
        compare_artifact_path=req.compare_artifact_path,
        out_dir=req.out_dir,
        max_avg_score_drop=req.max_avg_score_drop,
        max_pass_rate_drop=req.max_pass_rate_drop,
        fail_on_any_regression_case=req.fail_on_any_regression_case,
        estimated_affected_query_pct=req.estimated_affected_query_pct,
        max_affected_query_pct=req.max_affected_query_pct,
        daily_query_volume=req.daily_query_volume,
        downstream_risk=req.downstream_risk,
        block_on_high_downstream_risk=req.block_on_high_downstream_risk,
    )
    return {
        "gate_artifact": result["output_path"],
        "gate_artifact_path": result["output_path"],
        "output_path": result["output_path"],
        "gate_details": result,
    }
