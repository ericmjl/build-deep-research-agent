"""Fixture-backed search for offline tutorial demos."""

from __future__ import annotations

from build_deep_research_agent.fixtures.loader import load_citation_fixtures
from build_deep_research_agent.models import CitationRecord


def search_fixture_library(query: str, limit: int = 5) -> list[CitationRecord]:
    """Substring search over bundled fixtures.

    :param query: Case-insensitive search string.
    :param limit: Maximum records to return.
    :returns: Matching citation records.
    """
    # @spec PROMPT-FIX-002
    needle = query.lower()
    matches: list[CitationRecord] = []
    for record in load_citation_fixtures():
        haystack = " ".join(
            [
                record.title,
                " ".join(record.creators),
                record.abstract or "",
            ]
        ).lower()
        if needle in haystack:
            matches.append(record)
        if len(matches) >= limit:
            break
    return matches
