from typing import Dict, Any


class MockModelClient:
    name = "mock"

    def generate(self, case_input: Dict[str, Any]) -> str:
        prompt = case_input.get("prompt", "")
        context = case_input.get("context", [])
        return f"{prompt} | ctx_items={len(context)}"
