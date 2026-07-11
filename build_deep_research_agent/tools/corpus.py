"""Raw llamabot ``LanceDBDocStore`` wiring over the Part 3 corpus.

This is the *reference* implementation of the phase-3 docstore wiring — used by
the notebook scaffolds (via ``exercises/solutions/part3.py``) and the standalone
corpus MCP server. It teaches the primitive directly: llamabot docstores are
**string-in / string-out**, so a side-table maps each stored chunk back to the
:class:`CorpusPaper` it came from (EMCP-DOC-011). Nothing here hides the
docstore behind a wrapper class.
"""

from __future__ import annotations

from typing import Any

from build_deep_research_agent.models import CorpusPaper

DEFAULT_TABLE = "corpus_papers"  # @spec EMCP-DOC-013
DEFAULT_EMBEDDING = "minishlab/potion-base-8M"  # @spec EMCP-DOC-013
CHUNK_SIZE = 1200


def chunk_text(text: str, *, size: int = CHUNK_SIZE) -> list[str]:
    """Split full text into roughly ``size``-char passages on paragraph breaks.

    :param text: Full paper text.
    :param size: Target passage length in characters.
    :returns: Non-empty passage strings.
    """
    # @spec EMCP-DOC-010
    passages: list[str] = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        while len(para) > size:
            passages.append(para[:size].strip())
            para = para[size:]
        if para:
            passages.append(para)
    return passages or [text[:size].strip()]


def build_corpus_docstore(
    papers: list[CorpusPaper],
    *,
    table_name: str = DEFAULT_TABLE,
    embedding_model: str = DEFAULT_EMBEDDING,
) -> tuple[Any, dict[str, list[CorpusPaper]]]:
    """Build a raw ``LanceDBDocStore`` + side-table over corpus papers.

    Each paper's ``full_text`` is chunked; every chunk is appended to the
    docstore and recorded in the side-table so retrieval can project back to the
    parent paper. The side-table maps each chunk text -> the list of papers that
    contain it (a chunk text shared by two papers — e.g. boilerplate — maps to
    both, so retrieval never silently loses a paper).

    :param papers: Corpus papers to ingest.
    :param table_name: LanceDB table name.
    :param embedding_model: Embedding model identifier.
    :returns: Tuple of ``(docstore, side_table)`` where ``side_table`` maps each
        stored chunk text -> the list of :class:`CorpusPaper` s containing it.
    """
    # @spec EMCP-DOC-010
    # @spec EMCP-DOC-011
    from llamabot import LanceDBDocStore

    docstore = LanceDBDocStore(
        table_name=table_name,
        embedding_model=embedding_model,
        auto_create_fts_index=False,  # we use vector semantic search, not keyword FTS
    )
    try:
        docstore.reset()  # idempotent: clear any persisted data from a prior run
    except Exception:  # noqa: BLE001
        pass
    side_table: dict[str, list[CorpusPaper]] = {}
    for paper in papers:
        for chunk in chunk_text(paper.full_text):
            docstore.append(chunk)
            side_table.setdefault(chunk, []).append(paper)
    return docstore, side_table


def connect_corpus_docstore(
    papers: list[CorpusPaper],
    *,
    table_name: str = DEFAULT_TABLE,
    embedding_model: str = DEFAULT_EMBEDDING,
) -> tuple[Any, dict[str, list[CorpusPaper]]]:
    """Connect to an existing corpus docstore, or build one if none exists.

    Unlike :func:`build_corpus_docstore` (which resets and re-ingests on every
    call), this function **preserves** an existing on-disk table. This lets a
    later notebook reconnect to a docstore built in an earlier one without
    re-chunking and re-embedding the entire corpus.

    The side-table is always rebuilt in memory from the same papers — it is a
    pure function of paper text → chunks, so it is identical across sessions.

    :param papers: Corpus papers (used to rebuild the side-table and to ingest
        if the docstore is empty).
    :param table_name: LanceDB table name.
    :param embedding_model: Embedding model identifier.
    :returns: Tuple of ``(docstore, side_table)`` where ``side_table`` maps each
        stored chunk text -> the list of :class:`CorpusPaper` s containing it.
    """
    from llamabot import LanceDBDocStore

    docstore = LanceDBDocStore(
        table_name=table_name,
        embedding_model=embedding_model,
        auto_create_fts_index=False,
    )

    side_table: dict[str, list[CorpusPaper]] = {}
    for paper in papers:
        for chunk in chunk_text(paper.full_text):
            side_table.setdefault(chunk, []).append(paper)

    if not docstore.existing_records:
        for chunk in side_table:
            docstore.append(chunk)

    return docstore, side_table


def retrieve_corpus(
    docstore: Any,
    side_table: dict[str, list[CorpusPaper]],
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Retrieve chunks and project to one hit per paper.

    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> list of :class:`CorpusPaper` s containing it.
    :param query: Search terms.
    :param limit: Maximum papers to return.
    :returns: Hit dicts (paper metadata + retrieved ``snippet``).
    """
    # @spec EMCP-DOC-012
    # @spec EMCP-DOC-040
    if not query.strip():  # @spec EMCP-DOC-041
        return []
    texts = list(docstore.retrieve(query, n_results=max(1, limit)))
    hits: list[dict] = []
    seen: set[str] = set()
    for text in texts:
        for paper in side_table.get(text, ()):
            if paper.source_id in seen:
                continue
            seen.add(paper.source_id)
            hits.append(
                {
                    "title": paper.title,
                    "authors": paper.authors,
                    "year": paper.year,
                    "url": paper.url,
                    "source": paper.source,
                    "domain": paper.domain,
                    "snippet": text,
                }
            )
            break
    return hits[:limit]


def search_corpus_payload(
    docstore: Any,
    side_table: dict[str, list[CorpusPaper]],
    query: str,
    limit: int = 5,
    *,
    mode: str = "corpus",
) -> dict:
    """Query the corpus docstore and return the result payload as a dict.

    Returns a plain dict (``mode``, ``items``, ``docstore_stats``); the llamabot
    ``@tool`` / FastMCP layer serializes it to JSON for the consumer.

    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> :class:`CorpusPaper` mapping.
    :param query: Search terms.
    :param limit: Maximum papers to return.
    :param mode: Backend mode reported in the result.
    :returns: Result dict with ``mode``, ``items``, and ``docstore_stats``.
    """
    # @spec EMCP-DOC-050
    hits = retrieve_corpus(docstore, side_table, query, limit)
    paper_count = len({p.source_id for papers in side_table.values() for p in papers})
    payload: dict = {
        "mode": mode,
        "items": hits,
        "docstore_stats": {
            "table_name": DEFAULT_TABLE,
            "document_count": paper_count,
            "embedding_model": DEFAULT_EMBEDDING,
            "backend": "lancedb",
        },
    }
    if not hits:  # @spec EMCP-DOC-041
        payload["message"] = (
            "Docstore is empty; no papers ingested."
            if paper_count == 0
            else "No documents matched the query."
        )
    return payload
