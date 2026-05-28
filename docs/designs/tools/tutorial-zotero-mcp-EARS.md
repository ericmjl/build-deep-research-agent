# Tutorial Zotero MCP Server — EARS

**Parent LLD**: [Tools LLD](./LLD.md)

## FastMCP Server

- [x] **TOOLS-TUT-001**: The repository shall provide `build_deep_research_agent/mcp/server.py` as a FastMCP stdio server exposing `zotero_search_items`.
- [x] **TOOLS-TUT-002**: The tutorial server shall be runnable via `python -m build_deep_research_agent.mcp.server` and the `tutorial-zotero-mcp` console script.
- [x] **TOOLS-TUT-003**: The tutorial server tool name shall be `zotero_search_items` so llamabot discovers `zotero__zotero_search_items`.

## pyzotero Backend

- [x] **TOOLS-TUT-010**: The repository shall provide `build_deep_research_agent/mcp/zotero_backend.py` using pyzotero when `ZOTERO_*` credentials are configured.
- [x] **TOOLS-TUT-011**: When Zotero credentials are absent, the tutorial server shall fall back to bundled citation fixtures and report `mode: fixtures` in JSON output.
- [x] **TOOLS-TUT-012**: The tutorial server shall support `ZOTERO_LOCAL=true` for local Zotero access via pyzotero.

## Source Selection

- [x] **TOOLS-TUT-020**: `resolve_zotero_mcp_server_config()` shall default to the tutorial server (`ZOTERO_MCP_SOURCE=tutorial`).
- [x] **TOOLS-TUT-021**: When `ZOTERO_MCP_SOURCE=upstream`, MCP client config shall spawn upstream zotero-mcp instead of the tutorial server.

## Part 3 Teaching Flow

- [ ] **TOOLS-TUT-030**: Notebook `03_tools_mcp_zotero.py` shall demonstrate the tutorial server as an optional warm-up before upstream install.
- [ ] **TOOLS-TUT-031**: Notebook `03_tools_mcp_zotero.py` shall document switching to `ZOTERO_MCP_SOURCE=upstream` for the hand-install path.

## Testing

- [x] **TOOLS-TUT-040**: `tests/test_mcp_client.py` shall verify fixture fallback and config resolution without a live MCP subprocess.

## Related Documents

- [Tools LLD](./LLD.md)
- [MCP Connection EARS](./mcp-connection-EARS.md)
- [Zotero Search EARS](./zotero-search-EARS.md)
