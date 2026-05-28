"""Tutorial FastMCP server for Zotero search (cooking-show fallback).

Run via::

    python -m build_deep_research_agent.mcp.server

or the ``tutorial-zotero-mcp`` console script. Uses pyzotero when credentials
are configured; otherwise searches bundled citation fixtures so Part 3 demos
work without upstream ``zotero-mcp`` installed.
"""

# @spec TOOLS-TUT-001
# @spec TUT-INFRA-022

from __future__ import annotations

from fastmcp import FastMCP

from build_deep_research_agent.mcp.zotero_backend import (
    records_to_search_json,
    search_zotero_items,
)

mcp = FastMCP(
    name="zotero",
    instructions=(
        "Tutorial Zotero MCP server for SciPy 2026. "
        "Search a participant library via pyzotero when configured, "
        "otherwise search bundled fixtures."
    ),
)


@mcp.tool
def zotero_search_items(query: str, limit: int = 5) -> str:
    """Search the Zotero library for items matching a query.

    Uses the Zotero Web API or local Zotero when ``ZOTERO_*`` env vars are set.
    Falls back to bundled tutorial fixtures for offline classroom demos.

    :param query: Search terms (title, author, or keywords).
    :param limit: Maximum number of items to return.
    :returns: JSON payload with ``mode`` and ``items`` fields.
    """
    # @spec TOOLS-TUT-003
    records, mode = search_zotero_items(query, limit=limit)
    return records_to_search_json(records, mode=mode)


def main() -> None:
    """Run the tutorial Zotero MCP server over stdio."""
    # @spec TOOLS-TUT-002
    mcp.run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()
