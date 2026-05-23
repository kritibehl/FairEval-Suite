import json
from pathlib import Path

def load(path, default):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else default

data = {
    "text_generation": load("nlp_experiments/local_model_comparison_report.json", {"summary": {}})["summary"],
    "responsible_ai": load("responsible_ai/responsible_ai_regression_summary.json", {"summary": {}})["summary"],
    "oversight": load("oversight_reliability_study/oversight_failure_results.json", {"summary": {}})["summary"],
    "agentic_release": load("safety_release_gate/agentic_release_gate_summary.json", {}),
    "rag": load("rag_groundedness_eval/rag_groundedness_report.json", {"summary": {}})["summary"],
    "latency_cost": load("latency_cost_eval/latency_cost_gate_report.json", {"summary": {}})["summary"],
    "warehouse": load("eval_warehouse/warehouse_summary.json", {}),
    "live_api": {
        "docs": "https://faireval-rai-api-126325674316.us-central1.run.app/docs",
        "health": "https://faireval-rai-api-126325674316.us-central1.run.app/rai/health"
    }
}

out = Path("dashboard_frontend/src/data/faireval_dashboard_data.json")
out.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Wrote {out}")
