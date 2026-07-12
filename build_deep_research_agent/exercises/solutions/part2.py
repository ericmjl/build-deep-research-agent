"""Part 2 memory exercises — instructor reference solutions."""

from __future__ import annotations

from llamabot import SimpleBot
from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message
from build_deep_research_agent.prompts import format_citations_for_context

CITATION_MEMORY_PROMPT = """
Here is citation context and paper summaries that may be helpful in answering the question.
"""


def summarize_paper(bot: SimpleBot, text: str) -> str:
    """Summarize paper text with a plain function (future ``@tool`` shape).

    :param bot: Configured research bot.
    :param text: Paper abstract or excerpt to summarize.
    :returns: Short summary string.
    """
    # @spec MEM-CITE-005
    response = bot(f"Summarize this paper in 2 sentences:\n\n{text}")
    return str(response.content)


class AppendOnlyMemory(BaseModel):
    """Immutable chat history for ``run_research_turn(..., history=...)``."""

    model_config = {"frozen": True}

    history: tuple[Message, ...] = Field(default_factory=tuple)

    def append(self, message: Message) -> AppendOnlyMemory:
        """Return a new memory with that turn added (don't mutate in place).

        :param message: Turn to append.
        :returns: Updated memory instance.
        """
        # @spec MEM-CHAT-001
        # @spec MEM-CHAT-002
        return AppendOnlyMemory(history=(*self.history, message))

    def messages(self) -> list[Message]:
        """Return the turns in order so the follow-up can see the prior Q&A.

        :returns: Ordered message list.
        """
        # @spec MEM-CHAT-003
        return list(self.history)

    def retrieve(self, n_results: int) -> list[Message]:
        """Return the most recent ``n_results`` turns (drops oldest).

        :param n_results: Maximum number of recent messages to return.
        :returns: Recent messages in chronological order.
        """
        # @spec MEM-CHAT-004
        if n_results <= 0:
            return []
        return list(self.history[-n_results:])


class CitationMemory(BaseModel):
    """Inventory of papers discussed, each paired with an LLM summary."""

    model_config = {"frozen": True}

    entries: tuple[tuple[CitationRecord, str], ...] = Field(default_factory=tuple)

    def add(self, citation: CitationRecord, summary: str) -> CitationMemory:
        """Store a citation plus a short summary of the paper.

        Return a new instance.

        :param citation: Bibliographic record from fixtures or MCP.
        :param summary: Short summary (e.g. from ``summarize_paper``).
        :returns: Updated memory instance.
        """
        # @spec MEM-CITE-001
        # @spec MEM-CITE-002
        return CitationMemory(entries=(*self.entries, (citation, summary)))

    def as_context(self) -> str:
        """Turn what's stored into a string you can pass as context text.

        When duplicate citation keys exist, the later summary wins.

        :returns: Plain-text block for LLM context.
        """
        # @spec MEM-CITE-003
        # @spec MEM-CITE-004
        if not self.entries:
            return "(no citations in memory)"

        by_key: dict[str, tuple[CitationRecord, str]] = {}
        for citation, summary in self.entries:
            by_key[citation.key] = (citation, summary)

        blocks: list[str] = []
        for citation, summary in by_key.values():
            base = format_citations_for_context([citation])
            blocks.append(f"{base}\nSummary: {summary}")
        body = "\n\n".join(blocks)
        return f"{CITATION_MEMORY_PROMPT}\n\n{body}"
