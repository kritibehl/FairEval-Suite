# How FairEval Works

FairEval is an AI evaluation and release-safety platform for synthetic GenAI, RAG, agentic, retail ML, and Responsible AI workflows.

## 1. Track inputs

FairEval tracks:
- dataset versions
- model versions
- prompt versions
- benchmark packs
- baseline and candidate runs

## 2. Run evaluations

Evaluation packs cover:
- text generation quality
- RAG groundedness
- hallucination / unsupported-answer detection
- Responsible AI false allows
- agent tool-call correctness
- retail search ranking
- recommendation quality
- dataset drift
- reviewer agreement

## 3. Detect regressions

FairEval compares baseline and candidate outputs using:
- groundedness checks
- instruction-following checks
- Precision@K / Recall@K / NDCG
- hallucination flags
- release-safety risk categories
- latency and cost thresholds

## 4. Gate releases

Candidate runs can be:
- shipped
- blocked
- sent to human review
- rolled back to baseline

## 5. Verify quickly

Hiring teams can verify:
- live Responsible AI API
- release gate artifacts
- evaluation warehouse reports
- dashboard frontend
- leaderboard HTML
- dataset drift report
- human reviewer agreement report
- release history timeline
