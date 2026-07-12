# Chat History — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## AppendOnlyMemory

- [x] **MEM-CHAT-001**: The `memory.py` module shall define `AppendOnlyMemory` with an `append(message: Message)` method.
- [x] **MEM-CHAT-002**: When `append` is called, `AppendOnlyMemory` shall return a new instance (immutable fluent style).
- [x] **MEM-CHAT-003**: `AppendOnlyMemory` shall expose `messages()` returning chat history in append order.
- [x] **MEM-CHAT-004**: `AppendOnlyMemory` shall expose `retrieve(n_results: int)` returning the most recent `n_results` messages in chronological order (oldest turns dropped).

## Part 2 Exercise 1

- [x] **MEM-CHAT-010**: Notebook `02_memory_state.py` shall use `AppendOnlyMemory` to record user and assistant turns.
- [x] **MEM-CHAT-011**: Notebook `02_memory_state.py` shall run a follow-up question that requires content from a prior turn.
- [x] **MEM-CHAT-012**: Notebook `02_memory_state.py` shall display the accumulated message list to the participant.
- [x] **MEM-CHAT-013**: Notebook `02_memory_state.py` shall demonstrate `retrieve(n_results)` vs full `messages()` for a follow-up turn.

## Discussion Content

- [x] **MEM-CHAT-020**: Notebook `02_memory_state.py` shall include facilitator prompts on why memory matters for multi-turn research (including recency vs full context).

## Part 2 Exercise module

- [x] **MEM-EX-001**: `exercises/part2.py` shall define frozen pydantic skeleton classes `AppendOnlyMemory` and `CitationMemory` (plus `summarize_paper`) with `NotImplementedError` method bodies; `exercises/solutions/part2.py` shall contain the reference implementations.
- [x] **MEM-EX-003**: Notebook `02_memory_state.py` shall import the exercise module directly in `part2_exercises` without `importlib.reload`; participants shall restart the kernel after editing `part2.py`.
- [x] **MEM-EX-030**: `tests/test_exercises_part2.py` shall verify learner stub methods raise `NotImplementedError`.

## Testing

- [x] **MEM-CHAT-030**: `tests/test_exercises_part2.py` shall verify append order is preserved across multiple turns.
- [x] **MEM-CHAT-031**: `tests/test_exercises_part2.py` shall verify `append` does not mutate the original `AppendOnlyMemory` instance.
- [x] **MEM-CHAT-032**: `tests/test_exercises_part2.py` shall verify `retrieve(n_results)` returns the most recent N messages.

## Related Documents

- [Memory LLD](./LLD.md)
- [Citation Memory EARS](./citation-memory-EARS.md)
