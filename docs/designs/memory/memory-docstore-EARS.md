# Memory Docstore — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## MemoryDocstore

- [x] **MEM-STORE-001**: `exercises/part2.py` shall define `MemoryDocstore` with pre-built backend initialization and `NotImplementedError` bodies for `add`, `search`, and `as_context`; `exercises/solutions/part2.py` shall contain the reference implementation.
- [x] **MEM-STORE-002**: `MemoryDocstore.add(text)` shall append the memory string to an in-memory list and to the LanceDB backend when available.
- [x] **MEM-STORE-003**: `MemoryDocstore.search(query, limit)` shall return an empty list for blank queries and otherwise return up to `limit` matching memory strings.
- [x] **MEM-STORE-004**: When the LanceDB backend cannot initialize or retrieve, `MemoryDocstore` shall fall back to keyword search over stored memories.
- [x] **MEM-STORE-005**: `MemoryDocstore.as_context(query, limit)` shall return `"(no relevant memories)"` when search returns no hits, otherwise a prompt-injection block prefixed with `MEMORY_PROMPT`.

## Part 2 Exercise 3

- [x] **MEM-STORE-010**: Notebook `02_memory_state.py` shall publish step-by-step implementation specs for `MemoryDocstore` in `ex3_implementation_specs`.
- [x] **MEM-STORE-011**: Notebook `02_memory_state.py` shall demonstrate how the docstore stores an input string and how `search` retrieves memories.
- [x] **MEM-STORE-012**: Notebook `02_memory_state.py` shall inject `MemoryDocstore.as_context(query)` into a subsequent LLM call.

## Testing

- [x] **MEM-STORE-030**: `tests/test_exercises_part2.py` shall verify learner `MemoryDocstore` stub methods raise `NotImplementedError` and the solution add/search/as_context round-trip works.

## Related Documents

- [Memory LLD](./LLD.md)
- [Chat History EARS](./chat-history-EARS.md)
- [Tools LLD](../tools/LLD.md) — Part 3 `ZoteroDocstore`
