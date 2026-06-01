# FairEval-Suite

> A production-style AI evaluation and release-safety platform that gates GenAI model deployments using regression detection, hallucination scoring, groundedness validation, and statistical significance testing.

`Python` · `FastAPI` · `SciPy` · `HuggingFace` · `SQLite`

🔗 **[Live Demo](https://huggingface.co/spaces/kriti0608/FairEval-Suite)** · 📄 **[Technical Report](https://doi.org/10.5281/zenodo.17625268)**

---

## Why This Project Matters

- Average score hides regressions: a model can hold a 0.79 average while silently failing the case class that matters most
- Most teams catch quality regressions after deployment; FairEval catches them at the gate, before they reach users
- The platform validates hardware serving safety too — a +47.1% p95 latency regression on AMD MI300X was blocked even though quality metrics passed
- This proves: AI evaluation infrastructure design, release gate engineering, statistical reasoning, and Responsible AI workflow discipline

---

## 30-Second Proof

| Signal | Verified output |
|---|---|
| False allows reduced | **16 → 0** |
| Mock regression gate decision | **BLOCK** · p=0.0 (Welch t-test + chi-squared) |
| Gemini 2.0 Flash gate decision | **BLOCK** · 40% pass rate |
| AMD MI300X p95 regression | **+47.1%** → **BLOCK** (quality metrics: PASS) |
| Reviewer agreement score | **0.7333** |
| Regression case types covered | **10** |
| GPU required | **None** — full pipeline runs in CI |

---

## Screenshots

> Add these to `docs/screenshots/` — highest ROI remaining improvement.

| Live Demo — Hugging Face | Gate Decision View |
|---|---|
| ![HF Demo](docs/images/hf-demo-full.png) | ![Gate Decision](docs/images/hf-demo-gate.png) |

**Release decision — what the comparison view shows:**

```
┌────────────────────────────────────────────────────────────────┐
│  FairEval Release Comparison                                    │
├──────────────────┬──────────────┬──────────────┬──────────────┤
│  Signal          │  Baseline    │  Candidate   │  Delta       │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│  Avg score       │  0.794       │  0.000       │  -0.794  ✗   │
│  Pass rate       │  100%        │  0%          │  -100%   ✗   │
│  Toxicity        │  0.0%        │  8.3%        │  +8.3pp  ✗   │
│  Citation cov.   │  91%         │  0%          │  -91pp   ✗   │
│  p95 latency     │  —           │  —           │  +47.1%  ✗   │
├──────────────────┴──────────────┴──────────────┴──────────────┤
│  Welch t-test: p=0.0  ·  chi-squared: p=0.0                    │
│                                                                │
│  ▶  Gate decision:  BLOCK                                      │
│     Rollback:       rollback_to_baseline                       │
│     False allows prevented:  16                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Demo

```bash
git clone https://github.com/kritibehl/FairEval-Suite
cd FairEval-Suite
make demo
```

Expected output:
```json
{
  "baseline_avg_score": 0.794,
  "candidate_avg_score": 0.000,
  "avg_score_delta": -0.794,
  "p_value_welch": 0.0,
  "p_value_chi_squared": 0.0,
  "gate_decision": "block",
  "rollback_recommendation": "rollback_to_baseline",
  "false_allows_prevented": 16
}
```

```bash
make test    # full eval suite · all gate decisions correct
make report  # comparison report → reports/latest/gate_decision.json
```

Or skip setup — use the **[live demo](https://huggingface.co/spaces/kriti0608/FairEval-Suite)**.

---

## Architecture

![FairEval Architecture](docs/architecture.png)

```
Dataset (cases.jsonl)
      │
      ▼
Model adapter  →  Gemini / OpenAI / Anthropic / mock
      │
      ▼
Scorer  →  keyword fallback / RAG-overlap / classification
      │
      ▼
Evaluation run  →  runs/<run_id>.json
      │
      ▼
Comparison engine
  avg_score_delta · pass_rate_delta · per-case regressions
  Welch t-test + chi-squared significance
      │
      ▼
Release gate  →  SHIP / BLOCK
  rollback recommendation · affected_query_pct · downstream_risk
      │
      ▼
RAI monitoring  →  toxicity · hallucination rate · quality score
```

---

## Core Workflows

### 1. Regression gate

Runs baseline and candidate, compares at case level, applies statistical significance test. Any signal outside threshold → BLOCK.

```bash
make demo
# → gate_decision: block · p_value: 0.0
```

### 2. Hallucination + groundedness validation

Checks citation coverage per answer. Zero citation coverage on a factual claim → unsupported answer → BLOCK.

| | |
|---|---|
| Prompt | What caused the outage? |
| Candidate answer | Memory leak in service X. |
| Citation coverage | 0% — unsupported |
| Decision | **BLOCK** |

### 3. Hardware serving gate

Gates on latency and throughput SLO, not just quality. Catches regressions that quality metrics miss.

| Signal | Value |
|---|---|
| Quality pass | `true` |
| AMD MI300X p95 regression | +47.1% |
| Latency gate | `false` |
| Final decision | **BLOCK** |

---

## Failure Scenarios Covered

| Regression type | Signal | Decision |
|---|---|---|
| Instruction-following drop | Pass rate collapse | **BLOCK** |
| JSON output contract break | Format regression | **BLOCK** |
| Safety style drift | Toxicity increase | **BLOCK** |
| Hallucination increase | Unsupported-answer rate up | **BLOCK** |
| Groundedness failure | Citation coverage drop | **BLOCK** |
| False allow (weak evaluator) | Unsafe answer passes baseline scorer | Flagged |
| Latency SLO violation | p95 > threshold | **BLOCK** |

---

## Engineering Decisions

**Why case-level comparison, not aggregate:** Average score obscures per-case regressions. A model that improves on easy cases while degrading on safety-critical ones shows a net-positive average. Case-level diffing surfaces this.

**Why Welch t-test + chi-squared:** Two different null hypotheses — one on means (quality), one on pass rates (binary outcomes). Running both reduces false alarm rate from scorer noise.

**Why a hardware serving gate:** A model can pass all quality evaluations but fail its serving SLO under real inference load. Quality-only gates miss this. FairEval treats latency as a first-class signal.

---

## What Is Intentionally Out of Scope

- Evaluation is simulation-based by default; live evaluation requires API keys
- Gate thresholds are static configuration, not adaptive baselines
- Designed for release-time gating, not continuous production monitoring
- Case library covers 10 failure types; coverage depends on included cases

---

## Resume Bullets

- Built an AI release safety platform with regression gating (Welch t-test + chi-squared), reducing false allows from 16 to 0 across a 10-type case library
- Detected a +47.1% p95 latency regression on AMD MI300X serving that passed all quality evaluations — blocked by the hardware serving gate
- Implemented Responsible AI monitoring (toxicity rate, hallucination detection, quality scoring) as a first-class gate signal alongside accuracy metrics

---

## Interview Walkthrough

*"FairEval answers one question: should this model change ship? Average score isn't enough — a model can degrade on the cases that matter while holding its average. FairEval compares at the case level, runs Welch t-test and chi-squared for statistical significance, and blocks on any signal outside threshold. I also added a hardware serving gate that caught a +47.1% p95 regression on AMD MI300X that quality metrics passed entirely. In controlled testing, I reduced false allows from 16 to 0."*

---

## Run Locally

```bash
git clone https://github.com/kritibehl/FairEval-Suite && cd FairEval-Suite
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make demo    # gate decision demo
make test    # full eval suite
make report  # comparison report
```

---

## Repository Map

```
FairEval-Suite/
├── evals/           Evaluation runner · scorer · adapter
├── gate/            Release gate logic + threshold config
├── compare/         Baseline vs candidate comparison engine
├── rai/             Responsible AI monitoring (toxicity · hallucination)
├── reports/         Gate decisions + comparison artifacts
├── docs/            Architecture + screenshots
└── app.py           Hugging Face demo entry point
```
