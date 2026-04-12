import json
import os
import sys

def main():
    vendor = sys.argv[1]

    if vendor == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        models = client.models.list()
        payload = []
        for m in models.data:
            payload.append({"id": m.id, "display_name": getattr(m, "display_name", None)})
        print(json.dumps(payload, indent=2))
        return

    if vendor == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        models = client.models.list()
        payload = [{"id": m.id} for m in models.data]
        print(json.dumps(payload, indent=2))
        return

    if vendor == "gemini":
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        models = client.models.list()
        payload = [{"name": getattr(m, "name", None), "display_name": getattr(m, "display_name", None)} for m in models]
        print(json.dumps(payload, indent=2))
        return

    raise SystemExit("usage: python scripts/list_vendor_models.py [anthropic|openai|gemini]")

if __name__ == "__main__":
    main()
