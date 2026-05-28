# Multi-Agent Systems — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Multi-agent
**Part**: 5 (30 min) — **Eric Ma**
**Notebook**: `notebooks/05_multi_agent_demo.py`

## Overview

Part 5 is **demo-heavy**: specialized Searcher and Synthesizer agents collaborate on a literature review, followed by discussion of failure modes, expansions (web search, PDF parsing, coding agents), and Q&A. Minimal new coding — participants are often tired by this point.

## Implementation Status

| Component | Status |
|-----------|--------|
| `agents.py` — SearcherAgent, SynthesizerAgent, ResearchOrchestrator | Done |
| `research_tools.py` — `@tool` helpers, EvidenceCollector | Done |
| `notebooks/05_multi_agent_demo.py` — fixture/mcp modes, empty + oversized presets | Done |
| MCP mode uses tutorial FastMCP server by default (`ZOTERO_MCP_SOURCE=tutorial`) | Done |
| Failure preset: low ReAct max-steps | Deferred (Part 4 not built) |
| Architecture recap mermaid diagram | Not started |
| `tests/test_agents.py` | Done (AgentBot mocked) |

## Learning Objectives

After Part 5, participants can:

- Describe how role-specialized agents divide search vs. synthesis.
- Name common failure modes: hallucination, context exhaustion, deadlocks.
- Articulate when custom research agents still matter alongside coding assistants.

## Discussion Prompts (Facilitator)

- Hallucination, context exhaustion, agent deadlocks — when do they appear?
- Expansions: web search, PDF parsing — what would each require?
- Why build agents when coding assistants exist?

## Notebook Content

### Demo 1 — Searcher + Synthesizer

- `mo.ui` controls: query input, run button.
- `ResearchOrchestrator` runs:

```text
user query → SearcherAgent → evidence → SynthesizerAgent → markdown report
```

- Searcher: llamabot **`AgentBot`** with `mcp_servers` (zotero-mcp) in live mode, or fixture `@tool` in offline mode
- Custom tools in `research_tools.py`: `search_fixture_library`, `cache_evidence`, `finish_search`
- Returns `list[CitationRecord]` collected during the agent run via `EvidenceCollector`
- Falls back to `search_fixture_library()` if AgentBot caches no records
- Synthesizer: llamabot **`AgentBot`** (no MCP); evidence passed in context; finishes via `respond_to_user`

### Demo 2 — Failure-mode presets

| Preset | What it demonstrates |
|--------|----------------------|
| Empty evidence | Synthesizer hallucination risk |
| Oversized context | Truncation / context exhaustion |
| Low max steps | ReAct deadlock / incomplete loop *(deferred until Part 4 `ReActRunner` exists)* |

Facilitator walks mitigations: max steps, truncation, structured outputs, human review.

### Architecture recap cell

Diagram linking all five capabilities (prompt → memory → tools → planning → multi-agent) for closure.

### Success criteria

End-to-end demo runs; failure presets reproducible from UI; discussion prompts included in notebook markdown.

## Library Module: `agents.py`

### `SearcherAgent`

- llamabot **`AgentBot`** with `mcp_servers` (zotero-mcp) in live mode, or fixture `@tool` in offline mode
- Custom tools in `research_tools.py`: `search_fixture_library`, `cache_evidence`, `finish_search`
- Returns `list[CitationRecord]` collected during the agent run

### `SynthesizerAgent`

- llamabot **`AgentBot`** (no MCP); finishes with `respond_to_user`
- Input: evidence list + original query
- Returns markdown report

### `ResearchOrchestrator`

Synchronous pipeline for tutorial simplicity:

```python
evidence = searcher.run(query)
report = synthesizer.run(query, evidence)
return report
```

Role prompts live in `prompts.py` (`SEARCHER_AGENTBOT_PROMPT`, `SYNTHESIZER_AGENTBOT_PROMPT`).

## Library Module: `research_tools.py`

| Export | Purpose |
|--------|---------|
| `EvidenceCollector` | Accumulates `CitationRecord` during Searcher AgentBot run |
| `make_searcher_tools(collector) -> list` | Returns `@tool` functions bound to collector |
| `search_fixture_library` | Fixture search `@tool` (offline mode) |
| `cache_evidence` | Parse and store MCP or fixture results |
| `finish_search` | Signal Searcher completion |

## Dependencies

- [Planning LLD](../planning/LLD.md) — ReAct patterns, max steps
- [Tools LLD](../tools/LLD.md) — Searcher MCP access
- [Memory LLD](../memory/LLD.md) — optional cross-turn demo extension
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`

## Non-Goals (Part 5)

- Implement web search or PDF parsing — discussion only
- Async orchestration or agent debate loops
- New MCP tools beyond zotero-mcp

## Tests

- `tests/test_agents.py` — orchestration with mocked LLM and MCP responses

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Planning LLD](../planning/LLD.md)
- [Searcher Synthesizer EARS](./searcher-synthesizer-EARS.md)
- [Failure Mode Demos EARS](./failure-mode-demos-EARS.md)
- [Discussion Prompts EARS](./discussion-prompts-EARS.md)
