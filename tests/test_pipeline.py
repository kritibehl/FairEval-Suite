import json
from pathlib import Path

from evals.pipeline import run_release_gate


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def test_release_gate_runs_end_to_end(tmp_path):
    dataset_path = tmp_path / "datasets" / "mini" / "cases.jsonl"

    rows = [
        {
            "id": "case-1",
            "input": {
                "prompt": "What is retrieval augmented generation?",
                "context": [
                    "Retrieval augmented generation uses retrieved context to ground responses."
                ],
            },
            "expected": {
                "answer_contains": ["retrieved", "context"]
            },
        }
    ]
    write_jsonl(dataset_path, rows)

    baseline_report_path = tmp_path / "reports" / "baseline123.json"
    baseline_report_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_report_path.write_text(
        json.dumps(
            {
                "run_id": "baseline123",
                "config": {"suite_name": "mini", "model_name": "mock"},
                "summary": {"num_cases": 1, "avg_score": 0.95, "pass_rate": 1.0},
                "results": [
                    {"case_id": "case-1", "score": 0.95, "passed": True, "details": {}}
                ],
            }
        ),
        encoding="utf-8",
    )

    res = run_release_gate(
        suite_name="mini",
        baseline_run_id="baseline123",
        dataset_path=str(dataset_path),
        model_name="mock",
        out_dir=str(tmp_path),
        reports_dir=str(tmp_path / "reports"),
        max_workers=1,
        timeout_seconds=5.0,
        max_avg_score_drop=1.0,
        max_pass_rate_drop=1.0,
        fail_on_any_regression_case=False,
    )

    assert "run" in res
    assert "compare" in res
    assert "gate" in res
    assert Path(res["compare"]["output_path"]).exists()
    assert Path(res["gate"]["output_path"]).exists()
