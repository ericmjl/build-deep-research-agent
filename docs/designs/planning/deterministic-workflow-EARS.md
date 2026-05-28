# Deterministic Workflow — EARS

**Parent LLD**: [Planning LLD](./LLD.md)

## DeterministicWorkflow

- [ ] **PLAN-DET-001**: The `workflows.py` module shall define `DeterministicWorkflow` with states `plan`, `search`, `summarize`, and `done`.
- [ ] **PLAN-DET-002**: `DeterministicWorkflow` shall transition in order: `plan` → `search` → `summarize` → `done`.
- [ ] **PLAN-DET-003**: `DeterministicWorkflow` shall accept injectable callables for search and summarize to support testing without live LLM or MCP.

## Part 4 Exercise 1

- [ ] **PLAN-DET-010**: Notebook `04_workflows.py` shall run `DeterministicWorkflow` on a sample research query.
- [ ] **PLAN-DET-011**: Notebook `04_workflows.py` shall display workflow state and accumulated evidence at each step.

## Error Handling

- [ ] **PLAN-DET-020**: If an invalid state transition is attempted, the workflow shall raise `InvalidStateTransitionError` naming the from-state and to-state.
- [ ] **PLAN-DET-021**: When search returns empty evidence, `DeterministicWorkflow` shall still proceed to the summarize step.

## Testing

- [ ] **PLAN-DET-030**: `tests/test_workflows.py` shall verify all valid state transitions complete in order.
- [ ] **PLAN-DET-031**: `tests/test_workflows.py` shall verify invalid transitions raise `InvalidStateTransitionError`.

## Related Documents

- [Planning LLD](./LLD.md)
- [ReAct Runner EARS](./react-runner-EARS.md)
