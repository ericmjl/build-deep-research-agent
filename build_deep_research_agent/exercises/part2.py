"""Part 2 memory exercises — learner stubs (edit this file)."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message

# @spec MEM-EX-001

DEFAULT_MEMORY_TABLE = "tutorial_part2_memory"
DEFAULT_EMBEDDING_MODEL = "minishlab/potion-base-8M"


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


class MemoryDocstore:
    """Semantic memory store backed by LanceDB with keyword fallback.

    Implementation spec: ``ex3_implementation_specs`` cell in
    ``notebooks/02_memory_state.py``.
    """

    # @spec MEM-STORE-001

    def __init__(
        self,
        table_name: str = DEFAULT_MEMORY_TABLE,
        storage_path: Path | None = None,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> None:
        self.table_name = table_name
        self.embedding_model = embedding_model
        self.storage_path = storage_path
        self._memories: list[str] = []
        self._backend = self._init_backend(table_name, storage_path, embedding_model)

    def _init_backend(
        self,
        table_name: str,
        storage_path: Path | None,
        embedding_model: str,
    ):  # type: ignore[no-untyped-def]
        """Create the LanceDB backend, returning None on failure (keyword fallback).

        :param table_name: LanceDB table name.
        :param storage_path: Optional on-disk persistence path.
        :param embedding_model: Embedding model identifier.
        :returns: A LanceDBDocStore, or None to signal keyword fallback mode.
        """
        # @spec MEM-STORE-004
        try:
            from llamabot import LanceDBDocStore

            kwargs: dict = {
                "table_name": table_name,
                "embedding_model": embedding_model,
            }
            if storage_path is not None:
                kwargs["storage_path"] = storage_path
            return LanceDBDocStore(**kwargs)
        except Exception:
            return None

    @property
    def backend_name(self) -> str:
        """Return the active backend name (``lancedb`` or ``keyword``)."""
        return "lancedb" if self._backend is not None else "keyword"

    def reset(self) -> None:
        """Clear stored memories and reset the backend."""
        self._memories.clear()
        if self._backend is not None:
            try:
                self._backend.reset()
            except Exception:
                pass

    def _retrieve_keyword(self, query: str, limit: int) -> list[str]:
        """Fallback: rank stored memories by keyword overlap with the query."""
        terms = [t for t in re.split(r"\W+", query.lower()) if t]
        scored: list[tuple[int, str]] = []
        for text in self._memories:
            haystack = text.lower()
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                scored.append((score, text))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [text for _, text in scored[:limit]]

    def add(self, text: str) -> None:
        """Store a memory string in the docstore.

        :param text: Memory text to store and make searchable.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement add in build_deep_research_agent/exercises/part2.py"
        )

    def search(self, query: str, limit: int = 3) -> list[str]:
        """Retrieve the most relevant memories for a query.

        :param query: Search terms.
        :param limit: Maximum number of memories to return.
        :returns: Matching memory strings in relevance order.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement search in build_deep_research_agent/exercises/part2.py"
        )

    def as_context(self, query: str, limit: int = 3) -> str:
        """Format retrieved memories for prompt injection.

        :param query: Search terms used to select relevant memories.
        :param limit: Maximum number of memories to include.
        :returns: Plain-text block for LLM context.
        :raises NotImplementedError: Until you implement this exercise.
        """
        raise NotImplementedError(
            "Implement as_context in build_deep_research_agent/exercises/part2.py"
        )
