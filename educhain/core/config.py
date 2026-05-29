"""
Configuration for Educhain's LLM access.

``LLMConfig`` is a thin, declarative description of *how* to reach a model.
It supports three layers of provider selection (in order of precedence):

1. A fully pre-built OpenAI-compatible client via ``client=...``
   (the escape hatch — e.g. ``AzureOpenAI`` or a custom-configured ``OpenAI``).
2. A named ``provider=...`` preset (``"groq"``, ``"openrouter"``, ...) which
   fills in the right ``base_url`` and reads the right API-key env var.
3. A raw ``base_url`` + ``api_key`` for any OpenAI-compatible endpoint.

If none of the above is given, Educhain defaults to OpenAI and reads
``OPENAI_API_KEY`` from the environment.
"""

from __future__ import annotations

import os
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional

from educhain.providers import Provider, get_provider

# How structured (Pydantic) output should be obtained from the model.
#   "auto"   - try native structured outputs, fall back to JSON mode.
#   "native" - always use OpenAI strict structured outputs (chat.parse).
#   "json"   - always use JSON mode + schema-in-prompt + local validation.
StructuredMode = Literal["auto", "native", "json"]

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class LLMConfig:
    """Declarative configuration for an LLM connection.

    Args:
        model: Chat model name (e.g. ``"gpt-4o-mini"``).
        api_key: API key. Falls back to the provider's env var(s).
        provider: Named provider preset (see :func:`educhain.list_providers`).
        base_url: Raw OpenAI-compatible base URL (overrides the preset).
        temperature: Sampling temperature.
        max_tokens: Max completion tokens (``None`` lets the model decide).
        default_headers: Extra HTTP headers (e.g. OpenRouter ranking headers).
        timeout: Per-request timeout in seconds.
        max_retries: SDK-level retry count for transient errors.
        structured_mode: Strategy for structured output (see above).
        embedding_model: Model used for RAG embeddings.
        client: A pre-built ``openai.OpenAI``-compatible client (escape hatch).
        extra_body: Extra JSON body params forwarded on every request.
    """

    model: str = DEFAULT_MODEL
    api_key: Optional[str] = None
    provider: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    default_headers: Optional[Dict[str, str]] = None
    timeout: Optional[float] = None
    max_retries: int = 2
    structured_mode: StructuredMode = "auto"
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    client: Optional[Any] = None
    extra_body: Optional[Dict[str, Any]] = None

    # Resolved at init from the provider preset (if any).
    _provider: Optional[Provider] = field(default=None, init=False, repr=False)

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        max_retries: int = 2,
        structured_mode: StructuredMode = "auto",
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        client: Optional[Any] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        **legacy: Any,
    ):
        # --- Backwards-compatibility shims for the pre-1.0 API -------------
        # The old LLMConfig used `model_name` and `custom_model`.
        if model is None and "model_name" in legacy:
            warnings.warn(
                "LLMConfig(model_name=...) is deprecated; use model=...",
                DeprecationWarning,
                stacklevel=2,
            )
            model = legacy.pop("model_name")
        if client is None and legacy.get("custom_model") is not None:
            warnings.warn(
                "LLMConfig(custom_model=...) is deprecated. Pass a pre-built "
                "openai.OpenAI client via client=..., or use provider/base_url.",
                DeprecationWarning,
                stacklevel=2,
            )
            client = legacy.pop("custom_model")
        legacy.pop("custom_model", None)
        if legacy:
            raise TypeError(
                f"Unexpected LLMConfig arguments: {', '.join(sorted(legacy))}"
            )

        self.model = model or DEFAULT_MODEL
        self.provider = provider
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.default_headers = default_headers
        self.timeout = timeout
        self.max_retries = max_retries
        self.structured_mode = structured_mode
        self.embedding_model = embedding_model
        self.client = client
        self.extra_body = extra_body

        # Resolve the provider preset (if a name was given).
        self._provider = get_provider(provider) if provider else None

        # Resolve base_url from the preset unless explicitly overridden.
        if self.base_url is None and self._provider is not None:
            self.base_url = self._provider.base_url

        # Resolve the API key: explicit > provider env vars > OPENAI_API_KEY.
        if self._provider is not None:
            self.api_key = self._provider.resolve_api_key(api_key)
        else:
            self.api_key = api_key
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")

        # Default model from the provider preset when caller didn't set one.
        if model is None and self._provider and self._provider.default_model:
            self.model = self._provider.default_model

    @property
    def provider_info(self) -> Optional[Provider]:
        """The resolved :class:`Provider` preset, if one was used."""
        return self._provider

    @property
    def supports_native_structured(self) -> bool:
        """Best-effort hint about strict structured-output support."""
        if self._provider is not None:
            return self._provider.supports_structured_outputs
        # Unknown custom endpoints: assume the default (OpenAI) supports it
        # only when there's no custom base_url.
        return self.base_url is None

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        key = "set" if self.api_key else "unset"
        target = self.provider or self.base_url or "openai"
        return (
            f"LLMConfig(model={self.model!r}, target={target!r}, "
            f"api_key=<{key}>, structured_mode={self.structured_mode!r})"
        )


__all__ = ["LLMConfig", "StructuredMode", "DEFAULT_MODEL", "DEFAULT_EMBEDDING_MODEL"]
