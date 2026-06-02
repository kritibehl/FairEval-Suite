# Benchmark Card: Instruction-Following Regression Gate

## Purpose
This benchmark evaluates whether an LLM candidate is safe to release by checking instruction-following behavior, output contracts, and regression-sensitive failure cases.

## Task category
Instruction following and model-release validation.

## Evaluation method
FairEval runs model outputs through a benchmark suite, compares baseline vs candidate behavior, and produces gate artifacts for release decisions.

## Metrics
- average score
- pass rate
- failed case count
- pass-rate delta
- score delta
- repeated-run variance
- regression case count

## Release criteria
A model release can be blocked when:
- average score drops beyond threshold
- pass rate drops beyond threshold
- required output contracts fail
- high-risk regression cases appear
- repeated-run variance indicates unstable behavior

## Known limitations
- Small benchmark suite intended for release-gating demonstration.
- Provider coverage depends on available API quota and credits.
- Score-only interpretation is insufficient; gate artifacts and failed constraints should be reviewed.

## Artifacts
- benchmark reports
- compare artifacts
- gate artifacts
- regression reports
- dashboard exports
- run lineage metadata
