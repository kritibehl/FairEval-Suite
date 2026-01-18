# Evaluation Datasets

Datasets are deterministic, versioned, and human-reviewable.

Each dataset is a directory containing:
- `cases.jsonl` — one JSON object per evaluation case

## JSONL Schema

Each line represents one evaluation case:

```json
{
  "id": "string",
  "input": {
    "prompt": "string",
    "context": ["string", "..."]
  },
  "expected": {
    "answer_contains": ["string", "..."]
  }
}
