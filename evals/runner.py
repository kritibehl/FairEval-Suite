import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .io import ensure_dir, load_jsonl_cases, write_json
from .spec import EvalReport, EvalResult, EvalRunConfig
from .models.mock import MockModelClient


def stable_run_id(suite_name: str, model_name: str, scorer_name: str) -> str:
    # Deterministic-ish id: includes timestamp but hashed for nice shortness
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw = f"{suite_name}|{model_name}|{scorer_name}|{ts}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{ts}_{suite_name}_{model_name}_{h}"


def mock_generate(case_input: Dict[str, Any]) -> str:
    """
    Deterministic 'model' response for v1 plumbing.
    We will replace with real model adapters in Commit 6.
    """
    prompt = case_input.get("prompt", "")
    context = case_input.get("context", [])
    # Deterministic response: echo a small summary-like string.
    return f"{prompt} | ctx_items={len(context)}"


def score_contains(expected: Dict[str, Any] | None, output_text: str) -> Dict[str, Any]:
    """
    Minimal v1 scoring: check 'answer_contains' substrings.
    Returns score in [0,1] with details.
    """
    if not expected:
        return {"score": 0.0, "passed": False, "hits": 0, "total": 0}

    needles = expected.get("answer_contains") or []
    if not isinstance(needles, list) or len(needles) == 0:
        return {"score": 0.0, "passed": False, "hits": 0, "total": 0}

    hits = 0
    lowered = output_text.lower()
    for n in needles:
        if isinstance(n, str) and n.lower() in lowered:
            hits += 1

    score = hits / len(needles)
    passed = score == 1.0
    return {"score": score, "passed": passed, "hits": hits, "total": len(needles)}


def run_suite(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    scorer_name: str = "contains_v1",
    out_dir: str = ".",
) -> Dict[str, Any]:
    cases = load_jsonl_cases(dataset_path)

    run_id = stable_run_id(suite_name, model_name, scorer_name)
    created_at = datetime.now(timezone.utc)

    config = EvalRunConfig(
        suite_name=suite_name,
        model_name=model_name,
        scorer_name=scorer_name,
        created_at=created_at,
    )

    results: List[EvalResult] = []
    outputs: List[Dict[str, Any]] = []

    for c in cases:
        out_text = mock_generate(c.input)
        score_info = score_contains(c.expected, out_text)

        results.append(
            EvalResult(
                case_id=c.id,
                score=float(score_info["score"]),
                passed=bool(score_info["passed"]),
                details={
                    "model_output": out_text,
                    "score_info": score_info,
                },
            )
        )

        outputs.append(
            {
                "case_id": c.id,
                "input": c.input,
                "expected": c.expected,
                "output": out_text,
                "score": float(score_info["score"]),
                "passed": bool(score_info["passed"]),
            }
        )

    avg_score = sum(r.score for r in results) / max(1, len(results))
    pass_rate = sum(1 for r in results if r.passed) / max(1, len(results))

    report = EvalReport(
        run_id=run_id,
        config=config,
        results=results,
        summary={
            "num_cases": len(results),
            "avg_score": round(avg_score, 4),
            "pass_rate": round(pass_rate, 4),
        },
    )

    root = Path(out_dir)
    runs_dir = ensure_dir(root / "runs")
    reports_dir = ensure_dir(root / "reports")

    run_artifact = {
        "run_id": run_id,
        "config": asdict(config),
        "cases": outputs,
    }

    report_artifact = {
        "run_id": run_id,
        "config": asdict(config),
        "summary": report.summary,
        "results": [
            {
                "case_id": r.case_id,
                "score": r.score,
                "passed": r.passed,
                "details": r.details,
            }
            for r in results
        ],
    }

    write_json(runs_dir / f"{run_id}.json", run_artifact)
    write_json(reports_dir / f"{run_id}.json", report_artifact)

    return {"run_id": run_id, **report.summary}
