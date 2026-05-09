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
