# FairEval-Suite (upgraded local implementation)

This local implementation upgrades FairEval into a more release-grade AI evaluation system with:

- SQL-backed run, compare, gate, and pack-run indexing via SQLite
- NoSQL-style flexible trace metadata via JSONL append-only records
- BI-ready dashboard exports for Power BI / Tableau / QuickSight
- repeated-run pack support with confidence intervals, Welch t-test, and Chi-squared checks
- dataset integrity validation: duplicate detection, missing-case detection, schema conformance, stale-baseline warnings, and pack completeness
- rollback-oriented compare and gate decisions

## Example commands

```bash
python -m evals.cli run --suite rag_basic --model mock --out-dir .
python -m evals.cli run-pack --suite rag_basic --model mock --repeat-count 5 --out-dir .
python -m evals.cli export-dashboard --out-dir .
```
