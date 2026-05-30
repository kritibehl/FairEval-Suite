# Dataset Hash and Prompt Version Examples

Example lineage artifact:

```json
{
  "run_id": "20260415T203654.860666Z_benchmark_instruction_following_openai_real_b75a5c833044",
  "parent_run_id": null,
  "model_name": "openai_real",
  "model_version": "unknown",
  "prompt_version": "prompt_v1",
  "dataset_hash": "sha256:<computed-dataset-hash>",
  "evaluator_version": "rag_overlap_v1",
  "threshold_version": "release_gate_v1",
  "timestamp": "2026-04-15T20:36:54Z"
}
FairEval records these fields so benchmark results can be reproduced, compared, and audited across model releases.
