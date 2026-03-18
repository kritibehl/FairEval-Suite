from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .spec import EvalCase


def load_jsonl_cases(path: str | Path) -> List[EvalCase]:
    p = Path(path)
    cases: List[EvalCase] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(
                EvalCase(
                    id=obj["id"],
                    input=obj["input"],
                    expected=obj.get("expected"),
                    metadata=obj.get("metadata"),
                )
            )
    return cases


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: str | Path, obj: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, default=str)
