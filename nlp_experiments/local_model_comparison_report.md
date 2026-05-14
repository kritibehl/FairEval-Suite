# Local Model Comparison Report

FairEval local text-generation evaluation comparing baseline vs candidate outputs.

## Summary

- baseline model: `baseline_mock_adapter`
- candidate model: `candidate_mock_adapter`
- tasks evaluated: 6
- regressions detected: 6
- baseline avg score: 1.0
- candidate avg score: 0.7
- latency_ms: 0.0651

## Criteria

- instruction adherence
- groundedness
- format compliance
- entity preservation
- conciseness

## Task Results

| Task | Type | Baseline Score | Candidate Score | Delta | Regression | Candidate Failures |
|---|---|---:|---:|---:|---|---|
| tg-001 | rewrite_for_clarity | 1.0 | 0.8 | -0.2 | True | unsupported_added_detail |
| tg-002 | summarization | 1.0 | 0.6 | -0.4 | True | missing_json_field_reference, missing_review_before_release |
| tg-003 | smart_reply_style_generation | 1.0 | 0.8 | -0.2 | True | too_verbose |
| tg-004 | instruction_following | 1.0 | 0.6 | -0.4 | True | exactly_two_bullets_failed |
| tg-005 | constrained_formatting | 1.0 | 0.8 | -0.2 | True | missing_reason_key |
| tg-006 | grounded_answer_generation | 1.0 | 0.6 | -0.4 | True | hallucinated_latency_reason, missing_grounded_json_field_reason |

## Safe Scope

This experiment uses local/mock adapter outputs to demonstrate text-generation evaluation workflows. It does not claim production model serving, transformer training, or fine-tuning.
