from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ScoreResult:
    score: float
    passed: bool
    details: Dict[str, Any]


class Scorer:
    name: str = "base"

    def score(self, case_input: Dict[str, Any], expected: Dict[str, Any], output_text: str) -> ScoreResult:
        raise NotImplementedError
