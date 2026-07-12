"""Part 2 memory exercises — learner stubs (edit this file).

You build two memory types plus a plain summarizer:

1. :class:`AppendOnlyMemory` — immutable chat history for multi-turn follow-ups,
   with ``retrieve(n_results)`` for a recent slice.
2. :func:`summarize_paper` — plain function that returns a short summary string
   (the shape Part 3 will wrap as a ``@tool``).
3. :class:`CitationMemory` — citation metadata plus LLM summaries for structured
   evidence context.

Reference answers: ``build_deep_research_agent/exercises/solutions/part2.py``
(instructors comment-swap the import in the notebook).
"""

from __future__ import annotations

from llamabot import SimpleBot
from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message

# @spec MEM-EX-001


def summarize_paper(bot: SimpleBot, text: str) -> str:
    """Summarize paper text with a plain function (future ``@tool`` shape).

    Call the bot with a short summarization prompt and return the content string.

    :param bot: Configured research bot.
    :param text: Paper abstract or excerpt to summarize.
    :returns: Short summary string.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Implement summarize_paper in build_deep_research_agent/exercises/part2.py"
    )


class AppendOnlyMemory(BaseModel):
    """Immutable chat history you can pass into ``run_research_turn(..., history=...)``.

    - ``append(message)`` — return a **new** memory with that turn added
      (don't mutate in place).
    - ``messages()`` — return the turns in order so the follow-up can see
      the prior Q&A.
    - ``retrieve(n_results)`` — return only the most recent ``n_results`` turns.
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

    def retrieve(self, n_results: int) -> list[Message]:
        """Return the most recent ``n_results`` turns (drops oldest).

        :param n_results: Maximum number of recent messages to return.
        :returns: Recent messages in chronological order.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement retrieve in build_deep_research_agent/exercises/part2.py"
        )


class CitationMemory(BaseModel):
    """Inventory of papers in the conversation — more useful than raw chat history alone.

    Think of summarizing two papers and then asking to compare them.

    - ``add(citation, summary)`` — store a citation plus a short summary;
      return a **new** instance.
    - ``as_context()`` — turn what's stored into a string you can pass as
      context text.

    Consider also that there may be multiple summaries per citation, and how to
    handle that on output, and how you'd want the model to use this block.
    """

    model_config = {"frozen": True}

    entries: tuple[tuple[CitationRecord, str], ...] = Field(default_factory=tuple)

    def add(self, citation: CitationRecord, summary: str) -> CitationMemory:
        """Store a citation plus a short summary of the paper.

        Return a **new** instance.

        :param citation: Bibliographic record from fixtures or MCP.
        :param summary: Short summary (e.g. from ``summarize_paper``).
        :returns: Updated memory instance.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement add in build_deep_research_agent/exercises/part2.py"
        )

    def as_context(self) -> str:
        """Turn what's stored into a string you can pass as context text.

        Consider multiple summaries per citation and how to handle that on output,
        and how you'd want the model to use this block.

        :returns: Plain-text block for LLM context.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement as_context in build_deep_research_agent/exercises/part2.py"
        )
