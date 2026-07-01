# Embedded Zotero MCP Server — EARS

**Parent LLD**: [./LLD.md](./LLD.md)

## Server Instantiation

- [x] **EMCP-SRV-001**: The system shall create a FastMCP server instance named `"zotero-research"`.
- [x] **EMCP-SRV-002**: The system shall use FastMCP version ≥3.3.1.
- [x] **EMCP-SRV-003**: The system shall use stdio transport (the default for `mcp.run()`).

## Tool Definition

- [x] **EMCP-SRV-010**: The system shall expose a single MCP tool named `zotero_search_items`.
- [x] **EMCP-SRV-011**: The `zotero_search_items` tool shall accept a required `query` parameter of type string.
- [x] **EMCP-SRV-012**: The `zotero_search_items` tool shall accept an optional `limit` parameter of type integer with default value 5.
- [x] **EMCP-SRV-013**: The `zotero_search_items` tool shall return a JSON string containing `mode`, `items`, and `docstore_stats` fields.
- [x] **EMCP-SRV-014**: Each item in the `items` array shall include: `key`, `title`, `creators`, `year`, `abstract`, `url`, `snippet`. *(Fields limited to the `CitationRecord` schema; `date`/`publicationTitle`/`tags` are out of scope for v1 fixtures.)*
- [x] **EMCP-SRV-015**: The `snippet` field shall contain the docstore-retrieved text excerpt most relevant to the query.

## Resource Definition

- [x] **EMCP-SRV-020**: The system shall expose an MCP resource URI pattern `zotero://metadata/{key}`.
- [x] **EMCP-SRV-021**: The `zotero://metadata/{key}` resource shall return full citation metadata for the given key.
- [x] **EMCP-SRV-022**: The `zotero://metadata` resource (no key) shall return a list of all available citation keys.

## Backend Resolution

- [x] **EMCP-SRV-030**: Where `TUTORIAL_ZOTERO_FORCE_FIXTURES` is set to `"true"`, the system shall use the bundled fixture backend for document ingestion.
- [x] **EMCP-SRV-031**: Where `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` are both set, the system shall use pyzotero to ingest live Zotero papers into the docstore.
- [x] **EMCP-SRV-032**: If neither fixture mode nor pyzotero credentials are available, the system shall fall back to the bundled fixture backend.
- [x] **EMCP-SRV-033**: The `mode` field in the tool output shall be `"fixtures"`, `"pyzotero"`, or `"error"` to indicate which backend was used. *(Implemented modes: `"fixtures"` and `"pyzotero"`; the `"error"` case degrades to fixtures via the fallback.)*

## Error Handling

- [x] **EMCP-SRV-040**: If a Zotero API call fails during ingestion, the system shall log the error and continue with available papers.
- [x] **EMCP-SRV-041**: If the `query` parameter is empty, the system shall return an empty `items` array (not an error).
- [x] **EMCP-SRV-042**: If the `limit` parameter is less than 1, the system shall clamp it to 1.

## Dual-Mode Guard

- [x] **EMCP-SRV-050**: The server entry point (`mcp.run()`) shall be guarded by `if __name__ == "__main__":` so it does not execute when imported by Marimo.
- [x] **EMCP-SRV-051**: Marimo narrative cells (using `@app.cell` or `marimo.md`) need no ImportError guard — the PEP 723 inline script metadata declares marimo as a dependency, so `uv run` always provides it.

## Related Documents

- [Embedded MCP LLD](./LLD.md)
