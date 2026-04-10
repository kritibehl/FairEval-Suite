from evals.alerts import detect_behavior_drift
from evals.monitoring.rollback import recommend_rollback
from evals.monitoring import summarize_run_metrics


def test_detect_behavior_drift_flags_regressions():
    compare_artifact = {
        "delta": {"avg_score": -0.2, "pass_rate": -0.5},
        "case_diffs": [
            {"case_id": "c1", "regressed": True},
            {"case_id": "c2", "regressed": True},
        ],
    }
    res = detect_behavior_drift(compare_artifact)
    assert "score_drift" in res["alerts"]
    assert "pass_rate_drift" in res["alerts"]
    assert res["regressed_case_count"] == 2


def test_recommend_rollback_on_fail_and_drift():
    gate_summary = {"decision": "fail"}
    drift_summary = {
        "alerts": ["score_drift", "pass_rate_drift"],
        "regressed_case_count": 2,
    }
    res = recommend_rollback(gate_summary, drift_summary)
    assert res["decision"] == "rollback_recommended"
    assert "release_gate_failed" in res["reasons"]


def test_summarize_run_metrics_includes_latency():
    results = [
        {"score": 0.8, "passed": True, "details": {"model_output": "abc", "latency_ms": 50.0, "cost_usd": 0.0}},
        {"score": 0.6, "passed": False, "details": {"model_output": "abcdef", "latency_ms": 70.0, "cost_usd": 0.0}},
    ]
    res = summarize_run_metrics(results)
    assert res["num_cases"] == 2
    assert res["avg_latency_ms"] == 60.0
