"""Tests for the LLMClient structured-output engine."""

from typing import List

import pytest
from pydantic import BaseModel

from educhain.core import client as client_module
from educhain.core.client import LLMClient, StructuredOutputError
from educhain.core.config import LLMConfig
from tests.conftest import usage


class Item(BaseModel):
    name: str
    qty: int


class Bag(BaseModel):
    items: List[Item]


@pytest.fixture(autouse=True)
def _clear_caches():
    """Keep the auto-mode capability caches from leaking across tests."""
    client_module._native_unsupported_base_urls.clear()
    client_module._non_strict_models.clear()
    yield
    client_module._native_unsupported_base_urls.clear()
    client_module._non_strict_models.clear()


def test_native_parse_returns_object(client, fake_openai):
    bag = Bag(items=[Item(name="apple", qty=3)])
    fake_openai.set_parsed(bag, usage=usage())
    out = client.generate(Bag, prompt="give me a bag", system="be helpful")
    assert out.items[0].name == "apple"
    # response_format should be the pydantic model
    _, kwargs = fake_openai.chat.completions.parse.call_args
    assert kwargs["response_format"] is Bag


def test_refusal_raises(client, fake_openai):
    fake_openai.set_parsed(None, refusal="I can't help with that")
    with pytest.raises(StructuredOutputError):
        client.generate(Bag, prompt="x")


def test_json_fallback_when_native_fails(fake_openai):
    cfg = LLMConfig(client=fake_openai, model="m", base_url="https://api.groq.com/openai/v1")
    c = LLMClient(cfg)
    fake_openai.fail_parse()
    fake_openai.set_content('```json\n{"items":[{"name":"pen","qty":2}]}\n```')
    out = c.generate(Bag, prompt="bag please")
    assert out.items[0].name == "pen"


def test_json_mode_explicit(fake_openai):
    cfg = LLMConfig(client=fake_openai, model="m", structured_mode="json")
    c = LLMClient(cfg)
    fake_openai.set_content('{"items": [{"name": "x", "qty": 1}]}')
    out = c.generate(Bag, prompt="x")
    assert out.items == [Item(name="x", qty=1)]
    fake_openai.chat.completions.parse.assert_not_called()


def test_native_mode_does_not_fall_back(fake_openai):
    cfg = LLMConfig(client=fake_openai, model="m", structured_mode="native")
    c = LLMClient(cfg)
    fake_openai.fail_parse(ValueError("boom"))
    with pytest.raises(Exception):
        c.generate(Bag, prompt="x")
    fake_openai.chat.completions.create.assert_not_called()


def test_auto_caches_non_strict_model(fake_openai):
    cfg = LLMConfig(client=fake_openai, model="m")  # openai default => native first
    c = LLMClient(cfg)
    fake_openai.fail_parse()
    fake_openai.set_content('{"items": []}')
    c.generate(Bag, prompt="x")
    # After one failure the model is remembered as non-strict.
    assert Bag.__qualname__ in client_module._non_strict_models
    # Second call should skip native entirely.
    fake_openai.chat.completions.parse.reset_mock()
    c.generate(Bag, prompt="y")
    fake_openai.chat.completions.parse.assert_not_called()


def test_bad_json_raises_structured_error(fake_openai):
    cfg = LLMConfig(client=fake_openai, model="m", structured_mode="json")
    c = LLMClient(cfg)
    fake_openai.set_content("this is not json at all")
    with pytest.raises(StructuredOutputError):
        c.generate(Bag, prompt="x")


def test_usage_tracking(client, fake_openai):
    fake_openai.set_parsed(Bag(items=[]), usage=usage(7, 3, 10))
    with client.track_usage() as u:
        client.generate(Bag, prompt="x")
        client.generate(Bag, prompt="y")
    assert u.requests == 2
    assert u.total_tokens == 20


def test_complete_returns_text(client, fake_openai):
    fake_openai.set_content("hello world")
    assert client.complete("hi") == "hello world"


def test_embed_returns_vectors(client, fake_openai):
    fake_openai.set_embeddings([[0.1, 0.2], [0.3, 0.4]])
    vectors = client.embed(["a", "b"])
    assert vectors == [[0.1, 0.2], [0.3, 0.4]]


def test_build_messages_with_system():
    msgs = LLMClient.build_messages(prompt="hi", system="sys")
    assert msgs == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "hi"},
    ]


def test_image_message_shape():
    msg = LLMClient.image_message("describe", "http://img", detail="high")
    assert msg["role"] == "user"
    assert msg["content"][0]["type"] == "text"
    assert msg["content"][1]["image_url"]["url"] == "http://img"


def test_parse_json_payload_slices_braces():
    out = LLMClient._parse_json_payload(
        'Sure! Here you go: {"items": [{"name": "z", "qty": 9}]} Hope that helps.',
        Bag,
    )
    assert out.items[0].name == "z"
