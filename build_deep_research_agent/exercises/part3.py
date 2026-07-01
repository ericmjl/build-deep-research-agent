"""Part 3 embedded-MCP exercises — learner stubs (edit this file).

You build the docstore-backed Zotero MCP server in three steps:

1. :func:`compose_doc_text` + :func:`make_docstore` — turn a citation into
   searchable text and ingest papers into a docstore.
2. :func:`zotero_search_items_fn` — the retrieval + JSON formatting body of the
   ``zotero_search_items`` MCP tool.
3. :func:`register_zotero_tools` — register the search tool and the
   ``zotero://metadata`` resources on a FastMCP server.

Implementation specs live in the markdown cells of ``notebooks/03_tools_mcp_zotero.py``.
Reference answers: ``build_deep_research_agent/exercises/solutions/part3.py``
(instructors comment-swap the import in the notebook).
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
        "Implement compose_doc_text in build_deep_research_agent/exercises/part3.py"
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
        "Implement make_docstore in build_deep_research_agent/exercises/part3.py"
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
        "Implement zotero_search_items_fn in build_deep_research_agent/exercises/part3.py"
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
        "Implement register_zotero_tools in build_deep_research_agent/exercises/part3.py"
    )
