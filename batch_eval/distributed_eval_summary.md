# Spark-Style Batch Evaluation Workflow

- execution mode: `pyspark_local`
- total cases: 8
- average score: 0.6813
- regression count: 5

## Grouped scoring

| Task Type | Cases | Avg Score | Regressions |
|---|---:|---:|---:|
| latency_cost | 1 | 0.5 | 1 |
| rag_groundedness | 2 | 0.7 | 1 |
| responsible_ai | 1 | 0.25 | 1 |
| rewrite | 2 | 0.8 | 1 |
| summarization | 2 | 0.85 | 1 |

## Safe scope

This workflow runs in PySpark local mode when PySpark is installed, with a Python fallback for portability. It is not a real distributed Spark cluster.
