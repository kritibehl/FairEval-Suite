# LLM Regression Gate Demo

FairEval is a release-gating system for LLMs.

Instead of only scoring model outputs, it answers a harder question:

> Should this candidate model ship, or should it be blocked?

## What this demo shows
- multi-model evaluation
- baseline vs candidate comparison
- regression detection
- automated release decisions
- production-style impact reasoning

## Core pipeline
Run → Compare → Gate

## Why this matters
Model updates often fail silently:
- instruction-following quality drops
- formatting contracts break
- structured outputs become unreliable
- context-sensitive behavior regresses

FairEval is designed to catch those regressions before deployment.

## Included artifacts
- public benchmark package
- regression case library
- compare artifacts
- gate artifacts

## Positioning
This is not just an evaluation tool.

It is a deployment-safety layer for LLM releases.
