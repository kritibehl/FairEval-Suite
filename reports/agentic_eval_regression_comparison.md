# Agentic Evaluation Regression Comparison Report

FairEval now includes release-safety checks for agentic and RAG-style workflows.

## Evaluated risks
- RAG groundedness failure
- hallucinated / unsupported answer
- missing expected context terms
- p95 latency threshold breach
- cost/request threshold breach
- release-gate failure aggregation

## Inputs
- `agent_eval_packs/agent_eval_scenarios.json`
- `rag_groundedness_eval/rag_groundedness_report.json`
- `latency_cost_eval/latency_cost_gate_report.json`
- `safety_release_gate/agentic_release_gate_summary.json`

## Safe scope
This is a synthetic evaluation pipeline for agentic release-safety review. It is not a production agent monitoring system.
