from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from evals.runner import run_suite
from evals.compare.diff import compare_reports
from evals.gate import apply_gate

app = FastAPI(
    title="FairEval API",
    description="Evaluation and regression-gating service for ML/GenAI systems.",
    version="0.1.0",
)


class EvaluateRequest(BaseModel):
    suite_name: str = Field(..., examples=["rag_basic", "classification_basic"])
    dataset_path: str
    model_name: str = Field(default="mock", examples=["mock", "distilbert-sst2"])
    scorer_name: Optional[str] = None
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


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/evaluate")
def evaluate(req: EvaluateRequest) -> Dict[str, Any]:
    dataset_path = Path(req.dataset_path)
    if not dataset_path.exists():
        raise HTTPException(status_code=400, detail=f"dataset_path not found: {dataset_path}")

    with TemporaryDirectory() as tmpdir:
        res = run_suite(
            suite_name=req.suite_name,
            dataset_path=str(dataset_path),
            model_name=req.model_name,
            scorer_name=req.scorer_name,
            out_dir=tmpdir,
            max_workers=req.max_workers,
            timeout_seconds=req.timeout_seconds,
        )

        report_path = Path(tmpdir) / "reports" / f'{res["run_id"]}.json'
        run_path = Path(tmpdir) / "runs" / f'{res["run_id"]}.json'

        return {
            "summary": res,
            "run_artifact_path": str(run_path),
            "report_artifact_path": str(report_path),
            "report": report_path.read_text(encoding="utf-8"),
        }


@app.post("/compare")
def compare(req: CompareRequest) -> Dict[str, Any]:
    if not Path(req.baseline_report_path).exists():
        raise HTTPException(status_code=400, detail="baseline_report_path not found")
    if not Path(req.candidate_report_path).exists():
        raise HTTPException(status_code=400, detail="candidate_report_path not found")

    with TemporaryDirectory() as tmpdir:
        res = compare_reports(
            baseline_report_path=req.baseline_report_path,
            candidate_report_path=req.candidate_report_path,
            out_dir=tmpdir,
            top_k=req.top_k,
        )
        compare_path = Path(res["output_path"])
        return {
            "summary": res,
            "compare_artifact_path": str(compare_path),
            "compare_artifact": compare_path.read_text(encoding="utf-8"),
        }


@app.post("/gate")
def gate(req: GateRequest) -> Dict[str, Any]:
    if not Path(req.compare_artifact_path).exists():
        raise HTTPException(status_code=400, detail="compare_artifact_path not found")

    with TemporaryDirectory() as tmpdir:
        res = apply_gate(
            compare_artifact_path=req.compare_artifact_path,
            out_dir=tmpdir,
            max_avg_score_drop=req.max_avg_score_drop,
            max_pass_rate_drop=req.max_pass_rate_drop,
            fail_on_any_regression_case=req.fail_on_any_regression_case,
        )
        gate_path = Path(res["output_path"])
        return {
            "summary": res,
            "gate_artifact_path": str(gate_path),
            "gate_artifact": gate_path.read_text(encoding="utf-8"),
        }
