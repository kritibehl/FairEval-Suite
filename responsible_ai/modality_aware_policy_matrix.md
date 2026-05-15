# Modality-Aware Policy Matrix

This is a metadata/schema planning artifact for future multimodal safety evaluation.

It is **not** an implemented multimodal classifier.

## Modalities

| Modality | Example signal | Risk categories | Review behavior |
|---|---|---|---|
| text | user prompt or answer | policy_bypass, unsafe_instruction, unsupported_claim | block or hold depending on risk |
| image_metadata | alt text, labels, provenance metadata | provenance_gap, privacy_risk | require review when source is unclear |
| audio_transcript | transcript text | unsupported_claim, privacy_risk | hold when sensitive info appears |
| video_caption | generated or provided caption | provenance_gap, unsupported_claim | require grounding/context review |

## Why this matters

Responsible AI evaluation often needs a shared risk schema across modalities even before a full multimodal classifier exists.

This artifact defines the schema and review expectations without claiming implemented multimodal model behavior.
