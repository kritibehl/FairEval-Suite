# Apple ML Positioning: Public Provider Benchmark

This benchmark makes FairEval easier to understand for Apple ML / AI Quality roles.

## What it evaluates
- groundedness
- instruction following
- hallucination risk

## Provider comparison
FairEval compares GPT/Claude/Gemini-style outputs using stored evaluation artifacts.

## Why this matters
User-facing AI systems need quality gates before release. A provider may look strong on average but still fail groundedness, instruction-following, or hallucination checks.

## Safe scope
This benchmark uses local/stored provider-style outputs unless explicitly replaced with real provider API outputs. It should be described as a provider-style benchmark unless real runs are performed.
