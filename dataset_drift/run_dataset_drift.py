import json
from pathlib import Path

BASE = json.loads(Path("dataset_drift/baseline_dataset_profile.json").read_text())
CAND = json.loads(Path("dataset_drift/candidate_dataset_profile.json").read_text())

base_entities = set(BASE["entity_counts"])
cand_entities = set(CAND["entity_counts"])

new_entity_names = sorted(cand_entities - base_entities)
new_entities = sum(CAND["entity_counts"][e] for e in new_entity_names)

intent_shift = {}
for intent in set(BASE["intent_distribution"]) | set(CAND["intent_distribution"]):
    b = BASE["intent_distribution"].get(intent, 0.0)
    c = CAND["intent_distribution"].get(intent, 0.0)
    delta = round(c - b, 4)
    if abs(delta) >= 0.10:
        intent_shift[intent] = delta

result = {
    "baseline_dataset": BASE["dataset_id"],
    "candidate_dataset": CAND["dataset_id"],
    "new_entity_names": new_entity_names,
    "new_entities": new_entities,
    "distribution_shift": bool(intent_shift),
    "shifted_intents": intent_shift,
    "release_readiness": "needs_review" if new_entities > 0 or intent_shift else "ship",
    "safe_scope": "Synthetic dataset drift analysis for evaluation dataset monitoring."
}

Path("dataset_drift/dataset_drift_report.json").write_text(json.dumps(result, indent=2))

md = [
    "# Dataset Drift Report",
    "",
    f"- baseline dataset: `{result['baseline_dataset']}`",
    f"- candidate dataset: `{result['candidate_dataset']}`",
    f"- new entities: `{result['new_entities']}`",
    f"- distribution shift: `{result['distribution_shift']}`",
    f"- release readiness: `{result['release_readiness']}`",
    "",
    "## New entity names",
    "",
    ", ".join(result["new_entity_names"]) or "None",
    "",
    "## Shifted intents",
    "",
]

for k, v in result["shifted_intents"].items():
    md.append(f"- {k}: {v:+.4f}")

md += [
    "",
    "## Safe scope",
    result["safe_scope"],
]

Path("dataset_drift/dataset_drift_report.md").write_text("\n".join(md) + "\n")
print(json.dumps(result, indent=2))
