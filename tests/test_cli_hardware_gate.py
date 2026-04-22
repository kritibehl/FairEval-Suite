import json
import subprocess
import sys
from pathlib import Path


def test_cli_gate_supports_serving_thresholds(tmp_path: Path):
    compare_path = tmp_path / "compare.json"
    compare_path.write_text(json.dumps({
        "delta": {"avg_score": -0.002, "pass_rate": 0.0},
        "case_diffs": [],
        "serving_delta": {
            "latency_p95_regression_pct": 41.8,
            "throughput_delta_pct": -5.0
        }
    }))

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "evals.cli",
            "gate",
            "--compare-artifact",
            str(compare_path),
            "--out-dir",
            str(tmp_path),
            "--max-latency-p95-regression-pct",
            "20",
            "--max-throughput-drop-pct",
            "15",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "block" in result.stdout.lower() or "fail" in result.stdout.lower()
