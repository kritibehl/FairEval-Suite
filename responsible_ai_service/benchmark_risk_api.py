import json
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "http://127.0.0.1:8030"

SUMMARY_OUT = Path("responsible_ai_service/risk_api_benchmark_summary.json")
REPORT_OUT = Path("responsible_ai_service/risk_api_service_readiness_report.md")


def post_json(path, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return urllib.request.urlopen(req, timeout=5)


def get(path):
    return urllib.request.urlopen(f"{BASE_URL}{path}", timeout=5)


def is_valid_eval_content_response(data):
    required = {
        "content_id",
        "risk_categories",
        "risk_severity",
        "recommended_action",
        "review_reason",
        "telemetry_tags",
    }
    return required.issubset(data.keys())


def is_valid_batch_response(data):
    required = {
        "run_id",
        "evaluated_items",
        "high_risk_items",
        "human_review_required",
        "release_recommendation",
        "results",
    }
    return required.issubset(data.keys())


def percentile(values, pct):
    if not values:
        return 0.0
    values = sorted(values)
    index = int(round((pct / 100) * (len(values) - 1)))
    return values[index]


synthetic_content_requests = [
    {
        "content_id": f"msg-{i:03d}",
        "content_type": "ai_generated_text",
        "scenario_category": category,
        "source": "candidate_model",
        "content": "Synthetic risk-review content for service-readiness benchmark.",
        "context": {
            "grounding_required": category in {"ungrounded_answer", "unsupported_high_stakes_claim"},
            "human_review_expected": category in {"sensitive_data_exposure_risk", "human_review_required"},
        },
    }
    for i, category in enumerate(
        [
            "sensitive_data_exposure_risk",
            "ungrounded_answer",
            "unsupported_high_stakes_claim",
            "instruction_conflict",
            "policy_bypass_attempt",
            "refusal_inconsistency",
            "human_review_required",
            "sensitive_data_exposure_risk",
            "ungrounded_answer",
            "instruction_conflict",
        ],
        start=1,
    )
]

batch_payload = {
    "run_id": "rai-benchmark-batch-001",
    "items": synthetic_content_requests[:5],
}

latencies = []
health_latencies = []
batch_eval_latency_ms = 0.0

total_requests = 0
successful_responses = 0
schema_valid_responses = 0
failed_requests = 0
health_success = 0
health_total = 5

for _ in range(health_total):
    total_requests += 1
    start = time.perf_counter()
    try:
        with get("/rai/health") as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            elapsed = (time.perf_counter() - start) * 1000
            health_latencies.append(elapsed)
            latencies.append(elapsed)
            successful_responses += int(resp.status == 200)
            health_success += int(payload.get("status") == "ok")
            schema_valid_responses += int("status" in payload and "service" in payload)
    except Exception:
        failed_requests += 1

for payload in synthetic_content_requests:
    total_requests += 1
    start = time.perf_counter()
    try:
        with post_json("/rai/evaluate-content", payload) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = (time.perf_counter() - start) * 1000
            latencies.append(elapsed)
            successful_responses += int(resp.status == 200)
            schema_valid_responses += int(is_valid_eval_content_response(data))
    except Exception:
        failed_requests += 1

total_requests += 1
start = time.perf_counter()
try:
    with post_json("/rai/evaluate-batch", batch_payload) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = (time.perf_counter() - start) * 1000
        batch_eval_latency_ms = elapsed
        latencies.append(elapsed)
        successful_responses += int(resp.status == 200)
        schema_valid_responses += int(is_valid_batch_response(data))
except Exception:
    failed_requests += 1

summary = {
    "total_requests": total_requests,
    "successful_responses": successful_responses,
    "schema_valid_responses": schema_valid_responses,
    "failed_requests": failed_requests,
    "p50_latency_ms": round(percentile(latencies, 50), 4),
    "p95_latency_ms": round(percentile(latencies, 95), 4),
    "max_latency_ms": round(max(latencies) if latencies else 0.0, 4),
    "batch_eval_latency_ms": round(batch_eval_latency_ms, 4),
    "health_check_success_rate": round(health_success / health_total, 4),
    "safe_scope": "Synthetic local service-readiness benchmark for Responsible AI risk-evaluation endpoints; not production load testing."
}

SUMMARY_OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")

REPORT_OUT.write_text(
    "\n".join([
        "# Responsible AI Risk API Service Readiness Report",
        "",
        "Synthetic local benchmark for FairEval Responsible AI risk-evaluation endpoints.",
        "",
        "## Summary",
        "",
        f"- total requests: {summary['total_requests']}",
        f"- successful responses: {summary['successful_responses']}",
        f"- schema-valid responses: {summary['schema_valid_responses']}",
        f"- failed requests: {summary['failed_requests']}",
        f"- p50 latency ms: {summary['p50_latency_ms']}",
        f"- p95 latency ms: {summary['p95_latency_ms']}",
        f"- max latency ms: {summary['max_latency_ms']}",
        f"- batch eval latency ms: {summary['batch_eval_latency_ms']}",
        f"- health check success rate: {summary['health_check_success_rate']}",
        "",
        "## Endpoints benchmarked",
        "",
        "- `GET /rai/health`",
        "- `POST /rai/evaluate-content`",
        "- `POST /rai/evaluate-batch`",
        "",
        "## Safe scope",
        "",
        summary["safe_scope"],
    ]) + "\n",
    encoding="utf-8",
)

print(json.dumps(summary, indent=2))
print(f"Wrote {SUMMARY_OUT}")
print(f"Wrote {REPORT_OUT}")
