FairEval-Suite: Evaluation Tools for LLM Alignment, Multimodal Safety & Bias

FairEval-Suite is a collection of lightweight evaluation tools for:

Large Language Models (LLMs)

speech intent systems

multimodal reasoning (audio + vision)

jailbreak detection and safety

Created during graduate research at UF to provide transparent, human-aligned evaluation, not just accuracy benchmarks.

📌 1. FairEval — Human-Aligned Evaluation for Generative Models

Repo: https://github.com/kritibehl/FairEval

Zenodo DOI: 10.5281/zenodo.17625268
ResearchGate: https://www.researchgate.net/publication/397660472

Medium overview:

https://medium.com/@kriti0608/faireval-a-human-aligned-evaluation-framework-for-generative-models-d822bfd5c99d

https://medium.com/@kriti0608/i-didnt-have-a-big-research-lab-so-i-built-my-own-ai-safety-tools-from-scratch-525deac360e6

Features

LLM-as-Judge rubric scoring

Safety + tone + helpfulness + reasoning scores

Group-wise toxicity & bias metrics

Human–model agreement (κ, correlation)

Interactive dashboard

Purpose
Evaluate behavior that affects trust, not just accuracy.

📌 2. SpeechIntentEval — Small-vocabulary Spoken Intent Evaluator

Repo: https://github.com/kritibehl/SpeechIntentEval

Features

Audio → intent classification

Precision, recall, confusion matrix

Lightweight baseline for speech control

Purpose
Benchmark voice-command safety and reliability.

📌 3. VoiceVisionReasoner — Audio + Image Multimodal Reasoning

Repo: https://github.com/kritibehl/VoiceVisionReasoner

Hugging Face (demo): https://huggingface.co/spaces/kriti0608/VoiceVisionReasoner

Features

Speech transcription

Vision captioning / analysis

Multimodal safety heuristics

Bias probing

Purpose
Test how models reason across modalities under real prompts.

📌 4. JailbreakDefense — Rule-Based Jailbreak Detector (Prototype)

Repo: https://github.com/kritibehl/JailBreakDefense

Hugging Face demo: https://huggingface.co/spaces/kriti0608/JailbreakDefense

Features

Detects patterns like:

ignore safety

DAN

roleplay as X

uncensored / no filter

Normalized risk score (0–1)

Repair or block output

Purpose
Transparent baseline filter for prompt moderation.

Install individual modules
git clone https://github.com/kritibehl/FairEval.git
git clone https://github.com/kritibehl/SpeechIntentEval.git
git clone https://github.com/kritibehl/VoiceVisionReasoner.git
git clone https://github.com/kritibehl/JailBreakDefense.git


Each includes a requirements.txt + quickstart.

Why FairEval-Suite exists

Most evaluation focuses on accuracy.
Real AI deployments require stability and trust:

Safety under pressure

Non-toxic responses

No demographic bias

Polite + helpful tone

Speech control reliability

Multimodal consistency

FairEval-Suite provides transparent and reproducible tooling in these areas.

Cite

Behl, K. (2025). FairEval: Human-Aligned Evaluation Framework for Generative Models.
Zenodo. https://doi.org/10.5281/zenodo.17625268

Roadmap

Unified scoring API

Docker deployment

Stable bias benchmarks

Vision safety slices

End-to-end evaluator

Maintainer:
Kriti Behl — Graduate Student, Computer & Information Science & Engineering (UF)
