import json
from pathlib import Path
import math


failed_cases = [
    {
        "case_id": "case_01_instruction_drop",
        "text": "Model ignored a required instruction and omitted a requested field.",
        "failure_type": "instruction_drop"
    },
    {
        "case_id": "case_02_schema_break",
        "text": "Model returned malformed JSON and missed required schema fields.",
        "failure_type": "schema_break"
    },
    {
        "case_id": "case_03_variance_regression",
        "text": "Model output changed across repeated runs with the same prompt.",
        "failure_type": "consistency_regression"
    }
]

query = "output missed required JSON reason field"

def embed(text: str, dim: int = 24):
    vec = [0.0] * dim
    for i, b in enumerate(text.lower().encode("utf-8")):
        vec[i % dim] += (b % 37) / 37.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]

def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))

query_vec = embed(query)

results = []
for case in failed_cases:
    score = cosine(query_vec, embed(case["text"]))
    results.append({
        "case_id": case["case_id"],
        "failure_type": case["failure_type"],
        "similarity": round(score, 4),
        "text": case["text"]
    })

results = sorted(results, key=lambda x: x["similarity"], reverse=True)

out = {
    "query": query,
    "top_matches": results,
    "note": "Lightweight embedding similarity demo for failed-case retrieval; not a production vector database."
}

Path("embedding_search/failed_case_similarity.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
