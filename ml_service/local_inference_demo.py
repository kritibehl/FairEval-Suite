import json
import time
from pathlib import Path

requests = [
    {
        "request_id": "req-001",
        "prompt": "Return JSON with decision and reason.",
        "batch_size": 1
    },
    {
        "request_id": "req-002",
        "prompt": "Explain why score-only evals can miss regressions.",
        "batch_size": 1
    }
]

responses = []

for req in requests:
    start = time.perf_counter()

    # Local deterministic response demo, not production model serving.
    response_text = (
        '{"decision": "review", "reason": "schema-sensitive output requires validation"}'
        if "JSON" in req["prompt"]
        else "Score-only evals can hide failed constraints, schema breaks, and subset regressions."
    )

    latency_ms = (time.perf_counter() - start) * 1000
    token_count = len(req["prompt"].split()) + len(response_text.split())

    responses.append({
        "request_id": req["request_id"],
        "prompt": req["prompt"],
        "response": response_text,
        "batch_size": req["batch_size"],
        "token_count_estimate": token_count,
        "latency_ms": round(latency_ms, 4)
    })

report = {
    "num_requests": len(responses),
    "avg_latency_ms": round(sum(r["latency_ms"] for r in responses) / len(responses), 4),
    "max_latency_ms": round(max(r["latency_ms"] for r in responses), 4),
    "avg_token_count_estimate": round(sum(r["token_count_estimate"] for r in responses) / len(responses), 2),
    "results": responses,
    "note": "Tiny local inference workflow demo; not production or distributed model serving."
}

Path("ml_service/model_latency_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
