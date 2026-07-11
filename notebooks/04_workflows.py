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
    """Imports available to every cell."""

    from textwrap import dedent

    import marimo as mo
    from llamabot import AgentBot, tool

    from build_deep_research_agent.exercises.solutions import part3
    from build_deep_research_agent.fixtures.loader import load_corpus_papers
    from build_deep_research_agent.llm import (
        get_completion_kwargs,
        get_model_name,
    )


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
                    "description": "This cell reconnects to the Part 3 docstore and defines search_corpus as a @tool the agent can call.",
                },
                {
                    "cell_name": "ex1_header",
                    "title": "Exercise 1: wire AgentBot",
                    "description": "Implement build_agent — give AgentBot the search_corpus tool and let it iterate. Fill in the blanks in the scaffold below.",
                },
                {
                    "cell_name": "ex1_run",
                    "title": "Watch it iterate",
                    "description": "The agent searches the corpus, observes results, then answers. This calls the LLM — give it a few seconds per loop.",
                },
                {
                    "cell_name": "ex2_header",
                    "title": "Exercise 2: inside the loop",
                    "description": "AgentBot ran, but you only saw the final answer. Use agent.spans to see each think/act/observe step.",
                },
                {
                    "cell_name": "ex3_header",
                    "title": "Exercise 3: deterministic vs AgentBot",
                    "description": "Implement deterministic_pipeline (one search, one summary — no loop) and count_decisions. Compare cost and answer quality to AgentBot.",
                },
                {
                    "cell_name": "ex4_header",
                    "title": "Exercise 4: when the loop matters",
                    "description": "Run both approaches on a multi-faceted question. You already implemented build_agent in Exercise 1 and deterministic_pipeline in Exercise 3.",
                },
                {
                    "cell_name": "ex5_header",
                    "title": "Exercise 5: the cost/quality dial",
                    "description": "Tune max_iterations from 1 (starved, approximately deterministic) to 5+ (fully agentic). This is the primary control knob for cost vs. adaptiveness.",
                },
                {
                    "cell_name": "recap",
                    "title": "Recap",
                    "description": "AgentBot = LLM + tools + loop. max_iterations is the dial between deterministic and agentic. Next: Part 5 shows specialized agents collaborating.",
                },
            ],
            auto_start=False,
        )
    )
    tour
    return


@app.cell(hide_code=True)
def loop_diagram():
    _loop_graph = dedent(
        """
        graph LR
            Think["🧠 Think"] -->|decide| Act["🔧 Act<br/>(call a tool)"]
            Act -->|result| Observe["👁 Observe"]
            Observe -->|reflect| Think
            Think -->|"enough info"| Answer["💬 Final answer"]
        """
    )
    mo.md(
        f"""
        ### The loop

        {mo.mermaid(_loop_graph)}

        Each lap of the loop is one **iteration**. `max_iterations` caps how
        many laps the agent gets before it must answer.
        """
    )
    return


