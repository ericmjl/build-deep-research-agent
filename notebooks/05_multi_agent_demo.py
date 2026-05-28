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


@app.cell(hide_code=True)
def intro():
    # @spec MULTI-AGENT-030
    import marimo as mo

    mo.md(
        """
        # Part 5: Multi-agent literature review demo

        We started with a simple idea: a research agent is an LLM plus context.
        By now you have added memory, tools, planning, and specialized roles on top.

        This notebook is the capstone. Two llamabot `AgentBot`s cooperate on a
        literature review: one searches, one synthesizes. You will see the full
        stack run end to end.
        """
    )
    return (mo,)


@app.cell(hide_code=True)
def tutorial_arc(mo):
    mo.md("""
    ## What we stacked, part by part

    Here is the arc we followed. Each part added one capability to the same
    mental model.

    | Part | Capability | What you added |
    |------|------------|----------------|
    | 1 | **Prompt / in-context learning** | System prompts and citation metadata in context |
    | 2 | **Memory** | Chat history and citation snippets that persist across turns |
    | 3 | **Tools (MCP)** | Zotero search via MCP so the agent can fetch fresh bibliographic data |
    | 4 | **Planning** | Deterministic workflows and ReAct loops for orchestration |
    | 5 | **Multi-agent** | **This notebook** — Searcher and Synthesizer as cooperating agents |

    Parts 1 through 4 gave you the ingredients. Part 5 shows how specialized
    agents divide the work.
    """)
    return


@app.cell(hide_code=True)
def this_demo(mo):
    mo.md("""
    ## What runs when you click **Run**

    The demo wires three library pieces together:

    1. **Searcher `AgentBot`** calls MCP (our tutorial FastMCP server) or the
       bundled fixture library, then returns structured `CitationRecord` evidence.
    2. **Synthesizer `AgentBot`** reads that evidence in context and writes a
       grounded markdown report via `respond_to_user`.
    3. **`ResearchOrchestrator`** runs a simple synchronous pipeline:
       `query → Searcher → evidence → Synthesizer → report`.

    I kept the orchestration deliberately boring on purpose. In a classroom
    demo, clarity beats cleverness.
    """)
    return


@app.cell(hide_code=True)
def how_to_use(mo):
    mo.md("""
    ## Play with the controls below

    - **Searcher mode** — fixture library for offline demos, or tutorial Zotero MCP when you want live search.
    - **Failure presets** — try empty evidence (hallucination probe) or oversized context (truncation stress test).
    - **Discussion cell** at the bottom — mitigations, expansions, and Q&A.

    A research agent is an LLM with the right prompts, state, tools, workflows,
    and sometimes specialized roles working together. You built each layer today.
    """)
    return


@app.cell
def controls(mo):
    # @spec MULTI-AGENT-020
    search_mode = mo.ui.dropdown(
        options={
            "fixture": "Fixture library (offline)",
            "mcp": "Tutorial Zotero MCP (live)",
        },
        value="fixture",
        label="Searcher mode",
    )
    query_input = mo.ui.text(
        value="Bayesian workflow applied research",
        label="Research question",
        full_width=True,
    )
    failure_preset = mo.ui.dropdown(
        options={
            "none": "Normal run",
            "empty": "Empty evidence (hallucination probe)",
            "oversized": "Oversized context",
        },
        value="none",
        label="Failure-mode preset",
    )
    run_button = mo.ui.run_button(label="Run multi-agent pipeline")
    mo.vstack([search_mode, query_input, failure_preset, run_button])
    return failure_preset, query_input, run_button, search_mode


@app.cell
def run_pipeline(failure_preset, mo, query_input, run_button, search_mode):
    mo.stop(not run_button.value, mo.md("_Click **Run** to execute the pipeline._"))

    from build_deep_research_agent.agents import (
        ResearchOrchestrator,
        SearcherAgent,
        SynthesizerAgent,
        oversized_evidence,
    )
    from build_deep_research_agent.fixtures.search import search_fixture_library

    orchestrator = ResearchOrchestrator(
        searcher=SearcherAgent(mode=search_mode.value),
        synthesizer=SynthesizerAgent(),
    )

    try:
        if failure_preset.value == "empty":
            # @spec MULTI-FAIL-001
            evidence = []
            report_md = orchestrator.synthesizer.run(query_input.value, evidence)
            result = {
                "query": query_input.value,
                "evidence": evidence,
                "report_markdown": report_md,
            }
        elif failure_preset.value == "oversized":
            # @spec MULTI-FAIL-002
            seed = search_fixture_library("Bayesian", limit=1)
            evidence = oversized_evidence(seed, repeat=10)
            report_md = orchestrator.synthesizer.run(query_input.value, evidence)
            result = {
                "query": query_input.value,
                "evidence": evidence,
                "report_markdown": report_md,
            }
        else:
            # @spec MULTI-AGENT-021
            report = orchestrator.run(query_input.value, limit=5)
            result = report.model_dump()
    finally:
        orchestrator.close()

    mo.md(
        f"""
        ## Evidence ({len(result["evidence"])} items)

        {chr(10).join(f"- {item['title']}" for item in result["evidence"]) or "_none_"}

        ## Report

        {result["report_markdown"]}
        """
    )
    return


@app.cell
def discussion(mo):
    # @spec MULTI-FAIL-010
    # @spec MULTI-DISC-001
    # @spec MULTI-DISC-002
    # @spec MULTI-DISC-003
    # @spec MULTI-DISC-010
    # @spec MULTI-DISC-011
    # @spec TUT-MARIMO-011
    mo.md("""
    ### Discussion prompts

    - When does the Synthesizer hallucinate without Searcher evidence?
    - How does MCP tool access change what the Searcher AgentBot can do?
    - Why build specialized agents instead of one general coding assistant?

    **Mitigations** for failure modes: max ReAct steps, context truncation,
    structured outputs, and human review before trusting synthesis.

    **Expansions** (discussion only — not implemented in v1): web search,
    PDF parsing, and when coding assistants replace custom research agents.
    """)
    return


if __name__ == "__main__":
    app.run()
