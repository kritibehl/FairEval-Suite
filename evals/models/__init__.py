# Optional provider imports so local tests / CI do not require all SDKs installed.

from .mock import MockModelClient
from .mock_regressed import MockRegressedModelClient
from .distilbert_sst2 import DistilBertSST2ModelClient

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
