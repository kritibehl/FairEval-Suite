CREATE TABLE IF NOT EXISTS gate_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compare_artifact_path TEXT,
    decision TEXT NOT NULL,
    release_decision TEXT NOT NULL,
    reason TEXT,
    avg_score_delta REAL,
    pass_rate_delta REAL,
    regressed_case_count INTEGER,
    created_at TEXT
);
