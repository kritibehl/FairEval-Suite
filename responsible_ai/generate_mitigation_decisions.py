import json
from collections import Counter, defaultdict
from pathlib import Path

SUMMARY_PATH = Path("responsible_ai/responsible_ai_regression_summary.json")
OUT_JSON = Path("responsible_ai/mitigation_decision_summary.json")
OUT_MD = Path("responsible_ai/mitigation_decision_report.md")

data = json.loads(SUMMARY_PATH.read_text())
candidate_results = data["candidate_results"]

def choose_action(r):
    if r["false_allow"]:
        return "block_release"
    if r["risk_category"] == "sensitive_data_exposure_risk":
        return "require_human_review"
    if r["risk_category"] in {"unsupported_high_stakes_claim", "ungrounded_answer"}:
        return "request_revision"
    if r["risk_category"] == "refusal_inconsistency":
        return "require_human_review"
    if r["risk_category"] == "policy_bypass_attempt":
        return "block_release"
    if r["safety_regression"]:
        return "request_revision"
    return "allow"

decisions = []
for r in candidate_results:
    action = choose_action(r)
    decisions.append({
        "scenario_id": r["scenario_id"],
        "risk_category": r["risk_category"],
        "safety_regression": r["safety_regression"],
        "false_allow": r["false_allow"],
        "mitigation_action": action,
        "failure_reason": r["failure_reason"]
    })

action_counts = Counter(d["mitigation_action"] for d in decisions)
risk_action = defaultdict(Counter)
for d in decisions:
    risk_action[d["risk_category"]][d["mitigation_action"]] += 1

summary = {
    "total_evaluated_cases": len(decisions),
    "block_release_count": action_counts["block_release"],
    "human_review_count": action_counts["require_human_review"],
    "revision_required_count": action_counts["request_revision"],
    "allow_count": action_counts["allow"],
    "risk_category_action_distribution": {
        risk: dict(counter) for risk, counter in risk_action.items()
    },
    "decisions": decisions
}

OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

md = [
    "# Responsible AI Mitigation Decision Report",
    "",
    f"- total evaluated cases: {summary['total_evaluated_cases']}",
    f"- block release count: {summary['block_release_count']}",
    f"- human review count: {summary['human_review_count']}",
    f"- revision required count: {summary['revision_required_count']}",
    f"- allow count: {summary['allow_count']}",
    "",
    "| Scenario | Risk Category | Safety Regression | False Allow | Mitigation Action | Failure Reason |",
    "|---|---|---:|---:|---|---|",
]

for d in decisions:
    md.append(
        f"| {d['scenario_id']} | {d['risk_category']} | {d['safety_regression']} | {d['false_allow']} | {d['mitigation_action']} | {d['failure_reason'] or '-'} |"
    )

md += [
    "",
    "## Safe scope",
    "This mitigation layer translates synthetic Responsible AI risk findings into release-review actions. It is not a production policy engine."
]

OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

print(json.dumps({
    "total_evaluated_cases": summary["total_evaluated_cases"],
    "block_release_count": summary["block_release_count"],
    "human_review_count": summary["human_review_count"],
    "revision_required_count": summary["revision_required_count"],
    "allow_count": summary["allow_count"]
}, indent=2))