@app.cell(hide_code=True)
def tools_setup():
    # Reuse the docstore from Part 3 (or build if not found) + define search_corpus.
    papers = load_corpus_papers()
    docstore, side_table = part3.connect_corpus_docstore(papers)

    @tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested paper corpus."""

        return part3.search_corpus(docstore, side_table, query, limit)

    print(
        f"docstore ready: {len(papers)} papers ({len(docstore.existing_records)} chunks indexed)"
    )
    return (search_corpus,)


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent(
            """
            ## Exercise 1 — Wire AgentBot with your search tool

            Give AgentBot the `search_corpus` tool and let it loose on a
            question. The agent will iterate: search, observe, decide, answer.

            Implement **`build_agent`** in the scaffold cell below.
            Every blank has a comment above it explaining what goes there.

            ```python
            def build_agent(search_tool):
                # Create an AgentBot with the search tool and a system prompt.
                return _______(
                    # Wrap the search tool in a list.
                    tools=[_______],
                    # Tell the agent to search first, then call respond_to_user
                    # with a 2-3 sentence summary grounded in the results.
                    system_prompt=_______,
                    # Get the model name from the tutorial config.
                    model_name=_______(),
                    # Cap the iterate loop (e.g. 5 laps).
                    max_iterations=_______,
                    # Pass through API kwargs (api_base, api_key, ...).
                    **_______(),
                )
            ```
            """
        )
    )
    return


@app.cell
def ex1_scaffold(search_corpus):
    from build_deep_research_agent.exercises.solutions import part4

    # Exercise 1 — build_agent (wire AgentBot with the search tool).
    # Default: delegates to the reference (part4.build_agent).
    # Override to wire AgentBot yourself (see the skeleton in the cell above).

    def build_agent(search_tool):
        # put your implementation here.
        pass

    # Once you are done, delete `part4.` from the line below, keeping only build_agent
    agent = part4.build_agent(search_corpus)
    return agent, part4


@app.cell(hide_code=True)
def ex1_run(agent):
    # This calls the LLM + iterates — may take a few seconds.
    try:
        result = agent("What papers discuss protein structure prediction?")
        output = mo.md(str(result))
    except Exception as e:
        output = mo.md(f"**AgentBot error:** {e}")
    output
    return (output,)


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent(
            """
            ## Exercise 2 — Observe the loop

            AgentBot ran, but you only saw the final answer. Where did the
            think → act → observe steps go? They are captured in
            **`agent.spans`** — a list of records, one per loop step.

            Each span records:

            - **`operation_name`** — what kind of step this was (e.g.
              `"decision"` when the model chose a tool or decided to answer)
            - **`iteration`** — which lap of the loop (1, 2, 3, ...)
            - **`chosen_tool`** — the tool the model selected, or
              `respond_to_user` when it decided it had enough to answer

            Run the cell below and inspect `agent.spans`. How many
            iterations did the loop run? Which tool was called?
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex2_scaffold(agent):
    # Exercise 2 — comment out the line below and note what you observe.
    agent.spans
    return


@app.cell
def _():
    # Put the textbox for recording observations here, it should save to some location that a student won't lose if they refresh the notebook or load it again.
    return


@app.cell(hide_code=True)
def ex3_header():
    mo.md(
        dedent(
            """
            ## Exercise 3 — Deterministic pipeline vs. AgentBot

            AgentBot iterates: search → observe → decide → maybe search
            again. But do you always *need* that? What if you just searched
            once and summarized?

            You already met `SimpleBot` in Part 2 (it is what `make_bot`
            wraps internally). It makes a **single LLM call** — no tools,
            no loop. That simplicity is exactly the contrast: AgentBot
            *decides* what to do next; SimpleBot just answers once.

            A **deterministic pipeline** runs fixed steps — no loop, no LLM
            deciding what to do next:

            ```python
            def deterministic_pipeline(search_tool, query):
                # Call the search tool to retrieve papers (no re-phrasing).
                hits = _______(query)

                # Build a SimpleBot summarizer.
                # Tell it to summarize the search results in 2-3 sentences
                # citing paper titles where relevant.
                summarizer = SimpleBot(
                    system_prompt=_______,
                    model_name=get_model_name(),
                    **get_completion_kwargs(),
                )

                # Serialize the search hits to JSON so the bot can read them.
                # Send the prompt and return the .content attribute.
                return summarizer(
                    f"Summarize: {_______._______(hits)}"
                )._______
            ```

            Implement it, then compare its answer to the AgentBot from
            Exercise 1 on the **same question**. Which took more LLM calls?
            Which answer is richer?
            """
        )
    )
    return


@app.cell
def ex3_scaffold():
    # Exercise 3 — fixed search → summarize pipeline (no loop).
    # @spec PLAN-COMP-001
    # @spec PLAN-COMP-002
    # @spec PLAN-COMP-003
    # Replace the body to implement deterministic_pipeline yourself.

    def deterministic_pipeline(search_tool, query):
        # put your implementation here.
        pass

    return


@app.cell(hide_code=True)
def ex3_run_det(part4, search_corpus):
    # Once you are done, delete `part4.` from the line below, keeping only deterministic_pipeline
    ex3_question = "What papers discuss protein structure prediction?"
    det_answer = part4.deterministic_pipeline(search_corpus, ex3_question)
    return (det_answer,)


