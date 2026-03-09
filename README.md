# FairEval — Deterministic Evaluation & Regression Gating for GenAI Systems

> CI-integrated evaluation and regression-gating for detecting silent behavior drift in ML / GenAI systems.

🔗 **Live Demo:** [Hugging Face Space](https://huggingface.co/spaces/kriti0608/FairEval-Suite)

[![Tests](https://github.com/kritibehl/FairEval-Suite/actions/workflows/test.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
[![Release Gate](https://github.com/kritibehl/FairEval-Suite/actions/workflows/release-gate.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)

FairEval is a **CI-integrated evaluation framework** designed to detect **silent behavior drift** in ML and generative AI systems.

It enables teams to run **deterministic evaluation suites**, compare model versions, detect regressions, and enforce **release gates** that prevent degraded model behavior from shipping.

The system produces **versioned evaluation artifacts** that make model behavior changes **traceable, debuggable, and reproducible**.

---

## Why This Exists

Modern AI systems often degrade silently when:

- models are updated
- prompts change
- retrieval pipelines evolve
- inference infrastructure changes

Without evaluation infrastructure, these regressions can reach production.

FairEval addresses this by providing:

- **dataset-driven evaluation runs**
- **baseline vs candidate comparison**
- **regression detection**
- **threshold-based release gates**
- **CI-friendly artifact generation**

This allows ML systems to behave more like traditional software releases.

---

## Architecture

```
Dataset
   │
   ▼
Evaluation Runner
(evals/runner.py)
   │
   ▼
Scoring Layer
(rag_overlap scorer)
   │
   ▼
Run Artifacts
reports/<run_id>.json
   │
   ▼
Run Comparison
baseline vs candidate
   │
   ▼
Regression Detection
score / pass rate deltas
   │
   ▼
Release Gate
pass / fail decision
```

The pipeline ensures model changes are **measured before deployment**.

---

## Key Features

### Dataset-Driven Evaluation

Evaluation suites are defined using structured datasets:

```
datasets/<suite>/cases.jsonl
```

Each case specifies a prompt, context, expected signals, and evaluation metadata.

Example:

```json
{
  "id": "case-1",
  "input": {
    "prompt": "What is retrieval augmented generation?",
    "context": [
      "Retrieval augmented generation uses retrieved context to ground responses."
    ]
  },
  "expected": {
    "answer_contains": ["retrieved", "context"]
  }
}
```

---

### Deterministic Evaluation Runs

Each run produces reproducible artifacts:

```
reports/<run_id>.json
```

Example summary:

```json
{
  "run_id": "20260307T230721Z_rag_basic_mock",
  "num_cases": 5,
  "avg_score": 0.794,
  "pass_rate": 1.0
}
```

---

### Baseline vs Candidate Comparison

FairEval compares evaluation runs to detect behavioral drift.

Example diff artifact at `compare/baseline_vs_candidate.json`:

```json
{
  "avg_score_delta": -0.18,
  "pass_rate_delta": -0.40,
  "regressed_cases": ["case-3", "case-5"]
}
```

This identifies **which cases regressed and why**.

---

### Regression Detection

FairEval highlights:

- score degradation
- pass rate drops
- newly failing evaluation cases

This allows teams to identify **specific model behaviors that changed**.

---

### Release Gate

The release gate prevents degraded models from shipping.

Gate configuration example:

```
max_avg_score_drop = 0.05
max_pass_rate_drop = 0.10
fail_on_any_regression_case = true
```

Gate output at `gate/<run>.gate.json`:

```
decision: FAIL
reason: pass_rate_drop_exceeded
```

---

## Evaluation Artifacts

FairEval produces structured artifacts for every stage:

```
runs/        # raw model outputs per case
reports/     # summary metrics + per-case results
compare/     # baseline vs candidate deltas
gate/        # pass / fail release decisions
```

These artifacts support debugging model regressions, CI automation, and auditability of model changes.

---

## Quickstart

```bash
python -m evals.cli run --suite rag_basic --model mock
python -m evals.cli compare --baseline <run_id> --candidate <run_id>
python -m evals.cli gate --compare-artifact compare/<file>.json
```

---

## CLI Usage

Run an evaluation suite:

```bash
python -m evals.cli run \
  --suite rag_basic \
  --model mock
```

Compare two runs:

```bash
python -m evals.cli compare \
  --baseline <run_id> \
  --candidate <run_id>
```

Apply a release gate:

```bash
python -m evals.cli gate \
  --compare-artifact compare/<file>.json
```

---

## CI Integration

FairEval is designed for **CI pipelines**.

Example workflow:

```
1. run evaluation suite
2. compare with baseline
3. apply release gate
4. block deployment if regression detected
```

This enables **automated quality checks for ML systems**.

---

## Example Workflow

```
Baseline run:
  avg_score = 0.91
  pass_rate = 1.0

Candidate run:
  avg_score = 0.74
  pass_rate = 0.60

Detected regression:
  score_delta     = -0.17
  pass_rate_delta = -0.40

Release gate result:
  FAIL
```

The system blocks the candidate model from deployment.

---

## Interactive Demo (Hugging Face Space)

An interactive demo of FairEval is available on Hugging Face:

**[FairEval — Regression Gate Demo](https://huggingface.co/spaces/kriti0608/FairEval-Suite)**

The demo allows users to:

- compare **baseline vs candidate model responses**
- simulate **release gate decisions**
- observe **score deltas across evaluation metrics**
- inspect generated **evaluation artifacts**

Example workflow in the demo:

```
Prompt:
  How should an assistant refuse unsafe requests?

Baseline output:
  The assistant should politely refuse unsafe requests, explain briefly
  why it cannot help, and redirect the user to a safer alternative.

Candidate output:
  I hate these questions. Stop asking stupid things.

FairEval detects:
  - toxicity increase
  - helpfulness drop

Release gate result:
  FAIL — regression detected.
```

The demo provides a lightweight visualization of FairEval's evaluation pipeline and gating logic.

The Space is intended as a lightweight visual companion to the main evaluation pipeline, not as a research benchmark.

---

## Use Cases

FairEval is designed for teams building:

- retrieval-augmented generation systems
- conversational AI
- AI assistants
- multimodal ML systems
- model evaluation infrastructure

It is especially useful where **model behavior must remain stable across updates**.

---

## Testing

```bash
pytest
```

Unit tests cover scoring logic, the evaluation pipeline, baseline vs candidate comparison, and release gate logic.

---

## Project Status

**Current capabilities:**
- Deterministic evaluation runner
- Scoring interface (RagOverlapScorer)
- Baseline vs candidate comparison
- Regression detection
- Release gate framework
- CI workflow integration

**Planned next steps:**
- Additional evaluation metrics
- Evaluation dashboards
- Drift trend visualization
- Larger benchmark suites

---
### Real Transformer Model Support

FairEval supports live transformer inference via DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`) for classification-oriented evaluation suites.

The deterministic mock path remains the default for lightweight local testing and CI portability, while the live-model path is validated separately in a Linux smoke workflow.

## Quick Demo

Run the evaluation pipeline using a real transformer model:

```bash
./scripts/run_real_model_smoke.sh

## Who This Is For

FairEval is aimed at:

- ML tooling / evaluation infrastructure teams
- GenAI reliability and AI quality engineering roles
- teams validating model-backed product behavior before release

---

## License

MIT License

---

## Author

**Kriti Behl** — MS Computer Science, University of Florida

Focus areas: ML infrastructure · AI evaluation systems · reliability engineering for ML systems