import json
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

torch.manual_seed(7)

prompts = [
    "Return JSON with decision and reason.",
    "Explain release gating in one sentence.",
    "Give exactly three bullets about model evaluation.",
]

baseline_outputs = [
    '{"decision": "ship", "reason": "no regression"}',
    "Release gating blocks unsafe model updates before deployment.",
    "- evaluate behavior\n- compare outputs\n- gate releases",
]

candidate_outputs = [
    '{"decision": "ship"}',
    "Release gating helps evaluate models.",
    "Model evals are useful.",
]

def simple_embed(text: str, dim: int = 16) -> torch.Tensor:
    vec = torch.zeros(dim)
    for i, ch in enumerate(text.encode("utf-8")):
        vec[i % dim] += float(ch % 31) / 31.0
    return F.normalize(vec, dim=0)

rows = []
for prompt, base, cand in zip(prompts, baseline_outputs, candidate_outputs):
    base_emb = simple_embed(base)
    cand_emb = simple_embed(cand)
    similarity = float(torch.dot(base_emb, cand_emb).item())

    failed_constraints = []
    if "decision" in prompt.lower() and "reason" not in cand:
        failed_constraints.append("missing_reason_field")
    if "exactly three bullets" in prompt.lower() and cand.count("-") < 3:
        failed_constraints.append("bullet_count_regression")

    rows.append({
        "prompt": prompt,
        "baseline_output": base,
        "candidate_output": cand,
        "embedding_similarity": round(similarity, 4),
        "failed_constraints": failed_constraints,
        "regression_detected": bool(failed_constraints or similarity < 0.75),
    })

summary = {
    "num_cases": len(rows),
    "regressions_detected": sum(r["regression_detected"] for r in rows),
    "avg_embedding_similarity": round(float(np.mean([r["embedding_similarity"] for r in rows])), 4),
    "note": "Mini PyTorch evaluation demo only; not a production ML training system.",
}

out = {
    "summary": summary,
    "rows": rows,
}

Path("reports/pytorch_mini_eval_report.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
