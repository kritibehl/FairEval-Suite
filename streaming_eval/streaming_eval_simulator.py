import json
import time
from pathlib import Path

events = [
    {"event_type": "eval_started", "run_id": "demo_stream_run", "model": "gemini_real"},
    {"event_type": "case_scored", "case_id": "if-001", "score": 1.0, "passed": True},
    {"event_type": "case_scored", "case_id": "if-002", "score": 0.67, "passed": True},
    {"event_type": "case_scored", "case_id": "if-003", "score": 0.0, "passed": False},
    {"event_type": "gate_decision", "decision": "review_before_release", "reason": "failed_cases_detected"},
]

out = Path("streaming_eval/sample_stream_events.jsonl")
with out.open("w") as f:
    for event in events:
        f.write(json.dumps(event) + "\n")
        time.sleep(0.01)

summary = {
    "event_count": len(events),
    "output": str(out),
    "note": "Streaming eval simulation only; not a production streaming inference system.",
}

Path("streaming_eval/stream_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
