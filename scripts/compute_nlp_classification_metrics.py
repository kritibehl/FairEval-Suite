import json
from collections import defaultdict
from pathlib import Path

report_path = Path("reports/nlp_eval_report.json")
if not report_path.exists():
    raise SystemExit(
        "Missing reports/nlp_eval_report.json. Run: "
        "PYTHONPATH=. python ml_baselines/nlp_eval/evaluate_nlp_outputs.py"
    )

report = json.loads(report_path.read_text())
rows = report["results"]

labels = sorted(set(r["expected"] for r in rows) | set(r["predicted"] for r in rows))

confusion = {actual: {pred: 0 for pred in labels} for actual in labels}
for r in rows:
    confusion[r["expected"]][r["predicted"]] += 1

per_label = {}
for label in labels:
    tp = confusion[label][label]
    fp = sum(confusion[actual][label] for actual in labels if actual != label)
    fn = sum(confusion[label][pred] for pred in labels if pred != label)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    per_label[label] = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "support": sum(confusion[label].values()),
    }

macro_precision = sum(v["precision"] for v in per_label.values()) / len(per_label)
macro_recall = sum(v["recall"] for v in per_label.values()) / len(per_label)
macro_f1 = sum(v["f1"] for v in per_label.values()) / len(per_label)
accuracy = sum(r["expected"] == r["predicted"] for r in rows) / len(rows)

metrics = {
    "num_examples": len(rows),
    "labels": labels,
    "accuracy": round(accuracy, 4),
    "macro_precision": round(macro_precision, 4),
    "macro_recall": round(macro_recall, 4),
    "macro_f1": round(macro_f1, 4),
    "per_label": per_label,
    "confusion_matrix": confusion,
    "note": "Simple NLP classification metrics for evaluation workflow demonstration; not production ML benchmarking."
}

out = Path("ml_baselines/nlp_eval/classification_metrics.json")
out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(json.dumps(metrics, indent=2))
