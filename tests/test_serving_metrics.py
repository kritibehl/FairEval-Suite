from evals.serving_metrics import build_serving_delta


def test_build_serving_delta():
    baseline = {
        "latency_p50_ms": 410,
        "latency_p95_ms": 690,
        "throughput_rps": 8.2,
    }
    candidate = {
        "latency_p50_ms": 438,
        "latency_p95_ms": 1015,
        "throughput_rps": 7.7,
    }

    delta = build_serving_delta(baseline, candidate)

    assert round(delta["latency_p95_regression_pct"], 1) == 47.1
    assert delta["throughput_delta_pct"] < 0
