# FairEval-Suite

A lightweight Python toolkit for evaluating generative model outputs with human-centered metrics:

- Rubric-based scoring for helpfulness, relevance, and clarity
- Simple toxicity flags over common unsafe patterns
- A clean API designed to be embedded in eval scripts, notebooks, and CI

This library is a minimal, pip-installable companion to the broader FairEval project (dashboard, benchmarks, and report).

---

## 1. Installation

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
