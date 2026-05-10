# Evaluator Disagreement Examples

## Example 01 — Partial instruction completion

### Reviewer A
Marked as pass because the primary task was completed.

### Reviewer B
Marked as fail because one required constraint was omitted.

### Resolution
Treat required constraints as mandatory for pass classification.

---

## Example 02 — Schema-valid but semantically incomplete

### Reviewer A
Accepted because JSON schema validated successfully.

### Reviewer B
Rejected because required semantic content was missing.

### Resolution
Schema validation alone is insufficient; semantic completeness must also be reviewed.

---

## Example 03 — Formatting drift

### Reviewer A
Accepted because the answer remained readable.

### Reviewer B
Rejected because downstream parsers require exact formatting.

### Resolution
Formatting regressions should be classified as operational failures when downstream systems depend on strict output structure.
