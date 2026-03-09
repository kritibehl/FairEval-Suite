import json
from pathlib import Path

from evals.compare.diff import compare_reports
from evals.gate import apply_gate


def test_gate_fails_on_confidence_regression(tmp_path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    baseline_report = reports_dir / "baseline.json"
    candidate_report = reports_dir / "candidate.json"

    baseline_report.write_text(
        json.dumps(
            {
                "run_id": "baseline",
                "config": {"suite_name": "classification_basic", "model_name": "distilbert-sst2"},
                "summary": {"num_cases": 1, "avg_score": 0.96, "pass_rate": 1.0},
                "results": [
                    {
                        "case_id": "sentiment_pos_1",
                        "score": 0.96,
                        "passed": True,
                        "details": {
                            "predicted_label": "POSITIVE",
                            "expected_label": "POSITIVE",
                            "confidence": 0.96,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    candidate_report.write_text(
        json.dumps(
            {
                "run_id": "candidate",
                "config": {"suite_name": "classification_basic", "model_name": "distilbert-sst2"},
                "summary": {"num_cases": 1, "avg_score": 0.72, "pass_rate": 0.0},
                "results": [
                    {
                        "case_id": "sentiment_pos_1",
                        "score": 0.72,
                        "passed": False,
                        "details": {
                            "predicted_label": "POSITIVE",
                            "expected_label": "POSITIVE",
                            "confidence": 0.72,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    compare_res = compare_reports(
        baseline_report_path=str(baseline_report),
        candidate_report_path=str(candidate_report),
        out_dir=str(tmp_path),
    )

    gate_res = apply_gate(
        compare_artifact_path=compare_res["output_path"],
        out_dir=str(tmp_path),
        max_avg_score_drop=0.05,
        max_pass_rate_drop=0.10,
        fail_on_any_regression_case=True,
    )

    assert gate_res["decision"] == "fail"
    assert gate_res["summary"]["avg_score_delta"] == -0.24
    assert gate_res["summary"]["pass_rate_delta"] == -1.0
