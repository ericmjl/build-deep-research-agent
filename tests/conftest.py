"""Shared test fixtures and patches."""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def _mock_llm_config():
    """Patch get_completion_kwargs so tests pass without LLM API keys."""
    with (
        patch(
            "build_deep_research_agent.agents.get_completion_kwargs",
            return_value={},
        ),
        patch(
            "build_deep_research_agent.deterministic_agent.get_completion_kwargs",
            return_value={},
        ),
    ):
        yield
