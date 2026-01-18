import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .io import ensure_dir, load_jsonl_cases, write_json
from .models.mock import MockModelClient
from .scorers.rag_overlap import RagOverlapScorer
from .spec import EvalReport, EvalResult, EvalRunConfig


def stable_run_id(suite_name: str, model_name: str, scorer_name: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw = f"{suite_name}|{model_name}|{scorer_name}|{ts}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{ts}_{suite_name}_{model_name}_{h}"


def run_suite(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    scorer_name: str | None = None,
    out_dir: str = ".",
) -> Dict[str, Any]:
    # 1) Load cases (fail fast)
    cases = load_jsonl_cases(dataset_path)
    if len(cases) == 0:
        raise RuntimeError(f"no cases loaded from dataset: {dataset_path}")

    # 2) Model adapter (deterministic mock for now)
    if model_name != "mock":
        raise RuntimeError(f"unsupported model_name={model_name} (v0 only supports mock)")
    model = MockModelClient()

    # 3) Scorer (deterministic RAG grounding proxy)
    scorer = RagOverlapScorer()
    scorer_name = scorer_name or scorer.name

    # 4) Metadata
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

    # 5) Run cases
    for c in cases:
        out_text = model.generate(c.input)

        sr = scorer.score(c.input, c.expected, out_text)

        results.append(
            EvalResult(
                case_id=c.id,
                score=float(sr.score),
                passed=bool(sr.passed),
                details={
                    "scorer": scorer.name,
                    "scorer_details": sr.details,
                    "model_output": out_text,
                },
            )
        )

        outputs.append(
            {
                "case_id": c.id,
                "input": c.input,
                "expected": c.expected,
                "output": out_text,
                "score": float(sr.score),
                "passed": bool(sr.passed),
                "details": sr.details,
            }
        )

    # 6) Summary
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

    # 7) Write artifacts
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
