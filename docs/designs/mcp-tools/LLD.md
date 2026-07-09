# Part 3: Tools — from llamabot `@tool` to MCP — Low-Level Design

**Created**: 2026-05-30 · **Revised**: 2026-07-07 (3-beat notebook arc — Zotero `@tool` exercise removed; `search_zotero_records` inlined; see line 18)

**HLD Link**: [../../high-level-design.md](../../high-level-design.md) (Decision 8)

**Capability**: Tools (`@tool` → docstore → MCP)
**Part**: 3 (40 min) — **Eric Ma**
**Notebook**: `notebooks/03_tools_mcp_zotero.py`
**Frameworks**: llamabot (`@tool`, `LanceDBDocStore`), pyzotero, FastMCP ≥3.3.1

> This LLD consolidates the former `tools/` (zotero-mcp client) and dual-mode-server designs into one Part 3 arc. The MCP server is a **standalone script** under `scripts/` (not embedded in the notebook); the legacy `mcp/server.py` + `mcp/client.py` are retained but superseded.

## Design intent

Part 3 teaches tools as a progression that **motivates MCP**, rather than starting cold with a FastMCP server. Learners build one real capability over a **bundled free corpus** that stands in for a reference library: a docstore (Exercise 1), a `@tool` exposing docstore query (Exercise 2), then the wall that only *this* process can call it — which MCP crosses. The arc deliberately minimizes hand-built abstraction: participants see llamabot's `LanceDBDocStore` and `@tool` primitives directly, and the repo delegates to packages (pyzotero, FastMCP) rather than wrapping them.

> **Notebook arc (revised 2026-07-07).** The notebook now teaches a 3-beat path — **free corpus → docstore → `@tool` → MCP**. The Zotero keyword-search `@tool` (former Phase 1) is no longer a notebook exercise; `search_zotero` remains a library capability in `exercises/solutions/part3.py` (now with the credential/fallback logic inlined — the `search_zotero_records` wrapper was removed), used by the standalone Zotero MCP server path. The conceptual phases below describe the full capability surface; only Phases 3 and 4 are scaffolded notebook exercises (Exercises 1–2) — Phases 2 and 6 appear as demo cells (corpus load, MCP server run).

## The phases

### Phase 1 — A llamabot `@tool` for Zotero keyword search

Learners wrap pyzotero keyword search of their own Zotero library in llamabot's `@tool` decorator.

- **Function**: `search_zotero(query: str, limit: int = 5) -> str` — calls pyzotero `top(q=query, limit=limit)`, formats hits as JSON.
- **Decorator**: `from llamabot import tool` → `@tool` nodeifies the typed function into a PocketFlow `FuncNode` (and `function_to_dict` exposes the JSON-schema tool contract an agent calls).
- **Credentials**: `ZOTERO_LIBRARY_ID` + `ZOTERO_API_KEY` (web) or `ZOTERO_LOCAL=true` (local). **Fixture fallback** when absent so the notebook stays green.
- **Teaching point**: a *tool* is a typed function with a describable contract; llamabot turns the signature into a schema any in-process agent can call.

### Phase 2 — A free corpus (arXiv + JOSS)

A bundled corpus that needs **no credentials** and always works — the substrate for the docstore.

