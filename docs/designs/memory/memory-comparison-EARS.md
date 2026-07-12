# Memory Comparison — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## Part 2 with/without memory

- [x] **MEM-COMP-001**: Notebook `02_memory_state.py` shall run the same follow-up question against an empty memory state and a populated memory state.
- [x] **MEM-COMP-002**: Notebook `02_memory_state.py` shall display both LLM outputs for participant comparison.
- [x] **MEM-COMP-003**: The populated compare path shall use combined chat history (`AppendOnlyMemory`) and `CitationMemory.as_context()` (summary inventory) as context for a multi-paper compare turn.

## Handoff

- [x] **MEM-COMP-010**: The final cells of `02_memory_state.py` shall recap that prompt + memory form the foundation before Part 3 introduces tools / Part 4 AgentBot loop memory (chat outputs + tool outputs).

## Tool-shaped chat alternative

- [x] **MEM-COMP-040**: Notebook `02_memory_state.py` shall demonstrate that paper summaries appended as `role="tool"` messages onto the existing `AppendOnlyMemory` chat history (passed as `history`, without `context_text` / `CitationMemory.as_context()`) can supply similar evidence to a compare turn.

## Success Criteria

- [x] **MEM-COMP-020**: The add-third-paper follow-up shall use citation context that includes the new paper's summary (not present before the third `add`).

## Testing

- [x] **MEM-COMP-030**: `tests/test_exercises_part2.py` shall verify empty vs. populated `as_context()` strings differ when summaries are added.

## Related Documents

- [Memory LLD](./LLD.md)
- [Chat History EARS](./chat-history-EARS.md)
- [Citation Memory EARS](./citation-memory-EARS.md)
- [Classroom Infrastructure EARS](../tutorial-delivery/classroom-infrastructure-EARS.md)
