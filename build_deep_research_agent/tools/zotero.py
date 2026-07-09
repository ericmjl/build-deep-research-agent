"""pyzotero keyword-search primitive for the Zotero ``@tool``.

``pyzotero_keyword_search`` delegates straight to the pyzotero package — the
credential check and fixture fallback live in ``search_zotero`` itself (see
``exercises/solutions/part3.py``), so participants see how the tool works end
to end rather than through a wrapper.
"""

from __future__ import annotations

import os
import re
from typing import Any

from build_deep_research_agent.models import CitationRecord


def _to_citation(item: dict) -> CitationRecord:
    """Convert a pyzotero item payload to a :class:`CitationRecord`.

    :param item: Raw item dict from pyzotero.
    :returns: Normalized citation record.
    """
    data = item.get("data", item)
    creators: list[str] = []
    for creator in data.get("creators", []):
        if creator.get("name"):
            creators.append(creator["name"])
            continue
        last = creator.get("lastName", "").strip()
        first = creator.get("firstName", "").strip()
        name = f"{last}, {first}" if first else last
        if name:
            creators.append(name)
    year = None
    match = re.search(r"\d{4}", data.get("date") or "")
    if match:
        year = int(match.group())
    return CitationRecord(
        key=str(data.get("key") or "UNKNOWN"),
        title=str(data.get("title") or "Untitled"),
        creators=creators,
        year=year,
        abstract=data.get("abstractNote") or None,
        url=data.get("url") or None,
    )


def pyzotero_keyword_search(query: str, limit: int = 5) -> list[CitationRecord]:
    """Keyword-search the participant's Zotero library via pyzotero.

    :param query: Quick-search query string.
    :param limit: Maximum records to return.
    :returns: Matching citation records.
    :raises RuntimeError: If pyzotero is unavailable or credentials are missing.
    """
    # @spec EMCP-TOOL-001
    from pyzotero import zotero

    library_id = os.getenv("ZOTERO_LIBRARY_ID", "")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.getenv("ZOTERO_API_KEY", "")
    if not library_id or not api_key:
        raise RuntimeError(
            "Set ZOTERO_LIBRARY_ID and ZOTERO_API_KEY to search your Zotero library."
        )
    client = zotero.Zotero(library_id, library_type, api_key)
    items = client.top(q=query, limit=limit)
    return [_to_citation(item) for item in items]


def zotero_client():
    """Build a pyzotero client from env credentials (raises if absent).

    :returns: An authenticated ``pyzotero.zotero.Zotero`` client.
    :raises RuntimeError: If ``ZOTERO_LIBRARY_ID`` or ``ZOTERO_API_KEY`` are not set.
    """
    from pyzotero import zotero

    library_id = os.getenv("ZOTERO_LIBRARY_ID", "")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.getenv("ZOTERO_API_KEY", "")
    if not library_id or not api_key:
        raise RuntimeError(
            "Set ZOTERO_LIBRARY_ID and ZOTERO_API_KEY to use your Zotero library."
        )
    return zotero.Zotero(library_id, library_type, api_key)


def fetch_zotero_items(limit: int = 100) -> list[CitationRecord]:
    """Fetch the participant's top-level Zotero items as citation records.

    :param limit: Maximum items to fetch (pyzotero caps a single page).
    :returns: Matching citation records (metadata + abstracts).
    """
    client = zotero_client()
    return [_to_citation(item) for item in client.top(limit=limit)]


def zotero_item_full_text(client: Any, item_key: str) -> str:
    """Extract full text from a Zotero item's stored PDF attachment.

    Walks the item's children for a PDF attachment, downloads it via
    ``client.file(...)``, and extracts text with pymupdf. Returns ``""`` when
    there is no PDF or extraction fails.

    :param client: An authenticated pyzotero client.
    :param item_key: The Zotero item key.
    :returns: Extracted full text, or ``""``.
    """
    import pymupdf

    for child in client.children(item_key):
        data = child.get("data", child)
        if data.get("contentType") == "application/pdf":
            try:
                raw = client.file(child["key"])  # PDF bytes
                if isinstance(raw, str):  # defensive: annotation says str
                    raw = raw.encode()
                doc = pymupdf.open(stream=raw, filetype="pdf")
                return "\n".join(page.get_text() for page in doc)
            except Exception:  # noqa: BLE001
                return ""
    return ""


def build_zotero_docstore(
    items: list[CitationRecord],
) -> tuple[Any, dict[str, list[CitationRecord]]]:
    """Build a raw ``LanceDBDocStore`` over Zotero items (abstract + PDF text).

    For each item the indexed text is its abstract plus the extracted full text
    of any stored PDF attachment. Each chunk is appended to the docstore and
    recorded in a side-table mapping chunk text -> the ``CitationRecord``(s) it
    came from (same shape as the corpus docstore in :mod:`tools.corpus`).

    :param items: Citation records fetched from Zotero.
    :returns: ``(docstore, side_table)``.
    """
    import shutil
    from pathlib import Path

    from llamabot import LanceDBDocStore

    from build_deep_research_agent.tools.corpus import (
        DEFAULT_EMBEDDING,
        chunk_text,
    )

    table_name = "zotero_items"
    # Force a clean slate: a prior table can wedge `reset()` on a re-build, so
    # remove the on-disk table dir first (llamabot stores under ~/.llamabot/lancedb).
    _table_dir = (
        Path.home() / ".llamabot" / "lancedb" / f"{table_name.replace('_', '-')}.lance"
    )
    if _table_dir.exists():
        shutil.rmtree(_table_dir, ignore_errors=True)

    docstore = LanceDBDocStore(
        table_name=table_name,
        embedding_model=DEFAULT_EMBEDDING,
        auto_create_fts_index=False,
    )
    try:
        docstore.reset()  # belt-and-suspenders; no-op after the rmtree above
    except Exception:  # noqa: BLE001
        pass

    client = zotero_client()
    side_table: dict[str, list[CitationRecord]] = {}
    for item in items:
        text = item.abstract or ""
        full = zotero_item_full_text(client, item.key)
        if full:
            text = f"{text}\n\n{full}" if text else full
        if not text.strip():
            continue
        for chunk in chunk_text(text):
            docstore.append(chunk)
            side_table.setdefault(chunk, []).append(item)
    return docstore, side_table


def retrieve_zotero(
    docstore: Any,
    side_table: dict[str, list[CitationRecord]],
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Retrieve Zotero chunks and project to one hit per item.

    :param docstore: The raw ``LanceDBDocStore``.
    :param side_table: Chunk text -> :class:`CitationRecord` mapping.
    :param query: Search terms.
    :param limit: Maximum items to return.
    :returns: Hit dicts (citation metadata + retrieved ``snippet``).
    """
    if not query.strip():
        return []
    texts = list(docstore.retrieve(query, n_results=max(1, limit)))
    hits: list[dict] = []
    seen: set[str] = set()
    for text in texts:
        for item in side_table.get(text, ()):
            if item.key in seen:
                continue
            seen.add(item.key)
            hits.append(
                {
                    "title": item.title,
                    "creators": item.creators,
                    "year": item.year,
                    "url": item.url,
                    "abstract": item.abstract,
                    "snippet": text,
                }
            )
            break
    return hits[:limit]
