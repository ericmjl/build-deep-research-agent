# Memory Comparison — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## Part 2 Exercise 3

- [ ] **MEM-COMP-001**: Notebook `02_memory_state.py` shall run the same follow-up question against an empty memory state and a populated memory state.
- [ ] **MEM-COMP-002**: Notebook `02_memory_state.py` shall display both LLM outputs side by side for participant comparison.
- [ ] **MEM-COMP-003**: The comparison exercise shall use `CitationMemory` or combined chat + citation memory as populated state.

## Handoff

- [ ] **MEM-COMP-010**: The final cells of `02_memory_state.py` shall recap that prompt + memory form the foundation before Part 3 introduces tools.

## Success Criteria

- [ ] **MEM-COMP-020**: The populated-memory run shall include citation context not present in the empty-memory run (verifiable by test or notebook assertion on context length).

## Testing

- [ ] **MEM-COMP-030**: `tests/test_memory.py` or notebook smoke tests shall verify empty vs. populated context strings differ when citations are added.

## Related Documents

- [Memory LLD](./LLD.md)
- [Chat History EARS](./chat-history-EARS.md)
- [Classroom Infrastructure EARS](../tutorial-delivery/classroom-infrastructure-EARS.md)
