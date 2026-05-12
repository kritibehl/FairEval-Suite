import json
import math
from pathlib import Path

prompts = [
    "Return JSON with decision and reason.",
    "Explain why score-only evals can miss regressions.",
    "Give exactly three bullets about model evaluation.",
    "Why does evaluator drift matter for model releases?"
]

def token_count(text: str) -> int:
    return len(text.split())

def embed(text: str, dim: int = 16):
    vec = [0.0] * dim
    for i, b in enumerate(text.lower().encode("utf-8")):
        vec[i % dim] += (b % 31) / 31.0
    norm = math.sqrt(sum(x*x for x in vec)) or 1.0
    return [x / norm for x in vec]

def cosine(a, b):
    return sum(x*y for x, y in zip(a, b))

counts = [token_count(p) for p in prompts]
base = embed(prompts[0])

embedding_distances = []
for p in prompts[1:]:
    sim = cosine(base, embed(p))
    embedding_distances.append({
        "baseline_prompt": prompts[0],
        "comparison_prompt": p,
        "cosine_similarity": round(sim, 4),
        "embedding_distance": round(1 - sim, 4)
    })

report = {
    "num_prompts": len(prompts),
    "min_tokens": min(counts),
    "max_tokens": max(counts),
    "avg_tokens": round(sum(counts) / len(counts), 2),
    "prompt_token_counts": [
        {"prompt": p, "token_count": token_count(p)}
        for p in prompts
    ],
    "embedding_distance_examples": embedding_distances,
    "note": "Simple tokenizer and embedding drift analysis; not production tokenizer instrumentation."
}

Path("analysis/token_distribution_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
