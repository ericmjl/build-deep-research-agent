# Prompting & In-Context Learning — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Prompt / in-context learning
**Part**: 1 (40 min) — **Ben Batorsky**
**Notebook**: `notebooks/01_intro_prompting.py`

## Overview

Part 1 establishes the first layer of the mental model: a research agent starts as an **LLM plus context**. Participants craft system prompts and run summarization over **static Zotero metadata** bundled in the repo — no memory, no tools, no workflows yet.

## Implementation Status

| Component | Status |
|-----------|--------|
| `prompts.py` — `RESEARCH_SYSTEM_PROMPT`, `format_citations_for_context`, `build_messages` | Done |
| `fixtures/` — `zotero_library.json`, `loader.py`, `search.py` | Done |
| `tests/test_prompts.py`, `tests/test_fixtures.py` | Done |
| `notebooks/01_intro_prompting.py` | Not started |
| Part 5 reuses prompts via `SEARCHER_AGENTBOT_PROMPT` / `SYNTHESIZER_AGENTBOT_PROMPT` | Done |

## Learning Objectives

After Part 1, participants can:

- Explain what a research agent is (and is not) at a high level.
- Read and edit a research-oriented system prompt.
- Pass citation metadata as in-context input and interpret summarization output.

## Discussion Prompts (Facilitator)

- What makes an LLM call a "research agent" vs. a chatbot?
- What can in-context learning accomplish without tools or memory?
- Use cases and limitations of literature summarization agents.

## Notebook Exercises

### Exercise 1 — System prompt anatomy

- Import `RESEARCH_SYSTEM_PROMPT` from `build_deep_research_agent.prompts`.
- Display template; participants edit role, constraints, output format in a Marimo UI or cell.
- Run one summarization call via `llm.py`.

### Exercise 2 — Static Zotero metadata summarization

- Load records from `build_deep_research_agent.fixtures` (same shape as live Zotero metadata).
- Format with `format_citations_for_context()`.
- Summarize: "What themes connect these papers?"

### Success criteria

Participant produces a structured summary from static metadata using an editable system prompt.

## Library Module: `prompts.py`

| Export | Purpose |
|--------|---------|
| `RESEARCH_SYSTEM_PROMPT` | Default system template for research tasks (Part 1) |
| `SEARCHER_AGENTBOT_PROMPT` | Searcher AgentBot system prompt (Part 5) |
| `SYNTHESIZER_AGENTBOT_PROMPT` | Synthesizer AgentBot system prompt (Part 5) |
| `format_citations_for_context(citations: list[CitationRecord]) -> str` | Serialize fixtures for LLM context |
| `build_messages(system, user, history=None) -> list[Message]` | Assemble message list for llamabot |

Prompts are plain strings — inspectable in notebooks, no hidden templates.

## Fixtures: `fixtures/`

- File: `zotero_library.json` — 5 diverse items (paper, preprint, chapter-style).
- `load_citation_fixtures()` in `loader.py`; `search_fixture_library(query, limit)` in `search.py`.
- Used in Part 1 (in-context), Part 2 (citation memory), and Part 5 fixture Searcher mode.
- Normalized to `CitationRecord` — not raw Zotero API JSON.

## Dependencies

- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — Marimo, `llm.py`, `CitationRecord`
- llamabot via `llm.py`
- Modal endpoint (tutorial-provided)

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Missing LLM config | Setup cell error with env var names |
| Empty fixture load | Fail fast with path hint |
| LLM timeout | Catch; suggest retry with shorter context |

## Tests

- `tests/test_prompts.py` — formatting, message assembly
- `tests/test_fixtures.py` — fixture loads into `CitationRecord`

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md)
- [Memory LLD](../memory/LLD.md) — next capability
- [System Prompt EARS](./system-prompt-EARS.md)
- [Static Summarization EARS](./static-summarization-EARS.md)
- [Fixtures EARS](./fixtures-EARS.md)
