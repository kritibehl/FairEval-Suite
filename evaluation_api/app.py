from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import glob
import json

app = FastAPI(title="FairEval Evaluation API", version="0.1.0")


class EvaluationSubmitRequest(BaseModel):
    suite: str
    model: str
    prompt_version: str = "prompt_v1"


class CompareRunsRequest(BaseModel):
    baseline_run_id: str
    candidate_run_id: str


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "faireval-evaluation-api"}


@app.post("/evaluations")
def submit_evaluation(req: EvaluationSubmitRequest):
    return {
        "status": "accepted",
        "job_type": "evaluation",
        "suite": req.suite,
        "model": req.model,
        "prompt_version": req.prompt_version,
        "note": "Demo API accepts evaluation jobs; async worker execution is handled separately."
    }


@app.post("/runs/compare")
def compare_runs(req: CompareRunsRequest):
    return {
        "status": "accepted",
        "baseline_run_id": req.baseline_run_id,
        "candidate_run_id": req.candidate_run_id,
        "comparison_artifact": "generated_by_compare_pipeline"
    }


@app.get("/regressions/summary")
def regression_summary():
    reports = sorted(glob.glob("reports/prompt_regression_report.json"))
    schema_breaks = sorted(glob.glob("reports/schema_breaks.json"))
    failed_constraints = Path("reports/failed_constraints.csv")

    return {
        "prompt_regression_report_available": bool(reports),
        "schema_breaks_available": bool(schema_breaks),
        "failed_constraints_available": failed_constraints.exists(),
        "summary": "Demo endpoint for regression report availability and review status."
    }
