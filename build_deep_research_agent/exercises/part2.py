"""Part 2 memory exercises — learner stubs (edit this file)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message

# @spec MEM-EX-001


class AppendOnlyMemory(BaseModel):
    """Immutable append-only conversation history.

    Implementation spec: ``ex_implementation_specs`` cell in
    ``notebooks/02_memory_state.py``.
    """

    model_config = {"frozen": True}

    history: tuple[Message, ...] = Field(default_factory=tuple)

    def append(self, message: Message) -> AppendOnlyMemory:
        """Return a new memory with one additional message.

        :param message: Turn to append.
        :returns: Updated memory instance.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement append in build_deep_research_agent/exercises/part2.py"
        )

    def messages(self) -> list[Message]:
        """Return chat history in append order.

        :returns: Ordered message list.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement messages in build_deep_research_agent/exercises/part2.py"
        )


class CitationMemory(BaseModel):
    """Immutable store of citation metadata plus conversation snippets.

    Implementation spec: ``ex_implementation_specs`` cell in
    ``notebooks/02_memory_state.py``.
    """

    model_config = {"frozen": True}

    entries: tuple[tuple[CitationRecord, str], ...] = Field(default_factory=tuple)

    def add(self, citation: CitationRecord, snippet: str) -> CitationMemory:
        """Return a new memory with one citation entry added.

        :param citation: Bibliographic record from fixtures or MCP.
        :param snippet: Short text captured when the paper was discussed.
        :returns: Updated memory instance.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement add in build_deep_research_agent/exercises/part2.py"
        )

    def as_context(self) -> str:
        """Format stored citations and snippets for prompt injection.

        When duplicate citation keys exist, the later entry shall win.

        Consider where this context is injected into the LLM prompt
        and how to instruct the LLM to use it.

        :returns: Plain-text block for LLM context.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement as_context in build_deep_research_agent/exercises/part2.py"
        )
