"""Part 3 embedded-MCP exercises — legacy stub module (not used by the notebook).

Part 3 exercises are now implemented as **in-cell scaffolds** directly in
``notebooks/03_tools_mcp_zotero.py`` (TUT-MARIMO-014): each scaffold imports
the reference answer from :mod:`build_deep_research_agent.exercises.solutions.part3`
by default and learners override the scaffold body. Reference answers live in
``build_deep_research_agent/exercises/solutions/part3.py``.

This stub module is retained only for layout parity with Parts 2 & 4
(TUT-MARIMO-023) and is not imported by the notebook.
"""

from __future__ import annotations

from fastmcp import FastMCP

from build_deep_research_agent.mcp.docstore import ZoteroDocstore
from build_deep_research_agent.models import CitationRecord


def compose_doc_text(record: CitationRecord) -> str:
    """Render a citation record as the searchable text stored in the docstore.

    Implementation spec: Exercise 1a in ``notebooks/03_tools_mcp_zotero.py``.

    The string you return is both what the docstore embeds/retrieves AND the key
    into the metadata side-table, so it must capture the content you want search
    to match (title + authors + abstract is a good starting point).

    :param record: Citation record to render.
    :returns: The searchable text blob for this paper.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Override the compose_doc_text scaffold in notebooks/03_tools_mcp_zotero.py (Exercise 1a)"
    )


def make_docstore(
    records: list[CitationRecord],
    *,
    table_name: str = "zotero_papers",
) -> ZoteroDocstore:
    """Create a ZoteroDocstore and ingest the given citation records.

    Implementation spec: Exercise 1b in ``notebooks/03_tools_mcp_zotero.py``.

    Pass your :func:`compose_doc_text` as the ``composer`` to
    ``store.ingest(...)`` so the docstore stores the text you designed.

    :param records: Citation records to ingest as searchable documents.
    :param table_name: LanceDB table name for the docstore.
    :returns: A populated ``ZoteroDocstore``.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Override the make_docstore scaffold in notebooks/03_tools_mcp_zotero.py (Exercise 1b)"
    )


def zotero_search_items_fn(
    store: ZoteroDocstore,
    query: str,
    limit: int = 5,
    *,
    mode: str = "fixtures",
) -> str:
    """Search the docstore and return the MCP JSON payload.

    Implementation spec: Exercise 2 in ``notebooks/03_tools_mcp_zotero.py``.

    :param store: The populated docstore to search.
    :param query: Search terms.
    :param limit: Maximum number of items to return.
    :param mode: Backend mode to report in the payload.
    :returns: JSON string with ``mode``, ``items``, and ``docstore_stats``.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Override the zotero_search_items_fn scaffold in notebooks/03_tools_mcp_zotero.py (Exercise 2)"
    )


def register_zotero_tools(
    mcp: FastMCP,
    store: ZoteroDocstore,
    *,
    mode: str = "fixtures",
) -> None:
    """Register the zotero_search_items tool and metadata resources on the server.

    Implementation spec: Exercise 3 in ``notebooks/03_tools_mcp_zotero.py``.

    :param mcp: The FastMCP server to register tools/resources on.
    :param store: The populated docstore backing the tools.
    :param mode: Backend mode reported by the search tool.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Override the register_zotero_tools scaffold in notebooks/03_tools_mcp_zotero.py (Exercise 3)"
    )
