"""Part 2 memory exercises — instructor reference solutions."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord, Message
from build_deep_research_agent.prompts import format_citations_for_context

CITATION_MEMORY_PROMPT = """
Here is citation context and conversation snippets that may be helpful in answering the question.
"""

DEFAULT_MEMORY_TABLE = "tutorial_part2_memory"
DEFAULT_EMBEDDING_MODEL = "minishlab/potion-base-8M"

MEMORY_PROMPT = """
Here are conversation memories that may be helpful in answering the question.
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
        body = "\n\n".join(blocks)
        return f"{CITATION_MEMORY_PROMPT}\n\n{body}"


class MemoryDocstore:
    """Semantic memory store backed by LanceDB with keyword fallback."""

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

    def _retrieve_semantic(self, query: str, limit: int) -> list[str]:
        """Query the LanceDB backend for stored memory text."""
        try:
            return list(self._backend.retrieve(query, n_results=limit))
        except Exception:
            return self._retrieve_keyword(query, limit)

    def add(self, text: str) -> None:
        """Store a memory string in the docstore.

        :param text: Memory text to store and make searchable.
        """
        # @spec MEM-STORE-002
        self._memories.append(text)
        if self._backend is not None:
            try:
                self._backend.append(text)
            except Exception:
                pass

    def search(self, query: str, limit: int = 3) -> list[str]:
        """Retrieve the most relevant memories for a query.

        :param query: Search terms.
        :param limit: Maximum number of memories to return.
        :returns: Matching memory strings in relevance order.
        """
        # @spec MEM-STORE-003
        if not query.strip():
            return []
        limit = max(1, limit)

        if self._backend is not None:
            results = self._retrieve_semantic(query, limit)
        else:
            results = self._retrieve_keyword(query, limit)

        return results[:limit]

    def as_context(self, query: str, limit: int = 3) -> str:
        """Format retrieved memories for prompt injection.

        :param query: Search terms used to select relevant memories.
        :param limit: Maximum number of memories to include.
        :returns: Plain-text block for LLM context.
        """
        # @spec MEM-STORE-005
        memories = self.search(query, limit=limit)
        if not memories:
            return "(no relevant memories)"
        body = "\n\n".join(memories)
        return f"{MEMORY_PROMPT}\n\n{body}"
