import json
from pathlib import Path

matrix = json.loads(Path("multi_model/provider_matrix.json").read_text())

lines = [
    "# Multi-Model Comparison Matrix",
    "",
    "| Provider | Adapter | Status | Note |",
    "|---|---|---|---|",
]

for p in matrix["providers"]:
    lines.append(f"| {p['name']} | `{p['adapter']}` | {p['status']} | {p['note']} |")

lines += [
    "",
    "## Comparison fields",
    "",
    *[f"- {field}" for field in matrix["comparison_fields"]],
]

Path("multi_model/provider_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote multi_model/provider_matrix.md")
