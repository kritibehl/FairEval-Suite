from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EvalCase:
    """
    A single evaluation example.
    Must be deterministic and serializable.
    """
    id: str
    input: Dict[str, Any]
    expected: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class EvalRunConfig:
    """
    Defines how an evaluation run is executed.
    """
    suite_name: str
    model_name: str
    scorer_name: str
    created_at: datetime


@dataclass
class EvalResult:
    """
    Result of evaluating a single case.
    """
    case_id: str
    score: float
    passed: bool
    details: Dict[str, Any]


@dataclass
class EvalReport:
    """
    Aggregated report for an evaluation run.
    """
    run_id: str
    config: EvalRunConfig
    results: List[EvalResult]
    summary: Dict[str, Any]
