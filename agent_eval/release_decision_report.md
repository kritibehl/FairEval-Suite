# Agent Evaluation Release Decision Report

## Scope
Synthetic agent evaluation for:
- tool selection correctness
- tool argument correctness
- retrieval quality
- grounded tool results
- unsupported action detection
- human-review routing
- release-readiness decision

## Results
See:
- `retrieval_quality_results.json`
- `unsupported_action_results.json`

## Release decision logic
A candidate agent workflow should be reviewed or blocked when:
- tool selection accuracy drops
- tool arguments are incorrect
- tool result is ungrounded
- unsupported tool action is attempted
- blocked release approval is attempted without human review

## Apple ML alignment
This maps to GenAI workflow evaluation, production ML solution quality, continuous improvement, release safety, and user-facing correctness.

## Safe scope
This is a synthetic agent-evaluation pack. It does not claim production agent monitoring or Apple internal system behavior.
