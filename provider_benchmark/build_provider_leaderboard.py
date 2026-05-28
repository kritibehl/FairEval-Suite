import json
from pathlib import Path

IN = Path("provider_benchmark/provider_outputs.json")
OUT = Path("public_benchmark/provider_leaderboard/provider_leaderboard.json")
MD = Path("public_benchmark/provider_leaderboard/provider_leaderboard.md")

data = json.loads(IN.read_text())
rows = []

for provider in data["providers"]:
    outputs = provider["outputs"]
    avg_score = sum(o["score"] for o in outputs) / len(outputs)
    hallucination_count = sum(o["hallucination"] for o in outputs)
    instruction_pass_rate = sum(o["instruction_following"] for o in outputs) / len(outputs)
    groundedness_scores = [o["score"] for o in outputs if o["task"] == "groundedness"]
    groundedness_score = groundedness_scores[0] if groundedness_scores else None

    release_decision = "ship"
    if hallucination_count > 0 or instruction_pass_rate < 0.8 or avg_score < 0.75:
        release_decision = "block"

    rows.append({
        "provider": provider["provider"],
        "model_id": provider["model_id"],
        "avg_score": round(avg_score, 4),
        "groundedness_score": round(groundedness_score, 4) if groundedness_score is not None else None,
        "instruction_pass_rate": round(instruction_pass_rate, 4),
        "hallucination_count": hallucination_count,
        "release_decision": release_decision
    })

rows = sorted(rows, key=lambda r: (r["release_decision"] != "ship", -r["avg_score"]))

summary = {
    "benchmark_name": data["benchmark_name"],
    "safe_scope": data["safe_scope"],
    "providers_compared": len(rows),
    "dimensions": [
        "groundedness",
        "instruction_following",
        "hallucination"
    ],
    "leaderboard": rows
}

OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")

md = [
    "# Public Provider Benchmark Leaderboard",
    "",
    "Compares GPT/Claude/Gemini-style outputs across groundedness, instruction following, and hallucination risk.",
    "",
    "## Safe scope",
    "",
    data["safe_scope"],
    "",
    "## Leaderboard",
    "",
    "| Rank | Provider | Avg Score | Groundedness | Instruction Pass Rate | Hallucinations | Release Decision |",
    "|---:|---|---:|---:|---:|---:|---|",
]

for i, row in enumerate(rows, start=1):
    md.append(
        f"| {i} | {row['provider']} | {row['avg_score']} | {row['groundedness_score']} | {row['instruction_pass_rate']} | {row['hallucination_count']} | {row['release_decision']} |"
    )

md += [
    "",
    "## What this demonstrates",
    "",
    "- provider-style comparison",
    "- groundedness scoring",
    "- instruction-following pass rates",
    "- hallucination-count reporting",
    "- release decision based on evaluation signals",
    "",
    "## Do-not-claim",
    "",
    "Do not claim this is a live frontier-model benchmark unless real API outputs are generated and stored with timestamps, prompts, and raw responses.",
]

MD.write_text("\n".join(md) + "\n", encoding="utf-8")

print(json.dumps(summary, indent=2))
