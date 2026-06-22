"""Part 2 memory exercises — instructor reference solutions."""

from __future__ import annotations

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message
from build_deep_research_agent.prompts import format_citations_for_context

CITATION_MEMORY_PROMPT = """
Here is citation context and conversation snippets that may be helpful in answering the question.
"""

class AppendOnlyMemory(BaseModel):
    """Immutable append-only conversation history."""

    model_config = {"frozen": True}

    history: tuple[Message, ...] = Field(default_factory=tuple)

    def append(self, message: Message) -> AppendOnlyMemory:
        """Return a new memory with one additional message.

        :param message: Turn to append.
        :returns: Updated memory instance.
        """
        # @spec MEM-CHAT-001
        # @spec MEM-CHAT-002
        return AppendOnlyMemory(history=(*self.history, message))

    def messages(self) -> list[Message]:
        """Return chat history in append order.

        :returns: Ordered message list.
        """
        # @spec MEM-CHAT-003
        return list(self.history)


class CitationMemory(BaseModel):
    """Immutable store of citation metadata plus conversation snippets."""

    model_config = {"frozen": True}

    entries: tuple[tuple[CitationRecord, str], ...] = Field(default_factory=tuple)

    def add(self, citation: CitationRecord, snippet: str) -> CitationMemory:
        """Return a new memory with one citation entry added.

        :param citation: Bibliographic record from fixtures or MCP.
        :param snippet: Short text captured when the paper was discussed.
        :returns: Updated memory instance.
        """
        # @spec MEM-CITE-001
        # @spec MEM-CITE-002
        return CitationMemory(entries=(*self.entries, (citation, snippet)))

    def as_context(self) -> str:
        """Format stored citations and snippets for prompt injection.

        When duplicate citation keys exist, the later entry wins.

        :returns: Plain-text block for LLM context using instruction prefix.
        """
        # @spec MEM-CITE-003
        # @spec MEM-CITE-004
        if not self.entries:
            return "(no citations in memory)"

        by_key: dict[str, tuple[CitationRecord, str]] = {}
        for citation, snippet in self.entries:
            by_key[citation.key] = (citation, snippet)

        blocks: list[str] = []
        for citation, snippet in by_key.values():
            base = format_citations_for_context([citation])
            blocks.append(f"{base}\nSnippet: {snippet}")
        return f"{CITATION_MEMORY_PROMPT}\n\n{'\n\n'.join(blocks)}"
