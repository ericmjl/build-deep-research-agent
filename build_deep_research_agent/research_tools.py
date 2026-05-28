"""Searcher tools for llamabot AgentBot."""

from __future__ import annotations

from dataclasses import dataclass, field

from llamabot.components.tools import tool

from build_deep_research_agent.fixtures.search import (
    search_fixture_library as _search_fixtures,
)
from build_deep_research_agent.mcp.client import normalize_search_json
from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.prompts import format_citations_for_context


@dataclass
class EvidenceCollector:
    """Mutable store populated by Searcher AgentBot tools."""

    query: str = ""
    records: list[CitationRecord] = field(default_factory=list)
    notes: str = ""


def make_searcher_tools(collector: EvidenceCollector) -> list:
    """Build @tool callables bound to a shared evidence collector.

    :param collector: Store updated when the agent searches or caches results.
    :returns: Tool list for :class:`~llamabot.AgentBot`.
    """

    @tool
    def search_fixture_library(query: str, limit: int = 5) -> str:
        """Search the bundled tutorial citation library for offline demos.

        :param query: Case-insensitive substring query.
        :param limit: Maximum number of records to return.
        :returns: Formatted citation context for the agent.
        """
        records = _search_fixtures(query, limit=limit)
        collector.records.extend(records)
        return format_citations_for_context(records)

    @tool
    def cache_evidence(raw_results: str) -> str:
        """Cache raw output from a zotero-mcp search tool for downstream synthesis.

        :param raw_results: Unparsed text or JSON returned by zotero-mcp.
        :returns: Confirmation message with item count.
        """
        # @spec TOOLS-SEARCH-012
        parsed = normalize_search_json(raw_results, fallback_query=collector.query)
        collector.records.extend(parsed)
        return f"Cached {len(parsed)} item(s) for synthesis."

    @tool(loopback_name=None)
    def finish_search(summary: str) -> str:
        """Finish the search phase after evidence is cached.

        :param summary: One-line summary of what was found.
        :returns: The same summary string.
        """
        collector.notes = summary
        return summary

    return [search_fixture_library, cache_evidence, finish_search]
