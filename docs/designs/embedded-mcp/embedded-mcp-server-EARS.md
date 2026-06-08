# Embedded Zotero MCP Server — EARS

**Parent LLD**: [./LLD.md](./LLD.md)

## Server Instantiation

- [ ] **EMCP-SRV-001**: The system shall create a FastMCP server instance named `"zotero-research"`.
- [ ] **EMCP-SRV-002**: The system shall use FastMCP version ≥3.3.1.
- [ ] **EMCP-SRV-003**: The system shall use stdio transport (the default for `mcp.run()`).

## Tool Definition

- [ ] **EMCP-SRV-010**: The system shall expose a single MCP tool named `zotero_search_items`.
- [ ] **EMCP-SRV-011**: The `zotero_search_items` tool shall accept a required `query` parameter of type string.
- [ ] **EMCP-SRV-012**: The `zotero_search_items` tool shall accept an optional `limit` parameter of type integer with default value 5.
- [ ] **EMCP-SRV-013**: The `zotero_search_items` tool shall return a JSON string containing `mode`, `items`, and `docstore_stats` fields.
- [ ] **EMCP-SRV-014**: Each item in the `items` array shall include: `key`, `title`, `creators`, `date`, `publicationTitle`, `tags`, `url`, `snippet`.
- [ ] **EMCP-SRV-015**: The `snippet` field shall contain the retrieved docstore chunk excerpt most relevant to the query.

## Resource Definition

- [ ] **EMCP-SRV-020**: The system shall expose an MCP resource URI pattern `zotero://metadata/{key}`.
- [ ] **EMCP-SRV-021**: The `zotero://metadata/{key}` resource shall return full citation metadata for the given key.
- [ ] **EMCP-SRV-022**: The `zotero://metadata/` resource (no key) shall return a list of all available citation keys.

## Backend Resolution

- [ ] **EMCP-SRV-030**: Where `TUTORIAL_ZOTERO_FORCE_FIXTURES` is set to `"true"`, the system shall use the bundled fixture backend for document ingestion.
- [ ] **EMCP-SRV-031**: Where `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` are both set, the system shall use pyzotero to ingest live Zotero papers into the docstore.
- [ ] **EMCP-SRV-032**: If neither fixture mode nor pyzotero credentials are available, the system shall fall back to the bundled fixture backend.
- [ ] **EMCP-SRV-033**: The `mode` field in the tool output shall be `"fixtures"`, `"pyzotero"`, or `"error"` to indicate which backend was used.

## Error Handling

- [ ] **EMCP-SRV-040**: If a Zotero API call fails during ingestion, the system shall log the error and continue with available papers.
- [ ] **EMCP-SRV-041**: If the `query` parameter is empty, the system shall return an empty `items` array (not an error).
- [ ] **EMCP-SRV-042**: If the `limit` parameter is less than 1, the system shall clamp it to 1.

## Dual-Mode Guard

- [ ] **EMCP-SRV-050**: The server entry point (`mcp.run()`) shall be guarded by `if __name__ == "__main__":` so it does not execute when imported by Marimo.
- [ ] **EMCP-SRV-051**: Marimo narrative cells (using `@app.cell` or `marimo.md`) need no ImportError guard — the PEP 723 inline script metadata declares marimo as a dependency, so `uv run` always provides it.

## Related Documents

- [Embedded MCP LLD](./LLD.md)
