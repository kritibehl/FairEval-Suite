# Real Provider Benchmark Leaderboard

This benchmark runs configured providers on the same prompts and evaluates groundedness, instruction-following, hallucination risk, and latency.

## Safe scope

Real provider API outputs were generated only for providers with configured API keys. Raw prompts and responses are stored for auditability.

## Leaderboard

| Rank | Provider | Model | Avg Score | Groundedness Pass | Instruction Pass | Hallucinations | Avg Latency ms | Errors | Decision |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | OpenAI | gpt-4o-mini | 0.0 | 0.0 | 0.0 | 0 | 658.3086 | 3 | block |
| 2 | Anthropic | REAL_CLAUDE_HAIKU_MODEL_ID | 0.0 | 0.0 | 0.0 | 0 | 378.7907 | 3 | block |
| 3 | Google Gemini | gemini-2.5-flash | 0.0 | 0.0 | 0.0 | 0 | 607.9621 | 3 | block |

## Raw artifacts

- `real_provider_benchmark/raw_provider_outputs.json`
- `real_provider_benchmark/scored_provider_outputs.json`
