CREATE TABLE IF NOT EXISTS regression_cases (
    case_id TEXT PRIMARY KEY,
    category TEXT,
    expected_behavior TEXT,
    regression_type TEXT,
    release_risk TEXT
);
