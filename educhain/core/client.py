"""
The LLM client that powers every Educhain engine.

This is the single place where Educhain talks to an LLM. It wraps the official
``openai`` SDK and exposes three primitives the engines build on:

* :meth:`LLMClient.generate` - prompt -> validated Pydantic object.
* :meth:`LLMClient.complete` - prompt -> plain text.
* :meth:`LLMClient.embed`    - text  -> embedding vectors (for RAG).

Structured output strategy
---------------------------
OpenAI supports *strict structured outputs* (``response_format`` set to a
Pydantic model, surfaced through ``chat.completions.parse``). It is the most
reliable option, but (a) not every OpenAI-compatible provider supports it, and
(b) it can't represent every schema (e.g. free-form ``dict``/``Any`` fields).

``LLMClient`` therefore supports two strategies and an ``"auto"`` mode:

* **native** - ``chat.completions.parse`` with the Pydantic model.
* **json**   - inject the JSON schema into the prompt, request JSON output, and
  validate locally with Pydantic (works on essentially any provider).

In ``"auto"`` mode the client tries native first and transparently falls back
to json, caching capability per endpoint/model so it doesn't repeat dead ends.
"""

from __future__ import annotations

import json
import re
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Type, TypeVar

from pydantic import BaseModel, ValidationError

from educhain.core.config import LLMConfig

T = TypeVar("T", bound=BaseModel)

Message = Dict[str, Any]

# Endpoints / models known (at runtime) to reject native structured outputs.
# Cached so "auto" mode stops retrying a strategy that already failed.
_native_unsupported_base_urls: set = set()
_non_strict_models: set = set()
_cache_lock = threading.Lock()


