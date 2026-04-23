from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
from typing import Any, Dict, List

from .io import load_cases_jsonl
from .scorers.rag_overlap import score_case


def _utc_ts_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def _short_hash(text: str) -> str:
    return sha1(text.encode("utf-8")).hexdigest()[:12]


def _resolve_model(model_name: str):
    name = model_name.lower()

    if name == "mock":
        from .models.mock import MockModelClient
        return MockModelClient()

    if name == "mock_regressed":
        from .models.mock_regressed import MockRegressedModelClient
        return MockRegressedModelClient()

    if name == "distilbert-sst2":
        from .models.distilbert_sst2 import DistilBertSST2ModelClient
        return DistilBertSST2ModelClient()

    if name == "openai_real":
        from .models.real.openai_real import OpenAIRealModelClient
        return OpenAIRealModelClient()

    if name == "gemini_real":
        from .models.real.gemini_real import GeminiRealModelClient
        return GeminiRealModelClient()

    if name == "anthropic_real":
        from .models.real.anthropic_real import AnthropicRealModelClient
        return AnthropicRealModelClient()

    raise ValueError(f"Unknown model: {model_name}")


def _score_one_case(model: Any, case: Dict[str, Any]) -> Dict[str, Any]:
    output = model.generate(case["input"])
    scored = score_case(case, output)

    return {
        "case_id": case["id"],
        "score": scored["score"],
        "passed": scored["passed"],
        "details": scored.get("details", {}),
        "output": output,
    }


def run_suite(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    out_dir: str = ".",
    max_workers: int = 1,
    timeout_seconds: float = 10.0,
) -> Dict[str, Any]:
    del timeout_seconds  # currently unused in local threaded execution

    cases = load_cases_jsonl(dataset_path)
    model = _resolve_model(model_name)

    results: List[Dict[str, Any]] = []

    if max_workers <= 1:
        for case in cases:
            results.append(_score_one_case(model, case))
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(_score_one_case, model, case): case for case in cases}
            for future in as_completed(future_map):
                results.append(future.result())

        results.sort(key=lambda r: r["case_id"])

    num_cases = len(results)
    avg_score = round(sum(r["score"] for r in results) / num_cases, 4) if num_cases else 0.0
    pass_rate = round(sum(1 for r in results if r["passed"]) / num_cases, 4) if num_cases else 0.0

    run_id = f"{_utc_ts_compact()}_{suite_name}_{model_name}_{_short_hash(str(dataset_path))}"

    artifact = {
        "run_id": run_id,
        "config": {
            "suite_name": suite_name,
            "dataset_path": dataset_path,
            "model_name": model_name,
            "max_workers": max_workers,
        },
        "summary": {
            "num_cases": num_cases,
            "avg_score": avg_score,
            "pass_rate": pass_rate,
        },
        "results": results,
    }

    out_root = Path(out_dir)
    reports_dir = out_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_path = reports_dir / f"{run_id}.json"
    report_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    return {
        "run_id": run_id,
        "output_path": str(report_path),
        "summary": artifact["summary"],
    }
