# Case Study 01 — Instruction Drop

## Failure class
Instruction-following regression

## Scenario
A model response remains fluent but misses one or more required instructions.

## Why score-only evals miss it
Average quality can remain acceptable even when required constraints are dropped.

## FairEval signal
- failed constraint
- lowered pass rate
- release-gate review signal

## Release impact
Instruction drops can break product workflows that depend on exact user constraints.
