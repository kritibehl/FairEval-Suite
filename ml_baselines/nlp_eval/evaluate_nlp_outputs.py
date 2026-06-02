import json
from pathlib import Path
from collections import Counter

from adapters.huggingface.hf_dataset_adapter import load_local_hf_style_dataset


def classify_issue(text: str) -> str:
    t = text.lower()
    if "json" in t or "field" in t or "schema" in t:
        return "schema_break"
    if "format" in t or "instruction" in t or "omitted" in t:
        return "instruction_drop"
    if "repeated" in t or "same prompt" in t or "changed" in t:
        return "consistency_regression"
    return "quality_regression"


rows = load_local_hf_style_dataset("datasets/hf_samples/nlp_eval_sample.jsonl")

results = []
for row in rows:
    pred = classify_issue(row["text"])
    results.append({
        "text": row["text"],
        "expected": row["label"],
        "predicted": pred,
        "passed": pred == row["label"],
    })

accuracy = sum(r["passed"] for r in results) / len(results)
summary = {
    "num_examples": len(results),
    "accuracy": round(accuracy, 4),
    "label_distribution": dict(Counter(r["expected"] for r in results)),
    "note": "Simple NLP classification/evaluation demo for model-output analysis; not production ML training."
}

out = {
    "summary": summary,
    "results": results,
}

Path("reports/nlp_eval_report.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
