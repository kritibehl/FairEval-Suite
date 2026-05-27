import json
from pathlib import Path
from statistics import mean

DATA = [
    {"case_id": "case-001", "task_type": "rewrite", "score": 1.0, "regression": False, "model": "baseline"},
    {"case_id": "case-002", "task_type": "summarization", "score": 1.0, "regression": False, "model": "baseline"},
    {"case_id": "case-003", "task_type": "rag_groundedness", "score": 1.0, "regression": False, "model": "baseline"},
    {"case_id": "case-004", "task_type": "rewrite", "score": 0.6, "regression": True, "model": "candidate"},
    {"case_id": "case-005", "task_type": "summarization", "score": 0.7, "regression": True, "model": "candidate"},
    {"case_id": "case-006", "task_type": "rag_groundedness", "score": 0.4, "regression": True, "model": "candidate"},
    {"case_id": "case-007", "task_type": "responsible_ai", "score": 0.25, "regression": True, "model": "candidate"},
    {"case_id": "case-008", "task_type": "latency_cost", "score": 0.5, "regression": True, "model": "candidate"}
]

def run_python_fallback(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault(row["task_type"], []).append(row)

    task_metrics = []
    for task_type, items in grouped.items():
        task_metrics.append({
            "task_type": task_type,
            "num_cases": len(items),
            "avg_score": round(mean(i["score"] for i in items), 4),
            "regression_count": sum(i["regression"] for i in items)
        })

    return {
        "execution_mode": "python_fallback",
        "total_cases": len(rows),
        "avg_score": round(mean(i["score"] for i in rows), 4),
        "regression_count": sum(i["regression"] for i in rows),
        "task_metrics": task_metrics
    }

def run_pyspark(rows):
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

    spark = (
        SparkSession.builder
        .appName("FairEvalBatchEvaluation")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.createDataFrame(rows)

    task_df = (
        df.groupBy("task_type")
        .agg(
            F.count("*").alias("num_cases"),
            F.round(F.avg("score"), 4).alias("avg_score"),
            F.sum(F.col("regression").cast("int")).alias("regression_count")
        )
        .orderBy("task_type")
    )

    total = df.count()
    avg_score = df.agg(F.avg("score")).collect()[0][0]
    regressions = df.agg(F.sum(F.col("regression").cast("int"))).collect()[0][0]

    task_metrics = [row.asDict() for row in task_df.collect()]

    spark.stop()

    return {
        "execution_mode": "pyspark_local",
        "total_cases": total,
        "avg_score": round(avg_score, 4),
        "regression_count": int(regressions),
        "task_metrics": task_metrics
    }

try:
    result = run_pyspark(DATA)
except Exception as exc:
    result = run_python_fallback(DATA)
    result["pyspark_fallback_reason"] = str(exc)

Path("batch_eval/batch_eval_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

md = [
    "# Spark-Style Batch Evaluation Workflow",
    "",
    f"- execution mode: `{result['execution_mode']}`",
    f"- total cases: {result['total_cases']}",
    f"- average score: {result['avg_score']}",
    f"- regression count: {result['regression_count']}",
    "",
    "## Grouped scoring",
    "",
    "| Task Type | Cases | Avg Score | Regressions |",
    "|---|---:|---:|---:|",
]

for row in result["task_metrics"]:
    md.append(
        f"| {row['task_type']} | {row['num_cases']} | {row['avg_score']} | {row['regression_count']} |"
    )

md += [
    "",
    "## Safe scope",
    "",
    "This workflow runs in PySpark local mode when PySpark is installed, with a Python fallback for portability. It is not a real distributed Spark cluster.",
]

Path("batch_eval/distributed_eval_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print(json.dumps(result, indent=2))
