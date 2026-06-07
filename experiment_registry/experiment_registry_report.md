# Experiment Registry Report

- total experiments: 3
- blocked or rolled back: 2
- avg score: 0.6222
- avg latency ms: 680.0
- avg cost USD: 0.007333

| Experiment | Dataset | Model | Release | Score | Latency ms | Cost USD | Decision |
|---|---|---|---|---:|---:|---:|---|
| exp-retail-rag-001 | retail_product_discovery_v1 | candidate_mock_adapter | rel-v2 | 0.7 | 950 | 0.012 | blocked |
| exp-agent-eval-001 | agent_tool_call_correctness_v1 | agentic_candidate_workflow | rel-v4 | 0.6667 | 610 | 0.006 | rolled_back |
| exp-drift-001 | retail_product_discovery_v2 | candidate_recommender_v2 | rel-v3 | 0.5 | 480 | 0.004 | needs_review |
