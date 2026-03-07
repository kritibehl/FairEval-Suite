import json
from pathlib import Path

from evals.runner import run_suite
from evals.compare.diff import compare_reports


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def test_run_suite_writes_run_and_report_artifacts(tmp_path):
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
        },
        {
            "id": "case-2",
            "input": {
                "prompt": "What helps reduce hallucinations?",
                "context": [
                    "Grounding responses in retrieved documents can reduce hallucinations."
                ],
            },
            "expected": {
                "answer_contains": ["retrieved"]
            },
        },
    ]

    write_jsonl(dataset_path, rows)

    res = run_suite(
        suite_name="mini",
        dataset_path=str(dataset_path),
        model_name="mock",
        out_dir=str(tmp_path),
        max_workers=1,
        timeout_seconds=5.0,
    )

    assert "run_id" in res
    assert res["num_cases"] == 2
    assert 0.0 <= res["avg_score"] <= 1.0
    assert 0.0 <= res["pass_rate"] <= 1.0

    run_path = tmp_path / "runs" / f'{res["run_id"]}.json'
    report_path = tmp_path / "reports" / f'{res["run_id"]}.json'

    assert run_path.exists()
    assert report_path.exists()

    run_data = json.loads(run_path.read_text(encoding="utf-8"))
    report_data = json.loads(report_path.read_text(encoding="utf-8"))

    assert run_data["run_id"] == res["run_id"]
    assert report_data["run_id"] == res["run_id"]
    assert len(run_data["cases"]) == 2
    assert len(report_data["results"]) == 2
    assert report_data["summary"]["num_cases"] == 2


def test_compare_reports_writes_diff_artifact(tmp_path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    baseline_report = reports_dir / "baseline.json"
    candidate_report = reports_dir / "candidate.json"

    baseline_report.write_text(
        json.dumps(
            {
                "run_id": "baseline",
                "config": {"suite_name": "mini", "model_name": "mock"},
                "summary": {"num_cases": 2, "avg_score": 0.8, "pass_rate": 1.0},
                "results": [
                    {"case_id": "case-1", "score": 0.9, "passed": True, "details": {}},
                    {"case_id": "case-2", "score": 0.7, "passed": True, "details": {}},
                ],
            }
        ),
        encoding="utf-8",
    )

    candidate_report.write_text(
        json.dumps(
            {
                "run_id": "candidate",
                "config": {"suite_name": "mini", "model_name": "mock"},
                "summary": {"num_cases": 2, "avg_score": 0.6, "pass_rate": 0.5},
                "results": [
                    {"case_id": "case-1", "score": 0.65, "passed": True, "details": {}},
                    {"case_id": "case-2", "score": 0.55, "passed": False, "details": {}},
                ],
            }
        ),
        encoding="utf-8",
    )

    res = compare_reports(
        baseline_report_path=str(baseline_report),
        candidate_report_path=str(candidate_report),
        out_dir=str(tmp_path),
        top_k=5,
    )

    assert "output_path" in res
    assert res["avg_score"] == -0.2
    assert res["pass_rate"] == -0.5

    compare_path = Path(res["output_path"])
    assert compare_path.exists()

    compare_data = json.loads(compare_path.read_text(encoding="utf-8"))
    assert compare_data["baseline"]["path"] == str(baseline_report)
    assert compare_data["candidate"]["path"] == str(candidate_report)
    assert len(compare_data["case_diffs"]) == 2
    assert len(compare_data["top_regressions"]) >= 1
