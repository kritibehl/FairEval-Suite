# Optional model/provider imports so CI and local tests do not require all SDKs.

from .mock import MockModelClient
from .mock_regressed import MockRegressedModelClient

try:
    from .distilbert_sst2 import DistilBertSST2ModelClient
except Exception:
    DistilBertSST2ModelClient = None

try:
    from .real.openai_real import OpenAIRealModelClient
except Exception:
    OpenAIRealModelClient = None

try:
    from .real.gemini_real import GeminiRealModelClient
except Exception:
    GeminiRealModelClient = None

try:
    from .real.anthropic_real import AnthropicRealModelClient
except Exception:
    AnthropicRealModelClient = None
