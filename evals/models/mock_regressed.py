from __future__ import annotations

from typing import Any, Dict


class MockRegressedModelClient:
    """
    Intentionally worse than MockModelClient on a few cases so repeated-pack
    comparisons show real score/pass-rate differences.
    """

    def generate(self, prompt: str, context: list[str] | None = None, **_: Any) -> Dict[str, Any]:
        prompt_l = prompt.lower()
        context = context or []

        # Keep some cases okay, degrade others on purpose.
        if "postgresql" in prompt_l:
            answer = "PostgreSQL is a database."
        elif "acid" in prompt_l:
            # Missing key expected term "Durability"
            answer = "ACID stands for Atomicity, Consistency, and Isolation."
        elif "redis" in prompt_l:
            # Missing expected "queue"
            answer = "Redis is used for cache."
        elif "docker" in prompt_l:
            # Still passes
            answer = "Docker is a container platform."
        elif "prometheus" in prompt_l:
            # Missing expected "metrics"
            answer = "Prometheus is used for monitoring."
        else:
            answer = " ".join(context[:1]) if context else "No answer available."

        return {
            "output_text": answer,
            "model_name": "mock_regressed",
            "response_preview": answer[:160],
        }
