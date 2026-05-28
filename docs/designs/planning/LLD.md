# Planning Workflows — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Planning
**Part**: 4 (30 min) — **Eric Ma**
**Notebook**: `notebooks/04_workflows.py`

## Implementation Status

**Not started.** `workflows.py` (DeterministicWorkflow, ReAct Runner) and `04_workflows.py` depend on Parts 1–3 library modules. The Part 5 low max-steps failure preset is deferred until ReAct Runner exists.

## Overview

Part 4 adds **planning**: orchestrating prompt, memory, and tools into repeatable research flows. Participants build a deterministic state-machine workflow and a **ReAct Runner** (*Re*ason + *Act*, not React.js) loop, then compare both on the same question.

## Learning Objectives

After Part 4, participants can:

- Contrast deterministic vs. agentic workflow trade-offs.
- Implement a fixed pipeline: plan → search → summarize → done.
- Run a ReAct loop with MCP tools and inspect the trace.

## Discussion Prompts (Facilitator)

- When is a deterministic workflow safer than open-ended ReAct?
- What failure modes appear when the loop has no max steps?
- How do workflows sit on top of Parts 1–3?

## Notebook Exercises

### Exercise 1 — Deterministic state machine

- Run `DeterministicWorkflow` with fixed transitions.
- Display current state and evidence at each step.

States: `plan` → `search` → `summarize` → `done`.

### Exercise 2 — ReAct loop

- Run `ReActWorkflow` with zotero-mcp tools.
- Render trace: thought → action → observation per step.

### Exercise 3 — Compare approaches

- Same research question through both workflows.
- Compare step count, trace length, and output structure in a table.

### Success criteria

Both workflows complete; comparison exercise renders in notebook.

## Library Module: `workflows.py`

Both workflows accept injectable callables for search/summarize (enables tests without live LLM/MCP).

### `DeterministicWorkflow`

| State | Action |
|-------|--------|
| `plan` | Parse query; set search terms |
| `search` | Call MCP search (or injected callable) |
| `summarize` | LLM synthesis over evidence |
| `done` | Return final answer |

Track state in `WorkflowState` (see tutorial-delivery shared models or local dataclass).

### `ReActWorkflow` / ReAct Runner

> **Naming**: *ReAct* = **Re**ason + **Act**. Implementation class: `ReActRunner` or `ReActWorkflow`.

| Input | Output |
|-------|--------|
| `query`, MCP tools, `max_steps` | `list[ReActStep]`, `final_answer` |

### `ReActStep`

| Field | Type |
|-------|------|
| `thought` | `str` |
| `action` | `str \| None` |
| `action_input` | `dict \| None` |
| `observation` | `str \| None` |

**Stop conditions**: final answer without tool call; `REACT_MAX_STEPS` reached; unrecoverable tool error in observation.

Env: `REACT_MAX_STEPS` (default 8) — see [Tutorial Delivery LLD](../tutorial-delivery/LLD.md).

## Dependencies

- [Tools LLD](../tools/LLD.md) — MCP search in workflow steps
- [Memory LLD](../memory/LLD.md) — optional memory injection between steps
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Max steps exceeded | Return partial trace + `WorkflowMaxStepsError` or graceful partial |
| Invalid FSM transition | `InvalidStateTransitionError` with state names |
| Empty search in workflow | Proceed to summarize with empty evidence (teaching moment) |

## Tests

- `tests/test_workflows.py` — FSM transitions, ReAct max steps, mocked tool injection

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Tools LLD](../tools/LLD.md)
- [Multi-Agent LLD](../multi-agent/LLD.md) — next capability
- [Deterministic Workflow EARS](./deterministic-workflow-EARS.md)
- [ReAct Runner EARS](./react-runner-EARS.md)
- [Workflow Comparison EARS](./workflow-comparison-EARS.md)
