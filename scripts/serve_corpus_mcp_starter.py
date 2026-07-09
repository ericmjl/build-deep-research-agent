"""Standalone corpus MCP server — Part 3, Exercise 3 scaffold.

This file IS the scaffold. Fill in the ``search_corpus`` tool body below, then
run it from a terminal::

    pixi run python scripts/serve_corpus_mcp_starter.py

and point your coding assistant at the stdio server. The reference answer is
``scripts/serve_corpus_mcp.py``.

Nothing is hidden behind a ``build_server()`` factory: the server construction,
docstore, tool attachment, and ``run`` are all inline at module level below, so
you can see every step of how an MCP server is assembled.
"""

from __future__ import annotations

from fastmcp import FastMCP

from build_deep_research_agent.exercises.solutions import part3
from build_deep_research_agent.fixtures.loader import load_corpus_papers

# 1. Create the MCP server. FastMCP is the Python library that turns
#    @mcp.tool-decorated functions into tools any MCP client can call.
mcp = FastMCP(  # @spec EMCP-SRV-001
    name="corpus-research",
    instructions=(
        "Corpus MCP server for SciPy 2026 Part 3, Exercise 3. "
        "Semantic search over an ingested arXiv + JOSS full-text corpus."
    ),
)

# 2. Build the docstore over the corpus. part3.build_corpus_docstore does the
#    Exercise 1 wiring for you (chunk each paper, append, keep the side-table).
#    A distinct table_name keeps this server's docstore separate from the
#    notebook's Exercise 1 docstore so the two don't clobber each other on disk.
papers = load_corpus_papers()  # @spec EMCP-DOC-004
docstore, side_table = part3.build_corpus_docstore(  # @spec EMCP-DOC-010
    papers, table_name="corpus_papers_mcp"
)


# 3. Attach the `search_corpus` tool to the server. The @mcp.tool decorator is
#    what BINDS this function to the server — that is the line that answers
#    "where is the tool attached?". Fill in the body (reuse your Exercise 2
#    logic: retrieve from `docstore`, project via `side_table`, return a dict).
#    FastMCP auto-serializes the dict to JSON for the client — no json.dumps.
@mcp.tool
def search_corpus(query: str, limit: int = 5) -> dict:  # @spec EMCP-SRV-011
    """Semantic search over the ingested paper corpus.

    :param query: Search terms (semantic match over full text).
    :param limit: Maximum papers to return.
    :returns: Dict with ``mode``, ``items``, and ``docstore_stats``.
    """
    # put your implementation here (retrieve + project + return a dict).
    # @spec EMCP-SRV-014
    # @spec EMCP-SRV-015
    ...


if __name__ == "__main__":  # @spec EMCP-SRV-010
    mcp.run(transport="stdio", show_banner=False)
