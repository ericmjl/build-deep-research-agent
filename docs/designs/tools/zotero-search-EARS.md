# Zotero Search — EARS

**Parent LLD**: [Tools LLD](./LLD.md)

## Tool Invocation

- [x] **TOOLS-SEARCH-001**: The `mcp/client.py` module shall expose search invocation via `ZoteroMCPClient.search_items(query, limit)`.
- [x] **TOOLS-SEARCH-002**: The `mcp/client.py` module shall expose `normalize_search_markdown` and `normalize_search_json` to parse search tool output into `list[CitationRecord]`.
- [x] **TOOLS-SEARCH-003**: Tool names used in the tutorial shall match the pinned zotero-mcp version — not tutorial-invented aliases.

## Part 3 Exercise 2

- [ ] **TOOLS-SEARCH-010**: Notebook `03_tools_mcp_zotero.py` shall invoke the zotero-mcp search tool with a participant-supplied query.
- [ ] **TOOLS-SEARCH-011**: Notebook `03_tools_mcp_zotero.py` shall display both raw tool output and normalized `CitationRecord` objects.
- [x] **TOOLS-SEARCH-012**: The Part 3 "build a Zotero search tool" exercise shall mean wiring the agent to call the upstream search tool — not implementing a new MCP tool in this repo.

## Empty Results

- [x] **TOOLS-SEARCH-020**: When search returns no items, normalization helpers shall return an empty list without raising an error.

## Testing

- [ ] **TOOLS-SEARCH-030**: `tests/test_mcp_client.py` shall verify normalization and fixture fallback.
- [x] **TOOLS-SEARCH-031**: Normalization tests shall cover at least one empty-result payload.

## Related Documents

- [Tools LLD](./LLD.md)
- [MCP Connection EARS](./mcp-connection-EARS.md)
- [Live Summarization EARS](./live-summarization-EARS.md)
