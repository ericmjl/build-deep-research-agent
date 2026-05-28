# Chat History — EARS

**Parent LLD**: [Memory LLD](./LLD.md)

## AppendOnlyMemory

- [ ] **MEM-CHAT-001**: The `memory.py` module shall define `AppendOnlyMemory` with an `append(message: Message)` method.
- [ ] **MEM-CHAT-002**: When `append` is called, `AppendOnlyMemory` shall return a new instance (immutable fluent style).
- [ ] **MEM-CHAT-003**: `AppendOnlyMemory` shall expose `messages()` returning chat history in append order.

## Part 2 Exercise 1

- [ ] **MEM-CHAT-010**: Notebook `02_memory_state.py` shall use `AppendOnlyMemory` to record user and assistant turns.
- [ ] **MEM-CHAT-011**: Notebook `02_memory_state.py` shall run a follow-up question that requires content from a prior turn.
- [ ] **MEM-CHAT-012**: Notebook `02_memory_state.py` shall display the accumulated message list to the participant.

## Discussion Content

- [ ] **MEM-CHAT-020**: Notebook `02_memory_state.py` shall include facilitator prompts on why memory matters for multi-turn research.

## Testing

- [ ] **MEM-CHAT-030**: `tests/test_memory.py` shall verify append order is preserved across multiple turns.
- [ ] **MEM-CHAT-031**: `tests/test_memory.py` shall verify `append` does not mutate the original `AppendOnlyMemory` instance.

## Related Documents

- [Memory LLD](./LLD.md)
- [Citation Memory EARS](./citation-memory-EARS.md)
