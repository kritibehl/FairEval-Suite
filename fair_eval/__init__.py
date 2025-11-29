"""
FairEval-Suite: human-aligned evaluation helpers for generative models.

Public API:
- evaluate(prompt, output) -> EvalResult
- EvalResult: score, rubric_breakdown, toxicity
"""

from .scorer import evaluate, EvalResult  # noqa: F401

__all__ = ["evaluate", "EvalResult"]

# Bump this when you release new versions
__version__ = "0.1.0"

