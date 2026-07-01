# Embedded Zotero MCP Server — Low-Level Design

**Created**: 2026-05-30
**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Tools (MCP)
**Part**: 3 (40 min) — **Eric Ma**
**Notebook**: `notebooks/03_tools_mcp_zotero.py`
**Framework**: FastMCP ≥3.3.1
**Docstore**: llamabot `LanceDBDocStore` (`[rag]` extra) + in-repo metadata side-table

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
| Docstore | `ZoteroDocstore` wrapping llamabot `LanceDBDocStore` + side-table (`mcp/docstore.py`) |
| Backend | pyzotero (live) or fixtures (fallback) for document ingestion |
| Entry guard | `if __name__ == "__main__": mcp.run()` |

### Tool Contract: `zotero_search_items`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search terms |
| `limit` | `int` | 5 | Maximum results |

**Returns**: JSON string with `mode`, `items` list, and `docstore_stats` (`table_name`, `document_count`, `embedding_model`, `backend`). A `message` field is included when no items are returned.

Each item includes: `key`, `title`, `creators`, `year`, `abstract`, `url`, `snippet` (retrieved text excerpt). Fields are limited to the `CitationRecord` schema; `date`/`publicationTitle`/`tags` are out of scope for v1 fixtures.

### Resource Contract: `zotero://metadata/{key}`

| URI pattern | Returns |
|-------------|---------|
| `zotero://metadata/{key}` | Full citation metadata for key `key` |
| `zotero://metadata` (no key) | List of all available keys |

## Document Pipeline (TurboQuant Docstore)

This is the core teaching concept: **building a document storage and retrieval system**, then exposing it as an MCP tool.

### Step 1: Document Ingestion

The real llamabot docstores (`LanceDBDocStore`, `TurboVecDocStore`) are **string-in / string-out** — they store and retrieve document *text* but do not carry structured per-document metadata. To expose rich citation items from an MCP tool, we wrap the docstore with a **metadata side-table** (`build_deep_research_agent/mcp/docstore.py: ZoteroDocstore`): a `dict[str, CitationRecord]` keyed by the exact stored document text. Ingestion composes a searchable text blob per paper, hands the text to the docstore, and records the same text → record mapping in the side-table.

```python
from llamabot import LanceDBDocStore
from build_deep_research_agent.mcp.docstore import ZoteroDocstore

store = ZoteroDocstore(  # wraps LanceDBDocStore + side-table
    table_name="zotero_papers",
    embedding_model="minishlab/potion-base-8M",
)

# Ingest papers from Zotero (pyzotero or fixtures)
store.ingest(papers)  # stores text + records key -> CitationRecord
```

### Step 2: Retrieval

Retrieval asks the docstore for the most relevant stored *text*, then maps each returned string back to its `CitationRecord` via the side-table, producing a `DocstoreSearchHit` that carries the citation fields plus a `snippet` (the retrieved text excerpt). Chunking and embeddings happen inside the docstore; the wrapper only projects results back to citation metadata.

```python
# The MCP tool wraps docstore retrieval
@mcp.tool
def zotero_search_items(query: str, limit: int = 5) -> str:
    hits = store.search(query, limit=limit)
    return build_search_json(hits, mode=mode, stats=store.stats)
```

### Teaching points

- **Why store documents?** A docstore lets the agent retrieve *relevant* papers by meaning rather than scanning the whole library.
- **Why embeddings?** Semantic search finds relevant papers even when query terms don't match exactly (LanceDB embeds documents and queries with the same model).
- **Why a side-table?** llamabot's docstores return text only; the side-table projects retrieved text back to rich citation metadata so the MCP tool can return structured items.
- **Why wrap in MCP?** Any MCP client (agent, CLI, web UI) can use the same retrieval backend.
- **Why dual-mode?** See the notebook, run it as a server — same code, different perspectives.

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
- **llamabot[rag] ≥0.19.0** — `LanceDBDocStore` for document storage and semantic retrieval
- **transformers <5** — pinned because llamabot's LanceDB reranker loads `colbert-ir/colbertv2.0`, which is incompatible with `transformers 5.x`
- **pyzotero** — Zotero Python API (conditional, when credentials available)
- **sentence-transformers** — embedding model (pulled in via llamabot `[rag]` extra)
- **Marimo** — notebook runtime
- **Existing library modules**: `mcp/client.py`, `mcp/zotero_backend.py`, `mcp/docstore.py`

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No Zotero credentials (ingestion) | Use fixture papers; explain in narrative |
| Embedding model download fails | `ZoteroDocstore` falls back to in-memory keyword search over the side-table (EMCP-DOC-060); narrative explains the degradation |
| Docstore initialization fails | Same fallback; the MCP tool still returns fixture-derived results |
| ColBERT reranker unavailable | Avoided by the `transformers<5` pin; if it still fails, keyword fallback covers retrieval |
| Invalid query parameter | FastMCP validates schema; returns 400 to client |
| Empty search results | Valid outcome; return `{"mode": "...", "items": [], "docstore_stats": {...}}` |

## Edge Cases

1. **Marimo availability**: The notebook uses PEP 723 inline script metadata declaring marimo as a dependency, so `uv run` always provides it. No ImportError guards needed for `@app.cell` or `marimo.md` cells.
2. **FastMCP version compatibility**: Use FastMCP ≥3.3.1 API (`FastMCP` class, `@mcp.tool` decorator, `mcp.run()`). Document minimum version in narrative.
3. **Concurrent server runs**: stdio transport is single-connection; if user runs the notebook twice, second instance gets connection conflict. Explain in narrative.
4. **Embedding model size**: `minishlab/potion-base-8M` is small (~8 MB); the LanceDB reranker also loads `colbert-ir/colbertv2.0` (~400 MB) on first run — classroom machines need internet for that first-time download.
5. **Docstore persistence**: LanceDB stores embeddings on disk under `storage_path`; the collection persists across notebook restarts. The metadata side-table is rebuilt on each `ingest()`.
6. **String-in/string-out**: llamabot docstores return stored text only (no native metadata). The `ZoteroDocstore` side-table is what makes structured citation items possible.

## Related Documents

- [High-Level Design](../../high-level-design.md) (Decision 8)
- [Tools LLD](../tools/LLD.md) — existing MCP client and tutorial server
- [Embedded MCP Server EARS](./embedded-mcp-server-EARS.md)
- [Dual-Mode Runtime EARS](./dual-mode-runtime-EARS.md)
- [Docstore & Retrieval EARS](./docstore-retrieval-EARS.md)
