"""
The :class:`Educhain` client - the main entry point to the library.

``Educhain`` ties a single :class:`~educhain.core.client.LLMClient` to the two
engines that do the work:

* ``client.qna``     - :class:`~educhain.engines.qna_engine.QnAEngine`
* ``client.content`` - :class:`~educhain.engines.content_engine.ContentEngine`

Quick start::

    from educhain import Educhain

    client = Educhain()                       # uses OPENAI_API_KEY
    mcqs = client.qna.generate("Photosynthesis", num=5)
    mcqs.show()

Other providers::

    client = Educhain.from_provider("groq", model="llama-3.3-70b-versatile")
    client = Educhain.from_client(my_openai_client, model="gpt-4o")
"""

from __future__ import annotations

from typing import Any, Optional

from educhain.core.client import LLMClient
from educhain.core.config import LLMConfig
from educhain.engines.content_engine import ContentEngine
from educhain.engines.qna_engine import QnAEngine


class Educhain:
    """The Educhain client: a configured LLM plus the QnA and content engines."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.client = LLMClient(self.config)
        self.qna = QnAEngine(client=self.client)
        self.content = ContentEngine(client=self.client)

    # ------------------------------------------------------------------ #
    # Convenience constructors
    # ------------------------------------------------------------------ #
    @classmethod
    def from_provider(
        cls,
        provider: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> "Educhain":
        """Build a client for a named provider preset (e.g. ``"groq"``)."""
        return cls(LLMConfig(provider=provider, model=model, api_key=api_key, **kwargs))

    @classmethod
    def from_client(cls, client: Any, model: str = "gpt-4o-mini", **kwargs: Any) -> "Educhain":
        """Build from a pre-configured ``openai.OpenAI``-compatible client."""
        return cls(LLMConfig(client=client, model=model, **kwargs))

    # ------------------------------------------------------------------ #
    # Config management
    # ------------------------------------------------------------------ #
    def get_config(self) -> LLMConfig:
        return self.config

    def update_config(self, new_config: LLMConfig) -> None:
        """Swap in a new configuration and rebuild the client and engines."""
        self.config = new_config
        self.client = LLMClient(self.config)
        self.qna = QnAEngine(client=self.client)
        self.content = ContentEngine(client=self.client)

    # ------------------------------------------------------------------ #
    # Backwards-compatibility shims for the pre-1.0 API
    # ------------------------------------------------------------------ #
    @property
    def qna_engine(self) -> QnAEngine:
        return self.qna

    @property
    def content_engine(self) -> ContentEngine:
        return self.content

    def get_qna_engine(self) -> QnAEngine:
        return self.qna

    def get_content_engine(self) -> ContentEngine:
        return self.content

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Educhain({self.config!r})"


__all__ = ["Educhain"]
