# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///
# @spec TUT-MARIMO-021

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    """Setup cell: imports available to all exercise wiring."""

    from textwrap import dedent


@app.cell(hide_code=True)
def intro():
    # @spec PLAN-DET-010
    import marimo as mo

    mo.md(
        dedent("""
        # Part 4: Planning workflows

        By now you have prompts, memory, and MCP tools. Part 4 is about
        **orchestration**: wiring those pieces into a repeatable plan.

        You will compare three styles:

        1. **Deterministic workflow** — linear PocketFlow: plan → search → summarize.
        2. **AgentBot workflow** — same tools, but an LLM decide node + prompt picks each step.
        3. **ReAct loop** — hand-rolled thought → action → observation until done.

        Edit **`exercises/part4.py`** for the exercise functions; restart the kernel after saving.
        """)
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        dedent("""
    ## How this notebook works

    **Your code lives in** `build_deep_research_agent/exercises/part4.py`.
    **Implementation specs** for each exercise function are in markdown cells in this notebook.
    After saving edits there, **restart the kernel** (marimo: *Restart* in the menu) so Python reloads the module.

    1. **Exercise 1a** — linear PocketFlow graph (deterministic wiring in code).
    2. **Exercise 1b** — same pipeline via llamabot **AgentBot** (prompt-controlled routing).
    3. **Exercise 2** — ReAct loop with `react_step_fn`.
    4. **Exercise 3** — compare deterministic vs ReAct outputs.

    Exercise 1b needs **Use live LLM** on (the decide node calls an LLM even if plan/summarize stubs are offline).
    """)
    )
    return


@app.cell(hide_code=True)
def instructor_note(mo):
    mo.md(
        dedent("""
    ### Instructors

    Reference solutions: `build_deep_research_agent/exercises/solutions/part4.py`

    In **part4_exercises**, comment out the learner import and uncomment the solutions import:

    ```python
    # from build_deep_research_agent.exercises import part4
    from build_deep_research_agent.exercises.solutions import part4
    ```

    Participants keep the default learner import only.
    """)
    )
    return


@app.cell
def notebook_controls(mo):
    research_query = mo.ui.text(
        value="Bayesian workflow",
        label="Research question",
        full_width=True,
    )
    use_live_llm = mo.ui.checkbox(
        value=True,
        label="Use live LLM for summarize / ReAct (requires API credentials)",
    )
    react_max_steps = mo.ui.number(
        value=8,
        start=1,
        stop=20,
        label="ReAct max steps",
    )
    react_mode = mo.ui.dropdown(
        options={
            "scripted": "Exercise 2a — your scripted step_fn",
            "llm": "Exercise 2b — LLM step_fn (make_llamabot_react_step_fn)",
        },
        value="scripted",
        label="ReAct step decider",
    )
    mo.vstack([research_query, use_live_llm, react_max_steps, react_mode])
    return react_max_steps, react_mode, research_query, use_live_llm


@app.cell
def part4_exercises():
    from build_deep_research_agent.exercises import part4

    # Instructors: swap imports to load reference solutions.
    # from build_deep_research_agent.exercises.solutions import part4

    def react_step_fn(query: str, trace, tools):
        return part4.react_step_fn(query, trace, tools)

    return part4, react_step_fn


