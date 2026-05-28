"""Tests for multi-agent orchestration with AgentBot."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from build_deep_research_agent.agents import (
    ResearchOrchestrator,
    SearcherAgent,
    SynthesizerAgent,
    oversized_evidence,
)
from build_deep_research_agent.fixtures.search import search_fixture_library


@pytest.fixture
def sample_query() -> str:
    """Return a fixture search query used across agent tests."""
    return "Bayesian workflow"


def test_search_fixture_library_finds_records(sample_query: str) -> None:
    """Fixture search returns records matching the sample query."""
    records = search_fixture_library(sample_query, limit=5)
    assert records
    assert any("Bayesian" in record.title for record in records)


def test_oversized_evidence_expands() -> None:
    """oversized_evidence duplicates seed records for context-stress demos."""
    base = search_fixture_library("Bayesian", limit=1)
    bloated = oversized_evidence(base, repeat=5)
    assert len(bloated) == 5
    assert bloated[0].key != bloated[1].key


@patch("build_deep_research_agent.agents.AgentBot")
def test_searcher_agentbot_fixture_mode(
    mock_agentbot: MagicMock, sample_query: str
) -> None:
    """SearcherAgent in fixture mode invokes AgentBot and returns records."""
    mock_bot = MagicMock()
    mock_agentbot.return_value = mock_bot

    searcher = SearcherAgent(mode="fixture")
    with patch(
        "build_deep_research_agent.agents.search_fixture_library",
        return_value=search_fixture_library(sample_query),
    ):
        records = searcher.run(sample_query, limit=3)

    assert len(records) >= 1
    mock_bot.assert_called_once()
    searcher.close()
    mock_bot.close_mcp.assert_called()


@patch("build_deep_research_agent.agents.AgentBot")
def test_research_orchestrator_uses_agentbots(
    mock_agentbot: MagicMock,
    sample_query: str,
) -> None:
    """ResearchOrchestrator passes Searcher evidence to the Synthesizer."""
    # @spec MULTI-AGENT-040
    evidence = search_fixture_library(sample_query, limit=2)

    mock_searcher_bot = MagicMock()
    mock_synth_bot = MagicMock()

    mock_agentbot.side_effect = [mock_searcher_bot, mock_synth_bot]

    searcher = SearcherAgent(mode="fixture")
    synthesizer = SynthesizerAgent()

    with patch.object(searcher, "run", return_value=evidence):
        with patch.object(
            synthesizer,
            "run",
            return_value="## Summary\nGrounded report.",
        ):
            orchestrator = ResearchOrchestrator(
                searcher=searcher, synthesizer=synthesizer
            )
            report = orchestrator.run(sample_query, limit=2)

    assert report.query == sample_query
    assert report.evidence == evidence
    assert "Summary" in report.report_markdown
    orchestrator.close()


@patch("build_deep_research_agent.agents.AgentBot")
def test_synthesizer_agentbot_run_with_empty_evidence(mock_agentbot: MagicMock) -> None:
    """SynthesizerAgent handles empty evidence without crashing."""
    # @spec MULTI-FAIL-030
    mock_bot = MagicMock()
    mock_bot.return_value = "No evidence found."
    mock_agentbot.return_value = mock_bot

    synthesizer = SynthesizerAgent()
    text = synthesizer.run("What is X?", [])
    assert "No evidence" in text
    synthesizer.close()
