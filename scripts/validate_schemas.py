import glob
import json
from pathlib import Path

from jsonschema import validate

checks = [
    (
        "schemas/gate_artifact.schema.json",
        sorted(glob.glob("benchmark_public/instruction_following/gates/**/*.json", recursive=True))[-1:]
    ),
    (
        "schemas/lineage_artifact.schema.json",
        sorted(glob.glob("artifacts/run_lineage/*.json"))[-1:]
    ),
    (
        "schemas/provider_comparison.schema.json",
        ["reports/provider_comparison.json"] if Path("reports/provider_comparison.json").exists() else []
    ),
]

validated = []

for schema_path, artifact_paths in checks:
    schema = json.loads(Path(schema_path).read_text())
    for artifact_path in artifact_paths:
        data = json.loads(Path(artifact_path).read_text())
        validate(instance=data, schema=schema)
        validated.append({"schema": schema_path, "artifact": artifact_path})

print(json.dumps({"validated": validated}, indent=2))
