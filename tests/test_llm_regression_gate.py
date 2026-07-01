import json
from pathlib import Path

BASELINE = {
    "groundedness": 1.0,
    "hallucination_count": 0,
    "decision": "PASS"
}

CANDIDATE = {
    "groundedness": 0.67,
    "hallucination_count": 2,
    "decision": "BLOCK"
}

def test_llm_regression_gate():
    groundedness_drop = BASELINE["groundedness"] - CANDIDATE["groundedness"]
    hallucination_regression = (
        CANDIDATE["hallucination_count"] >
        BASELINE["hallucination_count"]
    )

    release_decision = (
        "BLOCK"
        if groundedness_drop > 0.20 or hallucination_regression
        else "PASS"
    )

    report = {
        "baseline_groundedness": BASELINE["groundedness"],
        "candidate_groundedness": CANDIDATE["groundedness"],
        "groundedness_drop": round(groundedness_drop, 2),
        "hallucination_regression": hallucination_regression,
        "prompt_output_comparison": "candidate introduced unsupported responses",
        "release_decision": release_decision
    }

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/ai_quality_gate_run.json").write_text(
        json.dumps(report, indent=2)
    )

    assert release_decision == "BLOCK"