@app.cell(hide_code=True)
def ex3_iterations_header():
    mo.md(
        dedent(
            """
            ### How many times did each approach call the LLM?

            The deterministic pipeline made **2 LLM calls** (one search, one
            summary). How many did AgentBot make? Each span in `agent.spans`
            records one step of the loop — a `"decision"` span marks each
            time the LLM chose a tool or decided to answer.

            Implement **`count_decisions`** in the scaffold cell below.
            Fill in the blanks:

            ```python
            def count_decisions(agent):
                # Iterate over the agent's recorded spans.
                # Each span has an `.operation_name` attribute.
                # Keep only those whose operation_name is "decision".
                # Return the count.
                return len(
                    [s for s in agent._______ if s._______ == "decision"]
                )
            ```
            """
        )
    )
    return


@app.cell
def ex3_iterations_scaffold(agent, part4):
    # Exercise 3 — count_decisions (filter agent spans for decision steps).
    # Default: delegates to the reference (part4.count_decisions).
    # Override to filter agent.spans yourself.

    def count_decisions(agent):
        # put your implementation here.
        pass

    # Once you are done, delete `part4.` from the line below, keeping only count_decisions
    agent_iterations = part4.count_decisions(agent)
    return (agent_iterations,)


@app.cell(hide_code=True)
def ex3_comparison(agent_iterations, det_answer, output):
    ex3_comparison = mo.vstack(
        [
            mo.callout(
                mo.md(
                    dedent(f"""
            **Deterministic pipeline** (2 LLM calls)

            {det_answer}
            """)
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    dedent(f"""
            **AgentBot** ({agent_iterations} iteration(s))

            {output}
            """)
                ),
                kind="info",
            ),
            mo.md(
                "The deterministic pipeline is cheaper and faster. "
                "But it searches exactly once — it cannot reformulate or dig deeper. "
                "That trade-off is the point."
            ),
        ]
    )
    ex3_comparison
    return


@app.cell(hide_code=True)
def ex4_header():
    # @spec PLAN-COMP-010
    mo.md(
        dedent(
            """
            ## Exercise 4 — When the loop matters

            The deterministic pipeline searched **once** and summarized. That works
            when the question maps cleanly to a single query. But what about a
            question that spans **multiple topics**?

            > "What computational methods appear across both astrophysics and
            > computational biology in this corpus?"

            No single search query covers both domains well. The deterministic
            pipeline must pick one phrasing and hope. AgentBot can **search,
            observe, then search again** from a different angle — adapting its
            strategy based on what it found.

            Run both approaches on this harder question. You already implemented
            `build_agent` in Exercise 1 and `deterministic_pipeline` in Exercise 3
            — the scaffold cell calls both.

            **Discussion:** When would you *choose* the deterministic pipeline
            despite its limitations? (Hint: cost, latency, reproducibility.)
            """
        )
    )
    return


@app.cell
def ex4_scaffold(part4, search_corpus):
    # Exercise 4 — run both approaches on a multi-faceted question.
    # build_agent was implemented in Exercise 1.
    # deterministic_pipeline was implemented in Exercise 3.
    # Once you are done, delete `part4.` from both lines below,
    # keeping only the function names.
    ex4_question = (
        "What computational methods appear across both astrophysics "
        "and computational biology in this corpus?"
    )
    ex4_det = part4.deterministic_pipeline(search_corpus, ex4_question)
    ex4_agent = part4.build_agent(search_corpus)
    ex4_agent_result = ex4_agent(ex4_question)
    return ex4_agent, ex4_agent_result, ex4_det, ex4_question


@app.cell(hide_code=True)
def ex4_iterations_header():
    mo.md(
        dedent(
            """
            ### How many iterations did the agent use?

            Use the same **`count_decisions`** you implemented in Exercise 3
            to count the decision steps from `ex4_agent.spans`:

            ```python
            ex4_agent_iterations = count_decisions(ex4_agent)
            ```
            """
        )
    )
    return


@app.cell
def ex4_iterations_scaffold(ex4_agent, part4):
    # Exercise 4 — count the agent's decision steps on the multi-faceted question.
    # count_decisions was implemented in Exercise 3.
    # Once you are done, delete `part4.` from the line below, keeping only count_decisions
    ex4_agent_iterations = part4.count_decisions(ex4_agent)
    return (ex4_agent_iterations,)


