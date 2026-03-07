import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def apply_gate(
    compare_artifact_path: str,
    out_dir: str = ".",
    max_avg_score_drop: float = 0.05,
    max_pass_rate_drop: float = 0.10,
    fail_on_any_regression_case: bool = False,
) -> Dict[str, Any]:
    compare_data = load_json(compare_artifact_path)

    delta = compare_data.get("delta", {}) or {}
    case_diffs = compare_data.get("case_diffs", []) or []

    avg_score_delta = float(delta.get("avg_score", 0.0))
    pass_rate_delta = float(delta.get("pass_rate", 0.0))

    reasons = []

    if avg_score_delta < -max_avg_score_drop:
        reasons.append(
            f"avg_score_drop_exceeded: {avg_score_delta:.4f} < {-max_avg_score_drop:.4f}"
        )

    if pass_rate_delta < -max_pass_rate_drop:
        reasons.append(
            f"pass_rate_drop_exceeded: {pass_rate_delta:.4f} < {-max_pass_rate_drop:.4f}"
        )

    regressed_cases = [c for c in case_diffs if c.get("regressed") is True]
    if fail_on_any_regression_case and regressed_cases:
        reasons.append(
            f"regressed_cases_detected: {len(regressed_cases)}"
        )

    decision = "fail" if reasons else "pass"

    artifact = {
        "decision": decision,
        "reasons": reasons,
        "thresholds": {
            "max_avg_score_drop": max_avg_score_drop,
            "max_pass_rate_drop": max_pass_rate_drop,
            "fail_on_any_regression_case": fail_on_any_regression_case,
        },
        "summary": {
            "avg_score_delta": avg_score_delta,
            "pass_rate_delta": pass_rate_delta,
            "regressed_case_count": len(regressed_cases),
        },
        "compare_artifact_path": compare_artifact_path,
    }

    gate_dir = Path(out_dir) / "gate"
    gate_dir.mkdir(parents=True, exist_ok=True)

    compare_stem = Path(compare_artifact_path).stem
    out_path = gate_dir / f"{compare_stem}.gate.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, sort_keys=False)

    return {"output_path": str(out_path), **artifact}
