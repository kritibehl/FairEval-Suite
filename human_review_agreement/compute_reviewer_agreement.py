import json
from itertools import combinations
from pathlib import Path

DATA = json.loads(Path("human_review_agreement/reviewer_labels.json").read_text())
reviewers = DATA["reviewers"]

pair_scores = []
case_rows = []

for case in DATA["cases"]:
    labels = case["labels"]
    agreements = []
    for a, b in combinations(reviewers, 2):
        agreements.append(labels[a] == labels[b])
    case_agreement = sum(agreements) / len(agreements)
    pair_scores.extend(agreements)
    case_rows.append({
        "case_id": case["case_id"],
        "labels": labels,
        "pairwise_agreement": round(case_agreement, 4),
        "needs_adjudication": case_agreement < 1.0
    })

overall = sum(pair_scores) / len(pair_scores)

result = {
    "reviewers": len(reviewers),
    "agreement": round(overall, 4),
    "cases_reviewed": len(DATA["cases"]),
    "adjudication_cases": sum(r["needs_adjudication"] for r in case_rows),
    "results": case_rows,
    "safe_scope": "Synthetic human-review agreement analysis for evaluation operations."
}

Path("human_review_agreement/reviewer_agreement_report.json").write_text(json.dumps(result, indent=2))

md = [
    "# Human Reviewer Agreement Report",
    "",
    f"- reviewers: `{result['reviewers']}`",
    f"- agreement: `{result['agreement']}`",
    f"- cases reviewed: `{result['cases_reviewed']}`",
    f"- adjudication cases: `{result['adjudication_cases']}`",
    "",
    "| Case | Pairwise Agreement | Needs Adjudication |",
    "|---|---:|---:|",
]

for row in case_rows:
    md.append(f"| {row['case_id']} | {row['pairwise_agreement']} | {row['needs_adjudication']} |")

md += [
    "",
    "## Safe scope",
    result["safe_scope"],
]

Path("human_review_agreement/reviewer_agreement_report.md").write_text("\n".join(md) + "\n")
print(json.dumps(result, indent=2))
