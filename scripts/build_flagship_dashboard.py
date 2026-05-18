import json
from pathlib import Path

def load(path, default):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else default

comparison = load("nlp_experiments/local_model_comparison_report.json", {"summary": {}})["summary"]
rai = load("responsible_ai/responsible_ai_regression_summary.json", {"summary": {}})["summary"]
oversight = load("oversight_reliability_study/oversight_failure_results.json", {"summary": {}})["summary"]
warehouse = load("eval_warehouse/warehouse_summary.json", {})

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>FairEval AI Evaluation Flagship Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(280px, 1fr)); gap: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; }}
    .metric {{ font-size: 26px; font-weight: bold; }}
    code {{ background: #f6f6f6; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>FairEval AI Evaluation Platform Dashboard</h1>
  <p>Evaluation flagship view covering baseline-vs-candidate comparison, Responsible AI release gates, oversight reliability, and warehouse lineage.</p>

  <div class="grid">
    <div class="card">
      <h2>Text Generation Comparison</h2>
      <p>Tasks evaluated</p>
      <div class="metric">{comparison.get("num_tasks", "n/a")}</div>
      <p>Regressions detected: <b>{comparison.get("regressions_detected", "n/a")}</b></p>
      <p>Baseline avg score: <b>{comparison.get("baseline_avg_score", "n/a")}</b></p>
      <p>Candidate avg score: <b>{comparison.get("candidate_avg_score", "n/a")}</b></p>
    </div>

    <div class="card">
      <h2>Responsible AI Safety Gate</h2>
      <p>Release decision</p>
      <div class="metric">{rai.get("release_decision", "n/a")}</div>
      <p>Safety regressions: <b>{rai.get("num_safety_regressions", "n/a")}</b></p>
      <p>False allows: <b>{rai.get("false_allows", "n/a")}</b></p>
      <p>Candidate pass rate: <b>{rai.get("candidate_pass_rate", "n/a")}</b></p>
    </div>

    <div class="card">
      <h2>Oversight Reliability Study</h2>
      <p>Weak evaluator false allows</p>
      <div class="metric">{oversight.get("weak_evaluator_false_allows", "n/a")}</div>
      <p>Composite false allows: <b>{oversight.get("composite_evaluator_false_allows", "n/a")}</b></p>
      <p>Weak recall: <b>{oversight.get("weak_evaluator_regression_recall", "n/a")}</b></p>
      <p>Composite recall: <b>{oversight.get("composite_evaluator_regression_recall", "n/a")}</b></p>
    </div>

    <div class="card">
      <h2>Evaluation Warehouse</h2>
      <p>Stored records by table</p>
      <pre>{json.dumps(warehouse, indent=2)}</pre>
    </div>
  </div>

  <h2>Live API</h2>
  <p><code>https://faireval-rai-api-126325674316.us-central1.run.app/docs</code></p>
</body>
</html>
"""

Path("dashboard/faireval_flagship_dashboard.html").write_text(html)
print("Wrote dashboard/faireval_flagship_dashboard.html")
