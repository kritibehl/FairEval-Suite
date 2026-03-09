import os
from typing import Any, Dict

# Avoid tokenizer parallelism issues on macOS / Apple Silicon
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class DistilBertSST2ModelClient:
    """
    Thin model adapter for real transformer inference.

    Uses:
      distilbert-base-uncased-finetuned-sst-2-english

    Input convention:
      case_input["text"] -> classification text

    Output convention:
      returns:
      "label=POSITIVE confidence=0.9987"
    """

    name = "distilbert-sst2"

    def __init__(self) -> None:
        model_id = "distilbert-base-uncased-finetuned-sst-2-english"

        # Use the Python tokenizer implementation, not the fast Rust tokenizer.
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.device = torch.device("cpu")
        self.model.to(self.device)
        self.model.eval()

    def generate(self, case_input: Dict[str, Any]) -> str:
        text = (case_input or {}).get("text", "") or ""
        if not text.strip():
            return "label=UNKNOWN confidence=0.0000"

        with torch.no_grad():
            encoded = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
            )
            encoded = {k: v.to(self.device) for k, v in encoded.items()}
            logits = self.model(**encoded).logits
            probs = torch.softmax(logits, dim=-1)[0]
            pred_idx = int(torch.argmax(probs).item())
            conf = float(probs[pred_idx].item())

        label = self.model.config.id2label[pred_idx]
        return f"label={label} confidence={conf:.4f}"
