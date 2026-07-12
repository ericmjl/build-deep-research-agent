# Memory & State Management — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-07-11

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Memory
**Part**: 2 (40 min) — **Ben Batorsky**
**Notebook**: `notebooks/02_memory_state.py`

## Implementation Status

**Implemented.** Exercise stubs in `exercises/part2.py`; reference solutions in
`exercises/solutions/part2.py`; re-exported from `memory.py`.

## Overview

Part 2 adds **state** to the agent: conversation history with recency retrieval,
and a citation inventory of LLM summaries (hand-built precursor to tool outputs).
Participants implement append-only memory, summarize papers with a plain function,
store summaries in citation memory, and combine both stores in one query — closing
Ben's segment before handoff to Eric.

## Learning Objectives

After Part 2, participants can:

- Explain why multi-turn research needs memory.
- Append chat turns, retrieve a recent slice, and inject prior context into the next LLM call.
- Call a plain summarizer, store results in `CitationMemory`, and combine chat + citation context.

## Discussion Prompts (Facilitator)

- When does `retrieve(n_results)` (recent turns) suffice vs full history / `as_context()`?
- When is chat history enough, and when does structured citation memory pay off?
- How is hand-recording `role="tool"` summaries like AgentBot's Part 4 loop memory?

## Notebook Exercises

### Exercise 1 — Append-only chat history + retrieve

- Use `AppendOnlyMemory` to record user/assistant turns.
- Ask a follow-up that requires prior turn content.
- Demonstrate `retrieve(n_results)` vs full `messages()`.

### Exercise 2 — Summaries + citation memory + combined query

- Implement `summarize_paper` (plain function) and `CitationMemory`.
- Summarize two papers, `add` each, compare via `as_context()` plus chat history.
- Add a third paper and ask what changed (full citation context + chat).

### Why `context_text`? (teaching beat after Exercise 2)

- Show that summarization-as-tool + summary-as-result can live *inside*
  the existing `AppendOnlyMemory` via `role="tool"` messages (no separate
  `context_text`).
- Keep `CitationMemory` in the main exercises for keyed inventory /
  `as_context()`; the tool-role demo previews Part 4 loop memory.

### Handoff cell (end of notebook)

Recap: prompt + memory = foundation; summaries can be citation store *or* tool
turns in chat; Part 3 wraps tools; Part 4 AgentBot records tool steps.
Memory becomes chat outputs + tool outputs.

### Success criteria

Visible difference with/without history; combined compare uses summaries; add-third
follow-up reflects the new paper.

## Library Module: `memory.py`

Immutable fluent style — mutating methods return new instances.

### `AppendOnlyMemory`

| Method | Returns | Behavior |
|--------|---------|----------|
| `append(message: Message)` | `AppendOnlyMemory` | Add turn |
| `messages()` | `list[Message]` | Ordered history |
| `retrieve(n_results: int)` | `list[Message]` | Most recent N turns |

### `CitationMemory`

| Method | Returns | Behavior |
|--------|---------|----------|
| `add(citation: CitationRecord, summary: str)` | `CitationMemory` | Append citation + summary |
| `as_context()` | `str` | Format for prompt injection |

### `summarize_paper(bot, text)`

Plain function (no `@tool`); returns a short summary string.

## Dependencies

- [Prompting LLD](../prompting/LLD.md) — fixtures, `format_citations_for_context`, prompts
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`, `Message`, `CitationRecord`

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Append to immutable snapshot | Document pattern: rebind variable to returned instance |
| Duplicate citation keys | Later entry wins (document in EARS) |
| Empty citation inventory | `as_context()` returns a clear empty placeholder |

## Tests

- `tests/test_exercises_part2.py` — append/retrieve order, immutability, summary
  recording, stubs, `summarize_paper`

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Prompting LLD](../prompting/LLD.md)
- [Tools LLD](../tools/LLD.md) — next capability (Eric)
- [Chat History EARS](./chat-history-EARS.md)
- [Citation Memory EARS](./citation-memory-EARS.md)
- [Memory Comparison EARS](./memory-comparison-EARS.md)
