# Planning Workflows — Low-Level Design

**Created**: 2026-05-27
**Updated**: 2026-07-11

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

**Capability**: Planning
**Part**: 4 (30 min) — **Eric Ma**
**Notebook**: `notebooks/04_workflows.py`

## Implementation Status

**Implemented.** `exercises/solutions/part4.py` provides `build_agent` (AgentBot wiring with `max_iterations` parameter) and `deterministic_pipeline` (SimpleBot-based search → summarize). `workflows.py` provides `DeterministicWorkflow`, `ReActRunner` (library/test infrastructure). `tools/corpus.py` provides `connect_corpus_docstore` for cross-notebook docstore reuse. Notebook `04_workflows.py` covers Exercises 1–5.

## Overview

Part 4 introduces **AgentBot** — llamabot's iterate-loop agent (ReAct pattern). Participants wire a search tool into AgentBot, inspect its iteration spans, then contrast it with a deterministic pipeline (SimpleBot: search once → summarize). Exercises 4–5 deepen the comparison: a multi-faceted question rewards the agent's adaptive loop, and `max_iterations` is the cost/quality dial between deterministic and fully agentic behavior.

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

- Wire an AgentBot with a search tool and a system prompt.
- Inspect `agent.spans` to trace each think → act → observe iteration.
- Contrast a deterministic pipeline (search once → summarize) with AgentBot's adaptive loop.
- Explain when the agentic loop earns its cost (multi-faceted questions) vs. when a deterministic pipeline suffices.
- Tune `max_iterations` as the primary control knob between deterministic (1) and fully agentic (5+) behavior.

## Discussion Prompts (Facilitator)

- When is a deterministic workflow safer than open-ended ReAct?
- What failure modes appear when the loop has no max steps?
- How do workflows sit on top of Parts 1–3?

## Notebook Exercises

Notebook `04_workflows.py` reconnects to the Part 3 corpus docstore via
`part3.connect_corpus_docstore(papers)` (no re-ingestion). Exercises 1–5:

### Exercise 1 — Wire AgentBot with search_corpus

Implement `build_agent(search_corpus)` in the scaffold cell: construct an
`AgentBot` with the search tool, a system prompt, and `max_iterations=5`.
Reference in `exercises/solutions/part4.py`.

### Exercise 2 — Observe the loop

Inspect `agent.spans` — each span records `operation_name`, `iteration`,
`chosen_tool`. Count decision iterations.

### Exercise 3 — Deterministic pipeline vs. AgentBot

Implement `deterministic_pipeline(search_tool, query)`: one `search_corpus`
call + one `SimpleBot` summary. Compare its answer and LLM-call count to
AgentBot from Exercise 1 on the same question. Reference in
`exercises/solutions/part4.py`.

### Exercise 4 — When the loop matters

Run-and-observe: a multi-faceted question (astrophysics + computational
biology) through both approaches. Fresh `AgentBot` per run (clean span
counts). Discussion prompt on when to choose deterministic despite
limitations.

### Exercise 5 — The cost/quality dial: `max_iterations`

Run-and-observe: rebuild the agent with `max_iterations=1` (starved) on the
Exercise 4 question. Compare to `max_iterations=5`. Shows that fewer
iterations degrades toward deterministic behavior.

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
