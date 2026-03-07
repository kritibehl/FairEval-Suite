from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class EvalCase:
    id: str
    input: Dict[str, Any]
    expected: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class EvalRunConfig:
    suite_name: str
    model_name: str
    scorer_name: str
    created_at: datetime
    artifact_version: str = "v1"
    suite_version: str = "2026.03"
    gate_rules_version: str = "v1"


@dataclass
class EvalResult:
    case_id: str
    score: float
    passed: bool
    details: Dict[str, Any]


@dataclass
class EvalReport:
    run_id: str
    config: EvalRunConfig
    results: List[EvalResult]
    summary: Dict[str, Any] = field(default_factory=dict)
