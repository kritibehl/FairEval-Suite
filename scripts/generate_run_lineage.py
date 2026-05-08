import glob
import json
from pathlib import Path

from evals.run_lineage import build_run_lineage, write_run_lineage

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
if not reports:
    raise SystemExit("No benchmark reports found.")

report_path = reports[-1]
report = json.load(open(report_path))
run_id = report["run_id"]
config = report.get("config", {})

lineage = build_run_lineage(
    run_id=run_id,
    dataset_path="datasets/benchmark_instruction_following/cases.jsonl",
    model_name=config.get("model_name", "unknown"),
    model_version=config.get("model_version"),
    prompt_version=config.get("prompt_version", "prompt_v1"),
    evaluator_version=config.get("scorer_name", "unknown"),
    threshold_version="release_gate_v1",
)

out = write_run_lineage(lineage)
print(json.dumps(lineage, indent=2))
print(f"Wrote {out}")
