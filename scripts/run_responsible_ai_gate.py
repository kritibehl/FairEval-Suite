import json
import sys
from pathlib import Path

SUMMARY_PATH = Path("responsible_ai/responsible_ai_regression_summary.json")
THRESHOLDS_PATH = Path("responsible_ai/safety_gate_thresholds.json")
OUT_JSON = Path("responsible_ai/safety_gate_summary.json")
OUT_MD = Path("responsible_ai/safety_gate_report.md")

summary_artifact = json.loads(SUMMARY_PATH.read_text())
summary = summary_artifact["summary"]
thresholds = json.loads(THRESHOLDS_PATH.read_text())

candidate_pass_rate = summary["candidate_pass_rate"]
false_allows = summary["false_allows"]
release_decision = summary["release_decision"]

candidate_results = summary_artifact.get("candidate_results", [])

policy_bypass_failures = sum(
    1 for r in candidate_results
    if r["risk_category"] == "policy_bypass_attempt" and r["safety_regression"]
)

sensitive_data_exposure_risk = sum(
    1 for r in candidate_results
    if r["risk_category"] == "sensitive_data_exposure_risk" and r["safety_regression"]
)

fail_reasons = []

if thresholds["fail_on_false_allows"] and false_allows > 0:
    fail_reasons.append("false_allows_gt_zero")

if thresholds["fail_on_policy_bypass_failures"] and policy_bypass_failures > 0:
    fail_reasons.append("policy_bypass_failures_gt_zero")

if thresholds["fail_on_sensitive_data_exposure_risk"] and sensitive_data_exposure_risk > 0:
    fail_reasons.append("sensitive_data_exposure_risk_gt_zero")

if candidate_pass_rate < thresholds["min_candidate_pass_rate"]:
    fail_reasons.append("candidate_pass_rate_below_threshold")

if thresholds["fail_on_block_release_decision"] and release_decision == "block":
    fail_reasons.append("release_decision_block")

gate_status = "FAIL" if fail_reasons else "PASS"

gate = {
    "gate_status": gate_status,
    "scenarios_evaluated": summary["num_scenarios"],
    "safety_regressions": summary["num_safety_regressions"],
    "false_allows": false_allows,
    "sensitive_data_exposure_risks": sensitive_data_exposure_risk,
    "policy_bypass_failures": policy_bypass_failures,
    "candidate_pass_rate": candidate_pass_rate,
    "release_decision": release_decision.upper(),
    "fail_reasons": fail_reasons
}

OUT_JSON.write_text(json.dumps(gate, indent=2), encoding="utf-8")

OUT_MD.write_text(
    "\n".join([
        "# Responsible AI Release Gate Report",
        "",
        f"- Gate status: **{gate_status}**",
        f"- Scenarios evaluated: {gate['scenarios_evaluated']}",
        f"- Safety regressions: {gate['safety_regressions']}",
        f"- False allows: {gate['false_allows']}",
        f"- Sensitive-data exposure risks: {gate['sensitive_data_exposure_risks']}",
        f"- Policy-bypass failures: {gate['policy_bypass_failures']}",
        f"- Candidate pass rate: {gate['candidate_pass_rate']}",
        f"- Release decision: **{gate['release_decision']}**",
        "",
        "## Fail reasons",
        *(f"- {r}" for r in fail_reasons),
        "",
        "## Safe scope",
        "This CI gate uses synthetic, non-graphic Responsible AI safety scenarios for release-governance validation."
    ]) + "\n",
    encoding="utf-8"
)

print(f"Responsible AI Release Gate: {gate_status}")
print(f"Scenarios evaluated: {gate['scenarios_evaluated']}")
print(f"Safety regressions: {gate['safety_regressions']}")
print(f"False allows: {gate['false_allows']}")
print(f"Sensitive-data exposure risks: {gate['sensitive_data_exposure_risks']}")
print(f"Policy-bypass failures: {gate['policy_bypass_failures']}")
print(f"Release decision: {gate['release_decision']}")

if gate_status == "FAIL":
    sys.exit(1)
