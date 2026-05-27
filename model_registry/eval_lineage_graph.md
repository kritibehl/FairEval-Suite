# Evaluation Lineage Graph

```text
baseline_mock_adapter@2026.05
        ↓
candidate_mock_adapter@2026.05
        ↓
text_generation_eval_v1
        ↓
responsible_ai_red_team_v1
        ↓
rag_groundedness_eval_v1
        ↓
agentic_release_gate_v1
        ↓
release_decision = block
        ↓
rollback_candidate = baseline_mock_adapter@2026.05
What this tracks
model versions
candidate vs baseline comparison
regression evidence
release decision
rollback candidate
Safe scope

This is lightweight evaluation lineage metadata, not a production ML model registry or deployment control plane.
