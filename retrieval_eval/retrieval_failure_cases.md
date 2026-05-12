# Retrieval-Augmented Evaluation Failure Cases

## Case 01 — Missing context causes vague answer
Without retrieved gate artifacts, the answer only says the model performed worse.

With retrieved context, the answer identifies failed constraints and schema-sensitive output violations.

## Case 02 — Evaluator drift explanation improves with lineage context
Without retrieved lineage docs, the answer only says evaluator drift affects evaluation.

With retrieved context, the answer identifies prompt, threshold, evaluator-version, dataset-hash, and failed-case drift.

## Why this matters
Retrieval-augmented evaluation helps compare answer quality with and without grounding context. This is useful for GenAI systems where hallucination risk, missing context, and incomplete explanations can affect release decisions.

## Safe scope
This is a retrieval-evaluation artifact, not a production RAG system.
