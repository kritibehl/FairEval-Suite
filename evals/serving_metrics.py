from __future__ import annotations

from typing import Any, Dict


def _pct_change(baseline: float, candidate: float) -> float:
    if baseline == 0:
        if candidate == 0:
            return 0.0
        return 100.0
    return round(((candidate - baseline) / baseline) * 100.0, 4)


def build_serving_delta(
    baseline: Dict[str, Any],
    candidate: Dict[str, Any],
) -> Dict[str, Any]:
    baseline_p50 = float(baseline.get("latency_p50_ms", 0.0))
    candidate_p50 = float(candidate.get("latency_p50_ms", 0.0))

    baseline_p95 = float(baseline.get("latency_p95_ms", 0.0))
    candidate_p95 = float(candidate.get("latency_p95_ms", 0.0))

    baseline_tput = float(baseline.get("throughput_rps", 0.0))
    candidate_tput = float(candidate.get("throughput_rps", 0.0))

    return {
        "baseline_latency_p50_ms": baseline_p50,
        "candidate_latency_p50_ms": candidate_p50,
        "baseline_latency_p95_ms": baseline_p95,
        "candidate_latency_p95_ms": candidate_p95,
        "baseline_throughput_rps": baseline_tput,
        "candidate_throughput_rps": candidate_tput,
        "latency_p50_regression_pct": _pct_change(baseline_p50, candidate_p50),
        "latency_p95_regression_pct": _pct_change(baseline_p95, candidate_p95),
        "throughput_delta_pct": _pct_change(baseline_tput, candidate_tput),
    }
