from typing import Any, Dict


def recommend_rollback(gate_summary: Dict[str, Any], drift_summary: Dict[str, Any]) -> Dict[str, Any]:
    reasons = []
    decision = "hold"

    if gate_summary.get("decision") == "fail":
        decision = "rollback_recommended"
        reasons.append("release_gate_failed")

    if "pass_rate_drift" in (drift_summary.get("alerts") or []):
        decision = "rollback_recommended"
        reasons.append("pass_rate_drift_detected")

    if "score_drift" in (drift_summary.get("alerts") or []):
        reasons.append("score_drift_detected")

    if (drift_summary.get("regressed_case_count") or 0) >= 2:
        reasons.append("multiple_regressed_cases")

    return {
        "decision": decision,
        "reasons": reasons,
    }
