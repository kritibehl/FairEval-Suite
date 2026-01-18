from typing import Any, Dict, List


class MockModelClient:
    """
    Deterministic mock "model" used for plumbing, CI, and scorer validation.

    Behavior:
      - echoes prompt
      - includes a deterministic snippet of context
      - if expected keywords exist in input, it tries to include them
    """

    name = "mock"

    def generate(self, case_input: Dict[str, Any]) -> str:
        prompt = (case_input or {}).get("prompt", "") or ""
        context: List[str] = (case_input or {}).get("context", []) or []

        # Take first ~12 words from context deterministically
        ctx_text = " ".join(context)
        ctx_words = ctx_text.split()
        ctx_snippet = " ".join(ctx_words[:12])

        # Try to include "expected" style hints if present (runner passes expected to scorer,
        # but dataset cases include expected keywords; here we support a convention:
        # case_input may optionally carry "expected_keywords" for mock alignment.)
        expected_keywords = (case_input or {}).get("expected_keywords", []) or []
        kw_text = " ".join([str(k) for k in expected_keywords[:5]])

        parts = [prompt.strip()]
        if ctx_snippet:
            parts.append(f"Context: {ctx_snippet}")
        if kw_text:
            parts.append(f"Keywords: {kw_text}")

        return " | ".join([p for p in parts if p])
