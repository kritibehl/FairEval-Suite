import re
from typing import Dict, Any, List, Set

from .base import Scorer, ScoreResult


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> Set[str]:
    return set(_WORD_RE.findall((text or "").lower()))


def _context_tokens(context: List[str]) -> Set[str]:
    toks: Set[str] = set()
    for chunk in context or []:
        toks |= _tokens(chunk)
    return toks


class RagOverlapScorer(Scorer):
    """
    Deterministic RAG grounding proxy.

    Computes:
      - context_precision: fraction of answer tokens that appear in context
      - context_recall: fraction of context tokens covered by answer tokens (capped)
      - score: harmonic-like mean favoring precision (simple weighted blend)

    This is NOT semantic faithfulness; it's a cheap, deterministic proxy that catches:
      - hallucinated content not present in context
      - answers that ignore provided context
    """

    name = "rag_overlap_v1"

    def score(self, case_input: Dict[str, Any], expected: Dict[str, Any], output_text: str) -> ScoreResult:
        ctx = case_input.get("context", []) or []
        out_toks = _tokens(output_text)
        ctx_toks = _context_tokens(ctx)

        if not out_toks:
            return ScoreResult(score=0.0, passed=False, details={"reason": "empty_output"})

        if not ctx_toks:
            # No context provided → can't score grounding; treat as neutral but fail pass gate.
            return ScoreResult(
                score=0.0,
                passed=False,
                details={"reason": "empty_context"},
            )

        overlap = out_toks & ctx_toks
        precision = len(overlap) / max(1, len(out_toks))

        # Recall is noisy because context is huge; cap denominator to reduce punishment
        denom = max(1, min(200, len(ctx_toks)))
        recall = len(overlap) / denom

        # Weighted blend: prioritize precision
        score = (0.7 * precision) + (0.3 * recall)

        # Pass criteria: enough grounding + optional keyword expectations
        passed = precision >= 0.35

        expected_contains = (expected or {}).get("answer_contains", [])
        missing = []
        for kw in expected_contains:
            if kw.lower() not in (output_text or "").lower():
                missing.append(kw)

        if expected_contains:
            passed = passed and (len(missing) == 0)

        return ScoreResult(
            score=round(float(score), 4),
            passed=bool(passed),
            details={
                "context_precision": round(float(precision), 4),
                "context_recall": round(float(recall), 4),
                "missing_expected": missing,
            },
        )