@dataclass
class Usage:
    """Token usage accumulated across calls."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    requests: int = 0

    def add(self, prompt: int, completion: int, total: int) -> None:
        self.prompt_tokens += prompt or 0
        self.completion_tokens += completion or 0
        self.total_tokens += total or 0
        self.requests += 1

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"Usage(requests={self.requests}, prompt={self.prompt_tokens}, "
            f"completion={self.completion_tokens}, total={self.total_tokens})"
        )


@dataclass
class _RetryPolicy:
    attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 8.0

    def delay(self, attempt: int) -> float:
        return min(self.max_delay, self.base_delay * (2 ** attempt))


class StructuredOutputError(RuntimeError):
    """Raised when the model could not produce valid structured output."""


class LLMClient:
    """A provider-agnostic structured-generation client over the OpenAI SDK."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self._client = self._build_client(self.config)
        self._usage_stack: List[Usage] = []
        self._retry = _RetryPolicy()

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #
    @staticmethod
    def _build_client(config: LLMConfig):
        if config.client is not None:
            return config.client
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - import guard
            raise ImportError(
                "The 'openai' package is required. Install with: pip install openai"
            ) from exc

        kwargs: Dict[str, Any] = {}
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if config.base_url:
            kwargs["base_url"] = config.base_url
        if config.default_headers:
            kwargs["default_headers"] = config.default_headers
        if config.timeout is not None:
            kwargs["timeout"] = config.timeout
        if config.max_retries is not None:
            kwargs["max_retries"] = config.max_retries
        return OpenAI(**kwargs)

    @property
    def raw(self):
        """The underlying ``openai.OpenAI`` client, for advanced use."""
        return self._client

    # ------------------------------------------------------------------ #
    # Usage tracking (replaces langchain's get_openai_callback)
    # ------------------------------------------------------------------ #
    @contextmanager
    def track_usage(self) -> Iterator[Usage]:
        """Context manager accumulating token usage for the enclosed calls.

        Example::

            with client.track_usage() as usage:
                client.generate(...)
            print(usage.total_tokens)
        """
        usage = Usage()
        self._usage_stack.append(usage)
        try:
            yield usage
        finally:
            self._usage_stack.pop()

    def _record_usage(self, response: Any) -> None:
        if not self._usage_stack:
            return
        u = getattr(response, "usage", None)
        if u is None:
            return
        prompt = getattr(u, "prompt_tokens", 0) or 0
        completion = getattr(u, "completion_tokens", 0) or 0
        total = getattr(u, "total_tokens", 0) or (prompt + completion)
        for tracker in self._usage_stack:
            tracker.add(prompt, completion, total)

    # ------------------------------------------------------------------ #
    # Message helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def build_messages(
        prompt: Optional[str] = None,
        system: Optional[str] = None,
        messages: Optional[Sequence[Message]] = None,
    ) -> List[Message]:
        """Assemble a chat ``messages`` list from convenient pieces."""
        if messages is not None:
            return list(messages)
        out: List[Message] = []
        if system:
            out.append({"role": "system", "content": system})
        out.append({"role": "user", "content": prompt or ""})
        return out

    @staticmethod
    def image_message(
        text: str,
        image_url: str,
        detail: str = "auto",
        role: str = "user",
    ) -> Message:
        """Build a multimodal (text + image) chat message."""
        return {
            "role": role,
            "content": [
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": image_url, "detail": detail}},
            ],
        }

    # ------------------------------------------------------------------ #
    # Core: structured generation
    # ------------------------------------------------------------------ #
    def generate(
        self,
        response_model: Type[T],
        prompt: Optional[str] = None,
        *,
        system: Optional[str] = None,
        messages: Optional[Sequence[Message]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        **extra: Any,
    ) -> T:
        """Generate a validated instance of ``response_model``.

        Raises :class:`StructuredOutputError` if a valid object can't be parsed.
        """
        msgs = self.build_messages(prompt=prompt, system=system, messages=messages)
        mode = self.config.structured_mode

        if mode == "native":
            return self._generate_native(response_model, msgs, temperature, max_tokens, model, extra)
        if mode == "json":
            return self._generate_json(response_model, msgs, temperature, max_tokens, model, extra)

        # auto: try native (unless we already know it won't work), else json.
        if self._should_try_native(response_model):
            try:
                return self._generate_native(
                    response_model, msgs, temperature, max_tokens, model, extra
                )
            except StructuredOutputError:
                # A refusal or empty parse is a real, terminal result - falling
                # back to JSON mode would not help, so let it propagate.
                raise
            except Exception:
                # A capability error (provider/SDK/schema) - remember it and
                # fall back to JSON mode.
                self._remember_native_failure(response_model)
        return self._generate_json(response_model, msgs, temperature, max_tokens, model, extra)

    def _should_try_native(self, response_model: Type[BaseModel]) -> bool:
        with _cache_lock:
            if (self.config.base_url or "openai") in _native_unsupported_base_urls:
                return False
            if response_model.__qualname__ in _non_strict_models:
                return False
        return self.config.supports_native_structured

    def _remember_native_failure(self, response_model: Type[BaseModel]) -> None:
        with _cache_lock:
            _non_strict_models.add(response_model.__qualname__)

    def _common_kwargs(
        self,
        temperature: Optional[float],
        max_tokens: Optional[int],
        model: Optional[str],
        extra: Dict[str, Any],
    ) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "model": model or self.config.model,
            "temperature": self.config.temperature if temperature is None else temperature,
        }
        mt = self.config.max_tokens if max_tokens is None else max_tokens
        if mt is not None:
            kwargs["max_tokens"] = mt
        if self.config.extra_body:
            kwargs["extra_body"] = dict(self.config.extra_body)
        kwargs.update(extra)
        return kwargs

    def _generate_native(
        self, response_model, messages, temperature, max_tokens, model, extra
    ):
        kwargs = self._common_kwargs(temperature, max_tokens, model, extra)

        def _call():
            return self._client.chat.completions.parse(
                messages=messages, response_format=response_model, **kwargs
            )

        response = self._with_retry(_call)
        self._record_usage(response)
        message = response.choices[0].message
        if getattr(message, "refusal", None):
            raise StructuredOutputError(f"Model refused the request: {message.refusal}")
        parsed = message.parsed
        if parsed is None:
            raise StructuredOutputError("Native structured parse returned no object.")
        return parsed

    def _generate_json(
        self, response_model, messages, temperature, max_tokens, model, extra
    ):
        schema = json.dumps(response_model.model_json_schema(), indent=2)
        instruction = (
            "Respond with a single JSON object that strictly conforms to the "
            "following JSON schema. Output only the JSON object - no markdown "
            "fences, no commentary.\n\nJSON schema:\n" + schema
        )
        msgs = self._augment_with_instruction(messages, instruction)
        kwargs = self._common_kwargs(temperature, max_tokens, model, extra)

        def _call(use_response_format: bool):
            call_kwargs = dict(kwargs)
            if use_response_format:
                call_kwargs["response_format"] = {"type": "json_object"}
            return self._client.chat.completions.create(messages=msgs, **call_kwargs)

        try:
            response = self._with_retry(lambda: _call(True))
        except Exception:
            # Some providers reject response_format={"type":"json_object"}.
            response = self._with_retry(lambda: _call(False))

        self._record_usage(response)
        content = response.choices[0].message.content or ""
        return self._parse_json_payload(content, response_model)

    @staticmethod
    def _augment_with_instruction(messages: List[Message], instruction: str) -> List[Message]:
        msgs = [dict(m) for m in messages]
        # Prefer extending an existing system message; else prepend one.
        for m in msgs:
            if m.get("role") == "system" and isinstance(m.get("content"), str):
                m["content"] = m["content"] + "\n\n" + instruction
                return msgs
        msgs.insert(0, {"role": "system", "content": instruction})
        return msgs

    @staticmethod
    def _parse_json_payload(content: str, response_model: Type[T]) -> T:
        text = content.strip()
        # Strip ```json ... ``` fences if present.
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text).strip()
        # First try the whole payload, then the outermost {...} slice.
        candidates = [text]
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidates.append(text[start : end + 1])
        last_error: Optional[Exception] = None
        for candidate in candidates:
            try:
                return response_model.model_validate_json(candidate)
            except ValidationError as exc:
                last_error = exc
            except Exception as exc:  # noqa: BLE001 - includes JSON errors
                last_error = exc
        raise StructuredOutputError(
            f"Could not parse a valid {response_model.__name__} from model output. "
            f"Last error: {last_error}\n--- Raw output ---\n{content[:2000]}"
        )

    # ------------------------------------------------------------------ #
    # Plain-text completion
    # ------------------------------------------------------------------ #
    def complete(
        self,
        prompt: Optional[str] = None,
        *,
        system: Optional[str] = None,
        messages: Optional[Sequence[Message]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        **extra: Any,
    ) -> str:
        """Return the model's plain-text response."""
        msgs = self.build_messages(prompt=prompt, system=system, messages=messages)
        kwargs = self._common_kwargs(temperature, max_tokens, model, extra)
        response = self._with_retry(
            lambda: self._client.chat.completions.create(messages=msgs, **kwargs)
        )
        self._record_usage(response)
        return response.choices[0].message.content or ""

    # ------------------------------------------------------------------ #
    # Embeddings (for RAG)
    # ------------------------------------------------------------------ #
    def embed(self, texts: Sequence[str], model: Optional[str] = None) -> List[List[float]]:
        """Embed a batch of texts into vectors."""
        response = self._with_retry(
            lambda: self._client.embeddings.create(
                model=model or self.config.embedding_model, input=list(texts)
            )
        )
        return [item.embedding for item in response.data]

    # ------------------------------------------------------------------ #
    # Retry helper (transient errors only)
    # ------------------------------------------------------------------ #
    def _with_retry(self, call):
        try:
            from openai import APIConnectionError, APITimeoutError, RateLimitError, InternalServerError

            transient: Tuple[type, ...] = (
                APIConnectionError,
                APITimeoutError,
                RateLimitError,
                InternalServerError,
            )
        except Exception:  # pragma: no cover - import guard
            transient = ()

        last_exc: Optional[Exception] = None
        for attempt in range(self._retry.attempts):
            try:
                return call()
            except transient as exc:  # type: ignore[misc]
                last_exc = exc
                if attempt == self._retry.attempts - 1:
                    break
                time.sleep(self._retry.delay(attempt))
        assert last_exc is not None
        raise last_exc


__all__ = ["LLMClient", "Usage", "StructuredOutputError"]
