# Baseline vs Candidate Search and Recommendation Report

## Scope
Synthetic retail-style product discovery evaluation comparing baseline and candidate search-ranking and recommendation outputs.

## Search ranking comparison

| Metric | Baseline Ranker | Candidate Ranker | Delta |
|---|---:|---:|---:|
| Precision@3 | 0.7778 | 0.6667 | -0.1111 |
| Recall@3 | 1.0 | 1.0 | 0.0 |
| NDCG@3 | 0.9012 | 0.7688 | -0.1324 |
| Ranking regressions | 0 | 2 | +2 |

Search release decision: `block_candidate`

Reason: Candidate ranker reduced NDCG@3 and introduced ranking regressions in synthetic retail discovery cases.

## Recommendation comparison

| Metric | Baseline Recommender | Candidate Recommender | Delta |
|---|---:|---:|---:|
| Hit rate | 1.0 | 1.0 | 0.0 |
| Avg recommendation precision | 0.6667 | 0.5 | -0.1667 |
| Irrelevant recommendation count | 1 | 3 | +2 |
| Quality regressions | 0 | 0 | 0 |

Recommendation release decision: `needs_review`

Reason: Candidate recommender preserved hit rate but reduced recommendation precision and increased irrelevant recommendations.

## Model lifecycle interpretation

```text
baseline search/recommendation
        ↓
candidate search/recommendation
        ↓
Precision@K / Recall@K / NDCG comparison
        ↓
regression flags
        ↓
release decision
Apple Store Online alignment

This maps to search quality, recommendation systems, product discovery, personalization evaluation, model lifecycle, continuous improvement, and release-readiness review.

Safe scope

This is a synthetic retail ML evaluation report. It does not use private customer data, production Apple data, or live Apple Store systems.
