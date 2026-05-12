import csv
import json
import glob
from pathlib import Path

reports = sorted(glob.glob("benchmark_public/instruction_following/runs/reports/*.json"))
variance_path = Path("benchmark_public/instruction_following/variance_summary.json")

rows = []
failed_cases = []

for p in reports:
    data = json.load(open(p))
    summary = data.get("summary", {})
    config = data.get("config", {})
    run_id = data.get("run_id")

    rows.append({
        "run_id": run_id,
        "model": config.get("model_name", "unknown"),
        "avg_score": summary.get("avg_score", 0),
        "pass_rate": summary.get("pass_rate", 0),
        "failed_case_count": summary.get("failed_case_count", 0),
        "num_cases": summary.get("num_cases", 0),
        "artifact_path": p,
    })

    for r in data.get("results", []):
        if not r.get("passed", False):
            failed_cases.append({
                "run_id": run_id,
                "model": config.get("model_name", "unknown"),
                "case_id": r.get("case_id"),
                "score": r.get("score"),
                "details": json.dumps(r.get("details", {}))[:300],
            })

variance = json.loads(variance_path.read_text()) if variance_path.exists() else {}

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>FairEval Benchmark Explorer</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; }}
    h1 {{ margin-bottom: 4px; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin: 16px 0; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 14px; }}
    th {{ background: #f5f5f5; }}
    input {{ padding: 8px; width: 320px; }}
    code {{ background: #f6f6f6; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>FairEval Benchmark Explorer</h1>
  <p>Compare runs, inspect regressions, review failed cases, and track variance.</p>

  <div class="card">
    <h2>Variance Analysis</h2>
    <pre>{json.dumps(variance, indent=2)}</pre>
  </div>

  <div class="card">
    <h2>Run Comparison</h2>
    <input id="runFilter" placeholder="Filter by model/run_id..." onkeyup="filterTable('runTable', this.value)" />
    <table id="runTable">
      <thead>
        <tr><th>Model</th><th>Run ID</th><th>Avg Score</th><th>Pass Rate</th><th>Failed</th><th>Total</th><th>Artifact</th></tr>
      </thead>
      <tbody>
        {''.join(f"<tr><td>{r['model']}</td><td><code>{r['run_id']}</code></td><td>{r['avg_score']}</td><td>{r['pass_rate']}</td><td>{r['failed_case_count']}</td><td>{r['num_cases']}</td><td>{r['artifact_path']}</td></tr>" for r in rows)}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Failed Case Inspection</h2>
    <input id="failFilter" placeholder="Filter failed cases..." onkeyup="filterTable('failTable', this.value)" />
    <table id="failTable">
      <thead>
        <tr><th>Model</th><th>Run ID</th><th>Case ID</th><th>Score</th><th>Details</th></tr>
      </thead>
      <tbody>
        {''.join(f"<tr><td>{r['model']}</td><td><code>{r['run_id']}</code></td><td>{r['case_id']}</td><td>{r['score']}</td><td>{r['details']}</td></tr>" for r in failed_cases)}
      </tbody>
    </table>
  </div>

<script>
function filterTable(tableId, query) {{
  query = query.toLowerCase();
  const rows = document.querySelectorAll("#" + tableId + " tbody tr");
  rows.forEach(row => {{
    row.style.display = row.innerText.toLowerCase().includes(query) ? "" : "none";
  }});
}}
</script>
</body>
</html>
"""

Path("dashboard/benchmark_explorer.html").write_text(html, encoding="utf-8")
print("Wrote dashboard/benchmark_explorer.html")
