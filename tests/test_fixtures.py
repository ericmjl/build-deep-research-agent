"""Tests for bundled citation fixtures."""

from build_deep_research_agent.fixtures.loader import load_citation_fixtures


def test_load_citation_fixtures() -> None:
    """Bundled fixtures deserialize into at least five citation records."""
    # @spec PROMPT-FIX-002
    # @spec PROMPT-FIX-030
    # @spec TUT-MODEL-040
    records = load_citation_fixtures()
    assert len(records) >= 5
    assert records[0].title
