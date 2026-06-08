# Dual-Mode Runtime — EARS

**Parent LLD**: [./LLD.md](./LLD.md)

## Server Mode

- [ ] **EMCP-RUN-001**: When invoked as `uv run notebooks/03_tools_mcp_zotero.py` (or `python notebooks/03_tools_mcp_zotero.py`), the system shall start a FastMCP stdio server and listen for MCP requests.
- [ ] **EMCP-RUN-002**: In server mode, the system shall remain running until interrupted (SIGINT/SIGTERM).
- [ ] **EMCP-RUN-003**: In server mode, Marimo-specific cells (narrative, UI) shall not execute and shall not cause import errors.

## Narrative Mode

- [ ] **EMCP-RUN-010**: When invoked as `marimo serve notebooks/03_tools_mcp_zotero.py`, the system shall render an interactive notebook with explanatory narrative cells.
- [ ] **EMCP-RUN-011**: In narrative mode, the server code cells shall be executable and the user shall be able to start the MCP server from a cell for testing.
- [ ] **EMCP-RUN-012**: In narrative mode, the system shall allow the user to run server code cells and client demo cells in sequence within the same notebook session.

## Mode Detection

- [ ] **EMCP-RUN-020**: The system shall distinguish server mode from narrative mode using `__name__ == "__main__"` (server) vs `__name__ != "__main__"` (narrative/imported).
- [ ] **EMCP-RUN-021**: Marimo is always available via PEP 723 inline script metadata when running with `uv run`; no ImportError handling is needed.

## Related Documents

- [Embedded MCP LLD](./LLD.md)
