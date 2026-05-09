from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import json
import glob

app = FastAPI(title="FairEval Release Gate API")

class GateRequest(BaseModel):
    compare_artifact_path: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "faireval-release-gate"}

@app.get("/benchmark/latest")
def latest_benchmark():
    reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
    if not reports:
        return {"status": "missing", "message": "no reports found"}
    p = reports[-1]
    data = json.loads(Path(p).read_text())
    return {
        "artifact_path": p,
        "run_id": data.get("run_id"),
        "summary": data.get("summary"),
        "model_name": data.get("config", {}).get("model_name"),
    }

@app.get("/gate/latest")
def latest_gate():
    gates = sorted(glob.glob("benchmark_public/instruction_following/gates/**/*.json", recursive=True))
    if not gates:
        return {"status": "missing", "message": "no gate artifacts found"}
    p = gates[-1]
    data = json.loads(Path(p).read_text())
    return {
        "artifact_path": p,
        "decision": data.get("decision"),
        "release_decision": data.get("release_decision"),
        "reason": data.get("reason"),
        "summary": data.get("summary"),
    }


@app.get("/metrics")
def metrics():
    reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
    gates = sorted(glob.glob("benchmark_public/instruction_following/gates/**/*.json", recursive=True))

    latest_report = json.loads(Path(reports[-1]).read_text()) if reports else {}
    latest_gate = json.loads(Path(gates[-1]).read_text()) if gates else {}

    summary = latest_report.get("summary", {})
    failed = summary.get("failed_case_count", 0) or 0
    total = summary.get("num_cases", 0) or 0
    pass_rate = summary.get("pass_rate", 0.0) or 0.0
    gate_block = 1 if latest_gate.get("release_decision") == "block" else 0

    lines = [
        "# HELP faireval_benchmark_runs_total Number of benchmark reports available",
        "# TYPE faireval_benchmark_runs_total counter",
        f"faireval_benchmark_runs_total {len(reports)}",
        "# HELP faireval_failed_cases Latest failed case count",
        "# TYPE faireval_failed_cases gauge",
        f"faireval_failed_cases {failed}",
        "# HELP faireval_total_cases Latest benchmark case count",
        "# TYPE faireval_total_cases gauge",
        f"faireval_total_cases {total}",
        "# HELP faireval_pass_rate Latest benchmark pass rate",
        "# TYPE faireval_pass_rate gauge",
        f"faireval_pass_rate {pass_rate}",
        "# HELP faireval_release_gate_block Latest gate block decision",
        "# TYPE faireval_release_gate_block gauge",
        f"faireval_release_gate_block {gate_block}",
    ]
    return "\n".join(lines) + "\n"
