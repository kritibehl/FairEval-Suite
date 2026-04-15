import json
from .release_policies import get_policy
from pathlib import Path
from typing import Any, Dict


def load_json(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _derive_affected_query_pct(
    *,
    explicit_pct: float | None,
    regressed_case_count: int,
    total_case_count: int,
) -> float:
    if explicit_pct is not None:
        return max(0.0, min(1.0, float(explicit_pct)))
    if total_case_count <= 0:
        return 0.0
    return max(0.0, min(1.0, regressed_case_count / total_case_count))


def _derive_downstream_risk(
    *,
    explicit_risk: str | None,
    affected_query_pct: float,
    reasons: list[str],
) -> str:
    if explicit_risk:
        return explicit_risk.lower()

    if any("drop_exceeded" in r for r in reasons) and affected_query_pct >= 0.10:
        return "high"
    if affected_query_pct >= 0.20:
        return "high"
    if affected_query_pct >= 0.05:
        return "medium"
    return "low"


def _impact_statement(
    *,
    affected_query_pct: float,
    estimated_affected_queries: int | None,
    downstream_risk: str,
    release_decision: str,
) -> str:
    pct_display = round(affected_query_pct * 100, 2)

    if estimated_affected_queries is not None:
        return (
            f"{release_decision.upper()} release: estimated impact to {pct_display}% of queries "
            f"(~{estimated_affected_queries} queries/day), downstream_risk={downstream_risk}."
        )

    return (
        f"{release_decision.upper()} release: estimated impact to {pct_display}% of queries, "
        f"downstream_risk={downstream_risk}."
    )


def apply_gate(
    compare_artifact_path: str,
    out_dir: str = ".",
    max_avg_score_drop: float = 0.05,
    max_pass_rate_drop: float = 0.10,
    fail_on_any_regression_case: bool = False,
    estimated_affected_query_pct: float | None = None,
    max_affected_query_pct: float = 0.10,
    daily_query_volume: int | None = None,
    downstream_risk: str | None = None,
    block_on_high_downstream_risk: bool = True,
) -> Dict[str, Any]:
    compare_data = load_json(compare_artifact_path)
    delta = compare_data.get("delta", {}) or {}
    case_diffs = compare_data.get("case_diffs", []) or []

    avg_score_delta = float(delta.get("avg_score", 0.0))
    pass_rate_delta = float(delta.get("pass_rate", 0.0))

    regressed_cases = [c for c in case_diffs if c.get("regressed") is True]
    regressed_case_count = len(regressed_cases)
    total_case_count = len(case_diffs)

    reasons: list[str] = []

    if avg_score_delta < -max_avg_score_drop:
        reasons.append(
            f"avg_score_drop_exceeded: {avg_score_delta:.4f} < {-max_avg_score_drop:.4f}"
        )

    if pass_rate_delta < -max_pass_rate_drop:
        reasons.append(
            f"pass_rate_drop_exceeded: {pass_rate_delta:.4f} < {-max_pass_rate_drop:.4f}"
        )

    if fail_on_any_regression_case and regressed_cases:
        reasons.append(f"regressed_cases_detected: {regressed_case_count}")

    affected_query_pct = _derive_affected_query_pct(
        explicit_pct=estimated_affected_query_pct,
        regressed_case_count=regressed_case_count,
        total_case_count=total_case_count,
    )

    if affected_query_pct >= max_affected_query_pct:
        reasons.append(
            f"affected_query_pct_exceeded: {affected_query_pct:.4f} >= {max_affected_query_pct:.4f}"
        )

    derived_downstream_risk = _derive_downstream_risk(
        explicit_risk=downstream_risk,
        affected_query_pct=affected_query_pct,
        reasons=reasons,
    )

    if block_on_high_downstream_risk and derived_downstream_risk == "high":
        reasons.append("downstream_risk_high")

    status = "fail" if reasons else "pass"
    release_decision = "block" if reasons else "ship"

    estimated_affected_queries = None
    if daily_query_volume is not None:
        estimated_affected_queries = int(round(daily_query_volume * affected_query_pct))

    impact_statement = _impact_statement(
        affected_query_pct=affected_query_pct,
        estimated_affected_queries=estimated_affected_queries,
        downstream_risk=derived_downstream_risk,
        release_decision=release_decision,
    )

    rollback_recommendation = "rollback_to_baseline" if reasons else "ship_candidate"

    artifact = {
        "decision": status,
        "release_decision": release_decision,
        "reasons": reasons,
        "thresholds": {
            "max_avg_score_drop": max_avg_score_drop,
            "max_pass_rate_drop": max_pass_rate_drop,
            "fail_on_any_regression_case": fail_on_any_regression_case,
            "max_affected_query_pct": max_affected_query_pct,
            "block_on_high_downstream_risk": block_on_high_downstream_risk,
        },
        "summary": {
            "avg_score_delta": avg_score_delta,
            "pass_rate_delta": pass_rate_delta,
            "regressed_case_count": regressed_case_count,
            "total_case_count": total_case_count,
        },
        "production_impact": {
            "estimated_affected_query_pct": affected_query_pct,
            "estimated_affected_query_count_per_day": estimated_affected_queries,
            "downstream_risk": derived_downstream_risk,
            "impact_statement": impact_statement,
        },
        "rollback_recommendation": rollback_recommendation,
        "compare_artifact_path": compare_artifact_path,
    }

    gate_dir = Path(out_dir) / "gate"
    gate_dir.mkdir(parents=True, exist_ok=True)

    compare_stem = Path(compare_artifact_path).stem
    out_path = gate_dir / f"{compare_stem}.gate.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, sort_keys=False)

    artifact["output_path"] = str(out_path)
    return artifact
