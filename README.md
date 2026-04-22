# FairEval — Regression Gating for GenAI Systems

**CI-integrated evaluation and regression gating framework for detecting silent behavior drift in ML and generative AI systems.**

🔗 **Live Demo:** [FairEval on Hugging Face](https://huggingface.co/spaces/kriti0608/FairEval-Suite)

[![Tests](https://github.com/kritibehl/FairEval-Suite/actions/workflows/test.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
[![Release Gate](https://github.com/kritibehl/FairEval-Suite/actions/workflows/release-gate.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
![GitHub Repo stars](https://img.shields.io/github/stars/kritibehl/FairEval-Suite?style=social)

---

FairEval treats model behavior like a **release contract**: measured, compared, versioned, and blocked when degraded.

Most evaluation projects stop at score reporting. FairEval answers a different question:

> **Should this candidate model be allowed to ship?**

It catches silent regressions before deployment — across model updates, prompt edits, retrieval pipeline changes, and inference infrastructure shifts.

```
Baseline:  avg_score 0.794  |  pass_rate 1.0
Candidate: avg_score 0.0    |  pass_rate 0.0
Gate:      BLOCK
Reason:    significant drift detected
```

---

## The Problem

Modern AI systems degrade silently. Without evaluation infrastructure, regressions reach production unnoticed.

| | Response |
|---|---|
| **Prompt** | How should an assistant refuse unsafe requests? |
| **Baseline** | The assistant politely refuses and explains why. |
| **Candidate** | I hate these questions. Stop asking. |
| **FairEval detects** | Helpfulness drop · Toxicity increase |
| **Gate result** | `BLOCK` |

---

## Controlled Regression Example

A controlled candidate regression produced these artifacts — exactly the signal a release-control system should surface before deployment.

**Baseline pack**
```json
{ "avg_score_confidence_interval": { "mean": 0.794 }, "pass_rate_confidence_interval": { "mean": 1.0 } }
```

**Candidate pack**
```json
{ "avg_score_confidence_interval": { "mean": 0.0 }, "pass_rate_confidence_interval": { "mean": 0.0 } }
```

**Pack comparison**
```json
{
  "score_change_test": { "test": "welch_t_test", "p_value": 0.0 },
  "pass_fail_distribution_test": { "test": "chi_squared", "p_value": 0.0 },
  "drift_significant": true
}
```

**Gate decision**
```json
{
  "decision": "block",
  "rollback_recommendation": "rollback_to_baseline",
  "reasons": ["candidate quality regressed beyond configured release thresholds"]
}
```

---

## Live Demo

🔗 [FairEval on Hugging Face](https://huggingface.co/spaces/kriti0608/FairEval-Suite) — accepts baseline and candidate responses, applies configurable regression thresholds, and outputs a gate decision with a downloadable artifact JSON.

![FairEval Hugging Face Demo](https://github.com/kritibehl/FairEval-Suite/raw/main/docs/images/hf-demo-full.png)

![FairEval Gate Controls and Delta Summary](https://github.com/kritibehl/FairEval-Suite/raw/main/docs/images/hf-demo-gate.png)

---

## Release Workflow

```
baseline run → candidate run → compare artifact → gate decision → ship or block
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

Suites are structured JSONL cases with explicit expected outputs — auditable and version-controlled.

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

### Baseline vs. Candidate Comparison

```json
{
  "avg_score_delta": -0.18,
  "pass_rate_delta": -0.40,
  "regressed_cases": ["case-3", "case-5"]
}
```

### Configurable Release Gate

```
max_avg_score_drop          = 0.05
max_pass_rate_drop          = 0.10
fail_on_any_regression_case = true

decision: FAIL
reason:   pass_rate_drop_exceeded
```

### Repeated-Run Pack Evaluation

Distinguishes deterministic regressions from run-to-run variance via confidence intervals, Welch t-test, and chi-squared pass/fail distribution checks.

### Versioned Artifacts

| Directory | Contents |
|---|---|
| `runs/` | Raw model outputs |
| `reports/` | Evaluation summaries |
| `compare/` | Baseline vs. candidate diffs |
| `gate/` | Release gate decisions |
| `packs/` | Repeated benchmark runs |
| `dashboard_exports/` | BI-ready CSVs |

---

## Quickstart

```bash
git clone https://github.com/kritibehl/FairEval-Suite.git
cd FairEval-Suite

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Full Release Check Workflow

```bash
# Step 1 — Baseline
python3 -m evals.cli run --suite rag_basic --model mock --out-dir .

# Step 2 — Candidate
python3 -m evals.cli run --suite rag_basic --model mock_regressed --out-dir .

# Step 3 — Compare
python3 -m evals.cli compare \
  --baseline <baseline_run_id> \
  --candidate <candidate_run_id> \
  --reports-dir ./reports \
  --out-dir .

# Step 4 — Gate
python3 -m evals.cli gate \
  --compare-artifact compare/<artifact>.json \
  --out-dir .
```

### Repeated-Run Pack Workflow

```bash
python3 -m evals.cli run-pack --suite rag_basic --model mock --repeat-count 4 --out-dir .
python3 -m evals.cli run-pack --suite rag_basic --model mock_regressed --repeat-count 4 --out-dir .

python3 -m evals.cli compare-packs \
  --baseline-pack-path packs/<baseline_pack>.json \
  --candidate-pack-path packs/<candidate_pack>.json \
  --out-dir .
```

### Export Dashboard Data

```bash
python3 -m evals.cli export-dashboard --out-dir .
```

---

## Real Transformer Support

The default evaluation path is deterministic mock — no GPU required, CI-portable. For live transformer validation:

```bash
python3 -m evals.cli run --suite classification_basic --model distilbert-sst2
```

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

**Deterministic mock evaluation** — full pipeline in CI, no GPU required.  
**Artifact-based outputs** — every run debuggable in isolation.  
**Dataset-driven suites** — new eval cases require no code changes.  
**Statistical confidence layer** — Welch t-test and chi-squared separate real regressions from noise.  
**SQL-indexed artifact history + JSONL trace store** — structured release traceability.  
**BI-ready exports** — `runs.csv`, `compares.csv`, `gates.csv` for Power BI / Tableau / QuickSight.

---

## Data Integrity Checks

- Duplicate-case and duplicate-payload detection
- Missing expected field detection
- Schema conformance validation
- Stale baseline warning hooks

---

## Repo Structure

```
FairEval-Suite/
├── api/                    FastAPI service
├── artifacts/              SQLite index + JSONL trace metadata
├── compare/                Baseline vs. candidate diffs
├── dashboard_exports/      BI-ready CSVs and dashboard spec
├── datasets/               Suite definitions (JSONL cases)
├── evals/                  Scoring, compare, gate, pack, stats logic
├── gate/                   Release gate outputs
├── packs/                  Repeated benchmark artifacts
├── reports/                Evaluation summaries
├── runs/                   Raw model outputs
└── tests/                  Evaluation coverage
```

---

## Running Tests

```bash
pytest
```

---

## Why This Project Matters

FairEval is a release-review system for AI changes — not a benchmark tool. It makes model changes measurable, comparable, and blockable before they reach production, which is directly relevant for AI infra, evaluation platform, and release-safety roles.

---

## Related Projects

- [Faultline](https://github.com/kritibehl/faultline) — correctness under failure for distributed systems
- [KubePulse](https://github.com/kritibehl/KubePulse) — resilience validation
- [DetTrace](https://github.com/kritibehl/dettrace) — incident replay and divergence analysis
- [AutoOps-Insight](https://github.com/kritibehl/autoops-insight) — operator-facing incident triage

---

## Tech Stack

Python · FastAPI · Typer · SQLite · SciPy · HuggingFace Transformers · PyTorch

---

## License

MIT

## Hardware-Aware Release Gate

FairEval supports hardware-aware release gating, where a candidate can preserve model quality yet still be blocked if it regresses serving behavior on target hardware.

Example AMD MI300X-style gate result:

- `quality_pass = true`
- `latency_pass = false`
- `release_decision = block`

This captures a production scenario where output quality remains acceptable, but p95 serving latency regresses enough to make the candidate unsafe to ship.

Example artifact:

`artifacts/amd_mi300x/gate/compare_serving_regression.gate.json`

Run it from the CLI:

```bash
python -m evals.cli gate \
  --compare-artifact artifacts/amd_mi300x/compare_serving_regression.json \
  --out-dir artifacts/amd_mi300x \
  --max-latency-p95-regression-pct 20 \
  --max-throughput-drop-pct 15

## Hardware-Aware Eval Gate

FairEval supports hardware-aware release gating, where a model candidate can preserve output quality yet still be blocked if it regresses serving behavior on target hardware.

Example AMD MI300X-style result:

- `summary.quality_pass = true`
- `serving_gate.latency_pass = false`
- `release_decision = block`

In the included example, the candidate preserved quality parity but showed a 47.1014% p95 latency regression, so the release was blocked.

Generate compare artifact:

```bash
python scripts/amd/build_hardware_compare.py
Apply gate:

python -m evals.cli gate \
  --compare-artifact artifacts/amd_mi300x/compare_serving_regression.json \
  --out-dir artifacts/amd_mi300x \
  --max-latency-p95-regression-pct 20 \
  --max-throughput-drop-pct 15

