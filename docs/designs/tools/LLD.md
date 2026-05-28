# Tools — MCP & Zotero Integration — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Tools
**Part**: 3 (40 min) — **Eric Ma** (session handoff)
**Notebook**: `notebooks/03_tools_mcp_zotero.py`

## Overview

Part 3 adds **tools** via MCP. Participants learn to install and connect to external **[zotero-mcp](https://github.com/54yyyu/zotero-mcp)**, discover tool schemas, invoke search, and summarize live results.

We also ship a **tutorial FastMCP server** in this repo — the cooking-show fallback that works out of the box (pyzotero when configured, bundled fixtures otherwise) while participants learn the hand-built upstream path.

## Implementation Status

| Component | Status |
|-----------|--------|
| `mcp/client.py` — client, normalize helpers, source resolution | Done |
| `mcp/server.py` — tutorial FastMCP server | Done |
| `mcp/zotero_backend.py` — pyzotero + fixture search | Done |
| `tests/test_mcp_client.py` | Done |
| Part 3 notebook `03_tools_mcp_zotero.py` | Not started |
| Part 5 Searcher uses `resolve_zotero_mcp_server_config()` via AgentBot | Done |

## Two MCP Server Paths

| Path | When | Command / config |
|------|------|------------------|
| **Tutorial (default)** | Classroom demos, cooking-show fallback | `ZOTERO_MCP_SOURCE=tutorial` → `python -m build_deep_research_agent.mcp.server` or `tutorial-zotero-mcp` |
| **Upstream (teaching)** | Part 3 hand-install exercise | `ZOTERO_MCP_SOURCE=upstream` → `zotero-mcp` (or `ZOTERO_MCP_COMMAND`) |

Both expose a `zotero_search_items` tool so client code and AgentBot wiring stay the same.

## Learning Objectives

After Part 3, participants can:

- Explain MCP as a tool boundary between agents and external systems.
- Install, configure, and connect to upstream zotero-mcp from a notebook.
- Invoke search tools and pass retrieved metadata to the summarizer.
- Contrast upstream integration with the tutorial FastMCP fallback server.

## Discussion Prompts (Facilitator)

- Why standardize tools via MCP instead of ad hoc Python functions?
- What does the agent see when a tool returns JSON?
- How do tools combine with prompt + memory from Parts 1–2?
- When is a cooking-show fallback server useful vs. misleading?

## Opening (Handoff from Ben)

Setup cell recaps: system prompt, memory, static fixtures. Introduces: **tools let the agent fetch fresh data from Zotero**.

## Notebook Exercises

### Exercise 0 — Tutorial server smoke test (optional warm-up)

- Run with default `ZOTERO_MCP_SOURCE=tutorial`.
- Connect via `ZoteroMCPClient`; call `search_items("Bayesian")`.
- Show fixture fallback when Zotero credentials are absent.

### Exercise 1 — Upstream MCP connection setup

- Install/configure zotero-mcp per upstream README.
- Set `ZOTERO_MCP_SOURCE=upstream`.
- Connect via `ZoteroMCPClient`; inspect `client.tool_names`.

### Exercise 2 — Zotero search tool

- Call `client.search_items(query, limit)`.
- Display raw output and normalized `CitationRecord` list via `normalize_search_json`.

Proposal wording "Building a Zotero search tool" means **wiring the agent to call** an MCP search tool — the upstream install path is the teaching moment; the tutorial server is the pre-baked demo.

### Exercise 3 — Live query + summarization

- Search → normalize → summarize with llamabot (Modal endpoint).
- Optionally store results in `CitationMemory` from Part 2.

### Success criteria

Search → retrieve → summarize pipeline works with tutorial server (fixtures) and, when configured, participant Zotero library via upstream or pyzotero.

## Library Module: `mcp/server.py`

FastMCP stdio server for classroom fallback.

| Export | Purpose |
|--------|---------|
| `zotero_search_items(query, limit)` | MCP tool — JSON results with `mode` + `items` |
| `main()` | CLI entry (`tutorial-zotero-mcp`) |

## Library Module: `mcp/zotero_backend.py`

| Export | Purpose |
|--------|---------|
| `search_zotero_items(query, limit)` | pyzotero web/local search, else fixtures |
| `zotero_item_to_citation(item)` | Map pyzotero payload → `CitationRecord` |
| `records_to_search_json(records, mode)` | Serialize for MCP tool output |

### Environment variables

| Variable | Purpose |
|----------|---------|
| `ZOTERO_API_KEY` | Zotero Web API key |
| `ZOTERO_LIBRARY_ID` | Library ID for web API |
| `ZOTERO_LIBRARY_TYPE` | `user` (default) or `group` |
| `ZOTERO_LOCAL` | `true` for local Zotero via pyzotero |
| `TUTORIAL_ZOTERO_FORCE_FIXTURES` | Force fixture backend (tests/demos) |
| `ZOTERO_MCP_SOURCE` | `tutorial` (default) or `upstream` |

## Library Module: `mcp/client.py`

| Export | Purpose |
|--------|---------|
| `tutorial_zotero_mcp_server_config()` | Stdio config for in-repo FastMCP server |
| `zotero_mcp_server_config(command?, args?)` | Stdio config for upstream zotero-mcp |
| `resolve_zotero_mcp_server_config()` | Pick source from `ZOTERO_MCP_SOURCE` |
| `ZoteroMCPClient` | `tool_names`, `search_items`, `close` |
| `normalize_search_markdown` / `normalize_search_json` | Parse tool output → `CitationRecord` |
| `ZOTERO_MCP_TOOL_NAME` | `zotero__zotero_search_items` |

Part 5 Searcher AgentBot uses `resolve_zotero_mcp_server_config()` in `mcp` mode.

## External Dependency: upstream zotero-mcp

- Source: https://github.com/54yyyu/zotero-mcp
- Used for Part 3 hand-install teaching path
- Pin minimum tested version in instructor materials

## Dependencies

- [Memory LLD](../memory/LLD.md) — optional citation memory for results
- [Prompting LLD](../prompting/LLD.md) — summarization patterns, fixtures
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`, classroom troubleshooting
- **pyzotero**, **fastmcp** — tutorial server backend

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Upstream zotero-mcp not installed | Tutorial server still works; Part 3 exercise links to upstream install |
| No Zotero credentials (tutorial server) | Fixture fallback with `mode: fixtures` in JSON |
| Connection refused (upstream) | Troubleshooting checklist; switch to tutorial source |
| Empty search results | Valid outcome; exercise handles `[]` |

## Tests

- `tests/test_mcp_client.py` — normalization, backend fixture fallback, config resolution

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Memory LLD](../memory/LLD.md)
- [Planning LLD](../planning/LLD.md) — next capability
- [MCP Connection EARS](./mcp-connection-EARS.md)
- [Tutorial Zotero MCP EARS](./tutorial-zotero-mcp-EARS.md)
- [Zotero Search EARS](./zotero-search-EARS.md)
- [Live Summarization EARS](./live-summarization-EARS.md)
