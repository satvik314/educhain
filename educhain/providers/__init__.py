"""
Provider registry for Educhain.

Educhain talks to LLMs exclusively through the official OpenAI Python SDK.
Because most modern LLM vendors expose an *OpenAI-compatible* HTTP endpoint,
we can support a wide range of providers simply by pointing the SDK at a
different ``base_url`` and supplying the right API key.

This module curates a registry of well-known providers so users can write::

    from educhain import Educhain

    client = Educhain.from_provider("groq", model="llama-3.3-70b-versatile")

instead of remembering base URLs by hand. You can always bypass the registry
and pass a raw ``base_url`` (or a fully pre-built ``openai.OpenAI`` client) via
:class:`~educhain.core.config.LLMConfig`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Provider:
    """Metadata describing an OpenAI-compatible LLM provider."""

    name: str
    #: OpenAI-compatible base URL. ``None`` means "use the OpenAI default".
    base_url: Optional[str]
    #: Environment variables that may hold the API key, tried in order.
    api_key_envs: List[str] = field(default_factory=list)
    #: A sensible default model for quick starts (informational only).
    default_model: Optional[str] = None
    #: Hint: does this provider generally support OpenAI strict structured
    #: outputs (``response_format`` with a JSON schema)? This is only a hint
    #: used to choose which strategy to try *first* in ``"auto"`` mode; the
    #: client always falls back gracefully if the hint is wrong.
    supports_structured_outputs: bool = True
    #: Human-friendly description.
    description: str = ""

    def resolve_api_key(self, explicit: Optional[str] = None) -> Optional[str]:
        """Return the API key, preferring an explicit value then env vars."""
        if explicit:
            return explicit
        for env in self.api_key_envs:
            value = os.getenv(env)
            if value:
                return value
        return None


# ---------------------------------------------------------------------------
# Curated registry of OpenAI-compatible providers.
#
# Base URLs verified against each provider's "OpenAI compatibility" docs.
# Add new providers here; nothing else in the codebase needs to change.
# ---------------------------------------------------------------------------
_PROVIDERS: Dict[str, Provider] = {
    "openai": Provider(
        name="openai",
        base_url=None,  # SDK default: https://api.openai.com/v1
        api_key_envs=["OPENAI_API_KEY"],
        default_model="gpt-4o-mini",
        supports_structured_outputs=True,
        description="OpenAI (GPT-4o, GPT-4.1, o-series, ...).",
    ),
    "azure": Provider(
        name="azure",
        base_url=None,  # Azure needs AzureOpenAI; pass a custom client instead.
        api_key_envs=["AZURE_OPENAI_API_KEY"],
        supports_structured_outputs=True,
        description="Azure OpenAI. Pass a pre-built AzureOpenAI client via "
        "LLMConfig(client=...).",
    ),
    "groq": Provider(
        name="groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_envs=["GROQ_API_KEY"],
        default_model="llama-3.3-70b-versatile",
        supports_structured_outputs=True,
        description="Groq LPU inference (Llama, Mixtral, Gemma, ...).",
    ),
    "openrouter": Provider(
        name="openrouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_envs=["OPENROUTER_API_KEY"],
        default_model="openai/gpt-4o-mini",
        supports_structured_outputs=True,
        description="OpenRouter aggregator (routes to 200+ models).",
    ),
    "together": Provider(
        name="together",
        base_url="https://api.together.xyz/v1",
        api_key_envs=["TOGETHER_API_KEY", "TOGETHER_AI_API_KEY"],
        default_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        supports_structured_outputs=True,
        description="Together AI open-model inference.",
    ),
    "gemini": Provider(
        name="gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key_envs=["GEMINI_API_KEY", "GOOGLE_API_KEY"],
        default_model="gemini-2.0-flash",
        supports_structured_outputs=True,
        description="Google Gemini via its OpenAI-compatible endpoint.",
    ),
    "mistral": Provider(
        name="mistral",
        base_url="https://api.mistral.ai/v1",
        api_key_envs=["MISTRAL_API_KEY"],
        default_model="mistral-large-latest",
        supports_structured_outputs=True,
        description="Mistral AI.",
    ),
    "cerebras": Provider(
        name="cerebras",
        base_url="https://api.cerebras.ai/v1",
        api_key_envs=["CEREBRAS_API_KEY"],
        default_model="llama-3.3-70b",
        supports_structured_outputs=True,
        description="Cerebras ultra-fast inference.",
    ),
    "xai": Provider(
        name="xai",
        base_url="https://api.x.ai/v1",
        api_key_envs=["XAI_API_KEY"],
        default_model="grok-3",
        supports_structured_outputs=True,
        description="xAI Grok models.",
    ),
    "deepseek": Provider(
        name="deepseek",
        base_url="https://api.deepseek.com/v1",
        api_key_envs=["DEEPSEEK_API_KEY"],
        default_model="deepseek-chat",
        supports_structured_outputs=False,
        description="DeepSeek chat/reasoner models.",
    ),
    "fireworks": Provider(
        name="fireworks",
        base_url="https://api.fireworks.ai/inference/v1",
        api_key_envs=["FIREWORKS_API_KEY"],
        default_model="accounts/fireworks/models/llama-v3p3-70b-instruct",
        supports_structured_outputs=True,
        description="Fireworks AI.",
    ),
    "deepinfra": Provider(
        name="deepinfra",
        base_url="https://api.deepinfra.com/v1/openai",
        api_key_envs=["DEEPINFRA_API_KEY"],
        supports_structured_outputs=True,
        description="DeepInfra open-model inference.",
    ),
    "perplexity": Provider(
        name="perplexity",
        base_url="https://api.perplexity.ai",
        api_key_envs=["PERPLEXITY_API_KEY", "PPLX_API_KEY"],
        default_model="sonar",
        supports_structured_outputs=False,
        description="Perplexity Sonar (web-grounded) models.",
    ),
    "nvidia": Provider(
        name="nvidia",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key_envs=["NVIDIA_API_KEY"],
        supports_structured_outputs=False,
        description="NVIDIA NIM hosted models.",
    ),
    "sambanova": Provider(
        name="sambanova",
        base_url="https://api.sambanova.ai/v1",
        api_key_envs=["SAMBANOVA_API_KEY"],
        supports_structured_outputs=False,
        description="SambaNova Cloud.",
    ),
    "anthropic": Provider(
        name="anthropic",
        base_url="https://api.anthropic.com/v1/",
        api_key_envs=["ANTHROPIC_API_KEY"],
        default_model="claude-sonnet-4-5",
        supports_structured_outputs=False,
        description="Anthropic Claude via its OpenAI-compatible endpoint.",
    ),
    "ollama": Provider(
        name="ollama",
        base_url="http://localhost:11434/v1",
        api_key_envs=["OLLAMA_API_KEY"],
        default_model="llama3.2",
        supports_structured_outputs=False,
        description="Local models served by Ollama.",
    ),
}


def get_provider(name: str) -> Provider:
    """Look up a provider by (case-insensitive) name."""
    key = (name or "").strip().lower()
    if key not in _PROVIDERS:
        available = ", ".join(sorted(_PROVIDERS))
        raise ValueError(
            f"Unknown provider '{name}'. Available providers: {available}. "
            "You can also pass a raw base_url instead of a provider name."
        )
    return _PROVIDERS[key]


def list_providers() -> List[str]:
    """Return the names of all registered providers."""
    return sorted(_PROVIDERS)


def register_provider(provider: Provider) -> None:
    """Register (or override) a provider at runtime."""
    _PROVIDERS[provider.name.strip().lower()] = provider


__all__ = [
    "Provider",
    "get_provider",
    "list_providers",
    "register_provider",
]
