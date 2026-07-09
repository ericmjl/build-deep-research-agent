"""Part 2 memory exercises — learner stubs (edit this file).

You build two memory types:

1. :class:`AppendOnlyMemory` — immutable chat history for multi-turn follow-ups.
2. :class:`CitationMemory` — citation metadata plus conversation snippets for
   structured context.

Reference answers: ``build_deep_research_agent/exercises/solutions/part2.py``
(instructors comment-swap the import in the notebook).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message

# @spec MEM-EX-001


class AppendOnlyMemory(BaseModel):
    """Immutable chat history you can pass into ``run_research_turn(..., history=...)``.

    - ``append(message)`` — return a **new** memory with that turn added
      (don't mutate in place).
    - ``messages()`` — return the turns in order so the follow-up can see
      the prior Q&A.
    """

    model_config = {"frozen": True}

    history: tuple[Message, ...] = Field(default_factory=tuple)

    def append(self, message: Message) -> AppendOnlyMemory:
        """Return a **new** memory with that turn added (don't mutate in place).

        :param message: Turn to append.
        :returns: Updated memory instance.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement append in build_deep_research_agent/exercises/part2.py"
        )

    def messages(self) -> list[Message]:
        """Return the turns in order so the follow-up can see the prior Q&A.

        :returns: Ordered message list.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement messages in build_deep_research_agent/exercises/part2.py"
        )


class CitationMemory(BaseModel):
    """Inventory of papers in the conversation — more useful than raw chat history alone.

    Think of discussing two papers and then asking to compare them.

    - ``add(citation, snippet)`` — store a citation plus a short snippet from
      when it was discussed; return a **new** instance.
    - ``as_context()`` — turn what's stored into a string you can pass as
      context text.

    Consider also that there may be multiple snippets per citation, and how to
    handle that on output, and how you'd want the model to use this block.
    """

    model_config = {"frozen": True}

    entries: tuple[tuple[CitationRecord, str], ...] = Field(default_factory=tuple)

    def add(self, citation: CitationRecord, snippet: str) -> CitationMemory:
        """Store a citation plus a short snippet from when it was discussed.

        Return a **new** instance.

        :param citation: Bibliographic record from fixtures or MCP.
        :param snippet: Short text captured when the paper was discussed.
        :returns: Updated memory instance.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement add in build_deep_research_agent/exercises/part2.py"
        )

    def as_context(self) -> str:
        """Turn what's stored into a string you can pass as context text.

        Consider multiple snippets per citation and how to handle that on output,
        and how you'd want the model to use this block.

        :returns: Plain-text block for LLM context.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement as_context in build_deep_research_agent/exercises/part2.py"
        )
