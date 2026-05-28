# Real Provider Benchmark Leaderboard

Status: **Not yet run successfully**

This benchmark framework is designed to run OpenAI, Anthropic, and Gemini on the same prompts and evaluate:

- groundedness
- instruction following
- hallucination risk
- latency
- release-readiness

## Current status

The first attempted run used placeholder API keys and produced authentication errors for all providers.

No model-output benchmark results should be claimed from this run.

## What is implemented

- shared benchmark prompts
- provider API runner
- raw prompt/response storage
- scoring logic
- leaderboard generation
- error capture
- latency capture
- release-decision logic

## Safe scope

This is currently a real-provider benchmark framework. It becomes a real benchmark only after valid provider API keys produce successful model responses.
