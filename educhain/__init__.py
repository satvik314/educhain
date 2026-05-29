"""
Educhain - generate educational content with AI.

Educhain 1.0 is built directly on the OpenAI Python SDK and works with any
OpenAI-compatible provider (OpenAI, Groq, Gemini, OpenRouter, Together, ...).

    from educhain import Educhain

    client = Educhain()
    client.qna.generate("The water cycle", num=5).show()
"""

from educhain.core.config import LLMConfig
from educhain.core.client import LLMClient, Usage, StructuredOutputError
from educhain.core.educhain import Educhain
from educhain.providers import (
    Provider,
    get_provider,
    list_providers,
    register_provider,
)

__version__ = "1.0.0"

__all__ = [
    "Educhain",
    "LLMConfig",
    "LLMClient",
    "Usage",
    "StructuredOutputError",
    "Provider",
    "get_provider",
    "list_providers",
    "register_provider",
    "__version__",
]
