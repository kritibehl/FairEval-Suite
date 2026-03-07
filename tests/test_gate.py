import json
from pathlib import Path

from evals.gate import apply_gate


def write_compare(path: Path, avg_score_delta: float, pass_rate_delta: float, regressed_count: int):
    case_diffs = []
    for i in range(regressed_count):
        case_diffs.append(
            {
                "case_id": f"case-{i}",
                "baseline_score": 0.8,
                "candidate_score": 0.6,
                "delta": -0.2,
                "baseline_passed": True,
                "candidate_passed": False,
                "regressed": True,
                "improved": False,
            }
        )

    payload = {
        "delta": {
            "avg_score": avg_score_delta,
            "pass_rate": pass_rate_delta,
            "num_cases": 0,
        },
        "case_diffs": case_diffs,
        "top_regressions": case_diffs,
        "top_improvements": [],
        "baseline": {"path": "baseline.json", "config": {}, "summary": {}},
        "candidate": {"path": "candidate.json", "config": {}, "summary": {}},
    }

    path.write_text(json.dumps(payload), encoding="utf-8")


def test_gate_passes_when_deltas_within_threshold(tmp_path):
    compare_path = tmp_path / "compare.json"
    write_compare(compare_path, avg_score_delta=-0.02, pass_rate_delta=-0.05, regressed_count=0)

    res = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        max_avg_score_drop=0.05,
        max_pass_rate_drop=0.10,
        fail_on_any_regression_case=False,
    )

    assert res["decision"] == "pass"
    assert res["reasons"] == []
    assert Path(res["output_path"]).exists()


def test_gate_fails_when_avg_score_drop_exceeds_threshold(tmp_path):
    compare_path = tmp_path / "compare.json"
    write_compare(compare_path, avg_score_delta=-0.20, pass_rate_delta=-0.05, regressed_count=0)

    res = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        max_avg_score_drop=0.05,
        max_pass_rate_drop=0.10,
        fail_on_any_regression_case=False,
    )

    assert res["decision"] == "fail"
    assert any("avg_score_drop_exceeded" in r for r in res["reasons"])


def test_gate_fails_when_regressed_cases_are_forbidden(tmp_path):
    compare_path = tmp_path / "compare.json"
    write_compare(compare_path, avg_score_delta=-0.01, pass_rate_delta=0.0, regressed_count=2)

    res = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        max_avg_score_drop=0.05,
        max_pass_rate_drop=0.10,
        fail_on_any_regression_case=True,
    )

    assert res["decision"] == "fail"
    assert any("regressed_cases_detected" in r for r in res["reasons"])
    assert res["summary"]["regressed_case_count"] == 2
