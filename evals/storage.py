from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .io import ensure_dir


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS run_index (
    run_id TEXT PRIMARY KEY,
    suite_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    scorer_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    dataset_path TEXT,
    avg_score REAL,
    pass_rate REAL,
    num_cases INTEGER,
    integrity_status TEXT,
    run_artifact_path TEXT,
    report_artifact_path TEXT
);
CREATE TABLE IF NOT EXISTS gate_history (
    gate_id TEXT PRIMARY KEY,
    compare_artifact_path TEXT NOT NULL,
    decision TEXT NOT NULL,
    created_at TEXT NOT NULL,
    avg_score_delta REAL,
    pass_rate_delta REAL,
    regressed_case_count INTEGER,
    rollback_recommendation TEXT,
    gate_artifact_path TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS compare_index (
    compare_id TEXT PRIMARY KEY,
    baseline_run_id TEXT,
    candidate_run_id TEXT,
    created_at TEXT NOT NULL,
    avg_score_delta REAL,
    pass_rate_delta REAL,
    regressed_case_count INTEGER,
    drift_alert TEXT,
    compare_artifact_path TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pack_runs (
    pack_run_id TEXT PRIMARY KEY,
    suite_name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    repeat_count INTEGER NOT NULL,
    avg_score_mean REAL,
    avg_score_ci_low REAL,
    avg_score_ci_high REAL,
    pass_rate_mean REAL,
    pass_rate_ci_low REAL,
    pass_rate_ci_high REAL,
    pack_artifact_path TEXT NOT NULL
);
"""


class ArtifactStore:
    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root)
        self.db_path = self.root / "artifacts" / "artifact_index.sqlite"
        ensure_dir(self.db_path.parent)
        self._init_db()
        self.trace_path = self.root / "artifacts" / "trace_metadata.jsonl"

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def append_trace(self, record: Dict[str, Any]) -> None:
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        with self.trace_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def index_run(self, record: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO run_index (
                    run_id, suite_name, model_name, scorer_name, created_at, dataset_path,
                    avg_score, pass_rate, num_cases, integrity_status, run_artifact_path, report_artifact_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["run_id"],
                    record["suite_name"],
                    record["model_name"],
                    record["scorer_name"],
                    record["created_at"],
                    record.get("dataset_path"),
                    record.get("avg_score"),
                    record.get("pass_rate"),
                    record.get("num_cases"),
                    record.get("integrity_status"),
                    record.get("run_artifact_path"),
                    record.get("report_artifact_path"),
                ),
            )
            conn.commit()

    def index_compare(self, record: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO compare_index (
                    compare_id, baseline_run_id, candidate_run_id, created_at,
                    avg_score_delta, pass_rate_delta, regressed_case_count, drift_alert, compare_artifact_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["compare_id"],
                    record.get("baseline_run_id"),
                    record.get("candidate_run_id"),
                    record["created_at"],
                    record.get("avg_score_delta"),
                    record.get("pass_rate_delta"),
                    record.get("regressed_case_count"),
                    record.get("drift_alert"),
                    record["compare_artifact_path"],
                ),
            )
            conn.commit()

    def index_gate(self, record: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO gate_history (
                    gate_id, compare_artifact_path, decision, created_at, avg_score_delta,
                    pass_rate_delta, regressed_case_count, rollback_recommendation, gate_artifact_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["gate_id"],
                    record["compare_artifact_path"],
                    record["decision"],
                    record["created_at"],
                    record.get("avg_score_delta"),
                    record.get("pass_rate_delta"),
                    record.get("regressed_case_count"),
                    record.get("rollback_recommendation"),
                    record["gate_artifact_path"],
                ),
            )
            conn.commit()

    def index_pack_run(self, record: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO pack_runs (
                    pack_run_id, suite_name, model_name, created_at, repeat_count,
                    avg_score_mean, avg_score_ci_low, avg_score_ci_high,
                    pass_rate_mean, pass_rate_ci_low, pass_rate_ci_high,
                    pack_artifact_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["pack_run_id"],
                    record["suite_name"],
                    record["model_name"],
                    record["created_at"],
                    record["repeat_count"],
                    record.get("avg_score_mean"),
                    record.get("avg_score_ci_low"),
                    record.get("avg_score_ci_high"),
                    record.get("pass_rate_mean"),
                    record.get("pass_rate_ci_low"),
                    record.get("pass_rate_ci_high"),
                    record["pack_artifact_path"],
                ),
            )
            conn.commit()
