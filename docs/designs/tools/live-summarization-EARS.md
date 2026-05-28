# Live Summarization — EARS

**Parent LLD**: [Tools LLD](./LLD.md)

## Part 3 Exercise 3

- [ ] **TOOLS-LIVE-001**: Notebook `03_tools_mcp_zotero.py` shall run a pipeline: zotero-mcp search → normalize results → LLM summarization.
- [ ] **TOOLS-LIVE-002**: The live summarization exercise shall use the Modal-hosted LLM path by default.
- [ ] **TOOLS-LIVE-003**: The live summarization exercise shall query the participant's Zotero library via zotero-mcp — not bundled fixtures.

## Optional Memory Integration

- [D] **TOOLS-LIVE-010**: Notebook `03_tools_mcp_zotero.py` may store normalized search results in `CitationMemory` from Part 2.

## Discussion Content

- [ ] **TOOLS-LIVE-020**: Notebook `03_tools_mcp_zotero.py` shall include facilitator prompts explaining MCP as a tool boundary and how tools combine with prompt + memory.

## Success Criteria

- [ ] **TOOLS-LIVE-030**: When Exercise 3 completes successfully, the notebook shall display a summary derived from live search results.

## Testing

- [ ] **TOOLS-LIVE-040**: Integration tests for live search may be marked `@pytest.mark.integration` and skipped when zotero-mcp is unavailable.

## Related Documents

- [Tools LLD](./LLD.md)
- [Zotero Search EARS](./zotero-search-EARS.md)
- [Static Summarization EARS](../prompting/static-summarization-EARS.md)
