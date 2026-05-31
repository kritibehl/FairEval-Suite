import sqlite3
from pathlib import Path

DB = "eval_warehouse/faireval_eval_warehouse.sqlite"
SCHEMA = Path("eval_warehouse/schema.sql").read_text()

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript(SCHEMA)

cur.execute("INSERT OR REPLACE INTO models VALUES (?, ?, ?, ?)",
            ("candidate_mock_adapter", "local_mock", "2026.05", "candidate"))

cur.execute("INSERT OR REPLACE INTO prompts VALUES (?, ?, ?)",
            ("prompt-retail-rag-v1", "v1", "retail_rag_grounding"))

cur.execute("INSERT OR REPLACE INTO datasets VALUES (?, ?, ?)",
            ("retail_product_discovery_v1", "synthetic-retail-v1", 3))

cur.execute("INSERT OR REPLACE INTO eval_runs VALUES (?, ?, ?, ?, datetime('now'), ?)",
            ("eval-run-retail-candidate-001", "candidate_mock_adapter", "prompt-retail-rag-v1",
             "retail_product_discovery_v1", "baseline_vs_candidate"))

for metric, value in [
    ("precision_at_3", 0.6667),
    ("recall_at_3", 1.0),
    ("ndcg_at_3", 0.7688),
    ("groundedness_pass_rate", 1.0),
]:
    cur.execute("INSERT INTO scores VALUES (?, ?, ?)",
                ("eval-run-retail-candidate-001", metric, value))

for category, count in [
    ("ranking_regression", 2),
    ("irrelevant_recommendations", 3),
]:
    cur.execute("INSERT INTO failures VALUES (?, ?, ?)",
                ("eval-run-retail-candidate-001", category, count))

cur.execute("INSERT OR REPLACE INTO release_decisions VALUES (?, ?, ?)",
            ("eval-run-retail-candidate-001", "block_candidate",
             "Candidate reduced NDCG@3 and introduced ranking regressions."))

cur.execute("INSERT OR REPLACE INTO cost_latency VALUES (?, ?, ?)",
            ("eval-run-retail-candidate-001", 950.0, 0.012))

conn.commit()
conn.close()

print("Ingested eval-run-retail-candidate-001")
