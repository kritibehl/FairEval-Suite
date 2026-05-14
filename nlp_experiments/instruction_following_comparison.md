# Instruction-Following Comparison

## Case 01 — Constrained JSON output

### Task input
Return JSON with keys `decision` and `reason`. Decision should be `review`.

### Baseline output
```json
{
  "decision": "review",
  "reason": "required fields need validation before release"
}
Candidate output
{
  "decision": "review"
}
Expected behavior

The output must include both decision and reason.

Observed failure

The candidate omitted the required reason field.

Why it matters for user-facing NLP quality

A missing field can break downstream automation even if the response appears semantically close.

Case 02 — Exact bullet-count instruction
Task input

Return exactly two bullet points explaining why evaluator drift matters.

Baseline output
- Prompt or evaluator changes can make scores incomparable across runs.
- Threshold changes can alter release decisions even when model behavior is unchanged.
Candidate output
Evaluator drift matters because it affects benchmark reliability and release decisions.
Expected behavior

The output must contain exactly two bullet points.

Observed failure

The candidate returned one prose sentence instead of two bullets.

Why it matters for user-facing NLP quality

Formatting constraints often support UI rendering, downstream parsing, and consistent product behavior.

Case 03 — Grounded answer generation
Task input

Context: The gate blocked release because required JSON fields were missing.
Question: Why was the release blocked?

Baseline output

The release was blocked because required JSON fields were missing.

Candidate output

The release was blocked because the model had high latency.

Expected behavior

The answer should be grounded only in the provided context.

Observed failure

The candidate hallucinated a latency-related reason that was not in context.

Why it matters for user-facing NLP quality

Groundedness failures can mislead users and weaken trust in AI-generated explanations.
