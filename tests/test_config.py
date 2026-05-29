"""Tests for LLMConfig and provider resolution."""


import pytest

from educhain import LLMConfig, get_provider, list_providers
from educhain.providers import Provider, register_provider


def test_default_config_uses_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-default")
    cfg = LLMConfig()
    assert cfg.model == "gpt-4o-mini"
    assert cfg.base_url is None
    assert cfg.api_key == "sk-default"
    assert cfg.supports_native_structured is True


def test_provider_preset_resolves_base_url_and_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gk-123")
    cfg = LLMConfig(provider="groq")
    assert cfg.base_url == "https://api.groq.com/openai/v1"
    assert cfg.api_key == "gk-123"
    # provider's default model is filled in when caller omits one
    assert cfg.model == "llama-3.3-70b-versatile"


def test_explicit_base_url_overrides_provider():
    cfg = LLMConfig(provider="groq", base_url="https://custom/v1", api_key="x")
    assert cfg.base_url == "https://custom/v1"


def test_explicit_api_key_beats_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "from-env")
    cfg = LLMConfig(provider="groq", api_key="explicit")
    assert cfg.api_key == "explicit"


def test_unknown_provider_raises():
    with pytest.raises(ValueError):
        LLMConfig(provider="does-not-exist")


def test_legacy_model_name_alias_warns():
    with pytest.warns(DeprecationWarning):
        cfg = LLMConfig(model_name="gpt-4o")
    assert cfg.model == "gpt-4o"


def test_legacy_custom_model_maps_to_client():
    sentinel = object()
    with pytest.warns(DeprecationWarning):
        cfg = LLMConfig(custom_model=sentinel)
    assert cfg.client is sentinel


def test_unexpected_kwarg_raises():
    with pytest.raises(TypeError):
        LLMConfig(nonsense=True)


def test_list_providers_includes_common_ones():
    names = list_providers()
    for expected in ("openai", "groq", "gemini", "openrouter", "together"):
        assert expected in names


def test_register_custom_provider():
    register_provider(Provider(name="myprov", base_url="https://my/v1", api_key_envs=["MY_KEY"]))
    assert get_provider("MyProv").base_url == "https://my/v1"
