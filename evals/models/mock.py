from __future__ import annotations

from typing import Dict, List


class MockModelClient:
    name = "mock"

    def generate(self, case_input: Dict[str, object]) -> str:
        prompt = (case_input or {}).get("prompt", "") or ""
        context: List[str] = (case_input or {}).get("context", []) or []
        ctx_words = " ".join(context).split()
        ctx_snippet = " ".join(ctx_words[:12])
        expected_keywords = (case_input or {}).get("expected_keywords", []) or []
        kw_text = " ".join([str(k) for k in expected_keywords[:5]])
        text = (case_input or {}).get("text", "") or ""
        if text:
            lower = str(text).lower()
            if any(x in lower for x in ["love", "excellent", "great", "beautifully"]):
                return "label=POSITIVE confidence=0.9721"
            if any(x in lower for x in ["terrible", "broke", "useless", "bad"]):
                return "label=NEGATIVE confidence=0.9812"
            return "label=NEUTRAL confidence=0.5010"
        parts = [str(prompt).strip()]
        if ctx_snippet:
            parts.append(f"Context: {ctx_snippet}")
        if kw_text:
            parts.append(f"Keywords: {kw_text}")
        return " | ".join([p for p in parts if p])
