# Deterministic Workflow — EARS

**Parent LLD**: [Planning LLD](./LLD.md)

## DeterministicWorkflow (library / tests)

- [x] **PLAN-DET-001**: The `workflows.py` module shall define `DeterministicWorkflow` with states `plan`, `search`, `summarize`, and `done`.
- [x] **PLAN-DET-002**: `DeterministicWorkflow` shall transition in order: `plan` → `search` → `summarize` → `done`.
- [x] **PLAN-DET-003**: `DeterministicWorkflow` shall accept injectable callables for search and summarize to support testing without live LLM or MCP.

## Part 4 Exercise 1 — direct tool bodies (no factory wrappers)

- [x] **PLAN-DET-004**: `exercises/part4.py` shall define `plan_research`, `search_literature`, and `summarize_evidence` as minimal PocketFlow tool-body stubs; `exercises/solutions/part4.py` shall contain the reference implementations.
- [x] **PLAN-DET-007**: Notebook `04_workflows.py` shall publish step-by-step implementation specs for those tool bodies in markdown cells (e.g. **ex1_implementation_specs**), not in learner module docstrings.
- [x] **PLAN-DET-005**: Notebook `04_workflows.py` shall wire `@tool(loopback_name=…)` decorators and PocketFlow edges in visible cells — not via a library factory such as `make_deterministic_workflow_tools`.
- [x] **PLAN-DET-006**: The notebook shall import the exercise module directly in **part4_exercises** without `importlib.reload`; participants shall restart the kernel after editing `part4.py`.

## Part 4 Exercise 1 — runtime and display

- [x] **PLAN-DET-010**: Notebook `04_workflows.py` shall run a linear PocketFlow graph on a sample research query via `run_deterministic_flow`.
- [x] **PLAN-DET-011**: Notebook `04_workflows.py` shall display workflow state and accumulated evidence at each step.

## Part 4 Exercise 1b — AgentBot (thin library wrapper only)

- [x] **PLAN-DET-015**: `make_agentbot_workflow_tools()` shall wrap the same three tool bodies from `part4.py` with default loopback to the LLM DecideNode.
- [x] **PLAN-DET-016**: `build_planning_agentbot()` shall construct an AgentBot using `WORKFLOW_AGENTBOT_PROMPT` and the AgentBot tool wrappers.

## Error Handling

- [x] **PLAN-DET-020**: If an invalid state transition is attempted, the workflow shall raise `InvalidStateTransitionError` naming the from-state and to-state.
- [x] **PLAN-DET-021**: When search returns empty evidence, the workflow shall still proceed to the summarize step.

## Testing

- [x] **PLAN-DET-030**: `tests/test_workflows.py` shall verify all valid state transitions complete in order.
- [x] **PLAN-DET-031**: `tests/test_workflows.py` shall verify invalid transitions raise `InvalidStateTransitionError`.
- [x] **PLAN-DET-032**: `tests/test_deterministic_agent.py` shall verify linear PocketFlow wiring using `@tool` nodes that call instructor `part4` tool bodies (mirroring the notebook pattern).

## Related Documents

- [Planning LLD](./LLD.md)
- [ReAct Runner EARS](./react-runner-EARS.md)
