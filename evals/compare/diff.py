import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class CaseDiff:
    case_id: str
    baseline_score: float
    candidate_score: float
    delta: float
    baseline_passed: bool
    candidate_passed: bool
    regressed: bool
    improved: bool


def _load_report(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def compare_reports(
    baseline_report_path: str,
    candidate_report_path: str,
    out_dir: str = ".",
    top_k: int = 10,
) -> Dict[str, Any]:
    baseline = _load_report(Path(baseline_report_path))
    candidate = _load_report(Path(candidate_report_path))

    b_sum = baseline.get("summary", {}) or {}
    c_sum = candidate.get("summary", {}) or {}

    b_results = {r["case_id"]: r for r in (baseline.get("results", []) or [])}
    c_results = {r["case_id"]: r for r in (candidate.get("results", []) or [])}

    all_case_ids = sorted(set(b_results.keys()) | set(c_results.keys()))

    diffs: List[CaseDiff] = []
    for cid in all_case_ids:
        br = b_results.get(cid)
        cr = c_results.get(cid)

        b_score = float(br["score"]) if br else 0.0
        c_score = float(cr["score"]) if cr else 0.0
        b_pass = bool(br["passed"]) if br else False
        c_pass = bool(cr["passed"]) if cr else False
        delta = c_score - b_score

        diffs.append(
            CaseDiff(
                case_id=cid,
                baseline_score=b_score,
                candidate_score=c_score,
                delta=delta,
                baseline_passed=b_pass,
                candidate_passed=c_pass,
                regressed=(b_pass and not c_pass) or (delta < -1e-9),
                improved=(not b_pass and c_pass) or (delta > 1e-9),
            )
        )

    # Sort: biggest regressions first (most negative deltas)
    regressions = sorted(diffs, key=lambda d: d.delta)[:top_k]
    improvements = sorted(diffs, key=lambda d: d.delta, reverse=True)[:top_k]

    out = {
        "baseline": {
            "path": baseline_report_path,
            "config": baseline.get("config", {}),
            "summary": b_sum,
        },
        "candidate": {
            "path": candidate_report_path,
            "config": candidate.get("config", {}),
            "summary": c_sum,
        },
        "delta": {
            "avg_score": round(float(c_sum.get("avg_score", 0.0)) - float(b_sum.get("avg_score", 0.0)), 4),
            "pass_rate": round(float(c_sum.get("pass_rate", 0.0)) - float(b_sum.get("pass_rate", 0.0)), 4),
            "num_cases": int(c_sum.get("num_cases", 0)) - int(b_sum.get("num_cases", 0)),
        },
        "top_regressions": [d.__dict__ for d in regressions],
        "top_improvements": [d.__dict__ for d in improvements],
        "case_diffs": [d.__dict__ for d in diffs],
    }

    compare_dir = Path(out_dir) / "compare"
    compare_dir.mkdir(parents=True, exist_ok=True)

    b_id = Path(baseline_report_path).stem
    c_id = Path(candidate_report_path).stem
    out_path = compare_dir / f"{c_id}_vs_{b_id}.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False)

    return {"output_path": str(out_path), **out["delta"]}
