from pathlib import Path
import importlib.util


MODULE_PATH = Path("multimodal_evals/video_temporal_consistency/evaluate_video_consistency.py")


def load_module():
    spec = importlib.util.spec_from_file_location("evaluate_video_consistency", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_video_eval_detects_temporal_and_grounding_regressions():
    module = load_module()

    task_pack = module.load_json(Path("multimodal_evals/video_temporal_consistency/video_task_pack.json"))
    candidate_outputs = module.load_json(Path("multimodal_evals/video_temporal_consistency/candidate_outputs.json"))

    summary = module.evaluate(task_pack, candidate_outputs)

    assert summary["tasks_evaluated"] == 3
    assert summary["average_temporal_consistency"] < 1.0
    assert summary["total_hallucinated_objects"] >= 1
    assert summary["review_required"] >= 1
    assert any(result["decision"] == "review" for result in summary["results"])