@app.cell(hide_code=True)
def ex4_comparison(ex4_agent_iterations, ex4_agent_result, ex4_det):
    ex4_comparison = mo.vstack(
        [
            mo.callout(
                mo.md(f"**Deterministic pipeline** (2 LLM calls)\n\n{ex4_det}"),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    f"**AgentBot** ({ex4_agent_iterations} iteration(s))\n\n{ex4_agent_result}"
                ),
                kind="info",
            ),
            mo.md(
                "**Observe:** Did the agent search more than once? Did it try different "
                "queries? That adaptive depth is what the loop buys you."
            ),
        ]
    )
    ex4_comparison
    return


@app.cell(hide_code=True)
def ex5_header():
    # @spec PLAN-COMP-011
    mo.md(
        dedent(
            """
            ## Exercise 5 — The cost/quality dial: `max_iterations`

            `max_iterations` controls how many laps the agent gets before it
            **must** answer. It is the dial between deterministic and fully
            agentic:

            | `max_iterations` | Behavior |
            |---|---|
            | **1** | One search, then forced answer — **starved** (≈ deterministic) |
            | **3** | Room to reformulate once or twice |
            | **5** (default) | Comfortable multi-step exploration |
            | **10+** | Deep research, but higher cost / latency |

            Pick a value from the dropdown below and see how the agent's
            behavior changes. The cell shows the full `AgentBot` constructor
            so you can see exactly what `build_agent` wraps — `max_iterations`
            is just one parameter on it.

            **Key insight:** `max_iterations` is not just a safety cap. It is
            the **primary control knob** for trading cost against
            adaptiveness.
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex5_controls():
    # Pick a max_iterations value — the cell below rebuilds and re-runs the agent.
    max_iters = mo.ui.dropdown(
        options=["1", "3", "5", "10"],
        value="1",
        label="max_iterations",
    )
    max_iters
    return (max_iters,)


@app.cell(hide_code=True)
def ex5_run(ex4_question, max_iters, search_corpus):
    # Build the agent with the selected max_iterations — this is what build_agent does inside.
    ex5_agent = AgentBot(
        tools=[search_corpus],
        system_prompt=(
            "You are a research assistant with access to a paper corpus. "
            "FIRST search for relevant papers using search_corpus. "
            "THEN, once you have results, call respond_to_user with a 2-3 sentence "
            "summary grounded in what the tool returned. "
            "You MUST use respond_to_user to deliver your final answer."
        ),
        model_name=get_model_name(),
        max_iterations=int(max_iters.value),
        **get_completion_kwargs(),
    )

    try:
        ex5_result = ex5_agent(ex4_question)
        ex5_iters = len([s for s in ex5_agent.spans if s.operation_name == "decision"])
        ex5_display = mo.vstack(
            [
                mo.callout(
                    mo.md(
                        f"**max_iterations={max_iters.value}** ({ex5_iters} iteration)\n\n"
                        f"{ex5_result}"
                    ),
                    kind="info",
                ),
                mo.md(
                    "### Compare other values\n\n"
                    "Change the dropdown above to try other values. With "
                    "max_iterations=1, the agent gets one shot — just like the "
                    "deterministic pipeline. With 5+, it can explore multiple angles.\n\n"
                    "**The dial:** More iterations = more adaptive, but more LLM calls "
                    "(more cost, more latency). Fewer = cheaper, more predictable."
                ),
            ]
        )
    except Exception as exc:
        ex5_display = mo.md(f"**AgentBot error:** {exc}")

    ex5_display
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
              the agent is not a single call, it is a conversation with its tools.
            - `max_iterations` caps the loop; `system_prompt` shapes behavior.

            ### Deterministic vs. agentic

            - A **deterministic pipeline** (search → summarize) is cheaper,
              faster, and predictable — but rigid. It searches once.
            - **AgentBot** adapts: it can search, observe, reformulate, and
              search again. This costs more but handles open-ended questions.
            - **`max_iterations`** is the dial between them: 1 iteration ≈
              deterministic; 5+ = fully agentic exploration.

            **Next:** Part 5 shows specialized agents (Searcher + Synthesizer)
            collaborating via AgentBot.
            """
        )
    )
    return


if __name__ == "__main__":
    app.run()
