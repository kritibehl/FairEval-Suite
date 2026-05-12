# Evaluator Drift Analysis

FairEval compares prompt, evaluator, threshold, dataset, and failed-case changes across benchmark runs.

- runs analyzed: 7
- lineage records: 2

## Drift dimensions
- prompt version drift
- evaluator version drift
- threshold version drift
- dataset hash drift
- failed-case set changes

## Run summary

| Run ID | Model | Prompt | Evaluator | Threshold | Avg Score | Pass Rate | Failed |
|---|---|---|---|---|---:|---:|---:|
| `20260412T171732.034140Z_benchmark_instruction_following_gemini_real_3067befa3a60` | gemini_real | unknown | unknown | unknown | 0.0 | 0.0 | 10 |
| `20260412T183717.101345Z_benchmark_instruction_following_gemini_real_3067befa3a60` | gemini_real | unknown | unknown | unknown | 0.0 | 0.0 | 10 |
| `20260412T185512.139379Z_benchmark_instruction_following_gemini_real_3067befa3a60` | gemini_real | unknown | unknown | unknown | 0.0 | 0.0 | 10 |
| `20260412T190324.891307Z_benchmark_instruction_following_gemini_real_3067befa3a60` | gemini_real | unknown | unknown | unknown | 0.3667 | 0.4 | 6 |
| `20260415T203612.588432Z_benchmark_instruction_following_openai_real_b75a5c833044` | openai_real | unknown | unknown | unknown | 0.0 | 0.0 | 10 |
| `20260415T203654.860666Z_benchmark_instruction_following_openai_real_b75a5c833044` | openai_real | prompt_v1 | rag_overlap_v1 | release_gate_v1 | 0.0 | 0.0 | 10 |
| `20260508T212003.905573Z_benchmark_instruction_following_gemini_real_3067befa3a60` | gemini_real | prompt_v1 | rag_overlap_v1 | release_gate_v1 | 0.0 | 0.0 | 10 |

## Pairwise drift comparisons

| Baseline | Candidate | Prompt drift | Evaluator drift | Threshold drift | Dataset drift | Avg Δ | Pass Δ | New failures | Resolved failures |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `20260412T171732.034140Z_benchmark_instruction_following_gemini_real_3067befa3a60` | `20260412T183717.101345Z_benchmark_instruction_following_gemini_real_3067befa3a60` | False | False | False | False | 0 | 0 | - | - |
| `20260412T183717.101345Z_benchmark_instruction_following_gemini_real_3067befa3a60` | `20260412T185512.139379Z_benchmark_instruction_following_gemini_real_3067befa3a60` | False | False | False | False | 0 | 0 | - | - |
| `20260412T185512.139379Z_benchmark_instruction_following_gemini_real_3067befa3a60` | `20260412T190324.891307Z_benchmark_instruction_following_gemini_real_3067befa3a60` | False | False | False | False | 0.3667 | 0.4 | - | if-001, if-002, if-003, if-005 |
| `20260412T190324.891307Z_benchmark_instruction_following_gemini_real_3067befa3a60` | `20260415T203612.588432Z_benchmark_instruction_following_openai_real_b75a5c833044` | False | False | False | False | -0.3667 | -0.4 | if-001, if-002, if-003, if-005 | - |
| `20260415T203612.588432Z_benchmark_instruction_following_openai_real_b75a5c833044` | `20260415T203654.860666Z_benchmark_instruction_following_openai_real_b75a5c833044` | True | True | True | True | 0 | 0 | - | - |
| `20260415T203654.860666Z_benchmark_instruction_following_openai_real_b75a5c833044` | `20260508T212003.905573Z_benchmark_instruction_following_gemini_real_3067befa3a60` | False | False | False | False | 0 | 0 | - | - |
