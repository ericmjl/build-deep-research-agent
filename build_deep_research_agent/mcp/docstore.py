"""Docstore wrapper exposing semantic retrieval as structured citation items.

llamabot's docstores (``LanceDBDocStore``, ``TurboVecDocStore``) are string-in /
string-out: they store and retrieve document *text* but carry no per-document
metadata. This module wraps such a docstore with a **metadata side-table** so the
Part 3 MCP server can return rich citation items from a semantic search.

The wrapper is the bridge between "retrieve relevant text" (the docstore's job)
and "return a structured ``CitationRecord``" (the MCP tool's job).
"""

# @spec EMCP-DOC-001

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from build_deep_research_agent.models import CitationRecord

if TYPE_CHECKING:
    from fastmcp import FastMCP

DEFAULT_TABLE_NAME = "zotero_papers"  # @spec EMCP-DOC-001
DEFAULT_EMBEDDING_MODEL = "minishlab/potion-base-8M"  # @spec EMCP-DOC-002


class DocstoreStats(BaseModel):
    """Summary statistics about the docstore, returned by the MCP tool."""

    table_name: str  # @spec EMCP-DOC-050
    document_count: int  # @spec EMCP-DOC-050
    embedding_model: str  # @spec EMCP-DOC-050
    backend: str = "lancedb"


class DocstoreSearchHit(BaseModel):
    """A single retrieval result: a citation record plus a text snippet."""

    key: str  # @spec EMCP-SRV-014
    title: str  # @spec EMCP-SRV-014
    creators: list[str] = Field(default_factory=list)  # @spec EMCP-SRV-014
    year: int | None = None  # @spec EMCP-SRV-014
    abstract: str | None = None  # @spec EMCP-SRV-014
    url: str | None = None  # @spec EMCP-SRV-014
    snippet: str  # @spec EMCP-SRV-015


def compose_document_text(record: CitationRecord) -> str:
    """Build the searchable text blob stored for a citation record.

    The same string is the key into the metadata side-table, so it must be a
    stable function of the record.

    :param record: Citation record to render as text.
    :returns: Concatenated title, authors, and abstract (or title fallback).
    """
    # @spec EMCP-DOC-012
    creators = ", ".join(record.creators) if record.creators else "Unknown"
    body = record.abstract or record.title
    return f"{record.title}\nAuthors: {creators}\n{body}"


