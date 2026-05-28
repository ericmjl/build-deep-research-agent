# ReAct Runner — EARS

**Parent LLD**: [Planning LLD](./LLD.md)

> **Naming**: *ReAct* = **Re**ason + **Act** (agent pattern). Not React.js.

## ReActWorkflow / ReActRunner

- [ ] **PLAN-REACT-001**: The `workflows.py` module shall define a ReAct loop runner (`ReActWorkflow` or `ReActRunner`) accepting `query`, MCP tools, and `max_steps`.
- [ ] **PLAN-REACT-002**: The ReAct runner shall return a trace as `list[ReActStep]` and a `final_answer` string.
- [ ] **PLAN-REACT-003**: Each `ReActStep` shall record `thought`, `action`, `action_input`, and `observation` fields.

## Stop Conditions

- [ ] **PLAN-REACT-010**: When the model produces a final answer without a tool call, the ReAct runner shall stop and return that answer.
- [ ] **PLAN-REACT-011**: When the step count reaches `REACT_MAX_STEPS` (default 8), the ReAct runner shall stop and return the partial trace.
- [ ] **PLAN-REACT-012**: If a tool call fails, the ReAct runner shall record the error in `observation` and allow the model to continue until a stop condition is met.

## Part 4 Exercise 2

- [ ] **PLAN-REACT-020**: Notebook `04_workflows.py` shall run the ReAct runner with zotero-mcp tools available.
- [ ] **PLAN-REACT-021**: Notebook `04_workflows.py` shall render the thought → action → observation trace for each step.

## Testing

- [ ] **PLAN-REACT-030**: `tests/test_workflows.py` shall verify the runner stops at `max_steps` using mocked LLM and tool responses.
- [ ] **PLAN-REACT-031**: `tests/test_workflows.py` shall verify a complete trace is returned when the model answers without further tool calls.

## Related Documents

- [Planning LLD](./LLD.md)
- [Deterministic Workflow EARS](./deterministic-workflow-EARS.md)
- [Workflow Comparison EARS](./workflow-comparison-EARS.md)
