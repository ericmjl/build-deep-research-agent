"""Part 3 embedded-MCP exercises — instructor reference solutions."""

from __future__ import annotations

import json

from fastmcp import FastMCP

from build_deep_research_agent.mcp.docstore import (
    ZoteroDocstore,
    build_search_json,
)
from build_deep_research_agent.models import CitationRecord


def compose_doc_text(record: CitationRecord) -> str:
    """Render a citation record as the searchable text stored in the docstore.

    :param record: Citation record to render.
    :returns: The searchable text blob for this paper.
    """
    # @spec EMCP-DOC-012
    creators = ", ".join(record.creators) if record.creators else "Unknown"
    body = record.abstract or record.title
    return f"{record.title}\nAuthors: {creators}\n{body}"


def make_docstore(
    records: list[CitationRecord],
    *,
    table_name: str = "zotero_papers",
) -> ZoteroDocstore:
    """Create a ZoteroDocstore and ingest the given citation records.

    :param records: Citation records to ingest as searchable documents.
    :param table_name: LanceDB table name for the docstore.
    :returns: A populated ``ZoteroDocstore``.
    """
    # @spec EMCP-DOC-010
    store = ZoteroDocstore(table_name=table_name)
    store.ingest(records, composer=compose_doc_text)
    return store


def zotero_search_items_fn(
    store: ZoteroDocstore,
    query: str,
    limit: int = 5,
    *,
    mode: str = "fixtures",
) -> str:
    """Search the docstore and return the MCP JSON payload.

    :param store: The populated docstore to search.
    :param query: Search terms.
    :param limit: Maximum number of items to return.
    :param mode: Backend mode to report in the payload.
    :returns: JSON string with ``mode``, ``items``, and ``docstore_stats``.
    """
    # @spec EMCP-DOC-040
    # @spec EMCP-DOC-042
    hits = store.search(query, limit=limit)
    return build_search_json(hits, mode=mode, stats=store.stats)


def register_zotero_tools(
    mcp: FastMCP,
    store: ZoteroDocstore,
    *,
    mode: str = "fixtures",
) -> None:
    """Register the zotero_search_items tool and metadata resources on the server.

    :param mcp: The FastMCP server to register tools/resources on.
    :param store: The populated docstore backing the tools.
    :param mode: Backend mode reported by the search tool.
    """
    # @spec EMCP-SRV-010

    @mcp.tool
    def zotero_search_items(query: str, limit: int = 5) -> str:
        """Search the ingested Zotero docstore for items matching a query.

        :param query: Search terms (semantic match over titles + abstracts).
        :param limit: Maximum number of items to return.
        :returns: JSON payload with ``mode``, ``items``, and ``docstore_stats``.
        """
        # @spec EMCP-SRV-011
        # @spec EMCP-SRV-012
        hits = store.search(query, limit=limit)
        return build_search_json(hits, mode=mode, stats=store.stats)

    @mcp.resource("zotero://metadata/{key}")
    def zotero_metadata(key: str) -> str:
        """Return full citation metadata for a Zotero item key.

        :param key: Zotero item key.
        :returns: JSON citation metadata, or a not-found fallback.
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
