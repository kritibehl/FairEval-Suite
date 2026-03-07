import hashlib
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .io import ensure_dir, load_jsonl_cases, write_json
from .models.mock import MockModelClient
from .scorers.rag_overlap import RagOverlapScorer
from .spec import EvalReport, EvalResult, EvalRunConfig


def stable_run_id(suite_name: str, model_name: str, scorer_name: str, dataset_path: str) -> str:
    # High-resolution timestamp so two runs in the same second don't collide
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")

    # Stable fingerprint of "what was evaluated" (helps debugging + compare)
    raw = f"{suite_name}|{model_name}|{scorer_name}|{dataset_path}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    # Keep readable + unique
    return f"{ts}_{suite_name}_{model_name}_{h}"


def run_suite(
    suite_name: str,
    dataset_path: str,
    model_name: str = "mock",
    scorer_name: str | None = None,
    out_dir: str = ".",
    max_workers: int = 4,
    timeout_seconds: float = 10.0,
) -> Dict[str, Any]:
    # 1) Load cases (fail fast)
    cases = load_jsonl_cases(dataset_path)
    if len(cases) == 0:
        raise RuntimeError(f"no cases loaded from dataset: {dataset_path}")

    # 2) Model adapter (deterministic mock for now)
    if model_name != "mock":
        raise RuntimeError(f"unsupported model_name={model_name} (v0 only supports mock)")
    model = MockModelClient()

    # 3) Scorer
    scorer = RagOverlapScorer()
    scorer_name = scorer_name or scorer.name

    # 4) Metadata
    run_id = stable_run_id(suite_name, model_name, scorer_name, dataset_path)
    created_at = datetime.now(timezone.utc)
    config = EvalRunConfig(
        suite_name=suite_name,
        model_name=model_name,
        scorer_name=scorer_name,
        created_at=created_at,
    )

    # --- parallel worker fn ---
    def process_case(idx: int, c) -> Tuple[int, EvalResult, Dict[str, Any]]:
        case_input = dict(c.input or {})
        expected_keywords = (c.expected or {}).get("answer_contains", []) or []
        case_input["expected_keywords"] = expected_keywords

        out_text = model.generate(case_input)

        # scorer signature: score(input, expected, output_text)
        sr = scorer.score(c.input, c.expected, out_text)

        result = EvalResult(
            case_id=c.id,
            score=float(sr.score),
            passed=bool(sr.passed),
            details={
                "scorer": scorer.name,
                "scorer_details": sr.details,
                "model_output": out_text,
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
        }

        return idx, result, output_row

    # 5) Run cases (bounded parallel + deterministic ordering)
    indexed_results: List[EvalResult | None] = [None] * len(cases)
    indexed_outputs: List[Dict[str, Any] | None] = [None] * len(cases)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_to_idx = {ex.submit(process_case, i, c): i for i, c in enumerate(cases)}

        # Iterate in submission order to keep behavior stable; we still place into index
        for fut, idx in future_to_idx.items():
            try:
                i, result, output_row = fut.result(timeout=timeout_seconds)
                indexed_results[i] = result
                indexed_outputs[i] = output_row

            except FuturesTimeoutError:
                case_id = cases[idx].id
                timeout_detail = {
                    "error": "timeout",
                    "timeout_seconds": timeout_seconds,
                }

                indexed_results[idx] = EvalResult(
                    case_id=case_id,
                    score=0.0,
                    passed=False,
                    details={
                        "scorer": scorer.name,
                        "scorer_details": timeout_detail,
                        "model_output": None,
                    },
                )

                indexed_outputs[idx] = {
                    "case_id": case_id,
                    "input": cases[idx].input,
                    "expected": cases[idx].expected,
                    "output": None,
                    "score": 0.0,
                    "passed": False,
                    "details": timeout_detail,
                }

            except Exception as e:
                case_id = cases[idx].id
                err_detail = {"error": "exception", "message": str(e)}

                indexed_results[idx] = EvalResult(
                    case_id=case_id,
                    score=0.0,
                    passed=False,
                    details={
                        "scorer": scorer.name,
                        "scorer_details": err_detail,
                        "model_output": None,
                    },
                )

                indexed_outputs[idx] = {
                    "case_id": case_id,
                    "input": cases[idx].input,
                    "expected": cases[idx].expected,
                    "output": None,
                    "score": 0.0,
                    "passed": False,
                    "details": err_detail,
                }

    results: List[EvalResult] = [r for r in indexed_results if r is not None]
    outputs: List[Dict[str, Any]] = [o for o in indexed_outputs if o is not None]

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
