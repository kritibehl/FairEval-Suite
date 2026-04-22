import json
from pathlib import Path

from evals.serving_metrics import build_serving_delta

baseline_quality = {
    "avg_score": 0.812,
    "pass_rate": 0.90,
}

candidate_quality = {
    "avg_score": 0.810,
    "pass_rate": 0.90,
}

baseline_serving = {
    "latency_p50_ms": 410,
    "latency_p95_ms": 690,
    "throughput_rps": 8.2,
}

candidate_serving = {
    "latency_p50_ms": 438,
    "latency_p95_ms": 1015,
    "throughput_rps": 7.7,
}

payload = {
    "delta": {
        "avg_score": round(candidate_quality["avg_score"] - baseline_quality["avg_score"], 4),
        "pass_rate": round(candidate_quality["pass_rate"] - baseline_quality["pass_rate"], 4),
    },
    "case_diffs": [],
    "serving_delta": build_serving_delta(baseline_serving, candidate_serving),
    "hardware": {
        "provider": "amd_dev_cloud",
        "gpu": "AMD MI300X",
    },
}

out_path = Path("artifacts/amd_mi300x/compare_serving_regression.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

print(out_path)
