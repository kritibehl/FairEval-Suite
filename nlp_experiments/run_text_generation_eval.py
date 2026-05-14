import json
import time
from pathlib import Path

TASK_PACK = Path("nlp_experiments/text_generation_task_pack.json")
BASELINE = Path("nlp_experiments/model_outputs/baseline_outputs.json")
CANDIDATE = Path("nlp_experiments/model_outputs/candidate_outputs.json")
REPORT_JSON = Path("nlp_experiments/local_model_comparison_report.json")
REPORT_MD = Path("nlp_experiments/local_model_comparison_report.md")


def load_json(path):
    return json.loads(path.read_text())


def safe_json_parse(text):
    try:
        return json.loads(text), True
    except Exception:
        return None, False


def score_output(task, output):
    constraints = task.get("required_constraints", [])
    text = output.lower()

    scores = {
        "instruction_adherence": 1.0,
        "groundedness": 1.0,
        "format_compliance": 1.0,
        "entity_preservation": 1.0,
        "conciseness": 1.0,
    }

    failures = []

    if "exactly_two_bullets" in constraints:
        bullet_count = output.count("- ")
        if bullet_count != 2:
            scores["instruction_adherence"] = 0.0
            scores["format_compliance"] = 0.0
            failures.append("exactly_two_bullets_failed")

    if "valid_json" in constraints:
        parsed, ok = safe_json_parse(output)
        if not ok:
            scores["format_compliance"] = 0.0
            failures.append("invalid_json")
        else:
            if "decision_key" in constraints and "decision" not in parsed:
                scores["entity_preservation"] = 0.0
                failures.append("missing_decision_key")
            if "reason_key" in constraints and "reason" not in parsed:
                scores["entity_preservation"] = 0.0
                failures.append("missing_reason_key")

    if "mention_failed_json_fields" in constraints and "json" not in text:
        scores["entity_preservation"] = 0.0
        failures.append("missing_json_field_reference")

    if "mention_review_before_release" in constraints and "review before release" not in text:
        scores["instruction_adherence"] = 0.0
        failures.append("missing_review_before_release")

    if "grounded_in_context" in constraints:
        if "latency" in text:
            scores["groundedness"] = 0.0
            failures.append("hallucinated_latency_reason")
        if "json fields" not in text and "json field" not in text:
            scores["entity_preservation"] = 0.0
            failures.append("missing_grounded_json_field_reason")

    if "no_new_facts" in constraints and ("unsafe" in text or "would be impacted" in text):
        scores["groundedness"] = 0.0
        failures.append("unsupported_added_detail")

    if "short" in constraints or "concise" in constraints:
        if len(output.split()) > 24:
            scores["conciseness"] = 0.0
            failures.append("too_verbose")

    avg_score = round(sum(scores.values()) / len(scores), 4)

    return {
        "scores": scores,
        "avg_score": avg_score,
        "failures": failures,
        "passed": avg_score >= 0.8 and not failures,
    }


def main():
    task_pack = load_json(TASK_PACK)
    baseline = load_json(BASELINE)
    candidate = load_json(CANDIDATE)

    baseline_outputs = {o["task_id"]: o for o in baseline["outputs"]}
    candidate_outputs = {o["task_id"]: o for o in candidate["outputs"]}

    rows = []

    start = time.perf_counter()

    for task in task_pack["tasks"]:
        task_id = task["task_id"]
        b = baseline_outputs[task_id]["output"]
        c = candidate_outputs[task_id]["output"]

        baseline_eval = score_output(task, b)
        candidate_eval = score_output(task, c)

        rows.append({
            "task_id": task_id,
            "task_type": task["task_type"],
            "baseline_output": b,
            "candidate_output": c,
            "baseline_eval": baseline_eval,
            "candidate_eval": candidate_eval,
            "regression_detected": candidate_eval["avg_score"] < baseline_eval["avg_score"],
            "score_delta": round(candidate_eval["avg_score"] - baseline_eval["avg_score"], 4),
        })

    latency_ms = round((time.perf_counter() - start) * 1000, 4)

    summary = {
        "baseline_model": baseline["model_name"],
        "candidate_model": candidate["model_name"],
        "num_tasks": len(rows),
        "regressions_detected": sum(r["regression_detected"] for r in rows),
        "baseline_avg_score": round(sum(r["baseline_eval"]["avg_score"] for r in rows) / len(rows), 4),
        "candidate_avg_score": round(sum(r["candidate_eval"]["avg_score"] for r in rows) / len(rows), 4),
        "latency_ms": latency_ms,
        "criteria": [
            "instruction_adherence",
            "groundedness",
            "format_compliance",
            "entity_preservation",
            "conciseness"
        ],
        "note": "Local mock-adapter text generation eval; no production model-serving claim."
    }

    report = {
        "summary": summary,
        "results": rows,
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Local Model Comparison Report",
        "",
        "FairEval local text-generation evaluation comparing baseline vs candidate outputs.",
        "",
        "## Summary",
        "",
        f"- baseline model: `{summary['baseline_model']}`",
        f"- candidate model: `{summary['candidate_model']}`",
        f"- tasks evaluated: {summary['num_tasks']}",
        f"- regressions detected: {summary['regressions_detected']}",
        f"- baseline avg score: {summary['baseline_avg_score']}",
        f"- candidate avg score: {summary['candidate_avg_score']}",
        f"- latency_ms: {summary['latency_ms']}",
        "",
        "## Criteria",
        "",
        "- instruction adherence",
        "- groundedness",
        "- format compliance",
        "- entity preservation",
        "- conciseness",
        "",
        "## Task Results",
        "",
        "| Task | Type | Baseline Score | Candidate Score | Delta | Regression | Candidate Failures |",
        "|---|---|---:|---:|---:|---|---|",
    ]

    for r in rows:
        md.append(
            f"| {r['task_id']} | {r['task_type']} | {r['baseline_eval']['avg_score']} | {r['candidate_eval']['avg_score']} | {r['score_delta']} | {r['regression_detected']} | {', '.join(r['candidate_eval']['failures']) or '-'} |"
        )

    md += [
        "",
        "## Safe Scope",
        "",
        "This experiment uses local/mock adapter outputs to demonstrate text-generation evaluation workflows. It does not claim production model serving, transformer training, or fine-tuning.",
    ]

    REPORT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote {REPORT_JSON}")
    print(f"Wrote {REPORT_MD}")


if __name__ == "__main__":
    main()
