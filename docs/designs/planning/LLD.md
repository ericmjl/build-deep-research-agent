# Planning Workflows — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-29

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Planning
**Part**: 4 (30 min) — **Eric Ma**
**Notebook**: `notebooks/04_workflows.py`

## Implementation Status

**Implemented.** `workflows.py` provides `DeterministicWorkflow`, `ReActRunner`, and comparison helpers. `deterministic_agent.py` provides PocketFlow execution helpers and AgentBot wiring for Exercise 1b. Notebook `04_workflows.py` covers Exercises 1–3. Part 5 `MULTI-FAIL-003` (low max-steps preset) remains optional follow-up.

## Overview

Part 4 adds **planning**: orchestrating prompt, memory, and tools into repeatable research flows. Participants build a deterministic linear PocketFlow graph and a **ReAct Runner** (*Re*ason + *Act*, not React.js) loop, then compare both on the same question.

## Design principle: minimize indirection

Earlier drafts stacked too many layers (`plan_fn` → factory → `@tool` → graph), which obscured what learners were actually building. Part 4 now follows a **direct implementation** model:

| Layer | Who writes it | What it contains |
|-------|----------------|------------------|
| **`exercises/part4.py`** | **Participant** | Minimal stubs (`NotImplementedError`) for `plan_research`, `search_literature`, `summarize_evidence`, plus `react_step_fn` for Exercise 2 |
| **`exercises/solutions/part4.py`** | **Instructor (reference)** | Full implementations of the same tool bodies — comment-swap import in **part4_exercises** |
| **Notebook markdown cells** | **Materials author** | Step-by-step **implementation specs** for each exercise function (participants read specs here, code in `part4.py`) |
| **Notebook cells** | **Participant (visible wiring)** | `@tool(loopback_name=…)` decorators, PocketFlow edge syntax, UI controls — orchestration stays in the notebook where it can be seen |
| **`deterministic_agent.py`** | **Library (small)** | `DeterministicWorkflowStore`, `run_deterministic_flow`, AgentBot helpers — **no** factory that hides tool construction for Exercise 1a |
| **`workflows.py`** | **Library (tests + ReAct)** | FSM class for unit tests, `ReActRunner`, comparison helpers — not the primary Exercise 1a teaching path |

**Avoid:**

- Notebook wrapper functions that re-export exercise callables under different names (`plan_fn` calling `part4.plan_fn`, etc.).
- `importlib.reload(part4)` — restart the marimo kernel after editing `part4.py`.
- Library factories that build `@tool` nodes from hidden inner functions (removed: `make_deterministic_workflow_tools`).

**One exception (Exercise 1b):** `make_agentbot_workflow_tools()` remains a thin library helper because AgentBot tools need default loopback to the LLM **DecideNode**, while Exercise 1a tools use explicit `loopback_name` edges. Same three tool bodies from `part4.py`; only the decorator/wiring differs.

## Learning Objectives

After Part 4, participants can:

- Contrast deterministic vs. agentic workflow trade-offs.
- Implement PocketFlow tool bodies for a fixed pipeline: plan → search → summarize → done.
- Wire a linear PocketFlow graph with `@tool` and edge syntax (no decide node).
- Run a ReAct loop with fixture tools and inspect the trace.

## Discussion Prompts (Facilitator)

- When is a deterministic workflow safer than open-ended ReAct?
- What failure modes appear when the loop has no max steps?
- How do workflows sit on top of Parts 1–3?

## Notebook Exercises

Hands-on structure: participants **edit `build_deep_research_agent/exercises/part4.py`**
(minimal stubs). **Implementation specs** live in markdown cells in `04_workflows.py`
(e.g. **ex1_implementation_specs**). The notebook imports the exercise module once in
**part4_exercises** (`from build_deep_research_agent.exercises import part4`).
After saving edits, **restart the kernel** so Python reloads the module.

Reference answers live in `exercises/solutions/part4.py`; instructors comment-swap
the import in the **part4_exercises** cell.

### Exercise 0 — FSM warm-up

- Call `validate_deterministic_transition` for valid and invalid pairs.
- Observe `InvalidStateTransitionError` on illegal jumps.

### Exercise 1a — Deterministic workflow via linear PocketFlow graph

**Read specs in the notebook** (**ex1_implementation_specs**). **Implement in `exercises/part4.py`**
(tool bodies, not separate `plan_fn` aliases):

| Function | FSM state | Responsibility |
|----------|-----------|----------------|
| `plan_research(store, *, use_live_llm)` | plan | Validate transition, set `store.search_terms`, append snapshot, return status |
| `search_literature(store)` | search | Validate transition, populate `store.evidence`, append snapshot, return status |
| `summarize_evidence(store, *, use_live_llm)` | summarize | Validate transition, set `store.report`, append snapshot, return markdown |

**Wire in the notebook** (`ex1_workflow_tools`):

