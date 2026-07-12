# Citation Memory — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## summarize_paper

- [x] **MEM-CITE-005**: `exercises/solutions/part2.py` shall define `summarize_paper(bot, text) -> str` as a plain function (no `@tool` decorator) that returns a short summary string.

## CitationMemory

- [x] **MEM-CITE-001**: The `memory.py` module shall define `CitationMemory` with an `add(citation: CitationRecord, summary: str)` method.
- [x] **MEM-CITE-002**: When `add` is called, `CitationMemory` shall return a new instance (immutable fluent style).
- [x] **MEM-CITE-003**: `CitationMemory` shall expose `as_context()` returning a string formatted for LLM prompt injection (citation metadata plus summary text).
- [x] **MEM-CITE-004**: When duplicate citation keys are added, the later entry shall supersede the earlier entry in `as_context()` output.

## Part 2 Exercise 2

- [x] **MEM-CITE-010**: Notebook `02_memory_state.py` shall populate `CitationMemory` using fixture `CitationRecord` entries and summaries from `summarize_paper`.
- [x] **MEM-CITE-011**: Notebook `02_memory_state.py` shall inject `CitationMemory.as_context()` into a subsequent LLM call.
- [x] **MEM-CITE-012**: Notebook `02_memory_state.py` shall call `summarize_paper` for at least two fixture papers before the compare turn.
- [x] **MEM-CITE-013**: Notebook `02_memory_state.py` shall add a third paper (summarize + `add`) and run a follow-up that uses full citation context plus chat history.

## Optional Truncation

- [D] **MEM-CITE-020**: `AppendOnlyMemory` or companion helper may expose `truncate(max_turns: int)` for context-limit discussion.

## Testing

- [x] **MEM-CITE-030**: `tests/test_exercises_part2.py` shall verify `as_context()` includes citation title and summary text.
- [x] **MEM-CITE-031**: `tests/test_exercises_part2.py` shall verify duplicate-key supersession behavior.
- [x] **MEM-CITE-032**: `tests/test_exercises_part2.py` shall verify learner stub `summarize_paper` raises `NotImplementedError` and solutions `summarize_paper` returns bot response content.

## Related Documents

- [Memory LLD](./LLD.md)
- [Fixtures EARS](../prompting/fixtures-EARS.md)
- [Memory Comparison EARS](./memory-comparison-EARS.md)
