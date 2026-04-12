import os
import anthropic


class AnthropicRealModelClient:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("ANTHROPIC_MODEL")
        if not self.model:
            raise RuntimeError("Set ANTHROPIC_MODEL, for example a current Claude Haiku model from the Anthropic models list API.")
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(self, prompt: str, context=None) -> str:
        full_prompt = prompt
        if context:
            if isinstance(context, list):
                ctx = "\n".join(str(x) for x in context)
            else:
                ctx = str(context)
            full_prompt = f"Context:\n{ctx}\n\nPrompt:\n{prompt}"

        resp = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[{"role": "user", "content": full_prompt}],
        )

        parts = []
        for block in resp.content:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
        return "\n".join(parts).strip()
