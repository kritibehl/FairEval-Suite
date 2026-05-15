import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/responsible-ai", tags=["responsible-ai"])

SUMMARY_PATH = Path("responsible_ai/responsible_ai_regression_summary.json")


class EvaluateRequest(BaseModel):
    run_id: str = "rai-eval-2026-05-15"
    candidate_name: str = "candidate_safety_mock"


@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    data = json.loads(SUMMARY_PATH.read_text())
    s = data["summary"]
    return {
        "run_id": req.run_id,
        "candidate_name": req.candidate_name,
        "release_decision": s["release_decision"],
        "safety_regressions": s["num_safety_regressions"],
        "false_allows": s["false_allows"],
        "human_review_required": s["release_decision"] in {"block", "needs_review"},
        "triggered_risk_categories": s["risk_categories_triggered"]
    }


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    data = json.loads(SUMMARY_PATH.read_text())
    return {
        "run_id": run_id,
        "summary": data["summary"],
        "candidate_results": data["candidate_results"]
    }


@router.get("/release-decision/{run_id}")
def get_release_decision(run_id: str):
    data = json.loads(SUMMARY_PATH.read_text())
    s = data["summary"]
    return {
        "run_id": run_id,
        "release_decision": s["release_decision"],
        "false_allows": s["false_allows"],
        "safety_regressions": s["num_safety_regressions"],
        "human_review_required": s["release_decision"] in {"block", "needs_review"}
    }
