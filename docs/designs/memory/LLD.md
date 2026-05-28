# Memory & State Management — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Memory
**Part**: 2 (40 min) — **Ben Batorsky**
**Notebook**: `notebooks/02_memory_state.py`

## Implementation Status

**Not started.** Shared `Message` and `CitationRecord` models exist in `models.py`; fixture loader is ready for Part 2 exercises. `memory.py` and `02_memory_state.py` are next after Part 5 reference demo stabilizes.

## Overview

Part 2 adds **state** to the agent: conversation history and citation context that persist across turns. Participants implement append-only memory, attach Zotero citation snippets, and compare responses with and without memory — closing Ben's segment before handoff to Eric.

## Learning Objectives

After Part 2, participants can:

- Explain why multi-turn research needs memory.
- Append chat turns and inject prior context into the next LLM call.
- Store citation metadata in memory and observe improved follow-up answers.

## Discussion Prompts (Facilitator)

- When does stateless prompting fail for multi-turn research?
- What belongs in memory vs. re-fetched each turn?
- How does citation context differ from raw chat history?

## Notebook Exercises

### Exercise 1 — Append-only chat history

- Use `AppendOnlyMemory` to record user/assistant turns.
- Ask a follow-up that requires prior turn content.
- Display message list in notebook.

### Exercise 2 — Citation-context memory

- Use `CitationMemory` with fixture `CitationRecord` entries.
- Add snippets as the conversation references papers.
- Inject via `as_context()` into the next prompt.

### Exercise 3 — With vs. without memory

- Same follow-up question: empty memory vs. populated memory.
- Side-by-side output (Marimo comparison UI or markdown).

### Handoff cell (end of notebook)

Brief recap: prompt + memory = foundation; Part 3 adds **tools** (Eric).

### Success criteria

Visible difference in follow-up quality when citation memory is present.

## Library Module: `memory.py`

Immutable fluent style — mutating methods return new instances.

### `AppendOnlyMemory`

| Method | Returns | Behavior |
|--------|---------|----------|
| `append(message: Message)` | `AppendOnlyMemory` | Add turn |
| `messages()` | `list[Message]` | Ordered history |

### `CitationMemory`

| Method | Returns | Behavior |
|--------|---------|----------|
| `add(citation: CitationRecord, snippet: str)` | `CitationMemory` | Append citation entry |
| `as_context()` | `str` | Format for prompt injection |

Optional: `truncate(max_turns: int)` for Part 2 discussion on context limits.

## Dependencies

- [Prompting LLD](../prompting/LLD.md) — fixtures, `format_citations_for_context`, prompts
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`, `Message`, `CitationRecord`

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Append to immutable snapshot | Document pattern: rebind variable to returned instance |
| Duplicate citation keys | Later entry wins (document in EARS) |

## Tests

- `tests/test_memory.py` — append order, immutability, `as_context()` formatting

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Prompting LLD](../prompting/LLD.md)
- [Tools LLD](../tools/LLD.md) — next capability (Eric)
- [Chat History EARS](./chat-history-EARS.md)
- [Citation Memory EARS](./citation-memory-EARS.md)
- [Memory Comparison EARS](./memory-comparison-EARS.md)
