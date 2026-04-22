import json
from pathlib import Path
from evals.gate import apply_gate


def test_blocks_when_quality_passes_but_latency_regresses(tmp_path: Path):
    compare_path = tmp_path / "compare.json"

    payload = {
        "delta": {
            "avg_score": -0.002,
            "pass_rate": 0.0
        },
        "case_diffs": [],
        "serving_delta": {
            "latency_p95_regression_pct": 41.8,
            "throughput_delta_pct": -5.0
        }
    }

    compare_path.write_text(json.dumps(payload))

    res = apply_gate(
        compare_artifact_path=str(compare_path),
        out_dir=str(tmp_path),
        max_latency_p95_regression_pct=20.0,
        max_throughput_drop_pct=15.0,
    )

    assert res["summary"]["quality_pass"] is True
    assert res["serving_gate"]["latency_pass"] is False
    assert res["release_decision"] == "block"
