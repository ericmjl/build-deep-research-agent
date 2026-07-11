# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    from textwrap import dedent

    import marimo as mo
    from llamabot import tool  # noqa: F401

    from build_deep_research_agent.agents import (  # noqa: F401
        ResearchOrchestrator,
        SearcherAgent,
        SynthesizerAgent,
    )
    from build_deep_research_agent.exercises.solutions import (  # noqa: F401
        part4,
    )
    from build_deep_research_agent.fixtures.loader import load_corpus_papers


@app.cell(hide_code=True)
def hero():
    mo.md(
        dedent(
            """
            <div style="display:flex;align-items:center;gap:1.2rem;background:linear-gradient(120deg,#0f172a,#1e293b);color:#e2e8f0;padding:1.3rem 1.6rem;border-radius:0.6rem;border-left:6px solid #34d399;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="8" y="10" width="18" height="18" rx="3" stroke="#34d399" stroke-width="2" fill="none"/>
                <rect x="34" y="10" width="18" height="18" rx="3" stroke="#34d399" stroke-width="2" fill="none"/>
                <rect x="8" y="34" width="18" height="18" rx="3" stroke="#60a5fa" stroke-width="2" fill="none"/>
                <rect x="34" y="34" width="18" height="18" rx="3" stroke="#60a5fa" stroke-width="2" fill="none"/>
                <path d="M26 19 L34 19" stroke="#34d399" stroke-width="1.5" stroke-dasharray="2 2"/>
                <path d="M17 28 L17 34" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="2 2"/>
                <path d="M43 28 L43 34" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="2 2"/>
                <text x="30" y="56" fill="#94a3b8" font-size="6" text-anchor="middle" font-family="monospace">build | reuse</text>
              </svg>
              <div>
                <div style="font-size:1.5rem;font-weight:700;letter-spacing:-0.01em;line-height:1.15;">Bonus &middot; Architecture choices &mdash; <span style="color:#34d399;">when to build, when to reuse</span></div>
                <div style="opacity:0.82;margin-top:0.25rem;font-size:0.95rem;">Build a Deep Research Agent &nbsp;&middot;&nbsp; SciPy 2026 &nbsp;&middot;&nbsp; Eric Ma</div>
              </div>
            </div>

            You built a research agent from scratch: prompts, memory, tools,
            planning, and multi-agent orchestration. That is five layers of
            custom infrastructure.

            This bonus notebook asks two questions that matter in the real world:

            1. **Does specialization help?** Compare a single generalist AgentBot
               against a specialist pipeline (SearcherAgent + SynthesizerAgent).
            2. **Should you build at all?** Compare your custom harness against
               opencode — a production agent tool — plugged into the MCP server
               you built in Part 3.

            By the end you will have a framework for deciding: **build, reuse, or
            specialize?**
            """
        )
    )
    return


@app.cell(hide_code=True)
def walkthrough():
    # A guided walkthrough of the bonus notebook. Click "Start tour" to get oriented.
    from wigglystuff import CellTour

    tour = mo.ui.anywidget(
        CellTour(
            steps=[
                {
                    "cell_name": "hero",
                    "title": "Bonus — Architecture choices",
                    "description": "This bonus notebook has one job: help you decide when to build a custom agent, when to specialize, and when to reach for a production tool. You will run the same research question through three architectures and compare.",
                },
                {
                    "cell_name": "setup_question",
                    "title": "The benchmark question",
                    "description": "This is the question all three architectures will answer. It spans two domains — no single search query covers both, which means the agent has to adapt.",
                },
                {
                    "cell_name": "contrast1_intro",
                    "title": "Contrast 1: Generalist vs. Specialist",
                    "description": "Background section. You are about to see two ways to answer the question: one AgentBot that does everything, and a two-agent pipeline where each agent has a focused role.",
                },
                {
                    "cell_name": "ex1_header",
                    "title": "Exercise 1: wire the specialists",
                    "description": "Hands-on section. You fill in blanks to connect two specialized agents — one that searches, one that synthesizes — into a single pipeline. The pieces are from Part 5.",
                },
                {
                    "cell_name": "contrast1_discussion",
                    "title": "Did specialization help?",
                    "description": "Reflection section. Look at the two answers above: the generalist ran one loop, the specialist ran two. Did the extra cost buy better evidence or a clearer report?",
                },
                {
                    "cell_name": "contrast2_intro",
                    "title": "Contrast 2: Custom harness vs. opencode",
                    "description": "Now a different question: you just built a custom agent harness in Python. But opencode already has tool calling, streaming, and MCP support built in. When is each the right choice?",
                },
                {
                    "cell_name": "architecture_diagram",
                    "title": "Two paths, same destination",
                    "description": "Both architectures reach the same LanceDB docstore. The difference is everything in between — who owns the loop, the prompts, the tool selection.",
                },
                {
                    "cell_name": "ex2_header",
                    "title": "Exercise 2: opencode + MCP",
                    "description": "Try-it-yourself section. You start the MCP server from Part 3, point opencode at it, and ask the same question. Then compare the experience to your custom harness.",
                },
                {
                    "cell_name": "contrast2_discussion",
                    "title": "Build vs. reuse",
                    "description": "Reflection section. Three architectures ran the same question — your generalist, the specialist pipeline, and opencode. What did each one cost, and what did each one get right?",
                },
                {
                    "cell_name": "recap",
                    "title": "Recap",
                    "description": "Wrap-up. You now have a decision framework for any agent project: start simple, specialize when quality demands it, and reuse production tools when speed matters.",
                },
            ],
            auto_start=False,
        )
    )
    tour
    return


