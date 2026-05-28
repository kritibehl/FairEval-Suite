# Real Provider Benchmark Leaderboard

Status: **Framework ready; successful provider-output run pending API credits**

This benchmark framework is designed to run configured providers on the same prompts and evaluate:

- groundedness
- instruction following
- hallucination risk
- latency
- release-readiness

## Current status

A Gemini API key was accepted, but the provider returned `RESOURCE_EXHAUSTED` because prepaid credits were depleted.

No successful model-output benchmark results should be claimed from this run.

## What is implemented

- shared benchmark prompts
- provider API runner
- raw prompt/response storage
- scoring logic
- leaderboard generation
- error capture
- latency capture
- release-decision logic
- provider failure reporting

## Safe scope

This is currently a real-provider benchmark framework. It becomes a real benchmark only after configured providers return successful model responses.
