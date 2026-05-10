# Scenario Collection Protocol

## Goal
Collect evaluation scenarios that represent realistic deployment risks and operational failure modes.

## Scenario sources
- failed benchmark runs
- production-adjacent regression simulations
- public model changelogs
- schema failure examples
- formatting regressions
- instruction-following failures

## Collection rules
- each scenario must contain reproducible inputs
- required constraints must be explicit
- expected outputs must be documented
- downstream operational impact should be recorded

## Metadata requirements
- scenario_id
- collection_source
- prompt_version
- dataset_hash
- evaluator_version
- failure_class

## Review workflow
1. collect scenario
2. validate schema
3. run evaluation
4. classify regression severity
5. generate release recommendation
