import json
from pathlib import Path
import torch

from ml_baselines.pytorch_text_classifier import TinyTextClassifier

labels = ["instruction_failure", "format_regression", "quality_regression"]
examples = [
    ([1, 2, 3, 4], 0),
    ([5, 6, 7, 8], 1),
    ([9, 10, 11, 12], 2),
]

model = TinyTextClassifier()
model.eval()

correct = 0
rows = []

with torch.no_grad():
    for tokens, label in examples:
        x = torch.tensor([tokens])
        pred = int(torch.argmax(model(x), dim=1).item())
        correct += int(pred == label)
        rows.append({
            "tokens": tokens,
            "expected": labels[label],
            "predicted": labels[pred],
        })

result = {
    "num_examples": len(examples),
    "accuracy": round(correct / len(examples), 4),
    "note": "Tiny PyTorch evaluation demo on synthetic issue categories; not production ML.",
    "rows": rows,
}

Path("ml_baselines/sample_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
