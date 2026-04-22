import os
from google import genai


class GeminiRealModelClient:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def generate(self, prompt: str, context=None) -> str:
        full_prompt = prompt
        if context:
            if isinstance(context, list):
                ctx = "\n".join(str(x) for x in context)
            else:
                ctx = str(context)
            full_prompt = f"Context:\n{ctx}\n\nPrompt:\n{prompt}"

        resp = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )
        return getattr(resp, "text", "") or ""
