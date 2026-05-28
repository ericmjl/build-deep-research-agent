# Searcher & Synthesizer — EARS

**Parent LLD**: [Multi-Agent LLD](./LLD.md)

## Agent Classes

- [x] **MULTI-AGENT-001**: The `agents.py` module shall define `SearcherAgent` that returns `list[CitationRecord]` — not final prose.
- [x] **MULTI-AGENT-002**: The `SearcherAgent` shall access Zotero MCP via llamabot `AgentBot` `mcp_servers` (tutorial or upstream server) or fixture `@tool` (offline mode).
- [x] **MULTI-AGENT-003**: The `agents.py` module shall define `SynthesizerAgent` that accepts evidence and a query and returns a markdown report.
- [x] **MULTI-AGENT-004**: In v1, `SynthesizerAgent` shall not invoke MCP tools directly.

## ResearchOrchestrator

- [x] **MULTI-AGENT-010**: The `agents.py` module shall define `ResearchOrchestrator` running synchronously: query → SearcherAgent → SynthesizerAgent → report.
- [x] **MULTI-AGENT-011**: `ResearchOrchestrator` shall pass Searcher output as structured evidence to the Synthesizer.

## Part 5 Demo 1

- [x] **MULTI-AGENT-020**: Notebook `05_multi_agent_demo.py` shall provide `mo.ui` controls for query input and run execution.
- [x] **MULTI-AGENT-021**: When the participant triggers the demo, the notebook shall display the markdown report from `ResearchOrchestrator`.

## Scope (Part 5)

- [x] **MULTI-AGENT-030**: Part 5 shall be demo-heavy with minimal new participant coding.
- [x] **MULTI-AGENT-031**: Part 5 shall not implement async orchestration or agent debate loops in v1.

## Testing

- [x] **MULTI-AGENT-040**: `tests/test_agents.py` shall verify orchestration with mocked Searcher and Synthesizer responses.

## Related Documents

- [Multi-Agent LLD](./LLD.md)
- [Failure Mode Demos EARS](./failure-mode-demos-EARS.md)
