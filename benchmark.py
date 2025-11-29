import csv
from fair_eval import evaluate

DATA = [
    {
        "model": "Claude",
        "prompt": "Explain attention in transformers to a beginner.",
        "output": "Attention lets the model look at all words and decide which ones matter most.",
    },
    {
        "model": "GPT-4o",
        "prompt": "Explain attention in transformers to a beginner.",
        "output": "Think of attention like highlighting key words so AI knows which parts are important.",
    },
    {
        "model": "DeepSeek-R1",
        "prompt": "Explain attention in transformers to a beginner.",
        "output": "Attention computes weighted similarity between tokens, enabling contextual representation learning.",
    },
]


def run():
    rows = []

    for ex in DATA:
        res = evaluate(ex["prompt"], ex["output"])

        rows.append({
            "model": ex["model"],
            "score": res.score,
            "helpfulness": res.rubric_breakdown["helpfulness"],
            "relevance": res.rubric_breakdown["relevance"],
            "clarity": res.rubric_breakdown["clarity"],
            "toxicity": res.toxicity.composite,
        })

    print("\n=== FairEval Mini Benchmark ===")
    print(f"{'Model':<12} | Score | Hlp | Rel | Clr | Toxic")
    print("-" * 56)
    for r in rows:
        print(
            f"{r['model']:<12} | {r['score']:.3f} | {r['helpfulness']:.3f} | "
            f"{r['relevance']:.3f} | {r['clarity']:.3f} | {r['toxicity']:.3f}"
        )

    # SAVE TO CSV (Important!!!)
    with open("benchmark_results.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(["model", "score", "helpfulness", "relevance", "clarity", "toxicity"])
        for r in rows:
            w.writerow(r.values())

    print("\nSaved results to benchmark_results.csv")


if __name__ == "__main__":
    run()
