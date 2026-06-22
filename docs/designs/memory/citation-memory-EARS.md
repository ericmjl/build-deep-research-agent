# Citation Memory — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## CitationMemory

- [x] **MEM-CITE-001**: The `memory.py` module shall define `CitationMemory` with an `add(citation: CitationRecord, snippet: str)` method.
- [x] **MEM-CITE-002**: When `add` is called, `CitationMemory` shall return a new instance (immutable fluent style).
- [x] **MEM-CITE-003**: `CitationMemory` shall expose `as_context()` returning a string formatted for LLM prompt injection.
- [x] **MEM-CITE-004**: When duplicate citation keys are added, the later entry shall supersede the earlier entry in `as_context()` output.

## Part 2 Exercise 2

- [x] **MEM-CITE-010**: Notebook `02_memory_state.py` shall populate `CitationMemory` using fixture `CitationRecord` entries.
- [x] **MEM-CITE-011**: Notebook `02_memory_state.py` shall inject `CitationMemory.as_context()` into a subsequent LLM call.

## Optional Truncation

- [D] **MEM-CITE-020**: `AppendOnlyMemory` or companion helper may expose `truncate(max_turns: int)` for context-limit discussion.

## Testing

- [x] **MEM-CITE-030**: `tests/test_memory.py` shall verify `as_context()` includes citation title and snippet text.
- [x] **MEM-CITE-031**: `tests/test_memory.py` shall verify duplicate-key supersession behavior.

## Related Documents

- [Memory LLD](./LLD.md)
- [Fixtures EARS](../prompting/fixtures-EARS.md)
