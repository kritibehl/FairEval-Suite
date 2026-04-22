from __future__ import annotations

import re
from typing import Any, Dict, List, Set

from .base import ScoreResult, Scorer

_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> Set[str]:
    return set(_WORD_RE.findall((text or "").lower()))


def _context_tokens(context: List[str]) -> Set[str]:
    toks: Set[str] = set()
    for chunk in context or []:
        toks |= _tokens(chunk)
    return toks


class RagOverlapScorer(Scorer):
    name = "rag_overlap_v1"

    def score(self, case_input: Dict[str, Any], expected: Dict[str, Any], output_text: str) -> ScoreResult:
        ctx = case_input.get("context", []) or []
        out_toks = _tokens(output_text)
        ctx_toks = _context_tokens(ctx)
        if not out_toks:
            return ScoreResult(score=0.0, passed=False, details={"reason": "empty_output"})
        # Fallback: if no context, evaluate using expected keywords only
        if not ctx_toks:
            expected_contains = (expected or {}).get("answer_contains", [])
            if not expected_contains:
                return ScoreResult(score=0.0, passed=False, details={"reason": "no_expected_terms"})

            output_lower = (output_text or "").lower()
            matches = sum(1 for kw in expected_contains if kw.lower() in output_lower)
            score = matches / len(expected_contains)

            return ScoreResult(
                score=round(float(score), 4),
                passed=score >= 0.5,
                details={"mode": "keyword_fallback", "matches": matches}
            )

        overlap = out_toks & ctx_toks
        precision = len(overlap) / max(1, len(out_toks))
        denom = max(1, min(200, len(ctx_toks)))
        recall = len(overlap) / denom
        score = (0.7 * precision) + (0.3 * recall)

        expected_contains = (expected or {}).get("answer_contains", [])
        missing = [kw for kw in expected_contains if kw.lower() not in (output_text or "").lower()]
        passed = precision >= 0.35 and len(missing) == 0
        return ScoreResult(
            score=round(float(score), 4),
            passed=bool(passed),
            details={
                "context_precision": round(float(precision), 4),
                "context_recall": round(float(recall), 4),
                "missing_expected": missing,
            },
        )
