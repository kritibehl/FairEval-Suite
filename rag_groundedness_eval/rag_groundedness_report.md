# RAG Groundedness Evaluation Report

- total scenarios: 3
- groundedness pass count: 2
- unsupported answer count: 1
- hallucination detected count: 1
- release risk: `block`

| Scenario | Task | Grounded | Unsupported | Missing Expected | Hallucinated Terms |
|---|---|---:|---:|---|---|
| agent-001 | rag_answer | True | False | - | - |
| agent-002 | unsupported_answer | False | True | schema validation | GPU memory |
| agent-003 | tool_use_summary | True | False | - | - |
