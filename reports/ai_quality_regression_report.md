# AI Quality Regression Report

## Summary

| Signal | Baseline | Candidate |
|---|---:|---:|
| Groundedness | 1.00 | 0.67 |
| Hallucination Count | 0 | 2 |
| Prompt/Output Comparison | Stable | Regression |

## Regression Analysis

- Groundedness decreased by **0.33**
- Hallucination count increased
- Candidate output introduced unsupported responses

## Release Decision

**BLOCK**

Reason:

- groundedness regression
- hallucination regression

## Safe Scope

Synthetic AI quality regression gate demonstrating baseline-vs-candidate comparison and release decision logic.
