import json
from pathlib import Path
from typing import Any, Dict


def load_pack(name: str) -> Dict[str, Any]:
    path = Path("benchmark_packs") / name / "pack.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
