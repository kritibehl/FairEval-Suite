import json
from pathlib import Path
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_evaluate_endpoint(tmp_path):
    dataset = tmp_path / "cases.jsonl"

    write_jsonl(dataset, [
        {
            "id": "c1",
            "input": {
                "prompt": "What is RAG?",
                "context": ["RAG uses retrieved context to ground answers."]
            },
            "expected": {"answer_contains": ["retrieved", "context"]},
        }
    ])

    r = client.post("/evaluate", json={
        "suite_name": "rag_basic",
        "dataset_path": str(dataset),
        "model_name": "mock",
        "max_workers": 1,
        "timeout_seconds": 5.0
    })

    assert r.status_code == 200
    body = r.json()

    assert "summary" in body
    assert "report" in body
    assert "report_artifact_path" in body

def test_compare_and_gate_endpoints(tmp_path):
    baseline = tmp_path / "baseline.json"
    candidate = tmp_path / "candidate.json"

    baseline.write_text(json.dumps({
        "run_id": "b1",
        "config": {"suite_name": "mini", "model_name": "mock"},
        "summary": {"num_cases": 1, "avg_score": 0.9, "pass_rate": 1.0},
        "results": [{"case_id": "c1", "score": 0.9, "passed": True, "details": {}}]
    }), encoding="utf-8")

    candidate.write_text(json.dumps({
        "run_id": "c1",
        "config": {"suite_name": "mini", "model_name": "mock"},
        "summary": {"num_cases": 1, "avg_score": 0.7, "pass_rate": 0.0},
        "results": [{"case_id": "c1", "score": 0.7, "passed": False, "details": {}}]
    }), encoding="utf-8")

    r = client.post("/compare", json={
        "baseline_report_path": str(baseline),
        "candidate_report_path": str(candidate),
        "top_k": 5
    })

    assert r.status_code == 200
    body = r.json()

    assert "compare_artifact" in body
    assert "summary" in body

    compare_path = tmp_path / "compare.json"
    compare_path.write_text(body["compare_artifact"], encoding="utf-8")

    r2 = client.post("/gate", json={
        "compare_artifact_path": str(compare_path),
        "max_avg_score_drop": 0.05,
        "max_pass_rate_drop": 0.10,
        "fail_on_any_regression_case": True
    })

    assert r2.status_code == 200
    assert r2.json()["summary"]["decision"] == "fail"
