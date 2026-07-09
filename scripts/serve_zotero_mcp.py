"""Headless FastMCP stdio server for the Zotero research docstore.

This is the **server-mode entrypoint** for Part 3, factored out of the
Marimo notebook so that Marimo's save (which rewrites the notebook's
``if __name__ == "__main__"`` footer to ``app.run()``) cannot clobber it.
The notebook (``notebooks/03_tools_mcp_zotero.py``) is the interactive
narrative; this shim is the runnable server. Both share one library
builder, :func:`build_deep_research_agent.mcp.docstore.build_zotero_research_server`.

Run:

    uv run scripts/serve_zotero_mcp.py
    # or: pixi run python scripts/serve_zotero_mcp.py
"""

from __future__ import annotations

from build_deep_research_agent.mcp.docstore import build_zotero_research_server


def main() -> None:
    """Build the reference Zotero research server and serve it over stdio."""
    # @spec EMCP-RUN-001
    # @spec EMCP-RUN-002
    # @spec EMCP-RUN-003
    # @spec EMCP-RUN-020
    # @spec EMCP-SRV-003
    # @spec EMCP-SRV-050
    build_zotero_research_server().run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()
