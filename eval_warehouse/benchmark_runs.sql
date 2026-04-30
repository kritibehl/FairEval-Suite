CREATE TABLE IF NOT EXISTS benchmark_runs (
    run_id TEXT PRIMARY KEY,
    suite_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    dataset_version TEXT,
    avg_score REAL,
    pass_rate REAL,
    failed_case_count INTEGER,
    num_cases INTEGER,
    created_at TEXT
);
