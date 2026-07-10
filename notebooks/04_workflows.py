# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    """Imports available to every cell."""

    from textwrap import dedent

    import marimo as mo
    from llamabot import AgentBot, tool

    from build_deep_research_agent.exercises.solutions import part3
    from build_deep_research_agent.fixtures.loader import load_corpus_papers
    from build_deep_research_agent.llm import get_completion_kwargs, get_model_name


@app.cell(hide_code=True)
def hero():
    mo.md(
        dedent(
            r"""
            <div style="display:flex;align-items:center;gap:1.2rem;background:linear-gradient(120deg,#0f172a,#1e293b);color:#e2e8f0;padding:1.3rem 1.6rem;border-radius:0.6rem;border-left:6px solid #a78bfa;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M30 8 L42 16 L42 32 L30 40 L18 32 L18 16 Z" stroke="#a78bfa" stroke-width="2" fill="none"/>
                                <circle cx="30" cy="24" r="5" fill="#a78bfa"/>
                                <text x="30" y="52" fill="#94a3b8" font-size="7" text-anchor="middle" font-family="monospace">loop</text>
                                <path d="M44 24 Q52 24 52 30 Q52 36 44 36" stroke="#a78bfa" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>
                                <path d="M44 36 L47 33 M44 36 L47 39" stroke="#a78bfa" stroke-width="1.5" fill="none"/>
              </svg>
              <div>
                <div style="font-size:1.5rem;font-weight:700;letter-spacing:-0.01em;line-height:1.15;">Part 4 &middot; Workflows &mdash; the <span style="color:#a78bfa;">AgentBot</span> iterate loop</div>
                <div style="opacity:0.82;margin-top:0.25rem;font-size:0.95rem;">Build a Deep Research Agent &nbsp;&middot;&nbsp; SciPy 2026 &nbsp;&middot;&nbsp; Eric Ma</div>
              </div>
            </div>
            """
        )
    )
    return


@app.cell(hide_code=True)
def intro():
    mo.md(
        dedent(
            """
            Part 3 gave you **tools** (search a corpus, search Zotero). Part 4
            gives you an **agent that uses them** — llamabot's **AgentBot**.

            AgentBot is the star: an LLM with a set of tools that **iterates in a
            loop**. It *thinks* about your question, *calls* a tool, *observes*
            the result, then thinks again — repeating until it has enough to
            answer. You don't script the steps; the LLM decides each one.

            This is the **ReAct pattern** (Reason + Act), and the loop is the
            whole point.
            """
        )
    )
    return


@app.cell(hide_code=True)
def walkthrough():
    # A guided, cell-by-cell walkthrough of Part 4. Click "Start tour" to see
    # how AgentBot iterates.
    from wigglystuff import CellTour

    tour = mo.ui.anywidget(
        CellTour(
            steps=[
                {
                    "cell_name": "intro",
                    "title": "AgentBot = LLM + tools + loop",
                    "description": "Part 4 introduces AgentBot — an LLM with tools that iterates in a loop (think, act, observe, repeat). The loop is the whole point.",
                },
                {
                    "cell_name": "loop_diagram",
                    "title": "The loop",
                    "description": "Each lap: think about the question, call a tool, observe the result, then think again — until the agent has enough to answer.",
                },
                {
                    "cell_name": "tools_setup",
                    "title": "Your tools",
                    "description": "This cell builds the Part 3 docstore and defines search_corpus as a @tool the agent can call.",
                },
                {
                    "cell_name": "ex1_header",
                    "title": "Exercise 1: wire AgentBot",
                    "description": "Give AgentBot the search_corpus tool and let it iterate. Fill in the blanks in the scaffold below.",
                },
                {
                    "cell_name": "ex1_run",
                    "title": "Watch it iterate",
                    "description": "The agent searches the corpus, observes results, then answers. This calls the LLM — give it a few seconds per loop.",
                },
                {
                    "cell_name": "ex2_header",
                    "title": "Exercise 2: inside the loop",
                    "description": "AgentBot ran, but you only saw the final answer. Use agent.display_spans() to see each think/act/observe step.",
                },
                {
                    "cell_name": "ex3_header",
                    "title": "Exercise 3: deterministic vs AgentBot",
                    "description": "When does a fixed workflow (plan, search, summarize) beat an adaptive loop? And vice versa?",
                },
                {
                    "cell_name": "recap",
                    "title": "Recap",
                    "description": "AgentBot = LLM + tools + loop. The LLM decides each step. Next: Part 5 shows specialized agents collaborating.",
                },
            ],
            auto_start=False,
        )
    )
    tour
    return


