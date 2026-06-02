import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT.parent / "reports"


def load_json(path: Path):
    return json.loads(path.read_text())


def object_persistence_score(expected_objects, predicted_objects_by_frame):
    total = 0
    matched = 0

    for obj in expected_objects:
        for frame_objects in predicted_objects_by_frame:
            total += 1
            if obj in frame_objects:
                matched += 1

    return matched / total if total else 1.0


def hallucinated_object_count(task_frames, predicted_objects_by_frame):
    allowed = set()
    for frame in task_frames:
        allowed.update(frame["objects"])

    hallucinations = 0
    for frame_objects in predicted_objects_by_frame:
        hallucinations += sum(1 for obj in frame_objects if obj not in allowed)

    return hallucinations


def action_sequence_score(expected_sequence, predicted_sequence):
    total = max(len(expected_sequence), len(predicted_sequence))
    if total == 0:
        return 1.0

    matched = sum(
        1
        for expected, predicted in zip(expected_sequence, predicted_sequence)
        if expected == predicted
    )
    return matched / total


def caption_grounding_score(reference_caption, candidate_caption, expected_objects):
    candidate = candidate_caption.lower()
    hits = sum(1 for obj in expected_objects if obj.replace("_", " ") in candidate or obj in candidate)
    return hits / len(expected_objects) if expected_objects else 1.0


def evaluate(task_pack, candidate_outputs):
    tasks_by_id = {task["task_id"]: task for task in task_pack["tasks"]}
    results = []

    for output in candidate_outputs["outputs"]:
        task = tasks_by_id[output["task_id"]]

        object_score = object_persistence_score(
            task["expected_objects"],
            output["predicted_objects_by_frame"],
        )
        hallucinations = hallucinated_object_count(
            task["frames"],
            output["predicted_objects_by_frame"],
        )
        action_score = action_sequence_score(
            task["expected_action_sequence"],
            output["predicted_action_sequence"],
        )
        caption_score = caption_grounding_score(
            task["reference_caption"],
            output["caption"],
            task["expected_objects"],
        )

        temporal_consistency = round((object_score + action_score) / 2, 3)
        overall_score = round(
            (object_score * 0.35)
            + (action_score * 0.35)
            + (caption_score * 0.2)
            + ((1 if hallucinations == 0 else 0) * 0.1),
            3,
        )

        results.append(
            {
                "task_id": output["task_id"],
                "domain": task["domain"],
                "object_persistence": round(object_score, 3),
                "action_consistency": round(action_score, 3),
                "caption_grounding": round(caption_score, 3),
                "temporal_consistency": temporal_consistency,
                "hallucinated_objects": hallucinations,
                "overall_score": overall_score,
                "decision": "pass" if overall_score >= 0.85 and hallucinations == 0 else "review",
            }
        )

    summary = {
        "model_name": candidate_outputs["model_name"],
        "tasks_evaluated": len(results),
        "average_object_persistence": round(sum(r["object_persistence"] for r in results) / len(results), 3),
        "average_action_consistency": round(sum(r["action_consistency"] for r in results) / len(results), 3),
        "average_caption_grounding": round(sum(r["caption_grounding"] for r in results) / len(results), 3),
        "average_temporal_consistency": round(sum(r["temporal_consistency"] for r in results) / len(results), 3),
        "total_hallucinated_objects": sum(r["hallucinated_objects"] for r in results),
        "review_required": sum(1 for r in results if r["decision"] == "review"),
        "results": results,
    }

    return summary


def build_report(summary):
    lines = [
        "# Multimodal Video Evaluation Report",
        "",
        "## Purpose",
        "",
        "This evaluation pack measures video-style model behavior across temporal consistency, object persistence, action continuity, caption grounding, and hallucinated visual entities.",
        "",
        "## Summary",
        "",
        f"- Model: `{summary['model_name']}`",
        f"- Tasks evaluated: {summary['tasks_evaluated']}",
        f"- Average temporal consistency: {summary['average_temporal_consistency']}",
        f"- Average object persistence: {summary['average_object_persistence']}",
        f"- Average action consistency: {summary['average_action_consistency']}",
        f"- Average caption grounding: {summary['average_caption_grounding']}",
        f"- Hallucinated objects: {summary['total_hallucinated_objects']}",
        f"- Review required: {summary['review_required']}",
        "",
        "## Task Results",
        "",
        "| Task | Domain | Temporal | Object Persistence | Action | Caption | Hallucinations | Decision |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]

    for r in summary["results"]:
        lines.append(
            f"| {r['task_id']} | {r['domain']} | {r['temporal_consistency']} | "
            f"{r['object_persistence']} | {r['action_consistency']} | "
            f"{r['caption_grounding']} | {r['hallucinated_objects']} | {r['decision']} |"
        )

    lines.extend(
        [
            "",
            "## Safe Scope",
            "",
            "This is a synthetic evaluation harness for multimodal/video model behavior. It does not claim production robotics deployment, real robot control, or large-scale video foundation model training.",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    task_pack = load_json(ROOT / "video_task_pack.json")
    candidate_outputs = load_json(ROOT / "candidate_outputs.json")

    summary = evaluate(task_pack, candidate_outputs)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "video_eval_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (REPORT_DIR / "video_eval_report.md").write_text(build_report(summary))

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
