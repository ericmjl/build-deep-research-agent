# MCP Connection — EARS

**Parent LLD**: [Tools LLD](./LLD.md)

## MCP Client Module

- [x] **TOOLS-MCP-001**: The repository shall provide `build_deep_research_agent/mcp/client.py` with MCP client helpers.
- [x] **TOOLS-MCP-002**: The `mcp/client.py` module shall expose `tutorial_zotero_mcp_server_config()` for the in-repo FastMCP server.
- [x] **TOOLS-MCP-003**: The `mcp/client.py` module shall expose `zotero_mcp_server_config()` for upstream zotero-mcp.
- [x] **TOOLS-MCP-004**: The `mcp/client.py` module shall expose `resolve_zotero_mcp_server_config()` selecting tutorial vs upstream via `ZOTERO_MCP_SOURCE`.
- [x] **TOOLS-MCP-005**: The `mcp/client.py` module shall expose `ZoteroMCPClient` with `tool_names` listing discovered MCP tools.

## Part 3 Exercise 1

- [ ] **TOOLS-MCP-010**: Notebook `03_tools_mcp_zotero.py` shall document installation of [zotero-mcp](https://github.com/54yyyu/zotero-mcp) per upstream instructions.
- [ ] **TOOLS-MCP-011**: When Exercise 1 runs, the notebook shall connect to a Zotero MCP server and display discovered tool schemas.
- [ ] **TOOLS-MCP-012**: Notebook `03_tools_mcp_zotero.py` shall open with a brief recap of Parts 1–2 (prompt + memory) before MCP setup.

## Error Handling

- [ ] **TOOLS-MCP-020**: If upstream zotero-mcp is not installed, Part 3 materials shall document falling back to the tutorial FastMCP server.
- [ ] **TOOLS-MCP-021**: If MCP connection fails, the notebook shall surface troubleshooting steps documented in `docs/index.md`.

## Testing

- [x] **TOOLS-MCP-030**: Unit tests shall mock or bypass live MCP subprocesses in default CI.

## Related Documents

- [Tools LLD](./LLD.md)
- [Tutorial Zotero MCP EARS](./tutorial-zotero-mcp-EARS.md)
- [Classroom Infrastructure EARS](../tutorial-delivery/classroom-infrastructure-EARS.md)
- [Zotero Search EARS](./zotero-search-EARS.md)
