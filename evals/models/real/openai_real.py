import os
from openai import OpenAI


class OpenAIRealModelClient:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate(self, prompt: str, context=None) -> str:
        full_prompt = prompt
        if context:
            if isinstance(context, list):
                ctx = "\n".join(str(x) for x in context)
            else:
                ctx = str(context)
            full_prompt = f"Context:\n{ctx}\n\nPrompt:\n{prompt}"

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0,
        )
        return resp.choices[0].message.content or ""
