# Tools (Part 3) — EARS

**Parent LLD**: [./LLD.md](./LLD.md) · **HLD**: Decision 8 (from `@tool` to MCP)

> Revised 2026-07-06 to the new arc. Legacy dual-mode specs (EMCP-RUN-*, EMCP-SRV-050/051) are retired — see [Dual-Mode Runtime EARS](./dual-mode-runtime-EARS.md).

## llamabot `@tool`s (phases 1 & 4)

- [x] **EMCP-TOOL-001**: The system shall provide `search_zotero(query: str, limit: int = 5) -> dict` performing keyword search of the participant's Zotero library via pyzotero. *(Library capability in `exercises/solutions/part3.py` — credential check inlined directly in `search_zotero` (raises if creds absent — no fixture fallback), returns a dict. Exercised as the **Exercise 4** stretch scaffold in the notebook; `pyzotero_keyword_search` is the underlying primitive in `tools/zotero.py`.)*
- [x] **EMCP-TOOL-002**: `search_zotero` (Exercise 4 stretch) shall **require** real credentials — when `ZOTERO_LIBRARY_ID` / `ZOTERO_API_KEY` are absent it raises a clear error instead of falling back to fixtures. *(The corpus exercises own the fixture path; the Zotero stretches are the real-thing path.)*
- [x] **EMCP-TOOL-003**: The system shall provide `search_corpus(query: str, limit: int = 5) -> dict` decorated with `@tool`, querying the corpus docstore and returning paper metadata + retrieved snippets. *(Notebook Exercise 2 scaffold; returns a dict — the llamabot `@tool` / FastMCP layer serializes it.)*
- [x] **EMCP-TOOL-010**: Both `@tool`s shall return a result carrying `mode` and `items` fields, consistent across tools (serialized to JSON by the `@tool`/MCP layer).

## Standalone MCP server (phase 6)

- [x] **EMCP-SRV-001**: `scripts/serve_corpus_mcp.py` shall create a FastMCP server exposing `search_corpus` as an MCP tool.
- [x] **EMCP-SRV-010**: When run as `pixi run python scripts/serve_corpus_mcp.py`, it shall start a stdio MCP server that remains running until interrupted.
- [x] **EMCP-SRV-011**: The `search_corpus` MCP tool shall accept a required `query: str` and optional `limit: int = 5`.
- [x] **EMCP-SRV-012**: The system shall ship a **scaffold** (placeholder tool body learners paste their docstore-query impl into) as a file distinct from the reference. *(Scaffold shipped as `scripts/serve_corpus_mcp_starter.py`; notebook Exercise 3 verify cell smoke-tests it in-process via FastMCP's in-memory `Client`.)*
- [x] **EMCP-SRV-013**: Instructor materials shall document connecting a coding agent (opencode / Claude / Cursor) to the running server — both the "ask the agent to self-configure" and "hand-edit config" paths. *(Documented in the notebook `ex3_connect` cell, covering both the starter and reference scripts.)*
- [x] **EMCP-SRV-014**: Each `search_corpus` result item shall include paper metadata (`title`, `authors`, `year`, `url`, `source`) plus a `snippet` (the retrieved passage).
- [x] **EMCP-SRV-015**: If `query` is empty, the tool shall return an empty `items` array (not an error).
- [x] **EMCP-SRV-022**: The server shall expose a `corpus://papers` resource listing the ingested papers (title + source id).

## Stretch exercises — your own Zotero library

Optional, credentials-dependent extensions for participants who finish early (ideally with a coding agent). All require real `ZOTERO_*` credentials (no fixture fallback). Exercise 4 (keyword `search_zotero`) is covered by **EMCP-TOOL-001/002** above.

- [x] **EMCP-TOOL-011**: The notebook stretch **Exercise 5** shall build a docstore over the participant's Zotero library — indexing each item's abstract plus the full text extracted from its stored PDF attachment (`pymupdf`) — and expose semantic retrieval as a `@tool` (`search_zotero_semantic`). *(Reference in `exercises/solutions/part3.py` (`build_zotero_docstore`, `search_zotero_semantic`) + `tools/zotero.py` (`fetch_zotero_items`, `zotero_client`, `zotero_item_full_text`, `build_zotero_docstore`, `retrieve_zotero`); notebook `ex5_header` skeleton + `ex5_build`/`ex5_search` scaffolds.)*
- [ ] **EMCP-SRV-060**: The notebook stretch **Exercise 6** shall provide a header skeleton for a standalone FastMCP server exposing `search_zotero_semantic` as an `@mcp.tool`; participants save it as a script under `scripts/` and connect a coding assistant. *(Notebook `ex6_header`; doc-only — no in-repo reference implementation of the new-pattern Zotero MCP server ships yet. The legacy `scripts/serve_zotero_mcp.py` uses the retired `build_zotero_research_server` API and is not the reference.)*

## Retired (dual-mode notebook)

- ~~**EMCP-SRV-050**~~: Server entry in a notebook `__main__` — retired; the server is now a standalone script (Decision 8).
- ~~**EMCP-SRV-051**~~: Notebook-as-server Marimo guard — retired.

## Legacy retained-code specs (`mcp/` — Zotero FastMCP server/client)

The retained `mcp/docstore.py` (`build_zotero_research_server`), `mcp/server.py`, and `mcp/zotero_backend.py` still carry `@spec` anchors for the behaviors below; they describe that superseded Zotero implementation (kept as legacy/fallback code), not the new corpus arc.

- [x] **EMCP-SRV-003**: The legacy server uses stdio transport (the default for `mcp.run()`).
- [x] **EMCP-SRV-021**: The legacy server exposes a `zotero://metadata/{key}` resource returning citation metadata.
- [x] **EMCP-SRV-030**: Where `TUTORIAL_ZOTERO_FORCE_FIXTURES` is set, the legacy server uses the fixture backend.
- [x] **EMCP-SRV-031**: Where `ZOTERO_API_KEY` + `ZOTERO_LIBRARY_ID` are set, the legacy server ingests via pyzotero.
- [x] **EMCP-SRV-032**: If neither is available, the legacy server falls back to fixtures.
- [x] **EMCP-SRV-033**: The legacy `mode` field reports `fixtures` / `pyzotero`.
- [x] **EMCP-SRV-040**: On Zotero API failure during ingestion, the legacy server logs and continues.
- [x] **EMCP-SRV-041**: On empty `query`, the legacy tool returns an empty `items` array.
- [x] **EMCP-SRV-042**: If `limit < 1`, the legacy tool clamps it to 1.

## Related documents

- [Embedded MCP LLD](./LLD.md)
- [Docstore & Retrieval EARS](./docstore-retrieval-EARS.md)
