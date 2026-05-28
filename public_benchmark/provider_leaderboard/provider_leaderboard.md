# Public Provider Benchmark Leaderboard

Compares GPT/Claude/Gemini-style outputs across groundedness, instruction following, and hallucination risk.

## Safe scope

GPT/Claude/Gemini-style benchmark using local stored outputs unless real provider artifacts are explicitly supplied.

## Leaderboard

| Rank | Provider | Avg Score | Groundedness | Instruction Pass Rate | Hallucinations | Release Decision |
|---:|---|---:|---:|---:|---:|---|
| 1 | Claude-style | 0.9 | 0.95 | 1.0 | 0 | ship |
| 2 | GPT-style | 0.85 | 0.9 | 1.0 | 0 | ship |
| 3 | Gemini-style | 0.7 | 0.75 | 0.6667 | 2 | block |

## What this demonstrates

- provider-style comparison
- groundedness scoring
- instruction-following pass rates
- hallucination-count reporting
- release decision based on evaluation signals

## Do-not-claim

Do not claim this is a live frontier-model benchmark unless real API outputs are generated and stored with timestamps, prompts, and raw responses.
