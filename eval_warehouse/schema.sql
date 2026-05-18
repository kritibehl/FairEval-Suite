CREATE TABLE IF NOT EXISTS model_registry (
  model_id TEXT PRIMARY KEY,
  provider TEXT,
  model_type TEXT,
  status TEXT,
  risk_review_required INTEGER
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
  run_id TEXT PRIMARY KEY,
  baseline_model TEXT,
  candidate_model TEXT,
  num_tasks INTEGER,
  regressions_detected INTEGER,
  baseline_avg_score REAL,
  candidate_avg_score REAL,
  latency_ms REAL
);

CREATE TABLE IF NOT EXISTS responsible_ai_runs (
  run_id TEXT PRIMARY KEY,
  num_scenarios INTEGER,
  safety_regressions INTEGER,
  false_allows INTEGER,
  candidate_pass_rate REAL,
  release_decision TEXT
);

CREATE TABLE IF NOT EXISTS oversight_studies (
  study_id TEXT PRIMARY KEY,
  num_scenarios INTEGER,
  safety_regressions_present INTEGER,
  weak_false_allows INTEGER,
  composite_false_allows INTEGER,
  weak_recall REAL,
  composite_recall REAL,
  evaluator_disagreement_rate REAL
);
