# Real Provider Benchmark Leaderboard

This benchmark runs configured providers on the same prompts and evaluates groundedness, instruction-following, hallucination risk, and latency.

## Safe scope

Real provider API outputs were generated only for providers with configured API keys. Raw prompts and responses are stored for auditability.

## Leaderboard

| Rank | Provider | Model | Avg Score | Groundedness Pass | Instruction Pass | Hallucinations | Avg Latency ms | Errors | Decision |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Google Gemini | gemini-2.5-flash | 0.0 | 0.0 | 0.0 | 0 | 571.9238 | 3 | block |

## Raw artifacts

- `real_provider_benchmark/raw_provider_outputs.json`
- `real_provider_benchmark/scored_provider_outputs.json`
