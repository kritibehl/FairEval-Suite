# FairEval — Deterministic Evaluation & Regression Gating for GenAI Systems

> CI-integrated evaluation and regression gating framework for detecting silent behavior drift in ML and generative AI systems.

🔗 **Live Demo:** [FairEval Hugging Face Space](https://huggingface.co/spaces/kriti0608/FairEval-Suite)

[![Tests](https://github.com/kritibehl/FairEval-Suite/actions/workflows/test.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
[![Release Gate](https://github.com/kritibehl/FairEval-Suite/actions/workflows/release-gate.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
![GitHub Repo stars](https://img.shields.io/github/stars/kritibehl/FairEval-Suite?style=social)

FairEval evaluates model behavior changes before deployment through dataset-driven runs, baseline comparisons, and regression gates.

---

## Overview

FairEval is an evaluation infrastructure framework designed to detect silent regressions in ML and GenAI systems **before deployment** — analogous to regression testing for traditional software systems.

It enables teams to:

- Run deterministic evaluation suites
- Compare baseline vs. candidate model runs
- Detect behavior drift
- Enforce threshold-based regression gates
- Generate versioned evaluation artifacts

---

## End-to-End Evaluation Flow

```
dataset / model change → evaluate → compare → gate → release decision
```

FairEval evaluates candidate model behavior, compares it against a baseline, and blocks release when configured regression thresholds are exceeded.

---

## Why This Exists

Modern AI systems often degrade silently when:

- Models are updated
- Prompts change
- Retrieval pipelines evolve
- Inference infrastructure changes

Without evaluation infrastructure, these regressions can reach production undetected. FairEval addresses this with dataset-driven evaluation suites, baseline comparisons, regression detection, CI-compatible release gates, and reproducible artifacts.

---

## System Architecture

```
Dataset
   │
   ▼
Model Inference
(Mock or DistilBERT)
   │
   ▼
Scoring Layer
(rag_overlap, classification_label scorers)
   │
   ▼
Evaluation Report
reports/<run_id>.json
   │
   ▼
Baseline vs Candidate Comparison
compare/<artifact>.json
   │
   ▼
Regression Detection
score / pass-rate deltas
   │
   ▼
Release Gate
gate/<run>.gate.json
```

This pipeline evaluates model outputs, compares behavioral changes across runs, and applies configurable regression thresholds before deployment.

---

## Key Features

### Dataset-Driven Evaluation

Evaluation suites are defined using structured datasets at `datasets/<suite>/cases.jsonl`. Each case includes a prompt, optional context, expected signals, and metadata.

```json
{
  "id": "case-1",
  "input": {
    "prompt": "What is retrieval augmented generation?",
    "context": ["Retrieval augmented generation uses retrieved context to ground responses."]
  },
  "expected": {
    "answer_contains": ["retrieved", "context"]
  }
}
```

### Deterministic Evaluation Runs

Each run produces reproducible artifacts at `reports/<run_id>.json`:

```json
{
  "run_id": "20260307T230721Z_rag_basic_mock",
  "num_cases": 5,
  "avg_score": 0.79,
  "pass_rate": 1.0
}
```

### Baseline vs. Candidate Comparison

FairEval compares evaluation runs to detect behavioral drift:

```json
{
  "avg_score_delta": -0.18,
  "pass_rate_delta": -0.40,
  "regressed_cases": ["case-3", "case-5"]
}
```

### Release Gate

The release gate prevents degraded models from shipping:

```
max_avg_score_drop         = 0.05
max_pass_rate_drop         = 0.10
fail_on_any_regression_case = true

decision: FAIL
reason:   pass_rate_drop_exceeded
```

### Evaluation Artifacts

| Directory  | Contents                           |
|------------|------------------------------------|
| `runs/`    | Raw model outputs                  |
| `reports/` | Evaluation summaries               |
| `compare/` | Baseline vs. candidate differences |
| `gate/`    | Regression gate decisions          |

---

## Installation

```bash
git clone https://github.com/kritibehl/FairEval-Suite.git
cd FairEval-Suite

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Quickstart

```bash
# Run an evaluation suite
python -m evals.cli run --suite rag_basic --model mock

# Compare two runs
python -m evals.cli compare \
  --baseline <run_id> \
  --candidate <run_id>

# Apply a regression gate
python -m evals.cli gate \
  --compare-artifact compare/<file>.json
```

These commands cover the core local workflow: run an evaluation, compare candidate vs baseline behavior, and apply a release gate.

---

## Example Workflow

```bash
# Step 1 — Baseline
python -m evals.cli run --suite rag_basic --model mock --out-dir baseline_artifacts

# Step 2 — Candidate
python -m evals.cli run --suite rag_basic --model mock --out-dir candidate_artifacts

# Step 3 — Compare
python -m evals.cli compare \
  --baseline <baseline_run_id> \
  --candidate <candidate_run_id>

# Step 4 — Gate
python -m evals.cli gate \
  --compare-artifact compare/<artifact>.json
```

---

## Real Transformer Model Support

FairEval supports live transformer evaluation via `distilbert-base-uncased-finetuned-sst-2-english` using HuggingFace Transformers and PyTorch:

```bash
python -m evals.cli run \
  --suite classification_basic \
  --model distilbert-sst2
```

Deterministic mock evaluation remains the default for lightweight local testing and CI portability.

---

## API Service

FairEval exposes a lightweight FastAPI service:

```bash
uvicorn api.main:app --reload
# Docs at: http://localhost:8000/docs
```

| Method | Endpoint    | Description             |
|--------|-------------|-------------------------|
| GET    | `/health`   | Health check            |
| POST   | `/evaluate` | Run an evaluation suite |
| POST   | `/compare`  | Compare two runs        |
| POST   | `/gate`     | Apply a regression gate |

### Example `/evaluate` Response

```json
{
  "summary": {
    "run_id": "20260312T225817Z_rag_basic_mock",
    "num_cases": 2,
    "avg_score": 0.77,
    "pass_rate": 1.0
  },
  "report_artifact_path": "reports/20260312T225817Z_rag_basic_mock.json"
}
```

This shows the generated evaluation summary and artifact location.

### Example `/compare` Response

```json
{
  "summary": {
    "avg_score": -0.2,
    "pass_rate": -0.5,
    "num_cases": 0
  },
  "compare_artifact_path": "compare/candidate_report_vs_baseline_report.json"
}
```

Negative values indicate degradation relative to the baseline.

### Example `/gate` Response

```json
{
  "summary": {
    "decision": "fail",
    "reasons": [
      "avg_score_drop_exceeded: -0.2000 < -0.0500",
      "pass_rate_drop_exceeded: -0.5000 < -0.1000",
      "regressed_cases_detected: 2"
    ]
  }
}
```

Together, these three endpoints cover the full evaluation pipeline: run → compare → gate.

---

## Interactive Demo

🔗 [FairEval Hugging Face Space](https://huggingface.co/spaces/kriti0608/FairEval-Suite)

The Hugging Face Space provides a lightweight interactive interface for experimenting with FairEval's regression-gating workflow.

The primary FairEval workflow runs through the CLI and FastAPI service, which execute full dataset-driven evaluation suites.

| | Output |
|---|---|
| **Prompt** | How should an assistant refuse unsafe requests? |
| **Baseline** | The assistant politely refuses and explains why. |
| **Candidate** | I hate these questions. Stop asking. |
| **FairEval detects** | Helpfulness drop · Toxicity increase |
| **Gate result** | `FAIL` |

---

## CLI Structure

```
evals/
├── cli.py
├── runner.py
├── scorers/
├── compare/
└── gate/
```

These modules implement evaluation execution, scoring, comparison, and release-gate enforcement.

---

## Testing

```bash
pytest
```

The test suite validates evaluation pipeline logic, scoring functions, regression gate behavior, and API endpoints.

---

## Use Cases

FairEval is designed for teams building:

- Retrieval-augmented generation (RAG) systems
- Conversational AI assistants
- Multimodal ML systems
- Model evaluation infrastructure

It is especially useful where **model behavior must remain stable across updates**.

---

## Engineering Decisions

FairEval was designed as **evaluation infrastructure**, not a benchmark:

- **Deterministic mock evaluation** for CI portability
- **Artifact-based outputs** for reproducibility and debugging
- **Dataset-driven suites** for extensibility
- **Regression gates** integrated into CI pipelines
- **Real transformer evaluation** via DistilBERT to validate on actual model outputs

---

## License

MIT License

---

## Author

**Kriti Behl** — MS Computer Science, University of Florida

*Focus: ML infrastructure · AI evaluation systems · Reliability engineering for ML*