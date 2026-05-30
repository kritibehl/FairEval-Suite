# Why Score-Only Evals Fail

Score parity is not release safety.

A candidate model can match or exceed an average score while still being unsafe to release because failures often concentrate in specific product-critical cases.

## Failure modes hidden by averages
- JSON contracts break while semantic quality looks acceptable
- formatting drift breaks downstream parsers
- instruction-following drops on multi-constraint prompts
- repeated-run variance creates unstable behavior
- safety-style drift changes response boundaries
- failed constraints appear in a small but high-risk subset

## What FairEval adds
FairEval combines:
- benchmark scores
- pass-rate deltas
- failed constraint reports
- regression case libraries
- run lineage
- prompt versions
- dataset hashes
- release-gate artifacts

The goal is not just to score a model.

The goal is to decide whether it should ship.
