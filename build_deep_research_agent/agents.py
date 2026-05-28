"""Multi-agent research orchestration (Searcher + Synthesizer via llamabot AgentBot)."""

# @spec TUT-MODEL-031

from __future__ import annotations

import os
from typing import Literal

from llamabot import AgentBot
from loguru import logger

from build_deep_research_agent.fixtures.search import search_fixture_library
from build_deep_research_agent.llm import get_completion_kwargs, get_model_name
from build_deep_research_agent.mcp.client import resolve_zotero_mcp_server_config
from build_deep_research_agent.models import CitationRecord, ResearchReport
from build_deep_research_agent.prompts import (
    SEARCHER_AGENTBOT_PROMPT,
    SYNTHESIZER_AGENTBOT_PROMPT,
    format_citations_for_context,
)
from build_deep_research_agent.research_tools import (
    EvidenceCollector,
    make_searcher_tools,
)

SearchMode = Literal["fixture", "mcp"]


class SearcherAgent:
    """Retrieve literature evidence using llamabot AgentBot and MCP or fixtures."""

    # @spec MULTI-AGENT-001

    def __init__(
        self,
        mode: SearchMode | None = None,
        model_name: str | None = None,
        max_iterations: int = 8,
    ) -> None:
        self.mode: SearchMode = mode or os.getenv("RESEARCH_SEARCH_MODE", "fixture")  # type: ignore[assignment]
        self._model_name = model_name or get_model_name()
        self._max_iterations = max_iterations
        self._collector = EvidenceCollector()
        self._bot: AgentBot | None = None

    def run(self, query: str, limit: int = 5) -> list[CitationRecord]:
        """Search for citation evidence via AgentBot tool orchestration.

        :param query: Research query or search terms.
        :param limit: Maximum records to retrieve.
        :returns: Retrieved citation records.
        """
        self.close()
        self._collector = EvidenceCollector(query=query)
        self._bot = self._build_bot()

        if self.mode == "fixture":
            instruction = (
                f"Find up to {limit} relevant papers for: {query}\n"
                "Use search_fixture_library, then finish_search, then respond_to_user."
            )
        else:
            instruction = (
                f"Find up to {limit} relevant papers for: {query}\n"
                "Use zotero MCP search tools, call cache_evidence with each raw result, "
                "then finish_search, then respond_to_user."
            )

        logger.info("Searcher AgentBot running in {} mode", self.mode)
        self._bot(instruction)

        if self._collector.records:
            return self._collector.records[:limit]

        logger.warning("AgentBot returned no cached records; using fixture fallback")
        return search_fixture_library(query, limit=limit)  # @spec MULTI-AGENT-001

    def _build_bot(self) -> AgentBot:
        """Construct a Searcher AgentBot for fixture or MCP mode."""
        # @spec MULTI-AGENT-002
        mcp_servers = (
            [resolve_zotero_mcp_server_config()] if self.mode == "mcp" else None
        )
        return AgentBot(
            tools=make_searcher_tools(self._collector),
            system_prompt=SEARCHER_AGENTBOT_PROMPT,
            model_name=self._model_name,
            max_iterations=self._max_iterations,
            mcp_servers=mcp_servers,
            **get_completion_kwargs(),
        )

    def close(self) -> None:
        """Release MCP sessions held by the underlying AgentBot."""
        if self._bot is not None:
            self._bot.close_mcp()
            self._bot = None


class SynthesizerAgent:
    """Turn retrieved evidence into a markdown report using llamabot AgentBot."""

    # @spec MULTI-AGENT-003
    # @spec MULTI-AGENT-004
    def __init__(self, model_name: str | None = None, max_iterations: int = 4) -> None:
        self._bot = AgentBot(
            tools=[],
            system_prompt=SYNTHESIZER_AGENTBOT_PROMPT,
            model_name=model_name or get_model_name(),
            max_iterations=max_iterations,
            **get_completion_kwargs(),
        )

    def run(self, query: str, evidence: list[CitationRecord]) -> str:
        """Synthesize a markdown report from evidence.

        :param query: Original research question.
        :param evidence: Retrieved citations (may be empty for failure demos).
        :returns: Markdown report text.
        """
        evidence_block = format_citations_for_context(evidence)
        prompt = (
            f"Research question:\n{query}\n\n"
            f"Evidence:\n{evidence_block}\n\n"
            "Write a concise markdown literature summary grounded in the evidence, "
            "then use respond_to_user with the full report."
        )
        result = self._bot(prompt)
        return str(result)

    def close(self) -> None:
        """Release MCP sessions (no-op unless MCP was configured)."""
        self._bot.close_mcp()


class ResearchOrchestrator:
    """Coordinate Searcher → Synthesizer AgentBots for the Part 5 demo."""

    # @spec MULTI-AGENT-010
    # @spec MULTI-AGENT-031

    def __init__(
        self,
        searcher: SearcherAgent | None = None,
        synthesizer: SynthesizerAgent | None = None,
    ) -> None:
        self.searcher = searcher or SearcherAgent()
        self.synthesizer = synthesizer or SynthesizerAgent()

    def run(self, query: str, limit: int = 5) -> ResearchReport:
        """Execute the multi-agent literature review pipeline.

        :param query: User research question.
        :param limit: Maximum search results passed to the Synthesizer.
        :returns: Structured report with evidence and markdown summary.
        """
        logger.info("Searcher AgentBot retrieving evidence for: {}", query)
        evidence = self.searcher.run(query, limit=limit)
        logger.info(
            "Synthesizer AgentBot writing report from {} records", len(evidence)
        )
        report_markdown = self.synthesizer.run(query, evidence)  # @spec MULTI-AGENT-011
        return ResearchReport(
            query=query,
            evidence=evidence,
            report_markdown=report_markdown,
        )

    def close(self) -> None:
        """Release resources held by sub-agents."""
        self.searcher.close()
        self.synthesizer.close()


def oversized_evidence(
    base: list[CitationRecord], repeat: int = 40
) -> list[CitationRecord]:
    """Build an intentionally large evidence block for context-exhaustion demos.

    :param base: Seed citations to repeat.
    :param repeat: Number of duplicated entries.
    :returns: Expanded evidence list.
    """
    # @spec MULTI-FAIL-002
    from build_deep_research_agent.fixtures.loader import load_citation_fixtures

    if not base:
        base = [load_citation_fixtures()[0]]
    bloated: list[CitationRecord] = []
    for index in range(repeat):
        source = base[index % len(base)]
        bloated.append(
            source.model_copy(
                update={
                    "key": f"{source.key}-{index}",
                    "abstract": (source.abstract or "") + (" context padding." * 200),
                }
            )
        )
    return bloated
