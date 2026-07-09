# Dual-Mode Runtime — EARS (LEGACY / RETIRED)

**Parent LLD**: [./LLD.md](./LLD.md)

> **Retired 2026-07-06** by HLD Decision 8 (new Part 3 arc). The Part 3 notebook is no longer an MCP server; the MCP server is a standalone script (`scripts/serve_corpus_mcp.py`). These specs are retained for traceability only — do not implement against them.

## Retired specs

- ~~**EMCP-RUN-001**~~: Notebook-as-stdio-server — retired; server is standalone.
- ~~**EMCP-RUN-002**~~: Server runs until interrupted — now satisfied by the standalone script (see EMCP-SRV-010).
- ~~**EMCP-RUN-003**~~: Narrative cells not imported in server mode — moot; server imports no notebook.
- ~~**EMCP-RUN-010/011/012**~~: Narrative-mode server cells — retired.
- ~~**EMCP-RUN-020**~~: `__name__ == "__main__"` mode detection — retired (no dual mode).
- ~~**EMCP-RUN-021**~~: Marimo PEP 723 availability — still true but no longer load-bearing for a server mode.

## Related documents

- [Embedded MCP LLD](./LLD.md) (current arc)
