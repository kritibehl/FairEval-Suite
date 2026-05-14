# Transformer Output Failure Examples

## Failure 01 — Entity omitted

### Input
Return JSON with keys `decision` and `reason`.

### Output
```json
{
  "decision": "ship"
}
Analysis

The model omitted the required reason entity. This is a structured-output failure, not just a style issue.

Failure 02 — Unsupported answer
Input

Context: The evaluator detected schema breaks.
Question: What issue was detected?

Output

The evaluator detected a latency regression.

Analysis

The output is unsupported by the context. This should be classified as an unsupported answer or hallucinated detail.

Failure 03 — Formatting violation
Input

Return exactly three bullets.

Output

The model should be tested carefully before release.

Analysis

The content may be reasonable, but it violates the required format.

Failure 04 — Verbosity mismatch
Input

Generate a short smart-reply style response.

Output

Thank you for providing this detailed update. I appreciate the information and will carefully review the results, evaluate the release risk, and determine next steps after additional investigation.

Analysis

The output is polite but too verbose for a smart-reply-style task.

Failure 05 — Groundedness gap
Input

Context: Release was blocked because the required reason field was missing.

Output

The release was blocked because the response failed validation.

Analysis

The answer is directionally correct but less grounded than expected because it omits the specific missing reason field.
