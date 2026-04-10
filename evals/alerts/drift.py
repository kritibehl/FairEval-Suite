from typing import Any, Dict, List


def detect_behavior_drift(compare_artifact: Dict[str, Any]) -> Dict[str, Any]:
    delta = compare_artifact.get("delta", {}) or {}
    case_diffs: List[Dict[str, Any]] = compare_artifact.get("case_diffs", []) or []

    avg_score_delta = float(delta.get("avg_score", 0.0))
    pass_rate_delta = float(delta.get("pass_rate", 0.0))
    regressed_cases = [c for c in case_diffs if c.get("regressed") is True]

    alerts = []
    if avg_score_delta < -0.05:
        alerts.append("score_drift")
    if pass_rate_delta < -0.10:
        alerts.append("pass_rate_drift")
    if len(regressed_cases) >= 2:
        alerts.append("multi_case_regression")

    return {
        "alerts": alerts,
        "regressed_case_count": len(regressed_cases),
        "avg_score_delta": avg_score_delta,
        "pass_rate_delta": pass_rate_delta,
    }
