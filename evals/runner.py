from __future__ import annotations

from evals.models.mock import MockModelClient
from evals.models.mock_regressed import MockRegressedModelClient

import hashlib
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .integrity import validate_cases
from .io import ensure_dir, load_jsonl_cases, write_json
from .models.mock import MockModelClient
from .scorers.classification_label import ClassificationLabelScorer
from .scorers.rag_overlap import RagOverlapScorer
from .spec import EvalReport, EvalResult, EvalRunConfig
from .storage import ArtifactStore


def stable_run_id(suite_name: str, model_name: str, scorer_name: str, dataset_path: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    raw = f"{suite_name}|{model_name}|{scorer_name}|{dataset_path}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{ts}_{suite_name}_{model_name}_{h}"


def _resolve_model(model_name: str):
    if model_name == "mock":
        return MockModelClient()
    if model_name == "mock_regressed":
        return MockRegressedModelClient()
    raise RuntimeError(f"unsupported model_name={model_name}")


def _resolve_scorer(suite_name: str, scorer_name: str | None):
    if scorer_name:
        if scorer_name == "rag_overlap_v1":
            return RagOverlapScorer()
        if scorer_name == "classification_label_v1":
            return ClassificationLabelScorer()
        raise RuntimeError(f"unsupported scorer_name={scorer_name}")
    if suite_name == "classification_basic":
        return ClassificationLabelScorer()
    return RagOverlapScorer()


def run_suite(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    scorer_name: str | None = None,
    out_dir: str = ".",
    max_workers: int = 4,
    timeout_seconds: float = 10.0,
) -> Dict[str, Any]:
    cases = load_jsonl_cases(dataset_path)
    if len(cases) == 0:
        raise RuntimeError(f"no cases loaded from dataset: {dataset_path}")

    integrity = validate_cases(cases)
    if integrity["status"] == "fail":
        raise RuntimeError(f"dataset integrity check failed: {integrity}")

    model = _resolve_model(model_name)
    scorer = _resolve_scorer(suite_name, scorer_name)
    scorer_name = scorer.name
    run_id = stable_run_id(suite_name, model_name, scorer_name, dataset_path)
    created_at = datetime.now(timezone.utc)
    config = EvalRunConfig(
        suite_name=suite_name,
        model_name=model_name,
        scorer_name=scorer_name,
        created_at=created_at,
    )

    def process_case(idx: int, c) -> Tuple[int, EvalResult, Dict[str, Any]]:
        case_input = dict(c.input or {})
        expected_keywords = (c.expected or {}).get("answer_contains", []) or []
        case_input["expected_keywords"] = expected_keywords
        out_text = model.generate(case_input)
        sr = scorer.score(c.input, c.expected, out_text)
        result = EvalResult(
            case_id=c.id,
            score=float(sr.score),
            passed=bool(sr.passed),
            details={
                "scorer": scorer.name,
                "scorer_details": sr.details,
                "model_output": out_text,
                "metadata": c.metadata or {},
            },
        )
        output_row = {
            "case_id": c.id,
            "input": c.input,
            "expected": c.expected,
            "output": out_text,
            "score": float(sr.score),
            "passed": bool(sr.passed),
            "details": sr.details,
            "metadata": c.metadata or {},
        }
        return idx, result, output_row

    indexed_results: List[EvalResult | None] = [None] * len(cases)
    indexed_outputs: List[Dict[str, Any] | None] = [None] * len(cases)

    if max_workers <= 1:
        for i, c in enumerate(cases):
            try:
                _, result, output_row = process_case(i, c)
                indexed_results[i] = result
                indexed_outputs[i] = output_row
            except Exception as e:
                err_detail = {"error": "exception", "message": str(e)}
                indexed_results[i] = EvalResult(case_id=c.id, score=0.0, passed=False, details=err_detail)
                indexed_outputs[i] = {
                    "case_id": c.id,
                    "input": c.input,
                    "expected": c.expected,
                    "output": None,
                    "score": 0.0,
                    "passed": False,
                    "details": err_detail,
                    "metadata": c.metadata or {},
                }
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            future_to_idx = {ex.submit(process_case, i, c): i for i, c in enumerate(cases)}
            for fut, idx in future_to_idx.items():
                try:
                    i, result, output_row = fut.result(timeout=timeout_seconds)
                    indexed_results[i] = result
                    indexed_outputs[i] = output_row
                except FuturesTimeoutError:
                    c = cases[idx]
                    timeout_detail = {"error": "timeout", "timeout_seconds": timeout_seconds}
                    indexed_results[idx] = EvalResult(case_id=c.id, score=0.0, passed=False, details=timeout_detail)
                    indexed_outputs[idx] = {
                        "case_id": c.id,
                        "input": c.input,
                        "expected": c.expected,
                        "output": None,
                        "score": 0.0,
                        "passed": False,
                        "details": timeout_detail,
                        "metadata": c.metadata or {},
                    }
                except Exception as e:
                    c = cases[idx]
                    err_detail = {"error": "exception", "message": str(e)}
                    indexed_results[idx] = EvalResult(case_id=c.id, score=0.0, passed=False, details=err_detail)
                    indexed_outputs[idx] = {
                        "case_id": c.id,
                        "input": c.input,
                        "expected": c.expected,
                        "output": None,
                        "score": 0.0,
                        "passed": False,
                        "details": err_detail,
                        "metadata": c.metadata or {},
                    }

    results: List[EvalResult] = [r for r in indexed_results if r is not None]
    outputs: List[Dict[str, Any]] = [o for o in indexed_outputs if o is not None]
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
            "failed_case_count": sum(1 for r in results if not r.passed),
        },
    )

    root = Path(out_dir)
    runs_dir = ensure_dir(root / "runs")
    reports_dir = ensure_dir(root / "reports")
    run_artifact = {
        "run_id": run_id,
        "config": asdict(config),
        "cases": outputs,
        "integrity": integrity,
    }
    report_artifact = {
        "run_id": run_id,
        "config": asdict(config),
        "summary": report.summary,
        "integrity": integrity,
        "results": [
            {"case_id": r.case_id, "score": r.score, "passed": r.passed, "details": r.details}
            for r in results
        ],
    }
    run_path = runs_dir / f"{run_id}.json"
    report_path = reports_dir / f"{run_id}.json"
    write_json(run_path, run_artifact)
    write_json(report_path, report_artifact)

    store = ArtifactStore(root)
    store.index_run(
        {
            "run_id": run_id,
            "suite_name": suite_name,
            "model_name": model_name,
            "scorer_name": scorer_name,
            "created_at": created_at.isoformat(),
            "dataset_path": dataset_path,
            "avg_score": report.summary["avg_score"],
            "pass_rate": report.summary["pass_rate"],
            "num_cases": report.summary["num_cases"],
            "integrity_status": integrity["status"],
            "run_artifact_path": str(run_path),
            "report_artifact_path": str(report_path),
        }
    )
    for row in outputs:
        store.append_trace(
            {
                "record_type": "trace_event",
                "run_id": run_id,
                "suite_name": suite_name,
                "model_name": model_name,
                "case_id": row["case_id"],
                "score": row["score"],
                "passed": row["passed"],
                "response_preview": str(row.get("output") or "")[:160],
                "metadata": row.get("metadata") or {},
            }
        )

    return {"run_id": run_id, **report.summary, "integrity": integrity}