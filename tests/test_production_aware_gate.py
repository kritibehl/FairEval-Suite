import json
from pathlib import Path

from evals.gate import apply_gate


def test_gate_blocks_on_estimated_production_impact(tmp_path: Path):
    compare_dir = tmp_path / "compare"
    compare_dir.mkdir(parents=True, exist_ok=True)

    compare_path = compare_dir / "candidate_vs_baseline.json"
    compare_payload = {
        "delta": {"avg_score": -0.794, "pass_rate": -1.0},
        "case_diffs": [
            {"case_id": "c1", "regressed": True},
            {"case_id": "c2", "regressed": False},
            {"case_id": "c3", "regressed": False},
            {"case_id": "c4", "regressed": False},
            {"case_id": "c5", "regressed": False},
        ],
    }
    compare_path.write_text(json.dumps(compare_payload), encoding="utf-8")

    result = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        estimated_affected_query_pct=0.12,
        max_affected_query_pct=0.10,
        daily_query_volume=100000,
        downstream_risk="high",
        block_on_high_downstream_risk=True,
    )

    assert result["decision"] == "fail"
    assert result["release_decision"] == "block"
    assert result["production_impact"]["estimated_affected_query_pct"] == 0.12
    assert result["production_impact"]["estimated_affected_query_count_per_day"] == 12000
    assert result["production_impact"]["downstream_risk"] == "high"
    assert "downstream_risk_high" in result["reasons"]


def test_gate_derives_impact_from_regressed_case_share(tmp_path: Path):
    compare_dir = tmp_path / "compare"
    compare_dir.mkdir(parents=True, exist_ok=True)

    compare_path = compare_dir / "candidate_vs_baseline.json"
    compare_payload = {
        "delta": {"avg_score": -0.01, "pass_rate": -0.01},
        "case_diffs": [
            {"case_id": "c1", "regressed": True},
            {"case_id": "c2", "regressed": True},
            {"case_id": "c3", "regressed": False},
            {"case_id": "c4", "regressed": False},
            {"case_id": "c5", "regressed": False},
        ],
    }
    compare_path.write_text(json.dumps(compare_payload), encoding="utf-8")

    result = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        max_affected_query_pct=0.30,
        block_on_high_downstream_risk=False,
    )

    assert result["production_impact"]["estimated_affected_query_pct"] == 0.4
    assert result["release_decision"] == "block"
