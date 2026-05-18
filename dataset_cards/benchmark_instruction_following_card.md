# Dataset Card: Benchmark Instruction Following

## Dataset name
`benchmark_instruction_following`

## Purpose
Small evaluation dataset for instruction-following, formatting, grounded-answer, and regression-review workflows.

## Intended use
- model-output evaluation
- prompt regression checks
- baseline-vs-candidate comparison
- release-gate validation
- Responsible AI regression review

## Not intended for
- production model training
- fine-tuning
- human preference modeling
- claims of benchmark generality

## Evaluation dimensions
- instruction adherence
- groundedness
- format compliance
- entity preservation
- conciseness
- safety-review behavior

## Known limitations
The dataset is synthetic and intentionally small. It is designed for reproducible portfolio experiments, not broad model capability measurement.

## Governance notes
Changes to prompts, expected behavior, evaluator rules, or thresholds should update run lineage metadata.
