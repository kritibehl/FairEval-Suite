from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List


def summarize_run_variance(report_paths: List[str]) -> Dict[str, Any]:
    reports = [json.loads(Path(p).read_text()) for p in report_paths]
    scores = [r.get("summary", {}).get("avg_score", 0.0) for r in reports]
    pass_rates = [r.get("summary", {}).get("pass_rate", 0.0) for r in reports]

    if len(scores) < 2:
        score_variance = 0.0
        pass_rate_variance = 0.0
    else:
        score_variance = statistics.pvariance(scores)
        pass_rate_variance = statistics.pvariance(pass_rates)

    return {
        "num_runs": len(reports),
        "avg_score_mean": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "pass_rate_mean": round(sum(pass_rates) / len(pass_rates), 4) if pass_rates else 0.0,
        "score_variance": round(score_variance, 4),
        "pass_rate_variance": round(pass_rate_variance, 4),
        "report_paths": report_paths,
    }
