CREATE TABLE IF NOT EXISTS models (
  model_id TEXT PRIMARY KEY,
  provider TEXT,
  version TEXT,
  role TEXT
);

CREATE TABLE IF NOT EXISTS prompts (
  prompt_id TEXT PRIMARY KEY,
  prompt_version TEXT,
  task_type TEXT
);

CREATE TABLE IF NOT EXISTS datasets (
  dataset_id TEXT PRIMARY KEY,
  dataset_hash TEXT,
  num_cases INTEGER
);

CREATE TABLE IF NOT EXISTS eval_runs (
  run_id TEXT PRIMARY KEY,
  model_id TEXT,
  prompt_id TEXT,
  dataset_id TEXT,
  timestamp TEXT,
  run_type TEXT
);

CREATE TABLE IF NOT EXISTS scores (
  run_id TEXT,
  metric TEXT,
  value REAL
);

CREATE TABLE IF NOT EXISTS failures (
  run_id TEXT,
  failure_category TEXT,
  count INTEGER
);

CREATE TABLE IF NOT EXISTS release_decisions (
  run_id TEXT PRIMARY KEY,
  decision TEXT,
  reason TEXT
);

CREATE TABLE IF NOT EXISTS cost_latency (
  run_id TEXT PRIMARY KEY,
  p95_latency_ms REAL,
  cost_per_request_usd REAL
);