@app.cell(hide_code=True)
def setup_corpus():
    # Reconnect to the Part 3 docstore and define search_corpus.
    papers = load_corpus_papers()

    from build_deep_research_agent.exercises.solutions import part3

    docstore, side_table = part3.connect_corpus_docstore(papers)

    @tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested paper corpus."""
        return part3.search_corpus(docstore, side_table, query, limit)

    mo.md(
        dedent(f"""
        **Corpus ready** — {len(papers)} papers, docstore reconnected from Part 3.

        We will use the same `search_corpus` tool for all comparisons.
        """)
    )
    return (search_corpus,)


@app.cell(hide_code=True)
def setup_question():
    bonus_question = (
        "What computational methods appear across both astrophysics "
        "and computational biology in this corpus?"
    )
    mo.md(
        dedent(f"""
        ## The benchmark question

        > "{bonus_question}"

        This is the same multi-faceted question from Part 4 Exercise 4.
        No single search query covers both domains — it rewards an agent
        that can **search, observe, then search again** from a different
        angle.

        We will ask it of three architectures and compare.
        """)
    )
    return (bonus_question,)


@app.cell(hide_code=True)
def contrast1_intro():
    mo.md(
        dedent("""
        ## Contrast 1 — Generalist vs. Specialist

        **Generalist** (Part 4): one AgentBot with `search_corpus`. It decides
        when to search, what to search for, and when to stop — all in one loop.

        **Specialist** (Part 5): two agents in a pipeline. A **SearcherAgent**
        focuses on finding evidence (multiple queries, tool calls). A
        **SynthesizerAgent** focuses on writing the report from the evidence.
        Each has its own system prompt, its own tools, its own loop.

        | | Generalist | Specialist |
        |---|---|---|
        | **Agents** | 1 AgentBot | Searcher + Synthesizer |
        | **System prompts** | 1 (do everything) | 2 (search well / write well) |
        | **LLM calls** | 1 loop, ~5 iterations | 2 loops, ~8 + ~4 iterations |
        | **Strength** | Simple, cheap | Focused, higher quality on hard questions |
        | **Weakness** | Jack of all trades | More moving parts, higher cost |
        """)
    )
    return


@app.cell(hide_code=True)
def run_generalist(bonus_question, search_corpus):
    # Approach A: single generalist AgentBot (recap from Part 4).
    generalist_agent = part4.build_agent(search_corpus)
    generalist_result = generalist_agent(bonus_question)

    mo.callout(
        mo.md(
            f"**Generalist AgentBot**\n\n"
            f"Iterations: {part4.count_decisions(generalist_agent)}\n\n"
            f"{generalist_result}"
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent("""
        ### Exercise 1 — Wire the specialist pipeline

        The specialist approach splits the work: a **SearcherAgent** that
        searches aggressively, and a **SynthesizerAgent** that writes the
        report from the evidence. A **ResearchOrchestrator** wires them
        into a synchronous pipeline.

        Implement **`run_specialist_pipeline`** in the scaffold cell below.
        Fill in the blanks — each has a comment above it.

        ```python
        def run_specialist_pipeline(query):
            # Create a SearcherAgent (fixture mode, max 8 iterations).
            searcher = _________(mode="fixture", max_iterations=8)
            # Create a SynthesizerAgent (max 4 iterations).
            synthesizer = _________(max_iterations=4)
            # Wire them into a ResearchOrchestrator.
            orchestrator = _________(searcher=_________, synthesizer=_________)
            # Run the pipeline and close the agents.
            report = orchestrator._______(query)
            orchestrator.close()
            return report
        ```
        """)
    )
    return


@app.cell
def ex1_scaffold(bonus_question):
    # Exercise 1 — run_specialist_pipeline (wire specialist agents).
    # Default: delegates to the reference (ResearchOrchestrator).
    # Override to wire SearcherAgent + SynthesizerAgent yourself.

    def run_specialist_pipeline(query):
        # put your implementation here.
        pass

    # Once you are done, delete the reference block below and call your own:
    #   specialist_result = run_specialist_pipeline(bonus_question)
    orch = ResearchOrchestrator()
    ref_report = orch.run(bonus_question)
    orch.close()
    specialist_result = ref_report.report_markdown
    return (specialist_result,)


@app.cell(hide_code=True)
def run_specialist(specialist_result):
    mo.callout(
        mo.md(
            f"**Specialist pipeline (Searcher + Synthesizer)**\n\n{specialist_result}"
        ),
        kind="success",
    )
    return


@app.cell(hide_code=True)
def contrast1_discussion():
    mo.md(
        dedent("""
        ### Discussion — did specialization help?

        Compare the two answers above. Consider:

        - **Quality** — did the specialist pipeline find more relevant evidence?
          Did the synthesizer's report cite specific papers?
        - **Cost** — the specialist ran two LLM loops (search + synthesize).
          Was the extra cost worth it?
        - **Control** — the specialist lets you tune the searcher and synthesizer
          independently (different prompts, different `max_iterations`). When
          does that matter?

        **Key insight:** specialization trades simplicity for focus. On easy
        questions the generalist is fine. On hard questions — multi-domain,
        multi-step — the specialist's focused prompts earn their cost.
        """)
    )
    return


@app.cell(hide_code=True)
def contrast2_intro():
    mo.md(
        dedent("""
        ## Contrast 2 — Custom harness vs. opencode + MCP

        You built a research agent from scratch: llamabot AgentBot, PocketFlow,
        LanceDB docstore, custom `@tool` functions, system prompts, iteration
        loops. That is hundreds of lines of Python.

        But **opencode** (or Claude Code, Cursor, etc.) already has all of that:
        an agent loop, tool calling, streaming, error handling, persistence.
        And it speaks **MCP** — the same protocol you used in Part 3.

        The question: **why build your own harness when you can plug a production
        tool into your MCP server?**
        """)
    )
    return


@app.cell(hide_code=True)
def architecture_diagram():
    custom_diagram = dedent(
        """
        graph TB
            CH_Q[/"Research question"/]
            CH_AB["AgentBot<br/>(llamabot)"]
            CH_T["search_corpus<br/>@tool"]
            CH_DS[("LanceDB<br/>docstore")]
            CH_Q --> CH_AB --> CH_T --> CH_DS
        """
    )

    opencode_diagram = dedent(
        """
        graph TB
            OC_Q[/"Research question"/]
            OC["opencode<br/>(production agent)"]
            OC_MCP["MCP server<br/>(FastMCP)"]
            OC_DS[("LanceDB<br/>docstore")]
            OC_Q --> OC --> OC_MCP --> OC_DS
        """
    )

    mo.md(
        dedent("""
        ### Two paths to the same destination

        Both paths end at the same LanceDB docstore. The difference is
        **what sits between the question and the data**:

        - **Custom harness** (left): you control every layer — prompts, tools,
          loop logic, iteration caps. You also maintain every layer.
        - **opencode + MCP** (right): you write zero agent code. opencode handles
          the loop, tool calling, streaming, and UI. You only maintain the MCP
          server that exposes your domain-specific tools.
        """)
    )

    mo.hstack(
        [
            mo.vstack(
                [
                    mo.md("**Custom harness (what you built)**"),
                    mo.mermaid(custom_diagram),
                ]
            ),
            mo.vstack(
                [
                    mo.md("**opencode + MCP**"),
                    mo.mermaid(opencode_diagram),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent("""
        ### Exercise 2 — Connect opencode to your MCP server

        In Part 3 you built a FastMCP server that exposes `search_corpus`.
        Now connect **opencode** to it and ask the same research question.

        **Step 1:** Start the MCP server (the cell below does this).

        **Step 2:** Add the server to your opencode config:

        ```json
        {{
            "mcp": {{
                "corpus-research": {{
                    "type": "stdio",
                    "command": "uv",
                    "args": ["run", "scripts/serve_corpus_mcp.py"]
                }}
            }}
        }}
        ```

        **Step 3:** Open a terminal and run:

        ```bash
        opencode "What computational methods appear across both astrophysics
        and computational biology in this corpus?"
        ```

        **Step 4:** Compare opencode's answer to the custom harness answers above.
        """)
    )
    return


@app.cell(hide_code=True)
def start_mcp_server():
    import subprocess
    import sys

    mo.md(
        dedent("""
        **MCP server launcher**

        The cell below starts the corpus MCP server in the background.
        Once it prints `MCP server running`, open a terminal and use opencode
        (or any MCP-compatible client) to connect.
        """)
    )

    # Start the MCP server as a subprocess (participants can also do this
    # manually in a terminal).
    mcp_process = subprocess.Popen(
        [sys.executable, "-m", "build_deep_research_agent.mcp.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    mo.md(
        dedent(
            """
        **MCP server started** (PID: {pid}).

        To use it from opencode, add this to your `opencode.json`:

        ```json
        {{
            "mcp": {{
                "corpus-research": {{
                    "type": "stdio",
                    "command": "{python}",
                    "args": ["-m", "build_deep_research_agent.mcp.server"]
                }}
            }}
        }}
        ```

        Then run: `opencode "{question}"`

        > **Note:** Kill the server when done: `kill {pid}`
        """.format(
                pid=mcp_process.pid,
                python=sys.executable,
                question="What computational methods appear across both astrophysics and computational biology?",
            )
        )
    )
    return


@app.cell(hide_code=True)
def contrast2_discussion():
    mo.md(
        dedent("""
        ### Discussion — build vs. reuse

        You just saw three approaches to the same research question:

        | Approach | Lines of code | Control | Maintenance |
        |----------|--------------|---------|-------------|
        | **Single AgentBot** | ~20 (your scaffold) | Full | You own the loop |
        | **Specialist pipeline** | ~60 (orchestrator + 2 agents) | Full, per-agent | More moving parts |
        | **opencode + MCP** | ~10 (MCP server config) | Minimal (opencode owns the loop) | Just the MCP server |

        **When to build your own harness:**

        - You need **domain-specific control** over the agent loop (custom
          stopping criteria, structured outputs, multi-agent coordination).
        - You are **teaching** — understanding every layer is the point.
        - You need the agent to run **inside your application** (embedded, not
          as a CLI tool).

        **When to use opencode (or similar):**

        - You need a **working tool today**, not a research project.
        - Your tools are already **MCP-compatible** — opencode just connects.
        - You want **streaming, persistence, error handling** without building them.
        - Your users are **developers** who already use agent tools.

        **The crossover:** most real projects start with opencode (or Claude
        Code, Cursor) for speed, then build a custom harness when they hit a
        limitation the production tool can't solve. Knowing both paths — which
        you now do — is the real skill.
        """)
    )
    return


@app.cell(hide_code=True)
def recap():
    mo.md(
        dedent("""
        ## Recap

        ### Three architectures, one question

        - **Generalist AgentBot** — one LLM, one tool, one loop. Simple and
          cheap. Good for easy questions.
        - **Specialist pipeline** — SearcherAgent + SynthesizerAgent in a
          synchronous orchestrator. Higher cost, focused quality. Good for
          hard, multi-domain questions.
        - **opencode + MCP** — zero custom agent code. Production-ready loop,
          streaming, error handling. Good when you need a working tool fast.

        ### The decision framework

        1. **Start with the simplest thing that works** — a single AgentBot.
        2. **Specialize when quality demands it** — split into focused agents
           with their own prompts and tools.
        3. **Reuse production tools when speed matters** — expose your tools
           via MCP and let opencode (or similar) drive the loop.

        The infrastructure you built this tutorial — prompts, memory, tools,
        MCP, workflows, multi-agent — is the vocabulary for making that
        decision. Whether you build or reuse, you now know what each layer
        does and why it exists.
        """)
    )
    return


if __name__ == "__main__":
    app.run()
