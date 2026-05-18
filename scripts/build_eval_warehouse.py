import json
import sqlite3
from pathlib import Path

DB = Path("eval_warehouse/faireval_eval_warehouse.sqlite")
SCHEMA = Path("eval_warehouse/schema.sql")

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript(SCHEMA.read_text())

registry = json.loads(Path("model_registry/model_registry.json").read_text())
for m in registry["models"]:
    cur.execute(
        """
        INSERT OR REPLACE INTO model_registry
        (model_id, provider, model_type, status, risk_review_required)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            m["model_id"],
            m["provider"],
            m["model_type"],
            m["status"],
            int(m["risk_review_required"]),
        ),
    )

comparison_path = Path("nlp_experiments/local_model_comparison_report.json")
if comparison_path.exists():
    s = json.loads(comparison_path.read_text())["summary"]
    cur.execute(
        """
        INSERT OR REPLACE INTO evaluation_runs
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "local_text_generation_eval",
            s["baseline_model"],
            s["candidate_model"],
            s["num_tasks"],
            s["regressions_detected"],
            s["baseline_avg_score"],
            s["candidate_avg_score"],
            s["latency_ms"],
        ),
    )

rai_path = Path("responsible_ai/responsible_ai_regression_summary.json")
if rai_path.exists():
    s = json.loads(rai_path.read_text())["summary"]
    cur.execute(
        """
        INSERT OR REPLACE INTO responsible_ai_runs
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "rai-eval-2026-05-15",
            s["num_scenarios"],
            s["num_safety_regressions"],
            s["false_allows"],
            s["candidate_pass_rate"],
            s["release_decision"],
        ),
    )

oversight_path = Path("oversight_reliability_study/oversight_failure_results.json")
if oversight_path.exists():
    s = json.loads(oversight_path.read_text())["summary"]
    cur.execute(
        """
        INSERT OR REPLACE INTO oversight_studies
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "oversight_reliability_2026_05",
            s["num_scenarios"],
            s["safety_regressions_present"],
            s["weak_evaluator_false_allows"],
            s["composite_evaluator_false_allows"],
            s["weak_evaluator_regression_recall"],
            s["composite_evaluator_regression_recall"],
            s["evaluator_disagreement_rate"],
        ),
    )

conn.commit()

summary = {}
for table in ["model_registry", "evaluation_runs", "responsible_ai_runs", "oversight_studies"]:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    summary[table] = cur.fetchone()[0]

Path("eval_warehouse/warehouse_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
print(f"Wrote {DB}")
conn.close()
