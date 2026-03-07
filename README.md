# FairEval

[![Tests](https://github.com/kritibehl/FairEval-Suite/actions/workflows/test.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)
[![Release Gate](https://github.com/kritibehl/FairEval-Suite/actions/workflows/release-gate.yml/badge.svg)](https://github.com/kritibehl/FairEval-Suite/actions)

Evaluation and regression-gating platform for ML / GenAI releases.

FairEval turns model evaluation into a **release safety check**.

Instead of relying on manual spot checks, FairEval:

• runs deterministic evaluation suites  
• compares baseline vs candidate model behavior  
• detects regressions  
• applies threshold-based release gates  
• generates machine-readable artifacts  

This allows teams to prevent degraded model outputs from shipping.

---

## Architecture

```
dataset
  ↓
model execution
  ↓
scoring
  ↓
evaluation report
  ↓
baseline vs candidate comparison
  ↓
release gate decision
```

---

## Key Capabilities

### Dataset-Driven Evaluation

Evaluation suites are defined as JSONL datasets. Each case includes:

- prompt
- context
- expected behavior
- optional evaluation hints

Example case:

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

### Deterministic Scoring

Scorers implement deterministic evaluation logic.

**RagOverlapScorer** measures grounding quality using:

- context precision
- context recall
- token overlap between answer and retrieved context

The scorer produces a score, pass/fail result, and detailed metrics.

---

### Evaluation Runs

Running an evaluation suite produces two artifacts:

**Run artifact** — contains model outputs, evaluation inputs, and scoring details:
```
runs/<run_id>.json
```

**Report artifact** — contains per-case results and summary metrics:
```
reports/<run_id>.json
```

Example summary:

```json
{
  "num_cases": 50,
  "avg_score": 0.81,
  "pass_rate": 0.92
}
```

---

### Baseline vs Candidate Comparison

FairEval compares evaluation runs to detect regressions. Comparison computes:

- score deltas
- pass-rate deltas
- per-case regressions
- per-case improvements

Example comparison output:

```json
{
  "avg_score_delta": -0.08,
  "pass_rate_delta": -0.15,
  "top_regressions": [...]
}
```

Compare artifacts are written to:
```
compare/<candidate>_vs_<baseline>.json
```

---

### Release Gate Decisions

FairEval applies configurable thresholds to determine if a candidate build should be accepted or rejected.

Example gate rules:

```
max_avg_score_drop = 0.05
max_pass_rate_drop = 0.10
fail_on_any_regression_case = false
```

Example gate output:

```
decision: fail
reasons:
  - avg_score_drop_exceeded
```

Gate artifacts are written to:
```
gate/<compare_id>.gate.json
```

---

## CLI Usage

### Run an evaluation suite

```bash
eval run --suite rag_basic --model mock
```

Produces `runs/<run_id>.json` and `reports/<run_id>.json`.

### Compare two runs

```bash
eval compare \
  --baseline <baseline_run_id> \
  --candidate <candidate_run_id>
```

Produces `compare/<candidate>_vs_<baseline>.json`.

### Apply a release gate

```bash
eval gate \
  --compare-artifact compare/<artifact>.json
```

Produces `gate/<artifact>.gate.json`.

---

## Artifact Structure

```
runs/        # raw model outputs + scoring details
reports/     # per-case results + summary metrics
compare/     # baseline vs candidate deltas
gate/        # release gate decisions
```

All artifacts are JSON for easy consumption by CI pipelines or dashboards.

---

## Testing

FairEval includes unit tests for scoring logic, the evaluation pipeline, baseline vs candidate comparison, and release gate logic.

```bash
pytest
```

---

## Why FairEval Exists

Many teams evaluate LLM systems using manual testing or ad-hoc scripts. FairEval treats evaluation as **release infrastructure** — making model behavior regressions detectable, reproducible, and automatable.

---

## Project Status

**Current features:**
- Dataset-driven evaluation
- Deterministic scoring
- Evaluation runner
- Baseline vs candidate comparison
- Configurable release gates
- CLI workflow
- Test coverage for core pipeline

**Planned:**
- HTML regression reports
- CI integration for automatic release gating
- Additional scoring modules
- Evaluation dashboards
- More realistic model clients

---

## License

MIT