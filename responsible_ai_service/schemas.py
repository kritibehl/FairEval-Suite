from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class TextRiskRequest(BaseModel):
    content_id: str
    content_type: str = "ai_generated_text"
    scenario_category: str
    source: str = "candidate_model"
    content: str
    context: Dict[str, bool] = Field(default_factory=dict)


class TextRiskResponse(BaseModel):
    content_id: str
    risk_categories: List[str]
    risk_severity: str
    recommended_action: str
    review_reason: str
    telemetry_tags: List[str]


class BatchEvalRequest(BaseModel):
    run_id: str
    items: List[TextRiskRequest]


class BatchEvalResponse(BaseModel):
    run_id: str
    evaluated_items: int
    high_risk_items: int
    human_review_required: int
    release_recommendation: str
    results: List[TextRiskResponse]
