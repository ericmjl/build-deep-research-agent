# Embedded Zotero MCP Server — Low-Level Design

**Created**: 2026-05-30
**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Tools (MCP)
**Part**: 3 (40 min) — **Eric Ma**
**Notebook**: `notebooks/03_tools_mcp_zotero.py`
**Framework**: FastMCP ≥3.3.1

## Overview

The Part 3 notebook is a **dual-mode artifact**: it is both an interactive Marimo teaching document and a valid Python file that runs as a headless FastMCP Zotero server. This LLD covers:

1. **MCP server anatomy** — tools, prompts, resources, and apps (FastMCP)
2. **Document pipeline** — chunking, storage via llamabot TurboQuant docstore
3. **Retrieval as an MCP tool** — docstore wrapped behind `zotero_search_items`
4. **Dual-mode runtime** — same file as server + narrative

## Dual-Mode Runtime

| Mode | Invocation | Behavior |
|------|-----------|----------|
| **Server** | `uv run notebooks/03_tools_mcp_zotero.py` | FastMCP stdio server, runs until interrupted |
| **Narrative** | `marimo serve notebooks/03_tools_mcp_zotero.py` | Marimo interactive notebook with explanatory cells |

The same file supports both modes because:
- FastMCP's `mcp.run()` is guarded by `if __name__ == "__main__":`
- Marimo wraps the file in a module context where `__name__ != "__main__"`
- Narrative cells (Marimo-specific) are wrapped in `@app.cell` decorators that don't interfere with plain Python execution

## MCP Server Anatomy

This is a key teaching moment: MCP servers expose **four primitive types** that agents can use:

| Primitive | Purpose | FastMCP decorator |
|-----------|---------|-------------------|
| **Tools** | Actions the agent can call (search, summarize, etc.) | `@mcp.tool` |
| **Resources** | Read-only data the agent can request (documents, configs) | `@mcp.resource` |
| **Prompts** | Pre-built message templates the agent can invoke | `@mcp.prompt` |
| **Apps** | Interactive UI components rendered in the conversation | `@mcp.app` (FastMCP-specific) |

The tutorial focuses on **tools** and **resources** for the Zotero server, with a brief mention of prompts and apps as extensions.

### Teaching progression

1. **Tools** — the primary primitive; `zotero_search_items` is a tool
2. **Resources** — the docstore index or citation metadata as a resource
3. **Prompts** — optional; a "research brief" prompt template
4. **Apps** — optional; FastMCP's interactive UI primitive

## Server Architecture

```
notebooks/03_tools_mcp_zotero.py
├── Narrative cells (Marimo @app.cell) — explain concepts
├── Server cells (plain Python) — run in both modes
│   ├── FastMCP server instantiation
│   ├── TurboQuant docstore setup (chunking, storage)
│   ├── Tool definitions (zotero_search_items)
│   ├── Resource definitions (optional: citation metadata)
│   └── mcp.run() entry point
└── Client demo cells (Marimo @app.cell) — test the server
```

### FastMCP Server Setup

| Component | Detail |
|-----------|--------|
| Server class | `FastMCP("zotero-research")` |
| Transport | stdio (default for MCP clients) |
| Tools | `zotero_search_items(query, limit)` — retrieval from docstore |
| Resources | `zotero://metadata/{key}` — citation metadata lookup |
| Docstore | llamabot TurboQuant docstore (chunking + vector storage) |
| Backend | pyzotero (live) or fixtures (fallback) for document ingestion |
| Entry guard | `if __name__ == "__main__": mcp.run()` |

### Tool Contract: `zotero_search_items`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search terms |
| `limit` | `int` | 5 | Maximum results |

**Returns**: JSON string with `mode`, `items` list, and `docstore_stats` (chunk count, embedding dimension).

Each item includes: `key`, `title`, `creators`, `date`, `publicationTitle`, `tags`, `url`, `snippet` (retrieved chunk excerpt).

### Resource Contract: `zotero://metadata/{key}`

| URI pattern | Returns |
|-------------|---------|
| `zotero://metadata/abc123` | Full citation metadata for key `abc123` |
| `zotero://metadata/` (no key) | List of all available keys |

## Document Pipeline (TurboQuant Docstore)

This is the core teaching concept: **building a document storage and retrieval system**, then exposing it as an MCP tool.

### Step 1: Document Ingestion

```python
from llamabot import TurboQuantDocstore

docstore = TurboQuantDocstore(
    collection="zotero_papers",
    embedding_model="all-MiniLM-L6-v2",
)

# Ingest papers from Zotero (pyzotero or fixtures)
for record in papers:
    docstore.add(
        doc_id=record.key,
        text=record.abstract or record.title,
        metadata={
            "title": record.title,
            "creators": record.creators,
            "date": record.date,
            "tags": record.tags,
        },
    )
```

### Step 2: Chunking

TurboQuant handles automatic text chunking:
- Splits documents into overlapping chunks
- Generates embeddings for each chunk
- Stores chunks in a vector index