@app.cell(hide_code=True)
def warmup_fsm():
    """Warm-up: which deterministic transitions are legal?"""

    from build_deep_research_agent.workflows import (
        InvalidStateTransitionError,
        validate_deterministic_transition,
    )

    pairs = [
        ("plan", "search"),
        ("search", "summarize"),
        ("summarize", "done"),
        ("plan", "done"),
    ]
    for src, dst in pairs:
        try:
            validate_deterministic_transition(src, dst)
            print(f"OK   {src} -> {dst}")
        except InvalidStateTransitionError:
            print(f"FAIL {src} -> {dst}  (InvalidStateTransitionError)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        dedent("""
    ## Exercise 1a — Deterministic linear PocketFlow

    Implement the three **PocketFlow tool bodies** below in `exercises/part4.py`.
    The next cell has the full spec for each function.

    | Function | FSM state |
    |----------|-----------|
    | `plan_research` | plan |
    | `search_literature` | search |
    | `summarize_evidence` | summarize |

    In **ex1_workflow_tools**, wrap them with llamabot ``@tool`` and set ``loopback_name``
    to wire the linear graph (see starter code there).

    Then wire edges in **ex1_pocketflow_graph**:

    `plan_research` → `search_literature` → `summarize_evidence` → done
    """)
    )
    return


@app.function(hide_code=True)
# @spec TUT-MARIMO-018
# @spec PLAN-DET-007
def ex1_implementation_specs(mo):
    mo.md(
        dedent("""
    ### Implementation specs — edit `exercises/part4.py`

    Reference answers: `build_deep_research_agent/exercises/solutions/part4.py`
    (instructors comment-swap the import in **part4_exercises**).

    Delete the ``raise NotImplementedError(...)`` line in each function and implement
    from the steps below. Restart the kernel after saving.

    ---

    #### `plan_research(store, *, use_live_llm=True) -> str`

    **Goal:** derive search terms from ``store.query``, save them on the store,
    record a workflow snapshot, and return a short status string for PocketFlow memory.

    1. Call ``validate_deterministic_transition("plan", "search")`` from
       ``build_deep_research_agent.workflows``.
    2. Produce comma-separated search terms from ``store.query``:

       - When ``use_live_llm`` is ``False``, use ``store.query.strip()`` as the terms string.
       - When ``use_live_llm`` is ``True``, call llamabot ``StructuredBot`` with a Pydantic
         model that has exactly **five** ``search_terms`` strings, then join them with
         ``", "``. Use ``get_model_name()`` and ``get_completion_kwargs()`` from
         ``build_deep_research_agent.llm``.
    3. Assign the string to ``store.search_terms``.
    4. Append a ``WorkflowStepSnapshot(state="plan", search_terms=store.search_terms)``
       to ``store.steps``.
    5. Return a status message such as ``f"Planned search terms: {store.search_terms}"``.

    ---

    #### `search_literature(store) -> str`

    **Goal:** retrieve citation evidence for the planned terms, update the store,
    record a snapshot, and return a status string listing what you found.

    1. Call ``validate_deterministic_transition("search", "summarize")`` from
       ``build_deep_research_agent.workflows``.
    2. Read search terms from ``store.search_terms`` (fall back to ``store.query`` if needed).
       Split on commas, strip whitespace, and skip empty pieces.
    3. For each term, call ``search_fixture_library(term, limit=3)`` from
       ``build_deep_research_agent.fixtures.search``.
    4. Dedupe records by ``record.key``; keep at most **five** records total.
    5. Assign the list to ``store.evidence``.
    6. Append a ``WorkflowStepSnapshot`` with ``state="search"``, the terms string, and
       ``evidence=list(store.evidence)`` to ``store.steps``.
    7. Return a status message such as
       ``f"Retrieved {len(store.evidence)} record(s): {titles}"`` where ``titles`` lists
       record titles or ``"(none)"`` when empty.

    ---

    #### `summarize_evidence(store, *, use_live_llm=True) -> str`

    **Goal:** write a markdown report from ``store.evidence``, save it on the store,
    record a snapshot, and return the report text.

    1. Call ``validate_deterministic_transition("summarize", "done")`` from
       ``build_deep_research_agent.workflows``.
    2. Build markdown and assign it to ``store.report``:

       - If ``store.evidence`` is empty, set an explicit markdown message that no evidence
         was retrieved for the query (see the reference solution for the exact format).
       - If ``use_live_llm`` is ``True``, call ``default_summarize_fn(store.query, store.evidence)``
         from ``build_deep_research_agent.workflows``.
       - Otherwise, format citations with ``format_citations_for_context`` from
         ``build_deep_research_agent.prompts`` and wrap in a simple offline markdown stub.
    3. Append a ``WorkflowStepSnapshot`` with ``state="summarize"``, ``store.search_terms``,
       ``evidence=list(store.evidence)``, and ``report_markdown=store.report`` to ``store.steps``.
    4. Return ``store.report``.
    """)
    )
    return


@app.cell
def ex1_store():
    from build_deep_research_agent.deterministic_agent import (
        DeterministicWorkflowStore,
    )

    workflow_store = DeterministicWorkflowStore()
    return (workflow_store,)


@app.cell
def ex1_workflow_tools(part4, use_live_llm, workflow_store):
    from llamabot.components.tools import tool

    # Uses part4 and workflow_store from earlier cells — do not re-import here.

    @tool(loopback_name="search_literature")
    def plan_research() -> str:
        """PocketFlow tool body for the **plan** state — implement in exercises/part4.py.

        Delete the raise NotImplementedError(...) line in part4.plan_research and implement:

        1. Derive comma-separated search terms from store.query (offline: store.query.strip();
           live LLM: StructuredBot with five search_terms, joined with ", ")
        2. Set store.search_terms and append WorkflowStepSnapshot(state="plan", ...)
        3. Return a short status string for PocketFlow memory

        :returns: Status message (e.g. planned search terms).
        """
        return part4.plan_research(workflow_store, use_live_llm=use_live_llm.value)

    return plan_research, tool


@app.cell
def _(
    part4,
    plan_research,
    search_literature,
    tool,
    use_live_llm,
    workflow_store,
):
    @tool(loopback_name=None)
    def summarize_evidence() -> str:
        """PocketFlow tool body for the **summarize** state — implement in exercises/part4.py.

        Delete the raise NotImplementedError(...) line in part4.summarize_evidence and implement:

        1. Build markdown into store.report (empty evidence, live default_summarize_fn, or offline stub)
        2. Append WorkflowStepSnapshot(state="summarize", report_markdown=store.report, ...)
        3. Return store.report

        :returns: Markdown report text.
        """
        return part4.summarize_evidence(workflow_store, use_live_llm=use_live_llm.value)

    workflow_tools = [plan_research, search_literature, summarize_evidence]
    return (workflow_tools,)


@app.cell
def _(part4, tool, workflow_store):
    @tool(loopback_name="summarize_evidence")
    def search_literature() -> str:
        """PocketFlow tool body for the **search** state — implement in exercises/part4.py.

        Delete the raise NotImplementedError(...) line in part4.search_literature and implement:

        1. Read store.search_terms (fallback: store.query); split on commas
        2. For each term, search_fixture_library(term, limit=3); dedupe by record.key; cap at five
        3. Set store.evidence and append a WorkflowStepSnapshot(state="search", ...)
        4. Return a status string listing retrieved titles

        :returns: Status message for PocketFlow memory.
        """
        return part4.search_literature(workflow_store)

    return (search_literature,)


@app.cell
def ex1_pocketflow_graph(mo, workflow_tools):
    from llamabot.components.pocketflow import flow_to_mermaid
    from pocketflow import Flow

    plan_tool, search_tool, summarize_tool = workflow_tools

    plan_tool - "search_literature" >> search_tool
    search_tool - "summarize_evidence" >> summarize_tool

    det_flow = Flow(start=plan_tool)

    mo.mermaid(flow_to_mermaid(det_flow))
    return (det_flow,)


@app.cell
def ex1_run(det_flow, research_query, workflow_store):
    from typing import Any

    from build_deep_research_agent.deterministic_agent import (
        DeterministicFlowRun,
        deterministic_result_from_store,
        reset_workflow_store,
    )

    reset_workflow_store(workflow_store, research_query.value)

    shared: dict[str, Any] = {
        "memory": [research_query.value],
        "globals_dict": {},
        "func_call": {},
        "workflow_store": workflow_store,
        "execution_history": [],
    }
    det_flow.run(shared)
    if workflow_store.report is None and shared.get("result") is not None:
        workflow_store.report = str(shared["result"])
    det_run = DeterministicFlowRun(
        result=deterministic_result_from_store(workflow_store),
        shared=shared,
    )
    det_run.result
    return


@app.function(hide_code=True)
def ex1_trace(det_run, mo):
    # Runtime trace display — add mo output here in a follow-up cell.
    return


@app.function(hide_code=True)
def ex1_display(det_result, mo):
    # @spec PLAN-DET-011
    # Workflow trace display — add mo output here in a follow-up cell.
    return


@app.cell(hide_code=True)
def ex1b_header(mo):
    mo.md(
        dedent("""
    ## Exercise 1b — Same pipeline, prompt-controlled AgentBot

    **Same three tool bodies** as Exercise 1a — ``plan_research`` / ``search_literature`` / ``summarize_evidence``.

    Here routing is **non-deterministic**: llamabot's LLM **DecideNode** picks the next tool
    after each step. You steer it with a system prompt (`WORKFLOW_AGENTBOT_PROMPT` in
    `prompts.py`), not with PocketFlow edges.

    The graph looks like: **decide → tool → decide → … → respond_to_user**

    Compare the Mermaid diagram to Exercise 1a. Turn **Use live LLM** on before running.
    """)
    )
    return


@app.cell(hide_code=True)
def ex1b_store():
    from build_deep_research_agent.deterministic_agent import (
        DeterministicWorkflowStore as _DeterministicWorkflowStore,
    )

    agentbot_store = _DeterministicWorkflowStore()
    return (agentbot_store,)


@app.cell
def ex1b_agent(agentbot_store, part4, use_live_llm):
    from build_deep_research_agent.deterministic_agent import (
        build_planning_agentbot,
    )

    planning_agent = build_planning_agentbot(
        agentbot_store,
        part4.plan_research,
        part4.search_literature,
        part4.summarize_evidence,
        use_live_llm=use_live_llm.value,
    )
    return (planning_agent,)


@app.cell(hide_code=True)
def ex1b_run(agentbot_store, mo, planning_agent, research_query, use_live_llm):
    from build_deep_research_agent.deterministic_agent import run_planning_agentbot

    mo.stop(
        not use_live_llm.value,
        mo.md("_Turn on **Use live LLM** to run the AgentBot decide node._"),
    )

    agentbot_result = run_planning_agentbot(
        planning_agent,
        agentbot_store,
        research_query.value,
    )

    mo.md(
        dedent(f"""
    ### Exercise 1b — AgentBot trace

    Tool steps recorded: {len(agentbot_result.steps) - 1} (plus done)

    #### Final answer (via respond_to_user)

    {agentbot_result.final_answer[:600]}{"…" if len(agentbot_result.final_answer) > 600 else ""}
    """)
    )
    return


@app.cell(hide_code=True)
def ex2_header(mo):
    mo.md(
        dedent("""
    ## Exercise 2 — Build a ReAct loop

    Implement **`react_step_fn`** in `exercises/part4.py`.

    1. Step 0: call `search_library`.
    2. Step 1: return `final_answer` without another tool call.

    Switch the dropdown to **LLM step_fn** when you want `make_llamabot_react_step_fn` instead.
    """)
    )
    return


@app.cell
def ex2_tools():
    from build_deep_research_agent.workflows import make_fixture_react_tools

    react_tools = make_fixture_react_tools()
    print("Available tools:", list(react_tools))
    return (react_tools,)


@app.function
def run_react_query(tools, step_fn, query, max_steps):
    from build_deep_research_agent.workflows import ReActRunner

    runner = ReActRunner(
        tools=tools,
        step_fn=step_fn,
        max_steps=max_steps,
    )
    return runner.run(query)


@app.cell
def ex2_run_react(
    react_max_steps,
    react_mode,
    react_step_fn,
    react_tools,
    research_query,
):
    # @spec PLAN-REACT-020
    if react_mode.value == "llm":
        from build_deep_research_agent.workflows import make_llamabot_react_step_fn

        step_fn = make_llamabot_react_step_fn()
    else:
        step_fn = react_step_fn

    react_result = run_react_query(
        react_tools,
        step_fn,
        research_query.value,
        int(react_max_steps.value),
    )
    return (react_result,)


@app.cell
def ex2_display(mo, react_result):
    trace_lines: list[str] = []
    for index, react_step in enumerate(react_result.trace, start=1):
        trace_lines.append(
            "\n".join(
                [
                    f"#### Step {index}",
                    f"- **Thought:** {react_step.thought}",
                    f"- **Action:** {react_step.action or '_none_'}",
                    f"- **Action input:** `{react_step.action_input}`",
                    f"- **Observation:** {react_step.observation or '_none_'}",
                ]
            )
        )

    # @spec PLAN-REACT-021
    mo.md(
        dedent(f"""
        ### Exercise 2 — ReAct trace

        Stopped because: `{react_result.stopped_reason}` ({len(react_result.trace)} steps)

        {chr(10).join(trace_lines) or "_empty trace_"}

        #### Final answer

        {react_result.final_answer}
        """)
    )
    return


@app.cell(hide_code=True)
def ex3_header(mo):
    mo.md(
        dedent("""
    ## Exercise 3 — Compare both workflows

    The table below updates when you change the question, step function, or max steps.
    Try setting `react_max_steps` to **1**, or return `[]` from `search_fn`.
    """)
    )
    return


@app.cell
def ex3_compare(det_result, react_result, research_query):
    from build_deep_research_agent.workflows import compare_workflow_results

    comparison = compare_workflow_results(
        research_query.value,
        det_result,
        react_result,
    )
    return (comparison,)


@app.cell
def ex3_comparison_table(comparison, mo, react_result):
    # @spec PLAN-COMP-001
    # @spec PLAN-COMP-002
    # @spec PLAN-COMP-003
    # @spec PLAN-COMP-020
    mo.md(
        dedent(f"""
        ### Side-by-side comparison

        | Metric | Deterministic | ReAct |
        |--------|---------------|-------|
        | Step / trace count | {comparison.deterministic_step_count} | {comparison.react_trace_length} |
        | Output structure | {comparison.deterministic_output_kind} | {comparison.react_output_kind} |
        | Stopped reason | done (FSM) | {react_result.stopped_reason} |

        #### Deterministic answer (excerpt)

        {comparison.deterministic_answer[:400]}{"…" if len(comparison.deterministic_answer) > 400 else ""}

        #### ReAct answer (excerpt)

        {comparison.react_answer[:400]}{"…" if len(comparison.react_answer) > 400 else ""}
        """)
    )
    return


@app.cell
def ex3_challenge(mo):
    run_challenge = mo.ui.run_button(label="Run ReAct with max_steps=1")
    mo.vstack(
        [
            mo.md(
                "_Stretch goal: one-step ReAct loop — inspect the partial trace above._"
            ),
            run_challenge,
        ]
    )
    return (run_challenge,)


@app.cell
def ex3_challenge_run(
    mo,
    react_mode,
    react_step_fn,
    react_tools,
    research_query,
    run_challenge,
):
    mo.stop(
        not run_challenge.value,
        mo.md("_Click **Run ReAct with max_steps=1** to execute the challenge._"),
    )

    if react_mode.value == "llm":
        from build_deep_research_agent.workflows import (
            make_llamabot_react_step_fn as _llm_step_fn,
        )

        _challenge_step_fn = _llm_step_fn()
    else:
        _challenge_step_fn = react_step_fn

    challenge_result = run_react_query(
        react_tools,
        _challenge_step_fn,
        research_query.value,
        1,
    )

    mo.md(
        dedent(f"""
        ### Max-steps challenge (`max_steps=1`)

        Stopped because: `{challenge_result.stopped_reason}`

        Partial answer: {challenge_result.final_answer[:300]}
        """)
    )
    return


@app.cell
def discussion(mo):
    # @spec PLAN-COMP-010
    # @spec PLAN-COMP-011
    mo.md(
        dedent("""
    ### Discussion prompts

    - When does a deterministic workflow beat open-ended ReAct in production?
    - What goes wrong when a ReAct loop has no step limit?
    - How do these workflows reuse prompts, memory, and MCP tools from earlier parts?

    **Teaching note:** the deterministic path still reaches summarize when search
    returns nothing. Edit `search_fn` to return `[]` and watch what `summarize_fn` does.
    """)
    )
    return


if __name__ == "__main__":
    app.run()
