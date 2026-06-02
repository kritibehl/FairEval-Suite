# FairEval Architecture Diagram

```mermaid
flowchart TD
    A[Dataset Versions] --> B[Benchmark Packs]
    B --> C[Baseline Run]
    B --> D[Candidate Run]
    C --> E[Evaluation Warehouse]
    D --> E

    E --> F[Regression Detection]
    F --> G[Responsible AI Gate]
    F --> H[RAG Groundedness Gate]
    F --> I[Agent Evaluation Gate]
    F --> J[Retail Search / Recommendation Eval]

    G --> K[Release Decision]
    H --> K
    I --> K
    J --> K

    K --> L[Human Review Queue]
    K --> M[Release History]
    K --> N[Dashboard / Leaderboard]

    O[Live RAI API] --> G
    P[Trace / Cost / Latency Exports] --> N
