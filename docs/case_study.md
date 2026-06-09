# FairEval Case Study

## Problem
Average model scores hide case-level regressions, hallucinations, citation failures, and serving latency issues.

## Design
FairEval compares baseline and candidate runs using case-level metrics, statistical tests, groundedness checks, and release gates.

## Validation
Reduced false allows from 16 to 0 and blocked a known-bad regression fixture.

## Tradeoffs
Adds evaluation complexity, but prevents unsafe model releases from reaching users.
