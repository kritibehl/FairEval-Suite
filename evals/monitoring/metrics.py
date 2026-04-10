from typing import Any, Dict, List


def summarize_run_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    num_cases = len(results)
    avg_score = round(sum(float(r.get("score", 0.0)) for r in results) / max(1, num_cases), 4)
    pass_rate = round(sum(1 for r in results if bool(r.get("passed"))) / max(1, num_cases), 4)

    total_chars = sum(len((r.get("details", {}) or {}).get("model_output", "") or "") for r in results)
    avg_response_chars = round(total_chars / max(1, num_cases), 2)

    total_latency_ms = 0.0
    latency_count = 0
    total_cost_usd = 0.0

    for r in results:
        details = r.get("details", {}) or {}
        latency_ms = details.get("latency_ms")
        cost_usd = details.get("cost_usd", 0.0)
        if latency_ms is not None:
            total_latency_ms += float(latency_ms)
            latency_count += 1
        total_cost_usd += float(cost_usd)

    avg_latency_ms = round(total_latency_ms / max(1, latency_count), 2) if latency_count else None

    return {
        "num_cases": num_cases,
        "avg_score": avg_score,
        "pass_rate": pass_rate,
        "avg_response_chars": avg_response_chars,
        "avg_latency_ms": avg_latency_ms,
        "estimated_total_cost_usd": round(total_cost_usd, 6),
    }
