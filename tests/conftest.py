"""Shared test fixtures.

These tests never hit the network: a fake OpenAI client lets us drive the
structured-output paths (native parse, JSON fallback), completions and
embeddings deterministically.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from educhain import Educhain, LLMConfig
from educhain.core.client import LLMClient


class FakeOpenAI:
    """A minimal stand-in for ``openai.OpenAI`` used in tests."""

    def __init__(self):
        self.chat = MagicMock()
        self.embeddings = MagicMock()
        self.responses = MagicMock()

    # -- helpers to script responses -------------------------------------
    def set_parsed(self, obj, *, refusal=None, usage=None):
        self.chat.completions.parse.side_effect = None
        self.chat.completions.parse.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(parsed=obj, refusal=refusal))],
            usage=usage,
        )

    def fail_parse(self, exc=Exception("native unsupported")):
        self.chat.completions.parse.side_effect = exc

    def set_content(self, text, *, usage=None):
        self.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=text))],
            usage=usage,
        )

    def set_embeddings(self, vectors):
        self.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=v) for v in vectors]
        )


@pytest.fixture
def fake_openai():
    return FakeOpenAI()


@pytest.fixture
def client(fake_openai):
    """An LLMClient backed by the fake OpenAI client."""
    return LLMClient(LLMConfig(client=fake_openai, model="gpt-4o-mini"))


@pytest.fixture
def educhain(fake_openai):
    """An Educhain instance backed by the fake OpenAI client."""
    return Educhain(LLMConfig(client=fake_openai, model="gpt-4o-mini"))


def usage(prompt=10, completion=5, total=15):
    return MagicMock(prompt_tokens=prompt, completion_tokens=completion, total_tokens=total)
