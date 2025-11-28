"""
FairEval-Suite

Lightweight programmatic API for scoring model outputs with
human-aligned metrics: rubric scores + simple toxicity estimate.

This is a minimal, self-contained version for demonstration.
"""

from .scorer import evaluate, EvalResult, ToxicityResult

__all__ = ["evaluate", "EvalResult", "ToxicityResult"]

