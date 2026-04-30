CREATE TABLE IF NOT EXISTS model_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    score REAL NOT NULL,
    passed BOOLEAN NOT NULL,
    model_output TEXT,
    scorer TEXT,
    FOREIGN KEY(run_id) REFERENCES benchmark_runs(run_id)
);
