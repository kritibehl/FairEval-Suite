# FairEval — Deterministic Evaluation & Regression Gating for GenAI Systems

**CI-integrated evaluation and regression gating framework for detecting silent behavior drift in ML and generative AI systems.**

🔗 **Live Demo:** [FairEval on Hugging Face](https://huggingface.co/spaces/kriti0608/FairEval-Suite)

[![Tests](https://github.com/kritibehl/FairEval-Suite/actions/workflows/test.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
[![Release Gate](https://github.com/kritibehl/FairEval-Suite/actions/workflows/release-gate.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
![GitHub Repo stars](https://img.shields.io/github/stars/kritibehl/FairEval-Suite?style=social)

FairEval is CI-integrated evaluation and regression gating for GenAI systems. It catches **silent behavior regressions before deployment** by running deterministic eval suites, comparing baseline vs. candidate outputs, and blocking releases when quality drifts past configured thresholds. It is useful not just for model updates, but for any change that can shift behavior — including prompt edits, retrieval pipeline changes, and inference infrastructure updates.

---

## The Problem

Modern AI systems degrade silently when models are updated, prompts change, retrieval pipelines evolve, or inference infrastructure shifts. Without evaluation infrastructure, these regressions reach production unnoticed.

**Example regression:**

| | Response |
|---|---|
| **Prompt** | How should an assistant refuse unsafe requests? |
| **Baseline** | The assistant politely refuses and explains why. |
| **Candidate** | I hate these questions. Stop asking. |
| **FairEval detects** | Helpfulness drop · Toxicity increase |
| **Gate result** | `FAIL` |

---

## Live Demo

🔗 [FairEval on Hugging Face](https://huggingface.co/spaces/kriti0608/FairEval-Suite) — accepts baseline and candidate responses, applies configurable regression thresholds, and outputs a gate decision with a downloadable artifact JSON.

![FairEval Hugging Face Demo](docs/images/hf-demo-full.png)

![FairEval Gate Controls and Delta Summary](docs/images/hf-demo-gate.png)

---

## Core Workflow

```
dataset / model change
    ↓
evaluate
    ↓
compare baseline vs candidate
    ↓
apply regression gate
    ↓
release decision
```

---

## System Architecture

```
Dataset
    ↓
Model Inference (mock or DistilBERT-backed)
    ↓
Scoring Layer (rag_overlap, classification_label, suite scorers)
    ↓
Evaluation Report  →  reports/<run_id>.json
    ↓
Baseline vs Candidate Comparison  →  compare/<artifact>.json
    ↓
Regression Detection (score / pass-rate deltas)
    ↓
Release Gate  →  gate/<run>.gate.json
```

---

## Key Features

### Dataset-Driven Evaluation

Suites are defined as structured JSONL cases with explicit expected outputs — making evaluation auditable and version-controlled.

```json
{
  "id": "case-1",
  "input": {
    "prompt": "What is retrieval augmented generation?",
    "context": ["Retrieval augmented generation uses retrieved context to ground responses."]
  },
  "expected": { "answer_contains": ["retrieved", "context"] }
}
```

### Deterministic Runs

Each run produces reproducible artifacts with a stable `run_id`:

```json
{
  "run_id": "20260307T230721Z_rag_basic_mock",
  "num_cases": 5,
  "avg_score": 0.79,
  "pass_rate": 1.0
}
```

### Baseline vs. Candidate Comparison

Detects silent behavior drift with per-case regression tracking:

```json
{
  "avg_score_delta": -0.18,
  "pass_rate_delta": -0.40,
  "regressed_cases": ["case-3", "case-5"]
}
```

### Configurable Release Gate

Blocks deployment when quality thresholds are exceeded:

```
max_avg_score_drop          = 0.05
max_pass_rate_drop          = 0.10
fail_on_any_regression_case = true

decision: FAIL
reason:   pass_rate_drop_exceeded
```

### Versioned Artifacts

| Directory | Contents |
|---|---|
| `runs/` | Raw model outputs |
| `reports/` | Evaluation summaries |
| `compare/` | Baseline vs. candidate diffs |
| `gate/` | Release gate decisions |

All runs, comparisons, and gate decisions are persisted for historical debugging across releases.

---

## Quickstart

```bash
git clone https://github.com/kritibehl/FairEval-Suite.git
cd FairEval-Suite

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Full Release Check Workflow

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

## Real Transformer Support

FairEval supports live evaluation via `distilbert-base-uncased-finetuned-sst-2-english` using HuggingFace Transformers and PyTorch for classification-oriented suites:

```bash
python -m evals.cli run \
  --suite classification_basic \
  --model distilbert-sst2
```

Deterministic mock evaluation remains the default for lightweight local testing and CI portability. The live-model path validates the pipeline against real transformer outputs.

---

## API Service

```bash
uvicorn api.main:app --reload
# Docs at: http://localhost:8000/docs
```

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/evaluate` | Run an evaluation suite |
| `POST` | `/compare` | Compare two runs |
| `POST` | `/gate` | Apply a regression gate |

---

## Engineering Decisions

**Deterministic mock evaluation** for CI portability — no GPU required to run the full pipeline.

**Artifact-based outputs** for reproducibility — every run can be debugged in isolation against stored artifacts.

**Dataset-driven suites** for extensibility — adding a new eval case doesn't require code changes.

**Regression gates integrated into CI** — evaluation is part of the release pipeline, not a manual step.

**Real transformer evaluation via DistilBERT** to validate the pipeline against actual model outputs, not just mock stubs.

---

## Repo Structure

```
evals/            scoring, compare, gate logic
datasets/         suite definitions / JSONL cases
reports/          evaluation summaries
compare/          baseline vs candidate artifacts
gate/             release gate outputs
api/              FastAPI service
demo/             Gradio / interactive demo assets
tests/            evaluation coverage
scripts/          helper workflows
docs/images/      demo screenshots
```

---

## Running Tests

```bash
pytest
```

---

## Why This Project Matters

FairEval treats model behavior like a release contract: measured, compared, versioned, and blocked when degraded. That framing makes it especially relevant for AI infrastructure, evaluation platform engineering, and release-safety roles — particularly on teams building RAG systems, conversational AI, or any ML system where behavior must remain stable across updates.

---

## Related Projects

- [Faultline](https://github.com/kritibehl/faultline) — correctness under failure for distributed systems
- [KubePulse](https://github.com/kritibehl/KubePulse) — resilience validation
- [DetTrace](https://github.com/kritibehl/dettrace) — incident replay and divergence analysis
- [AutoOps-Insight](https://github.com/kritibehl/autoops-insight) — operator-facing incident triage

## License

MIT
