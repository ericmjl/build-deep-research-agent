"""Standalone corpus MCP server — Part 3 reference answer.

Run::

    pixi run python scripts/serve_corpus_mcp.py

Then point your coding assistant (opencode / Claude Desktop / Cursor) at this
stdio MCP server and ask it about the corpus. This is the payoff of Part 3: the
capability you built as an in-process llamabot ``@tool`` is now reachable by any
client that speaks MCP.

Same shape as ``scripts/serve_corpus_mcp_starter.py`` but with the reference
``search_corpus`` implementation (and a ``corpus://papers`` resource), registered
via ``part3.register_corpus_tools``.
"""

from __future__ import annotations

from fastmcp import FastMCP

from build_deep_research_agent.exercises.solutions import part3
from build_deep_research_agent.fixtures.loader import load_corpus_papers

# 1. Create the MCP server.
mcp = FastMCP(  # @spec EMCP-SRV-001
    name="corpus-research",
    instructions=(
        "Embedded corpus MCP server for SciPy 2026 Part 3. "
        "Semantic search over an ingested arXiv + JOSS full-text corpus."
    ),
)

# 2. Build the docstore over the corpus (own table, separate from the
#    notebook's Exercise 1 docstore).
papers = load_corpus_papers()  # @spec EMCP-DOC-004
docstore, side_table = part3.build_corpus_docstore(  # @spec EMCP-DOC-010
    papers, table_name="corpus_papers_mcp"
)

# 3. Attach the search_corpus tool + a corpus://papers resource (the answer).
part3.register_corpus_tools(mcp, docstore, side_table, mode="corpus")

if __name__ == "__main__":  # @spec EMCP-SRV-010
    mcp.run(transport="stdio", show_banner=False)
