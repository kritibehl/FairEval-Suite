# FairEval-Suite

A lightweight, extensible toolkit for **human-aligned evaluation of generative models**.

This repo hosts the core `fair_eval` Python API that scores model outputs using:
- Simple **rubric-style scoring** (helpfulness, relevance, clarity)
- A tiny **toxicity heuristic** (keyword-based, extensible later)
- A clean `EvalResult` object you can log, serialize, or plug into dashboards.

It’s designed as a *minimal, readable* foundation that can be upgraded to use the full FairEval framework, BiasBench-Vision, or speech intent metrics later.

---

## Install (local dev)

```bash
git clone https://github.com/kritibehl/FairEval-Suite.git
cd FairEval-Suite

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt  # currently minimal; extend as needed

