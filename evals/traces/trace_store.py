import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

TRACE_DIR = Path("traces")
TRACE_FILE = TRACE_DIR / "events.jsonl"


def append_trace(event: Dict[str, Any]) -> str:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    return str(TRACE_FILE)


def load_traces(limit: int = 100) -> List[Dict[str, Any]]:
    if not TRACE_FILE.exists():
        return []
    rows: List[Dict[str, Any]] = []
    with TRACE_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows[-limit:]
