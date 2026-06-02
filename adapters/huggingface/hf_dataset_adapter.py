import json
from pathlib import Path
from typing import List, Dict, Any


def load_local_hf_style_dataset(path: str) -> List[Dict[str, Any]]:
    """Load a small Hugging Face-style JSONL dataset for offline evaluation demos."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def convert_to_faireval_cases(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert HF-style text/label rows into FairEval case format."""
    cases = []
    for i, row in enumerate(rows, start=1):
        cases.append({
            "id": f"hf-eval-{i:03d}",
            "input": {
                "prompt": row["text"],
                "context": row.get("context", [])
            },
            "expected": {
                "label": row["label"],
                "answer_contains": row.get("expected_terms", [])
            },
            "metadata": {
                "source": row.get("source", "hf_style_local_sample"),
                "task": row.get("task", "nlp_classification_eval")
            }
        })
    return cases


if __name__ == "__main__":
    rows = load_local_hf_style_dataset("datasets/hf_samples/nlp_eval_sample.jsonl")
    cases = convert_to_faireval_cases(rows)
    out = Path("datasets/hf_samples/converted_faireval_cases.json")
    out.write_text(json.dumps(cases, indent=2), encoding="utf-8")
    print(json.dumps({"loaded_rows": len(rows), "converted_cases": len(cases), "output": str(out)}, indent=2))
