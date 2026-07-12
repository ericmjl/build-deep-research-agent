"""Tests for the two-model LLM configuration in llm.py."""

import pytest

from build_deep_research_agent.llm import (
    DEFAULT_LARGE_MODEL,
    DEFAULT_SMALL_MODEL,
    get_completion_kwargs,
    get_large_model_name,
    get_small_model_name,
)


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all tutorial LLM env vars."""
    for key in (
        "LLM_MODEL",
        "LLM_MODEL_SMALL",
        "LLM_MODEL_LARGE",
        "TUTORIAL_LLM_BASE_URL",
        "TUTORIAL_LLM_API_KEY",
        "OPENAI_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)


class TestSmallModel:
    def test_default_small_model(self, clean_env):
        assert get_small_model_name() == DEFAULT_SMALL_MODEL

    def test_custom_small_model(self, clean_env, monkeypatch):
        monkeypatch.setenv("LLM_MODEL_SMALL", "ollama_chat/llama3.2")
        assert get_small_model_name() == "ollama_chat/llama3.2"


class TestLargeModel:
    def test_default_large_model(self, clean_env):
        assert get_large_model_name() == DEFAULT_LARGE_MODEL

    def test_custom_large_model(self, clean_env, monkeypatch):
        monkeypatch.setenv("LLM_MODEL_LARGE", "openai/gemma4:12b")
        assert get_large_model_name() == "openai/gemma4:12b"


class TestCompletionKwargs:
    def test_local_ollama_returns_empty(self, clean_env):
        """Both models ollama_chat/ → no api_base/api_key needed."""
        assert get_completion_kwargs() == {}

    def test_remote_modal_returns_endpoint(self, clean_env, monkeypatch):
        """Both models openai/ → return api_base + api_key."""
        monkeypatch.setenv("LLM_MODEL_SMALL", "openai/gemma2:2b")
        monkeypatch.setenv("LLM_MODEL_LARGE", "openai/gemma4:12b")
        monkeypatch.setenv("TUTORIAL_LLM_BASE_URL", "https://example.com/v1")
        kwargs = get_completion_kwargs()
        assert kwargs["api_base"] == "https://example.com/v1"

    def test_mixed_prefix_returns_endpoint(self, clean_env, monkeypatch):
        """If either model is openai/, endpoint kwargs are returned."""
        monkeypatch.setenv("LLM_MODEL_SMALL", "ollama_chat/gemma2:2b")
        monkeypatch.setenv("LLM_MODEL_LARGE", "openai/gemma4:12b")
        monkeypatch.setenv("TUTORIAL_LLM_BASE_URL", "https://example.com/v1")
        kwargs = get_completion_kwargs()
        assert "api_base" in kwargs


class TestDeprecation:
    def test_get_model_name_warns(self, clean_env):
        """get_model_name() is deprecated but still returns the large model."""
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from build_deep_research_agent.llm import get_model_name

            result = get_model_name()
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert result == DEFAULT_LARGE_MODEL
