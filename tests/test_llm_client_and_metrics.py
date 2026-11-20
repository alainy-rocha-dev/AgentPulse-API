"""LLM client (no network), environment wiring and the deterministic-metrics check."""

import json

import httpx
import pytest

from app.services.agent_orchestrator import AgentOrchestrator
from app.services.llm_client import ChatCompletionsClient, LLMError, client_from_env
from app.services.repair_loop import RepairLoopService, SchemaValidationError


def _response(status, body=None, headers=None):
    request = httpx.Request("POST", "https://example.test")
    return httpx.Response(status, json=body or {}, headers=headers or {}, request=request)


def _ok(content):
    return _response(200, {"choices": [{"message": {"content": content}}]})


class FakePost:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def __call__(self, *args, **kwargs):
        item = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        if isinstance(item, Exception):
            raise item
        return item


def test_client_retries_rate_limit_then_succeeds():
    sleeps = []
    post = FakePost([_response(429, headers={"retry-after": "2"}), _ok('{"a": 1}')])
    client = ChatCompletionsClient("groq", "key", sleep=sleeps.append, http_post=post)
    assert client("prompt") == '{"a": 1}'
    assert post.calls == 2
    assert sleeps == [2.0]


def test_client_fails_fast_on_invalid_key():
    post = FakePost([_response(401, {"error": "invalid key"})])
    client = ChatCompletionsClient("groq", "bad", sleep=lambda s: None, http_post=post)
    with pytest.raises(LLMError, match="HTTP 401"):
        client("prompt")
    assert post.calls == 1


def test_client_gives_up_after_network_errors():
    post = FakePost([httpx.ConnectError("down")])
    client = ChatCompletionsClient("openai", "key", max_retries=2, sleep=lambda s: None, http_post=post)
    with pytest.raises(LLMError, match="Network error"):
        client("prompt")
    assert post.calls == 3


def test_client_from_env_prefers_groq(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "g")
    monkeypatch.setenv("OPENAI_API_KEY", "o")
    monkeypatch.delenv("AGENTPULSE_LLM_MODEL", raising=False)
    assert client_from_env().label == "groq:openai/gpt-oss-120b"
    monkeypatch.delenv("GROQ_API_KEY")
    assert client_from_env().label == "openai:gpt-4o-mini"
    monkeypatch.delenv("OPENAI_API_KEY")
    assert client_from_env() is None


def test_orchestrator_uses_stub_without_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = AgentOrchestrator().run_task("contract_analysis", {"items": [{"issue": "x", "severity": "HIGH"}]})
    assert result.metadata.model_used == AgentOrchestrator.STUB_LABEL
    assert result.metrics.total_score == 75.0


EXPECTED = {"total_score": 75.0, "risk_level": "MEDIUM", "calculated_items": 1}


def _answer(metrics):
    return json.dumps({"summary": "s", "key_findings": ["k"], "metrics": metrics})


def test_altered_metrics_are_rejected_and_repaired():
    answers = [_answer({**EXPECTED, "total_score": 80.0}), _answer(EXPECTED)]
    prompts = []

    def llm(prompt):
        prompts.append(prompt)
        return answers[len(prompts) - 1]

    service = RepairLoopService(llm_client=llm, max_attempts=3)
    result = service.execute_with_repair("p", expected_metrics=EXPECTED, model_label="fake:model")

    assert result.metrics.total_score == 75.0
    assert result.metadata.repair_attempts == 1
    assert result.metadata.model_used == "fake:model"
    assert service.attempt_errors[0].startswith("MetricsMismatchError")
    assert "esperado 75.0" in prompts[1]


def test_metrics_never_saved_when_llm_keeps_changing_them():
    service = RepairLoopService(llm_client=lambda p: _answer({**EXPECTED, "risk_level": "LOW"}), max_attempts=3)
    with pytest.raises(SchemaValidationError):
        service.execute_with_repair("p", expected_metrics=EXPECTED)
    assert len(service.attempt_errors) == 3


def test_non_object_json_is_a_validation_error():
    answers = ["[1, 2]", _answer(EXPECTED)]
    calls = []

    def llm(prompt):
        calls.append(prompt)
        return answers[len(calls) - 1]

    result = RepairLoopService(llm_client=llm).execute_with_repair("p", expected_metrics=EXPECTED)
    assert result.metadata.repair_attempts == 1
