import glob
import json
from pathlib import Path
from evals.variance import summarize_run_variance

paths = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*gemini_real*.json"))
summary = summarize_run_variance(paths)

out = Path("benchmark_public/instruction_following/variance_summary.json")
out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

print(json.dumps(summary, indent=2))
print(f"\nWrote {out}")
