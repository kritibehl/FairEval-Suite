from __future__ import annotations

import re
from typing import Any, Dict

from .base import ScoreResult, Scorer

_LABEL_RE = re.compile(r"label=([A-Z_]+)")
_CONF_RE = re.compile(r"confidence=([0-9]*\.?[0-9]+)")


def _parse_output(output_text: str) -> tuple[str, float]:
    label_match = _LABEL_RE.search(output_text or "")
    conf_match = _CONF_RE.search(output_text or "")
    label = label_match.group(1) if label_match else "UNKNOWN"
    confidence = float(conf_match.group(1)) if conf_match else 0.0
    return label, confidence


class ClassificationLabelScorer(Scorer):
    name = "classification_label_v1"

    def score(self, case_input: Dict[str, Any], expected: Dict[str, Any], output_text: str) -> ScoreResult:
        parsed_label, parsed_conf = _parse_output(output_text)
        expected_label = (expected or {}).get("label", "UNKNOWN")
        min_conf = float((expected or {}).get("min_confidence", 0.0))
        label_match = parsed_label == expected_label
        confidence_ok = parsed_conf >= min_conf
        score = parsed_conf if label_match else 0.0
        passed = bool(label_match and confidence_ok)
        return ScoreResult(
            score=round(float(score), 4),
            passed=passed,
            details={
                "predicted_label": parsed_label,
                "expected_label": expected_label,
                "confidence": round(float(parsed_conf), 4),
                "min_confidence": round(float(min_conf), 4),
                "label_match": label_match,
                "confidence_ok": confidence_ok,
            },
        )
