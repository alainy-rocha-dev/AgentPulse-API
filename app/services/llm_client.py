"""
Minimal LLM client for OpenAI-compatible chat completions (works with Groq and OpenAI).

Configuration (environment variables):
    GROQ_API_KEY          -> Groq (https://api.groq.com/openai/v1), default model openai/gpt-oss-120b
    OPENAI_API_KEY        -> OpenAI, used when there is no Groq key, default model gpt-4o-mini
    AGENTPULSE_LLM_MODEL  -> overrides the provider's default model

The orchestrator accepts any function `prompt -> str`; this client is one of them.
Without a key, the orchestrator falls back to a built-in stub (see agent_orchestrator.py).
"""

from __future__ import annotations

import os
import time
from typing import Callable, Optional

import httpx

PROVIDERS = {
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key_env": "GROQ_API_KEY",
        "default_model": "openai/gpt-oss-120b",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
    },
}

SYSTEM_PROMPT = (
    "You are an analysis agent inside an automated pipeline. "
    "Answer with a single JSON object and nothing else: no markdown, no code fences, no comments."
)


class LLMError(Exception):
    """The provider could not be reached or returned an error."""


class ChatCompletionsClient:
    """Calls a chat-completions endpoint. Retries rate limits (429) and provider errors (5xx)."""

    RETRYABLE_STATUS = {429, 500, 502, 503, 504}

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        timeout_s: float = 60.0,
        max_retries: int = 4,
        sleep: Callable[[float], None] = time.sleep,
        http_post: Optional[Callable[..., httpx.Response]] = None,
    ):
        if provider not in PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        self.provider = provider
        self.url = PROVIDERS[provider]["url"]
        self.api_key = api_key
        self.model = model or os.getenv("AGENTPULSE_LLM_MODEL") or PROVIDERS[provider]["default_model"]
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self._sleep = sleep
        self._post = http_post or httpx.post

    @property
    def label(self) -> str:
        return f"{self.provider}:{self.model}"

    def __call__(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }
        resp = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._post(
                    self.url,
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=self.timeout_s,
                )
            except httpx.HTTPError as exc:
                if attempt < self.max_retries:
                    self._sleep(self._backoff(attempt, None))
                    continue
                raise LLMError(f"Network error calling {self.label}: {exc.__class__.__name__}") from exc
            if resp.status_code in self.RETRYABLE_STATUS and attempt < self.max_retries:
                self._sleep(self._backoff(attempt, resp.headers.get("retry-after")))
                continue
            break
        if resp.status_code != 200:
            # Never log the request body (task data) or the key.
            raise LLMError(f"{self.label} returned HTTP {resp.status_code}: {resp.text[:200]}")
        try:
            return resp.json()["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMError(f"Unexpected response from {self.label}") from exc

    @staticmethod
    def _backoff(attempt: int, retry_after: Optional[str]) -> float:
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return min(2.0 * (2**attempt), 30.0)


def client_from_env() -> Optional[ChatCompletionsClient]:
    """Builds a client from the keys in the environment; None when there is no key."""
    for provider in ("groq", "openai"):
        key = os.getenv(PROVIDERS[provider]["key_env"], "").strip()
        if key:
            return ChatCompletionsClient(provider, key)
    return None