### Step 3: Retrieval

```python
# The MCP tool wraps docstore retrieval
@mcp.tool
def zotero_search_items(query: str, limit: int = 5) -> str:
    results = docstore.similarity_search(query, k=limit)
    return format_results(results)
```

### Teaching points

- **Why chunk?** LLMs have context limits; chunking enables retrieval of relevant excerpts
- **Why embeddings?** Semantic search finds relevant papers even when query terms don't match exactly
- **Why wrap in MCP?** Any MCP client (agent, CLI, web UI) can use the same retrieval backend
- **Why dual-mode?** See the notebook, run it as a server — same code, different perspectives

## Notebook Cell Structure

The notebook is organized as a progressive walkthrough:

### Part A: Setup (Narrative)
- Introduction to MCP and the Model Context Protocol
- What this notebook will build (docstore + MCP server)
- Environment setup cell (imports, config)

### Part B: MCP Server Anatomy (Narrative + Code)
- **Narrative cell**: What is MCP? Why standardize tools?
- **Narrative cell**: The four MCP primitives — tools, resources, prompts, apps
- **Code cell**: `from fastmcp import FastMCP` — explain the import
- **Code cell**: `mcp = FastMCP("zotero-research")` — server instantiation
- **Narrative cell**: What does `@mcp.tool` do? Schema generation, validation

### Part C: Document Pipeline (Narrative + Code)
- **Narrative cell**: Why a docstore for research? Chunking, embeddings, retrieval
- **Code cell**: `from llamabot import TurboQuantDocstore` — introduce the docstore
- **Code cell**: Create docstore instance, configure embedding model
- **Narrative cell**: How chunking works — splitting documents into searchable pieces
- **Code cell**: Ingest papers from Zotero (pyzotero or fixtures) into docstore
- **Narrative cell**: How retrieval works — similarity search over embeddings
- **Code cell**: Test docstore retrieval directly (before wrapping in MCP)

### Part D: Building the MCP Tool (Mixed)
- **Narrative cell**: Wrapping docstore retrieval as an MCP tool
- **Code cell**: Define `zotero_search_items` tool with `@mcp.tool`
- **Narrative cell**: Adding a resource for citation metadata lookup
- **Code cell**: Define `zotero://metadata/{key}` resource with `@mcp.resource`
- **Code cell**: `if __name__ == "__main__": mcp.run()` — entry point

### Part E: Testing (Narrative)
- **Narrative cell**: How to run in server mode vs narrative mode
- **Code cell**: Smoke test — start server, connect client, run query
- **Narrative cell**: What just happened? Protocol walkthrough (request → tool → result)

### Part F: Integration with Agent (Narrative)
- **Narrative cell**: How an agent connects to this server via MCP client
- **Code cell**: Client-side demo using `ZoteroMCPClient` from library
- **Narrative cell**: Recap — docstore + MCP = extensible research backend

## Dependencies

- **FastMCP ≥3.3.1** — MCP server framework (Prefect)
- **llamabot ≥0.19.0** — TurboQuantDocstore for document chunking and retrieval
- **pyzotero** — Zotero Python API (conditional, when credentials available)
- **sentence-transformers** — embedding model (via llamabot TurboQuant)
- **Marimo** — notebook runtime
- **Existing library modules**: `mcp/client.py`, `mcp/zotero_backend.py`

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No Zotero credentials (ingestion) | Use fixture papers; explain in narrative |
| Embedding model download fails | Use cached model or fallback to fixture-based keyword search |
| Docstore initialization fails | Explain in narrative; fall back to simple fixture search |
| Invalid query parameter | FastMCP validates schema; returns 400 to client |
| Empty search results | Valid outcome; return `{"mode": "...", "items": [], "docstore_stats": {...}}` |

## Edge Cases

1. **Marimo availability**: The notebook uses PEP 723 inline script metadata declaring marimo as a dependency, so `uv run` always provides it. No ImportError guards needed for `@app.cell` or `marimo.md` cells.
2. **FastMCP version compatibility**: Use FastMCP ≥3.3.1 API (`FastMCP` class, `@mcp.tool` decorator, `mcp.run()`). Document minimum version in narrative.
3. **Concurrent server runs**: stdio transport is single-connection; if user runs the notebook twice, second instance gets connection conflict. Explain in narrative.
4. **Embedding model size**: `all-MiniLM-L6-v2` is ~80MB; explain that classroom machines need internet for first-run download.
5. **Docstore persistence**: TurboQuant stores embeddings on disk; explain that the collection persists across notebook restarts.

## Related Documents

- [High-Level Design](../../high-level-design.md) (Decision 8)
- [Tools LLD](../tools/LLD.md) — existing MCP client and tutorial server
- [Embedded MCP Server EARS](./embedded-mcp-server-EARS.md)
- [Dual-Mode Runtime EARS](./dual-mode-runtime-EARS.md)
- [Docstore & Retrieval EARS](./docstore-retrieval-EARS.md)
