from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Dict

import pandas as pd

from .io import ensure_dir


def export_bi_views(root: str = ".") -> Dict[str, str]:
    root_path = Path(root)
    db_path = root_path / "artifacts" / "artifact_index.sqlite"
    if not db_path.exists():
        raise RuntimeError(f"artifact index not found: {db_path}")
    export_dir = ensure_dir(root_path / "dashboard_exports")
    conn = sqlite3.connect(str(db_path))
    try:
        runs = pd.read_sql_query("SELECT * FROM run_index ORDER BY created_at", conn)
        compares = pd.read_sql_query("SELECT * FROM compare_index ORDER BY created_at", conn)
        gates = pd.read_sql_query("SELECT * FROM gate_history ORDER BY created_at", conn)
        packs = pd.read_sql_query("SELECT * FROM pack_runs ORDER BY created_at", conn)
    finally:
        conn.close()

    run_csv = export_dir / "runs.csv"
    compare_csv = export_dir / "compares.csv"
    gate_csv = export_dir / "gates.csv"
    pack_csv = export_dir / "pack_runs.csv"
    runs.to_csv(run_csv, index=False)
    compares.to_csv(compare_csv, index=False)
    gates.to_csv(gate_csv, index=False)
    packs.to_csv(pack_csv, index=False)

    dashboard_spec = {
        "tool_targets": ["Power BI", "Tableau", "QuickSight"],
        "recommended_views": [
            "baseline_vs_candidate_avg_score",
            "pass_rate_trends",
            "drift_alerts",
            "rollback_recommendations",
            "regressed_case_counts",
            "benchmark_pack_performance_over_time",
        ],
        "files": {
            "runs": str(run_csv),
            "compares": str(compare_csv),
            "gates": str(gate_csv),
            "pack_runs": str(pack_csv),
        },
    }
    spec_path = export_dir / "dashboard_spec.json"
    spec_path.write_text(json.dumps(dashboard_spec, indent=2), encoding="utf-8")
    return {"runs_csv": str(run_csv), "compares_csv": str(compare_csv), "gates_csv": str(gate_csv), "pack_runs_csv": str(pack_csv), "dashboard_spec": str(spec_path)}