class ZoteroDocstore:
    """Semantic docstore + metadata side-table for Zotero citation items.

    Wraps a llamabot ``LanceDBDocStore`` for embedding-based retrieval and keeps a
    ``dict[stored_text -> CitationRecord]`` side-table so retrieved text can be
    projected back to structured citation metadata.

    If the docstore backend cannot initialize (missing model download, dependency
    conflict), retrieval transparently falls back to keyword search over the
    side-table so classroom demos keep working (EMCP-DOC-060).
    """

    # @spec EMCP-DOC-001

    def __init__(
        self,
        table_name: str = DEFAULT_TABLE_NAME,
        storage_path: Path | None = None,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> None:
        self.table_name = table_name
        self.embedding_model = embedding_model
        self.storage_path = storage_path
        self._text_to_record: dict[str, CitationRecord] = {}
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
        # @spec EMCP-DOC-060
        try:
            from llamabot import LanceDBDocStore

            kwargs: dict = {
                "table_name": table_name,
                "embedding_model": embedding_model,
            }
            if storage_path is not None:
                kwargs["storage_path"] = storage_path  # @spec EMCP-DOC-003
            return LanceDBDocStore(**kwargs)  # @spec EMCP-DOC-020
        except Exception:
            return None

    @property
    def backend_name(self) -> str:
        """Return the active backend name (``lancedb`` or ``keyword``)."""
        return "lancedb" if self._backend is not None else "keyword"

    def reset(self) -> None:
        """Clear the backend and the side-table."""
        self._text_to_record.clear()
        if self._backend is not None:
            try:
                self._backend.reset()
            except Exception:
                pass

    def ingest(
        self,
        records: list[CitationRecord],
        composer: Callable[[CitationRecord], str] | None = None,
    ) -> int:
        """Store citation records as searchable documents.

        :param records: Citation records to ingest.
        :param composer: Callable mapping a record to its stored text. Defaults
            to :func:`compose_document_text`; participants pass their own in
            Exercise 1.
        :returns: Number of newly stored documents.
        """
        # @spec EMCP-DOC-010
        if composer is None:
            composer = compose_document_text
        added = 0
        for record in records:
            text = composer(record)
            self._text_to_record[text] = record  # @spec EMCP-DOC-013
            if self._backend is not None:
                try:
                    self._backend.append(text)
                except Exception:
                    pass
            added += 1
        return added

    def search(self, query: str, limit: int = 5) -> list[DocstoreSearchHit]:
        """Retrieve the most relevant citation items for a query.

        :param query: Search terms.
        :param limit: Maximum number of hits to return.
        :returns: Search hits carrying citation metadata and a text snippet.
        """
        # @spec EMCP-DOC-040
        # @spec EMCP-DOC-043
        if not query.strip():  # @spec EMCP-SRV-041
            return []
        limit = max(1, limit)  # @spec EMCP-SRV-042

        if self._backend is not None:
            texts = self._retrieve_semantic(query, limit)
        else:
            texts = self._retrieve_keyword(query, limit)  # @spec EMCP-DOC-060

        hits: list[DocstoreSearchHit] = []
        for text in texts:
            record = self._text_to_record.get(text)  # @spec EMCP-DOC-021
            if record is None:
                continue
            hits.append(self._to_hit(record, text))  # @spec EMCP-DOC-042
        return hits[:limit]

    def _retrieve_semantic(self, query: str, limit: int) -> list[str]:
        """Query the LanceDB backend for stored document text."""
        try:
            return list(self._backend.retrieve(query, n_results=limit))
        except Exception:
            return self._retrieve_keyword(query, limit)

    def _retrieve_keyword(self, query: str, limit: int) -> list[str]:
        """Fallback: rank stored documents by keyword overlap with the query."""
        terms = [t for t in re.split(r"\W+", query.lower()) if t]
        scored: list[tuple[int, str]] = []
        for text in self._text_to_record:
            haystack = text.lower()
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                scored.append((score, text))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [text for _, text in scored[:limit]]

    @staticmethod
    def _to_hit(record: CitationRecord, snippet: str) -> DocstoreSearchHit:
        """Project a citation record + retrieved text into a search hit."""
        # @spec EMCP-SRV-014
        return DocstoreSearchHit(
            key=record.key,
            title=record.title,
            creators=list(record.creators),
            year=record.year,
            abstract=record.abstract,
            url=record.url,
            snippet=snippet,
        )

    @property
    def stats(self) -> DocstoreStats:
        """Return summary statistics for the docstore."""
        # @spec EMCP-DOC-050
        return DocstoreStats(
            table_name=self.table_name,
            document_count=len(self._text_to_record),
            embedding_model=self.embedding_model,
            backend=self.backend_name,
        )

    def get_metadata(self, key: str) -> CitationRecord | None:
        """Look up a citation record by Zotero key.

        :param key: Zotero item key.
        :returns: Matching record, or None.
        """
        for record in self._text_to_record.values():
            if record.key == key:
                return record
        return None

    def all_keys(self) -> list[str]:
        """Return all known Zotero item keys in the side-table."""
        # @spec EMCP-DOC-011
        return sorted({record.key for record in self._text_to_record.values()})


def build_search_json(
    hits: list[DocstoreSearchHit],
    mode: str,
    stats: DocstoreStats,
) -> str:
    """Serialize docstore search hits for MCP tool output.

    :param hits: Search hits to return.
    :param mode: Backend mode used for ingestion (``fixtures``/``pyzotero``/...).
    :param stats: Docstore statistics.
    :returns: JSON string with ``mode``, ``items``, and ``docstore_stats``;
        includes a ``message`` field when no hits are returned.
    """
    # @spec EMCP-SRV-013
    payload: dict = {
        "mode": mode,
        "items": [hit.model_dump() for hit in hits],
        "docstore_stats": stats.model_dump(),
    }
    if not hits:  # @spec EMCP-DOC-061
        if stats.document_count == 0:
            payload["message"] = "Docstore is empty; no papers ingested."
        else:
            payload["message"] = "No documents matched the query."
    return json.dumps(payload, ensure_ascii=False)


def load_ingest_records() -> tuple[list[CitationRecord], str]:
    """Load papers for docstore ingestion from pyzotero or fixtures.

    :returns: Tuple of citation records and the backend mode used.
    """
    # @spec EMCP-SRV-031
    # @spec EMCP-SRV-032
    import os

    from loguru import logger

    from build_deep_research_agent.fixtures.loader import load_citation_fixtures
    from build_deep_research_agent.mcp.zotero_backend import _search_with_pyzotero

    if os.getenv("TUTORIAL_ZOTERO_FORCE_FIXTURES", "").lower() in {"1", "true", "yes"}:
        return (
            load_citation_fixtures(),
            "fixtures",
        )  # @spec EMCP-SRV-030  # @spec EMCP-SRV-033

    has_creds = bool(os.getenv("ZOTERO_LIBRARY_ID") and os.getenv("ZOTERO_API_KEY"))
    if has_creds:
        try:
            return _search_with_pyzotero("", limit=50), "pyzotero"  # @spec EMCP-SRV-033
        except Exception as exc:  # @spec EMCP-SRV-040
            logger.warning(
                "pyzotero ingestion failed; falling back to fixtures: {}", exc
            )
    return load_citation_fixtures(), "fixtures"


def build_zotero_research_server(
    store: ZoteroDocstore | None = None,
) -> FastMCP:
    """Assemble the reference docstore-backed Zotero MCP server.

    Used by the Part 3 notebook's ``__main__`` block for reliable dual-mode
    server execution (the cooking-show dish already in the oven). In narrative
    mode, participants assemble the equivalent server themselves from
    ``exercises/part3.py``.

    :param store: Optional pre-built docstore; otherwise fixtures are ingested.
    :returns: A ``FastMCP`` server ready for ``.run()``.
    """
    # @spec EMCP-SRV-001
    from fastmcp import FastMCP

    if store is None:
        store = ZoteroDocstore()
        records, mode = load_ingest_records()
        store.ingest(records)
    else:
        mode = "fixtures"

    mcp = FastMCP(
        name="zotero-research",
        instructions=(
            "Embedded Zotero MCP server for SciPy 2026 Part 3. "
            "Semantic search over an ingested citation docstore."
        ),
    )

    @mcp.tool
    def zotero_search_items(query: str, limit: int = 5) -> str:
        """Search the ingested Zotero docstore for items matching a query.

        :param query: Search terms (semantic match over titles + abstracts).
        :param limit: Maximum number of items to return.
        :returns: JSON payload with ``mode``, ``items``, and ``docstore_stats``.
        """
        # @spec EMCP-SRV-010
        # @spec EMCP-SRV-013
        # @spec EMCP-DOC-041
        hits = store.search(query, limit=limit)
        return build_search_json(hits, mode=mode, stats=store.stats)

    @mcp.resource("zotero://metadata/{key}")
    def zotero_metadata(key: str) -> str:
        """Return full citation metadata for a Zotero item key.

        :param key: Zotero item key.
        :returns: JSON citation metadata, or an empty-object fallback.
        """
        # @spec EMCP-SRV-021
        record = store.get_metadata(key)
        if record is None:
            return json.dumps({"key": key, "found": False}, ensure_ascii=False)
        return json.dumps({**record.model_dump(), "found": True}, ensure_ascii=False)

    @mcp.resource("zotero://metadata")
    def zotero_metadata_index() -> str:
        """Return the list of all available citation keys.

        :returns: JSON list of Zotero item keys in the docstore.
        """
        # @spec EMCP-SRV-022
        return json.dumps(store.all_keys(), ensure_ascii=False)

    return mcp