@app.cell(hide_code=True)
def loop_diagram():
    mo.md(
        dedent(
            """
    ### The loop

    ```mermaid
    graph LR
        Think["🧠 Think"] -->|decide| Act["🔧 Act<br/>(call a tool)"]
        Act -->|result| Observe["👁 Observe"]
        Observe -->|reflect| Think
        Think -->|"enough info"| Answer["💬 Final answer"]
    ```

    Each lap of the loop is one **iteration**. `max_iterations` caps how
    many lapses the agent gets before it must answer.
            """
        )
    )
    return


@app.cell
def tools_setup():
    # Build the Part 3 docstore + define the search_corpus tool that AgentBot will use.
    papers = load_corpus_papers()
    docstore, side_table = part3.build_corpus_docstore(papers)

    @tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested paper corpus."""

        return part3.search_corpus(docstore, side_table, query, limit)

    print(f"docstore ready: {len(papers)} papers")
    return (search_corpus,)


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent(
            """
            ## Exercise 1 — Wire AgentBot with your search tool

            Give AgentBot the `search_corpus` tool from Part 3 and let it loose on
            a question. The agent will iterate: search → observe → decide → answer.

            **Fill in the blanks** in the scaffold below.

            ```python
            agent = AgentBot(
                tools=[_______],               # the search_corpus @tool
                system_prompt=_______,          # tell the agent its job
                model_name=get_model_name(),
                max_iterations=_______,         # cap the loop (e.g. 5)
                **get_completion_kwargs(),
            )
            ```
            """
        )
    )
    return


@app.cell
def ex1_scaffold(search_corpus):
    # Exercise 1 — wire AgentBot with search_corpus.
    # Default below is a working reference; tweak the system_prompt or
    # max_iterations to see how the loop changes.

    agent = AgentBot(
        tools=[search_corpus],
        system_prompt=(
            "You are a research assistant with access to a paper corpus. "
            "FIRST search for relevant papers using search_corpus. "
            "THEN, once you have results, call respond_to_user with a 2-3 sentence "
            "summary grounded in what the tool returned. "
            "You MUST use respond_to_user to deliver your final answer."
        ),
        model_name=get_model_name(),
        max_iterations=5,
        **get_completion_kwargs(),
    )
    return (agent,)


@app.cell
def ex1_run(agent):
    mo.md(
        "**Running AgentBot…** (this calls the LLM + iterates — may take a few seconds)"
    )
    try:
        result = agent("What papers discuss protein structure prediction?")
        mo.md(str(result))
    except Exception as e:
        mo.md(f"**AgentBot error:** {e}")
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent(
            """
            ## Exercise 2 — Observe the loop

            AgentBot ran, but you only saw the final answer. Let's look
            **inside the loop** — each think/act/observe step is captured in
            `agent.spans`.

            **Fill in the blank**: call `agent.display_spans()` (or iterate
            `agent.spans`) to see each iteration.
            """
        )
    )
    return


@app.cell
def ex2_scaffold(agent):
    # Exercise 2 — show the iteration trace.
    # Try agent.display_spans() for a formatted view, or iterate agent.spans.
    try:
        agent.display_spans()
    except Exception as e:  # noqa: BLE001
        print(f"display_spans not available on this llamabot version: {e}")
        print(f"spans count: {len(agent.spans) if hasattr(agent, 'spans') else '?'}")
    return


@app.cell(hide_code=True)
def ex3_header():
    mo.md(
        dedent(
            """
            ## Exercise 3 — Deterministic vs AgentBot

            Two ways to build a research workflow:

            | | **Deterministic** (PocketFlow) | **AgentBot** (LLM-driven loop) |
            |---|---|---|
            | **Who decides?** | You (fixed plan→search→summarize) | The LLM (each iteration) |
            | **Flexibility** | Rigid — same steps every time | Adaptive — skips/loops as needed |
            | **Predictability** | High — you know the path | Lower — the LLM chooses |
            | **Cost** | One LLM call per step | Multiple LLM calls per loop |
            | **Best for** | Pipelines you run repeatedly | Open-ended exploration |

            **When does AgentBot win?** When the path isn't known in advance —
            exploratory research, ad-hoc Q&A, or when the agent might need to
            search, see nothing relevant, and rephrase.

            **When does deterministic win?** When the steps are known and
            repeatable — a nightly literature scan, a fixed report pipeline.
            """
        )
    )
    return


@app.cell(hide_code=True)
def recap():
    mo.md(
        dedent(
            """
            ## Recap

            - **AgentBot** = LLM + tools + iterate loop. The LLM decides each
              step (which tool, when to stop).
            - The **loop** (think → act → observe → repeat) is the core idea —
              the agent isn't a single call, it's a conversation with its tools.
            - `max_iterations` caps the loop; `system_prompt` shapes behavior.
            - **Deterministic workflows** (fixed steps) win for repeatable
              pipelines; **AgentBot** wins for adaptive exploration.

            **Next:** Part 5 shows specialized agents (Searcher + Synthesizer)
            collaborating via AgentBot.
            """
        )
    )
    return


if __name__ == "__main__":
    app.run()
