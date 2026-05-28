import json
import os
import time
from pathlib import Path

CASES = Path("real_provider_benchmark/benchmark_cases.json")
RAW_OUT = Path("real_provider_benchmark/raw_provider_outputs.json")
SCORED_OUT = Path("real_provider_benchmark/scored_provider_outputs.json")
LEADERBOARD_JSON = Path("public_benchmark/real_provider_leaderboard/real_provider_leaderboard.json")
LEADERBOARD_MD = Path("public_benchmark/real_provider_leaderboard/real_provider_leaderboard.md")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

def call_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=220,
    )
    return resp.output_text

def call_anthropic(prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=220,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(
        block.text for block in msg.content
        if getattr(block, "type", None) == "text"
    )

def call_gemini(prompt):
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return resp.text or ""

def score_output(case, output):
    text = output.lower()

    expected_hits = [
        term for term in case["expected_terms"]
        if term.lower() in text
    ]
    forbidden_hits = [
        term for term in case["forbidden_terms"]
        if term.lower() in text
    ]

    expected_score = len(expected_hits) / max(len(case["expected_terms"]), 1)
    hallucination_score = 0.0 if forbidden_hits else 1.0

    format_pass = True
    if case["format_requirement"] == "exactly_two_bullets":
        bullet_lines = [
            line for line in output.splitlines()
            if line.strip().startswith(("-", "*"))
        ]
        format_pass = len(bullet_lines) == 2

    format_score = 1.0 if format_pass else 0.0
    score = round((expected_score + hallucination_score + format_score) / 3, 4)

    return {
        "score": score,
        "expected_terms_found": expected_hits,
        "forbidden_terms_found": forbidden_hits,
        "format_pass": format_pass,
        "hallucination_detected": bool(forbidden_hits),
        "instruction_following_pass": format_pass and expected_score >= 0.8,
        "groundedness_pass": not forbidden_hits and expected_score >= 0.8,
    }

def main():
    cases = json.loads(CASES.read_text())["cases"]

    providers = []

    if os.getenv("OPENAI_API_KEY"):
        providers.append(("OpenAI", OPENAI_MODEL, call_openai))
    if os.getenv("ANTHROPIC_API_KEY"):
        providers.append(("Anthropic", ANTHROPIC_MODEL, call_anthropic))
    if os.getenv("GEMINI_API_KEY"):
        providers.append(("Google Gemini", GEMINI_MODEL, call_gemini))

    if not providers:
        raise SystemExit(
            "No provider API keys found. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY."
        )

    raw_rows = []
    scored_rows = []

    for provider_name, model_id, fn in providers:
        for case in cases:
            start = time.perf_counter()
            try:
                response = fn(case["prompt"])
                latency_ms = round((time.perf_counter() - start) * 1000, 4)
                error = None
            except Exception as exc:
                response = ""
                latency_ms = round((time.perf_counter() - start) * 1000, 4)
                error = str(exc)

            raw = {
                "provider": provider_name,
                "model_id": model_id,
                "case_id": case["case_id"],
                "dimension": case["dimension"],
                "prompt": case["prompt"],
                "response": response,
                "latency_ms": latency_ms,
                "error": error,
            }
            raw_rows.append(raw)

            if error:
                score = {
                    "score": 0.0,
                    "expected_terms_found": [],
                    "forbidden_terms_found": [],
                    "format_pass": False,
                    "hallucination_detected": False,
                    "instruction_following_pass": False,
                    "groundedness_pass": False,
                }
            else:
                score = score_output(case, response)

            scored_rows.append({**raw, **score})

    RAW_OUT.write_text(json.dumps({"outputs": raw_rows}, indent=2), encoding="utf-8")
    SCORED_OUT.write_text(json.dumps({"outputs": scored_rows}, indent=2), encoding="utf-8")

    leaderboard = []
    for provider_name, model_id, _ in providers:
        rows = [r for r in scored_rows if r["provider"] == provider_name]
        avg_score = sum(r["score"] for r in rows) / len(rows)
        hallucinations = sum(r["hallucination_detected"] for r in rows)
        groundedness_pass_rate = sum(r["groundedness_pass"] for r in rows) / len(rows)
        instruction_pass_rate = sum(r["instruction_following_pass"] for r in rows) / len(rows)
        avg_latency_ms = sum(r["latency_ms"] for r in rows) / len(rows)
        errors = sum(1 for r in rows if r["error"])

        release_decision = "ship"
        if errors or hallucinations > 0 or avg_score < 0.8:
            release_decision = "block"

        leaderboard.append({
            "provider": provider_name,
            "model_id": model_id,
            "avg_score": round(avg_score, 4),
            "groundedness_pass_rate": round(groundedness_pass_rate, 4),
            "instruction_pass_rate": round(instruction_pass_rate, 4),
            "hallucination_count": hallucinations,
            "avg_latency_ms": round(avg_latency_ms, 4),
            "errors": errors,
            "release_decision": release_decision,
        })

    leaderboard = sorted(leaderboard, key=lambda r: (-r["avg_score"], r["hallucination_count"]))

    summary = {
        "benchmark_name": "real_provider_groundedness_instruction_hallucination_v1",
        "providers_evaluated": len(leaderboard),
        "cases_per_provider": len(cases),
        "safe_scope": "Real provider API outputs were generated only for providers with configured API keys. Raw prompts and responses are stored for auditability.",
        "leaderboard": leaderboard,
    }

    LEADERBOARD_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# Real Provider Benchmark Leaderboard",
        "",
        "This benchmark runs configured providers on the same prompts and evaluates groundedness, instruction-following, hallucination risk, and latency.",
        "",
        "## Safe scope",
        "",
        summary["safe_scope"],
        "",
        "## Leaderboard",
        "",
        "| Rank | Provider | Model | Avg Score | Groundedness Pass | Instruction Pass | Hallucinations | Avg Latency ms | Errors | Decision |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for i, row in enumerate(leaderboard, start=1):
        md.append(
            f"| {i} | {row['provider']} | {row['model_id']} | {row['avg_score']} | {row['groundedness_pass_rate']} | {row['instruction_pass_rate']} | {row['hallucination_count']} | {row['avg_latency_ms']} | {row['errors']} | {row['release_decision']} |"
        )

    md += [
        "",
        "## Raw artifacts",
        "",
        "- `real_provider_benchmark/raw_provider_outputs.json`",
        "- `real_provider_benchmark/scored_provider_outputs.json`",
    ]

    LEADERBOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