- **Contents**: ≥30 paper full texts across AI, astrophysics, computational biology, and other domains.
- **Sources**: arXiv (PDF → extracted text) and JOSS (markdown from the paper's GitHub repo).
- **Location**: `build_deep_research_agent/fixtures/corpus/*.txt` / `*.md` (extracted text only; **no PDFs committed**).
- **Fetcher**: `scripts/fetch_corpus.py` (PEP 723 inline script metadata; reproducible). Re-run to refresh; outputs are committed so the classroom needs no network for this step.
- **Model**: `CorpusPaper` — `title`, `authors`, `abstract`, `full_text`, `source` (`arxiv`/`joss`), `source_id` (arXiv id / DOI), `url`, `domain`.
- **Loader**: `load_corpus_papers() -> list[CorpusPaper]`.

### Phase 3 — Build a llamabot docstore over the corpus

Learners wire **raw** `LanceDBDocStore` directly — not behind `ZoteroDocstore` — so they see the primitive.

- **Primitive**: `from llamabot import LanceDBDocStore`; `docstore.append(text)` / `docstore.retrieve(query, n_results=n)`. String-in / string-out.
- **Side-table**: because the docstore carries no per-document metadata, learners keep `chunks_by_text: dict[str, CorpusPaper]` (and a chunk locator) so retrieved text maps back to the paper it came from.
- **Chunking**: split each paper's `full_text` into passages (naive splitter is fine for teaching); append each chunk and record the mapping.
- **Teaching point**: docstores retrieve *text*; the side-table is how you project retrieved text back to structured metadata. This is the concept `ZoteroDocstore` used to hide.

### Phase 4 — A `@tool` exposing docstore query

Learners wrap semantic retrieval as a second `@tool`.

- **Function**: `search_corpus(query: str, limit: int = 5) -> str` — `docstore.retrieve(query, n_results=limit)`, map hits via the side-table, return JSON (paper metadata + retrieved snippet).
- Reuses the JSON-envelope helper so output shape is consistent across tools.

### Phase 5 — The limitation (motivates MCP)

Both `search_zotero` and `search_corpus` live **in-process** inside llamabot. Only an agent built in *this* process can call them. The participant's coding agent (Cursor / Claude / opencode) cannot reach them. This is the gap MCP fills: a standard protocol so any client can invoke the capability you built.

- **Teaching point**: stated as a deliberate "now go further" beat, not a bug. The notebook shows an agent calling `search_corpus` in-process, then asks: *how would your editor call this?*

### Phase 6 — Scaffolded MCP server + connect your coding agent

Learners copy their `search_corpus` implementation into a **standalone** MCP server script and run it from the terminal.

- **Scaffold**: `scripts/serve_corpus_mcp.py` — a FastMCP server with a placeholder body for the `search_corpus` tool (learners paste their docstore-query impl). A reference version is provided for instructors.
- **Run**: `pixi run python scripts/serve_corpus_mcp.py` (stdio transport).
- **Connect**: learners either (a) ask their coding agent to configure itself to connect to the server, or (b) hand-edit the agent's MCP client config (e.g. opencode/Claude Desktop config).
- **Payoff**: the participant chats with the arXiv/JOSS corpus *through their coding agent*, which calls `search_corpus` over MCP — the same path any MCP client takes.

## Module layout (planned)

```
build_deep_research_agent/
├── models.py                          # + CorpusPaper
├── fixtures/
│   └── corpus/                        # ≥30 arXiv+JOSS extracted texts
├── fixtures/loader.py                 # + load_corpus_papers()
└── tools/                             # llamabot @tools (NEW)
    ├── zotero.py                      # pyzotero keyword-search primitive (library only; surfaced by the standalone Zotero MCP path, not the notebook)
    └── corpus.py                      # raw LanceDB docstore wiring + search_corpus_payload (decorated @tool in the notebook)
scripts/
├── fetch_corpus.py                    # PEP 723 corpus fetcher
└── serve_corpus_mcp.py                # standalone MCP server scaffold + reference
notebooks/
└── 03_tools_mcp_zotero.py             # the 3-beat arc (corpus → docstore → @tool → MCP)
```

> `mcp/docstore.py` (`ZoteroDocstore`, `build_zotero_research_server`) stays for the legacy citation-fixtures path / Parts 1–2; the corpus path teaches raw `LanceDBDocStore` directly.

## Notebook cell structure

Progressive walkthrough mirroring the 3-beat arc (corpus → docstore → tool → MCP):

- **A. Setup** — imports, env, `from build_deep_research_agent.exercises.solutions import part3`.
- **B. Intro** — the 3-beat outline (free corpus → docstore → `@tool` → MCP) + "what is a tool" with a `search_corpus` example.
- **C. Free corpus** — `load_corpus_papers()`; show domains/counts. The corpus stands in for a reference library so nothing needs credentials.
- **D. Exercise 1** — raw `LanceDBDocStore` wiring scaffold (chunk → append → side-table).
- **E. Exercise 2** — `search_corpus` `@tool` scaffold.
- **F. The limitation** — in-process agent call demo + the limitation callout (only this process can call `search_corpus`).
- **G. Exercise 3 — Standalone MCP server** — participants fill in `scripts/serve_corpus_mcp_starter.py` (a FastMCP server with a stubbed `search_corpus` tool body), smoke-test it in-process via FastMCP's in-memory `Client`, then connect a coding assistant (reference answer: `scripts/serve_corpus_mcp.py`).

Scaffolds follow TUT-MARIMO-014: in-cell, delegate to `exercises/solutions/part3.py` by default, run green, learners override.

## Dependencies

- **llamabot[rag]** — `@tool`, `LanceDBDocStore`.
- **pyzotero** — Zotero keyword search (phase 1).
- **FastMCP ≥3.3.1** — the standalone MCP server (phase 6).
- **ipython** — required so `sentence-transformers` imports cleanly and `LanceDBDocStore` initializes (without it, init fails silently; see `pyproject.toml`).
- **transformers <5** — pinned for llamabot's ColBERT reranker.
- **pymupdf** — PDF→text extraction: the corpus fetcher script *and* the Zotero full-text docstore (Part 3 stretch Exercise 5) extract text from stored PDF attachments at runtime.

## Error handling & fallbacks

| Condition | Behavior |
|-----------|----------|
| No Zotero credentials (phase 1) | `search_zotero` uses fixture fallback; notebook stays green. |
| Embedding model can't load (phase 3) | Documented degradation; the corpus path assumes LanceDB init succeeds (env fix: `ipython` dep). |
| Coding agent can't auto-configure (phase 6) | Hand-config instructions provided; both paths documented. |
| Empty retrieval | Valid outcome; return empty `items` with a descriptive message. |

## Related documents

- [High-Level Design](../../high-level-design.md) (Decision 8)
- [Tools (Part 3) EARS](./mcp-tools-EARS.md)
- [Docstore & Retrieval EARS](./docstore-retrieval-EARS.md)
- [Dual-Mode Runtime EARS](./dual-mode-runtime-EARS.md) *(legacy — mostly retired by this arc)*
