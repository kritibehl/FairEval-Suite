# Evaluation Lineage Diagram

```mermaid
flowchart LR
    A[Dataset] --> B[Dataset Hash]
    C[Prompt Version] --> D[Benchmark Run]
    B --> D
    E[Model Metadata] --> D
    F[Evaluator Version] --> D
    G[Threshold Version] --> H[Gate]
    D --> I[Compare Artifact]
    I --> H
    H --> J[Release Decision]
    H --> K[Dashboard Export]
    D --> L[Run Lineage Artifact]
