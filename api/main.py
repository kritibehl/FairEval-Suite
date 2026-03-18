from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from evals.compare.diff import compare_reports
from evals.dashboard import export_bi_views
from evals.gate import apply_gate
from evals.packs import compare_pack_artifacts, run_pack
from evals.runner import run_suite

app = FastAPI(title="FairEval API", description="Evaluation and regression-gating service for ML/GenAI systems.", version="0.2.0")


class EvaluateRequest(BaseModel):
    suite_name: str = Field(..., examples=["rag_basic", "classification_basic"])
    dataset_path: str
    model_name: str = Field(default="mock", examples=["mock"])
    max_workers: int = 1
    timeout_seconds: float = 10.0


class CompareRequest(BaseModel):
    baseline_report_path: str
    candidate_report_path: str
    top_k: int = 10


class GateRequest(BaseModel):
    compare_artifact_path: str
    max_avg_score_drop: float = 0.05
    max_pass_rate_drop: float = 0.10
    fail_on_any_regression_case: bool = False


class PackRequest(BaseModel):
    suite_name: str
    dataset_path: str
    model_name: str = "mock"
    repeat_count: int = 5


class PackCompareRequest(BaseModel):
    baseline_pack_path: str
    candidate_pack_path: str


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/evaluate")
def evaluate(req: EvaluateRequest) -> Dict[str, Any]:
    dataset_path = Path(req.dataset_path)
    if not dataset_path.exists():
        raise HTTPException(status_code=400, detail=f"dataset_path not found: {dataset_path}")
    return run_suite(
        suite_name=req.suite_name,
        dataset_path=str(dataset_path),
        model_name=req.model_name,
        out_dir=".",
        max_workers=req.max_workers,
        timeout_seconds=req.timeout_seconds,
    )


@app.post("/compare")
def compare(req: CompareRequest) -> Dict[str, Any]:
    if not Path(req.baseline_report_path).exists():
        raise HTTPException(status_code=400, detail="baseline_report_path not found")
    if not Path(req.candidate_report_path).exists():
        raise HTTPException(status_code=400, detail="candidate_report_path not found")
    return compare_reports(req.baseline_report_path, req.candidate_report_path, out_dir=".", top_k=req.top_k)


@app.post("/gate")
def gate(req: GateRequest) -> Dict[str, Any]:
    if not Path(req.compare_artifact_path).exists():
        raise HTTPException(status_code=400, detail="compare_artifact_path not found")
    return apply_gate(
        compare_artifact_path=req.compare_artifact_path,
        out_dir=".",
        max_avg_score_drop=req.max_avg_score_drop,
        max_pass_rate_drop=req.max_pass_rate_drop,
        fail_on_any_regression_case=req.fail_on_any_regression_case,
    )


@app.post("/run-pack")
def run_pack_endpoint(req: PackRequest) -> Dict[str, Any]:
    if not Path(req.dataset_path).exists():
        raise HTTPException(status_code=400, detail=f"dataset_path not found: {req.dataset_path}")
    return run_pack(
        suite_name=req.suite_name,
        dataset_path=req.dataset_path,
        model_name=req.model_name,
        repeat_count=req.repeat_count,
        out_dir=".",
    )


@app.post("/compare-packs")
def compare_packs_endpoint(req: PackCompareRequest) -> Dict[str, Any]:
    return compare_pack_artifacts(req.baseline_pack_path, req.candidate_pack_path, out_dir=".")


@app.post("/export-dashboard")
def export_dashboard() -> Dict[str, Any]:
    return export_bi_views(root=".")
