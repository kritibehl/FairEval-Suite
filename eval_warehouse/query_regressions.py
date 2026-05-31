import sqlite3
from pathlib import Path

DB = "eval_warehouse/faireval_eval_warehouse.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
SELECT
  e.run_id,
  e.model_id,
  f.failure_category,
  f.count,
  r.decision
FROM eval_runs e
JOIN failures f ON e.run_id = f.run_id
JOIN release_decisions r ON e.run_id = r.run_id
ORDER BY f.count DESC
""").fetchall()

lines = [
    "# Weekly Evaluation Regression Report",
    "",
    "| Run | Model | Failure Category | Count | Release Decision |",
    "|---|---|---|---:|---|",
]

for row in rows:
    lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |")

Path("eval_warehouse/weekly_eval_report.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
conn.close()
