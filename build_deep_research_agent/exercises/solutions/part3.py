"""Part 3 exercises — instructor reference solutions (new ``@tool`` → MCP arc).

The notebook scaffolds delegate to these by default so they run green; learners
override a scaffold body to implement it themselves. These in turn delegate to
the library capabilities in :mod:`build_deep_research_agent.tools`.
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP

from build_deep_research_agent.models import CitationRecord, CorpusPaper
from build_deep_research_agent.tools.corpus import build_corpus_docstore as _build
from build_deep_research_agent.tools.corpus import (
    connect_corpus_docstore as _connect,
)
from build_deep_research_agent.tools.corpus import (
    search_corpus_payload as _search_payload,
)
from build_deep_research_agent.tools.zotero import pyzotero_keyword_search


def search_zotero(query: str, limit: int = 5) -> dict:
    """Keyword-search the participant's Zotero library (requires credentials).

    No fixture fallback — this is the real-thing stretch, so it raises if
    ``ZOTERO_LIBRARY_ID`` / ``ZOTERO_API_KEY`` are not set.

    :param query: Search terms.
    :param limit: Maximum records to return.
    :returns: Dict with ``mode`` ("zotero") and ``items``.
    """
    # @spec EMCP-TOOL-001
    # @spec EMCP-TOOL-010
    records = pyzotero_keyword_search(query, limit=limit)  # raises if no creds
    return {"mode": "zotero", "items": [r.model_dump() for r in records]}


def build_zotero_docstore():
    """Fetch the participant's Zotero items and build a docstore over them.

    Delegates to :mod:`build_deep_research_agent.tools.zotero`. Indexed text is
    each item's abstract plus extracted PDF full text.

    :returns: ``(docstore, side_table)``.
    """
    # @spec EMCP-TOOL-011
    from build_deep_research_agent.tools.zotero import (
        build_zotero_docstore as _build,
    )
    from build_deep_research_agent.tools.zotero import (
        fetch_zotero_items,
    )

    return _build(fetch_zotero_items())


def search_zotero_semantic(
    docstore: Any,
    side_table: dict[str, list[CitationRecord]],
    query: str,
    limit: int = 5,
) -> dict:
    """Semantic search over the Zotero docstore; result dict.

    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> :class:`CitationRecord` mapping.
    :param query: Search terms.
    :param limit: Maximum items to return.
    :returns: Dict with ``mode`` ("zotero-semantic") and ``items``.
    """
    # @spec EMCP-TOOL-011
    from build_deep_research_agent.tools.zotero import retrieve_zotero

    hits = retrieve_zotero(docstore, side_table, query, limit)
    return {"mode": "zotero-semantic", "items": hits}


def build_corpus_docstore(
    papers: list[CorpusPaper], *, table_name: str = "corpus_papers"
) -> tuple[Any, dict[str, list[CorpusPaper]]]:
    """Build a raw ``LanceDBDocStore`` + side-table over the corpus.

    :param papers: Corpus papers to ingest.
    :param table_name: LanceDB table name.
    :returns: ``(docstore, side_table)`` — the side-table maps each stored chunk
        text back to its :class:`CorpusPaper`.
    """
    # @spec EMCP-DOC-010
    # @spec EMCP-DOC-011
    return _build(papers, table_name=table_name)


def connect_corpus_docstore(
    papers: list[CorpusPaper], *, table_name: str = "corpus_papers"
) -> tuple[Any, dict[str, list[CorpusPaper]]]:
    """Connect to an existing corpus docstore, or build one if none exists.

    Reuses the on-disk LanceDB table from a prior notebook (e.g. notebook 3)
    without resetting it. Falls back to ingesting if the table is empty.

    :param papers: Corpus papers (used to rebuild the side-table).
    :param table_name: LanceDB table name.
    :returns: ``(docstore, side_table)`` — the side-table maps each stored chunk
        text back to its :class:`CorpusPaper`.
    """
    return _connect(papers, table_name=table_name)


def search_corpus(
    docstore: Any,
    side_table: dict[str, list[CorpusPaper]],
    query: str,
    limit: int = 5,
    *,
    mode: str = "corpus",
) -> dict:
    """Query the corpus docstore; result dict with items + docstore_stats.

    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> :class:`CorpusPaper` mapping.
    :param query: Search terms.
    :param limit: Maximum papers to return.
    :param mode: Backend mode reported in the result.
    :returns: Dict with ``mode``, ``items``, and ``docstore_stats`` — the
        llamabot ``@tool`` / FastMCP layer serializes it to JSON.
    """
    # @spec EMCP-DOC-040
    # @spec EMCP-DOC-050
    # @spec EMCP-TOOL-010
    return _search_payload(docstore, side_table, query, limit, mode=mode)


def register_corpus_tools(
    mcp: FastMCP,
    docstore: Any,
    side_table: dict[str, list[CorpusPaper]],
    *,
    mode: str = "corpus",
) -> None:
    """Register the ``search_corpus`` MCP tool + a papers-index resource.

    :param mcp: The FastMCP server to register on.
    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> :class:`CorpusPaper` mapping.
    :param mode: Backend mode reported by the search tool.
    """
    # @spec EMCP-SRV-001
    # @spec EMCP-SRV-011

    @mcp.tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested paper corpus.

        :param query: Search terms (semantic match over full text).
        :param limit: Maximum papers to return.
        :returns: Dict with ``mode``, ``items``, and ``docstore_stats`` (FastMCP
            serializes it to JSON for the client).
        """
        # @spec EMCP-SRV-014
        # @spec EMCP-SRV-015
        return _search_payload(docstore, side_table, query, limit, mode=mode)

    @mcp.resource("corpus://papers")
    def corpus_papers_index() -> str:
        """List the papers in the corpus (title + source id)."""
        # @spec EMCP-SRV-022
        seen = {}
        for paper in side_table.values():
            seen.setdefault(paper.source_id, paper)
        return json.dumps(
            [
                {"title": p.title, "source_id": p.source_id, "source": p.source}
                for p in seen.values()
            ],
            ensure_ascii=False,
        )
