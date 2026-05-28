# Citation Fixtures — EARS

**Parent LLD**: [Prompting LLD](./LLD.md)

## Fixture Data

- [x] **PROMPT-FIX-001**: The repository shall include bundled citation fixture data under `build_deep_research_agent/fixtures/`.
- [x] **PROMPT-FIX-002**: The bundled fixture shall contain at least five `CitationRecord`-compatible items representing diverse publication types.
- [x] **PROMPT-FIX-003**: Fixture records shall use the normalized `CitationRecord` shape — not raw Zotero Web API JSON.

## Usage Scope

- [ ] **PROMPT-FIX-010**: Parts 1–2 shall use bundled fixtures for in-context and memory exercises before live MCP is introduced. *(Library ready; Part 1–2 notebooks not started.)*
- [x] **PROMPT-FIX-011**: Bundled fixtures shall not be documented as the default substitute for Part 3 live Zotero queries.

## Loading API

- [x] **PROMPT-FIX-020**: The package shall expose a function or module path for notebooks to load fixture citations without manual JSON parsing in notebook cells.

## Testing

- [x] **PROMPT-FIX-030**: `tests/test_fixtures.py` shall verify all bundled fixtures deserialize to valid `CitationRecord` instances.
- [ ] **PROMPT-FIX-031**: Fixture tests shall include at least one record with a non-ASCII character in title or creator name.

## Related Documents

- [Prompting LLD](./LLD.md)
- [Shared Models EARS](../tutorial-delivery/shared-models-EARS.md)
- [Citation Memory EARS](../memory/citation-memory-EARS.md)