```python
from llamabot.components.tools import tool

@tool(loopback_name="search_literature")
def plan_research() -> str:
    return part4.plan_research(workflow_store, use_live_llm=use_live_llm.value)

@tool(loopback_name="summarize_evidence")
def search_literature() -> str:
    return part4.search_literature(workflow_store)

@tool(loopback_name=None)
def summarize_evidence() -> str:
    return part4.summarize_evidence(workflow_store, use_live_llm=use_live_llm.value)

workflow_tools = [plan_research, search_literature, summarize_evidence]
```

**Wire edges** (`ex1_pocketflow_graph`):

```python
plan_tool - "search_literature" >> search_tool
search_tool - "summarize_evidence" >> summarize_tool
det_flow = Flow(start=plan_tool)
```

Display the `Flow` in marimo (Mermaid). `run_deterministic_flow()` returns a
`DeterministicFlowRun` (`.result` + `.shared` with `execution_history`) for traces
and Exercise 3.

States: `plan` → `search` → `summarize` → `done` (linear chain, not AgentBot routing).

### Exercise 1b — Same tool bodies via AgentBot (prompt-controlled)

- Reuses **`plan_research` / `search_literature` / `summarize_evidence`** from `part4.py`.
- `build_planning_agentbot(store, part4.plan_research, …)` — library wraps tool bodies with `@tool` loopback to **DecideNode**.
- `WORKFLOW_AGENTBOT_PROMPT` in `prompts.py` steers plan → search → summarize → `respond_to_user`.
- Requires live LLM for the decide node (even when exercise stubs are offline).

### Exercise 2 — ReAct loop

- Single notebook wrapper: `react_step_fn` in **part4_exercises** delegates to `part4.react_step_fn` (keeps Exercise 2 cell signatures stable).
- Run `ReActRunner`; render thought → action → observation trace.
- Optional: dropdown to LLM `make_llamabot_react_step_fn()`.

### Exercise 3 — Compare approaches

- Reactive comparison table driven by Exercise 1–2 outputs.
- Tune `react_max_steps`; optional run-button challenge at `max_steps=1`.

### Success criteria

Both workflows complete; comparison exercise renders in notebook.

## Library Modules

### `deterministic_agent.py` (PocketFlow + AgentBot path)

| Piece | Role |
|-------|------|
| `DeterministicWorkflowStore` | Mutable state shared across tool bodies |
| `run_deterministic_flow()` | Reset store, run linear `Flow`, return `DeterministicFlowRun` |
| `make_agentbot_workflow_tools()` | Thin `@tool` wrappers for Exercise 1b (decide loopback) |
| `build_planning_agentbot()` | AgentBot + `WORKFLOW_AGENTBOT_PROMPT` |
| `run_planning_agentbot()` | Execute and return `DeterministicResult` |

**Removed:** `make_deterministic_workflow_tools()` — Exercise 1a wiring lives in the notebook.

Contrast with Part 5 **AgentBot**, where an LLM decide node loops until `respond_to_user`.

### `workflows.py` (FSM tests, ReAct, comparison)

Both workflows accept injectable callables where useful (enables tests without live LLM/MCP).

`DeterministicWorkflow` remains for **unit tests** and direct FSM teaching — not the primary PocketFlow exercise path:

| Method | State | Action |
|--------|-------|--------|
| `plan(query)` | `plan` | Call injectable plan callable; return search terms + snapshot |
| `search(query, search_terms)` | `search` | Call injectable search callable; return evidence + snapshot |
| `summarize(query, search_terms, evidence)` | `summarize` | Call injectable summarize callable; return report + snapshot |
| `done_snapshot(...)` | `done` | Build terminal snapshot (no callable) |
| `run(query)` | all | Convenience runner over the steps above |

Transition table: `DETERMINISTIC_TRANSITIONS` in `workflows.py`.

### `ReActWorkflow` / ReAct Runner

> **Naming**: *ReAct* = **Re**ason + **Act**. Implementation class: `ReActRunner`.

| Input | Output |
|-------|--------|
| `query`, fixture/MCP tools, `max_steps` | `list[ReActStep]`, `final_answer` |

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
- [Tutorial Delivery LLD](../tutorial-delivery/LLD.md) — `llm.py`, marimo conventions

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Max steps exceeded | Return partial trace + graceful partial answer |
| Invalid FSM transition | `InvalidStateTransitionError` with state names |
| Empty search in workflow | Proceed to summarize with empty evidence (teaching moment) |
| Learner stub not implemented | `NotImplementedError` from `exercises/part4.py` until implemented |

## Tests

- `tests/test_workflows.py` — FSM transitions, ReAct max steps, mocked tool injection
- `tests/test_deterministic_agent.py` — linear PocketFlow wiring (mirrors notebook `@tool` pattern), AgentBot loopback
- `tests/test_exercises_part4.py` — learner stubs vs. instructor solutions

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Tools LLD](../tools/LLD.md)
- [Multi-Agent LLD](../multi-agent/LLD.md) — next capability
- [Deterministic Workflow EARS](./deterministic-workflow-EARS.md)
- [ReAct Runner EARS](./react-runner-EARS.md)
- [Workflow Comparison EARS](./workflow-comparison-EARS.md)
