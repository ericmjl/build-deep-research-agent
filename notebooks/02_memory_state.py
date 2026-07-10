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
    """Setup cell: imports and helpers available to all exercise wiring."""

    from textwrap import dedent

    import marimo as mo
    from llamabot import SimpleBot, set_debug_mode
    from llamabot.components.messages import AIMessage

    from build_deep_research_agent.fixtures.loader import load_citation_fixtures
    from build_deep_research_agent.models import Message
    from build_deep_research_agent.prompts import (
        RESEARCH_SYSTEM_PROMPT,
        format_citations_for_context,
    )
    from build_deep_research_agent.utils import format_messages_preview, make_bot

    set_debug_mode(enabled=False)

    fixtures = load_citation_fixtures()

    def assemble_research_prompt(user_query: str, context_text: str = "") -> str:
        parts: list[str] = []
        if context_text.strip():
            parts.append(f"Context:\n{context_text.strip()}")
        if user_query.strip():
            parts.append(f"User: {user_query.strip()}")
        return "\n\n".join(parts)

    def run_research_turn(
        bot: SimpleBot,
        user_query: str,
        context_text: str = "",
        history: list[Message] | None = None,
    ) -> AIMessage:
        """Call the research bot with optional prior chat turns (roles preserved)."""
        model_prompt = assemble_research_prompt(user_query, context_text)
        if history:
            turns = list(history) + [Message(role="user", content=model_prompt)]
            return bot(format_messages_preview(turns))
        return bot(model_prompt)

    from build_deep_research_agent.llm import (
        MissingLLMConfigError as _MissingLLMConfigError,
    )
    from build_deep_research_agent.llm import (
        get_completion_kwargs as _get_completion_kwargs,
    )

    llm_config_warning = None
    try:
        _get_completion_kwargs()
    except _MissingLLMConfigError as exc:
        # @spec PROMPT-SUM-030
        llm_config_warning = mo.callout(
            mo.md(
                f"**LLM credentials not configured** — configure credentials before running Exercise 1.\n\n{exc}"
            ),
            kind="warn",
        )

    if llm_config_warning is not None:
        llm_config_warning


@app.cell(hide_code=True)
def hero():
    mo.md(
        dedent(
            r"""
            <div style="display:flex;align-items:center;gap:1.2rem;background:linear-gradient(120deg,#0f172a,#1e293b);color:#e2e8f0;padding:1.3rem 1.6rem;border-radius:0.6rem;border-left:6px solid #fbbf24;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="12" y="10" width="36" height="12" rx="3" stroke="#fbbf24" stroke-width="2" fill="none"/>
                <rect x="12" y="26" width="36" height="12" rx="3" stroke="#fbbf24" stroke-width="2" fill="none"/>
                <rect x="12" y="42" width="36" height="8" rx="3" stroke="#fbbf24" stroke-width="2" fill="none"/>
                <circle cx="20" cy="16" r="2" fill="#fbbf24"/>
                <circle cx="20" cy="32" r="2" fill="#fbbf24"/>
              </svg>
              <div>
                <div style="font-size:1.5rem;font-weight:700;letter-spacing:-0.01em;line-height:1.15;">Part 2 &middot; Memory &mdash; <span style="color:#fbbf24;">state that persists</span> across turns</div>
                <div style="opacity:0.82;margin-top:0.25rem;font-size:0.95rem;">Build a Deep Research Agent &nbsp;&middot;&nbsp; SciPy 2026 &nbsp;&middot;&nbsp; Ben Batorsky</div>
              </div>
            </div>
            """
        )
    )
    return


@app.cell(hide_code=True)
def intro():
    mo.md(
        dedent("""
        # Part 2: Memory & state management

        Part 1 showed how to put citation metadata **in context** for a single turn.
        Part 2 adds **state** that persists across turns:

        - **Chat history** — prior user and assistant messages
        - **Citation memory** — paper metadata plus snippets from the conversation

        We'll be using some pre-populated citations and research prompts, but feel free
        to replace with your own. The fixture is a list of `CitationRecord` objects —
        see `models.py`.
        """)
    )
    return


@app.cell(hide_code=True)
def learning_objectives():
    mo.md(
        dedent("""
        ## Learning objectives

        After this part, you should be able to:

        - Explain why multi-turn research needs memory.
        - Append chat turns and inject prior context into the next LLM call.
        - Store citation metadata in memory and observe improved follow-up answers.
        """)
    )
    return


@app.cell(hide_code=True)
def how_this_notebook_works():
    mo.md(
        dedent("""
        ## How this notebook works

        **Your code lives in** `build_deep_research_agent/exercises/part2.py`.
        **Implementation specs** for each exercise are in markdown cells in this notebook and in docstrings in the code.
        After saving edits there, **restart the kernel** (marimo: *Restart* in the menu)
        so Python reloads the module.

        1. **Exercise 1** — `AppendOnlyMemory.append` / `messages` for chat history,
           and compare answers with and without populated memory.
        2. **Exercise 2** — `CitationMemory.add` / `as_context` for citation context.
        """)
    )
    return


@app.cell(hide_code=True)
def instructor_note():
    mo.md(
        dedent("""
        ### Instructors

        Reference solutions: `build_deep_research_agent/exercises/solutions/part2.py`

        In **part2_exercises**, comment out the learner import and uncomment the
        solutions import:

        ```python
        # from build_deep_research_agent.exercises import part2
        from build_deep_research_agent.exercises.solutions import part2
        ```

        Participants keep the default learner import only.
        """)
    )
    return


@app.cell
def _():
    # @spec MEM-EX-003
    # @spec TUT-MARIMO-022
    from build_deep_research_agent.exercises import part2

    # Instructors: swap imports to load reference solutions.
    # from build_deep_research_agent.exercises.solutions import part2
    return (part2,)


@app.cell(hide_code=True)
def setup_env_check():
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Let's first take a look at some of the fixtures we'll be importing.

    We'll be using a pre-defined system prompt for these experiments.  Feel free to modify it!

    Our citations are predefined as `CitationRecord` objects.  It might be useful to get familiar with the attributes here, as we'll be using them throughout the rest of the workshop.
    """)
    return


@app.cell
def _():
    print(f"System prompt:\n{RESEARCH_SYSTEM_PROMPT}")

    print("Citations")
    for f in fixtures:
        print(type(f))
        print(f.title)
        print(f.abstract)
        print("---")
    return


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent("""
        ## Exercise 1 — Append-only chat history

        Why do we need history? Let's see what happens if we continue the conversation about a paper
        """)
    )
    return


@app.cell
def ex1_seed():
    ex1_paper = fixtures[0]
    ex1_citation_context = format_citations_for_context([ex1_paper])
    research_bot = make_bot(RESEARCH_SYSTEM_PROMPT)

    ex1_question = mo.ui.text_area(
        value="What is this paper about?",
        label="Initial question",
        full_width=True,
    )

    run_ex1 = mo.ui.run_button(label="Run Exercise 1")

    mo.vstack([ex1_question, run_ex1])
    return ex1_citation_context, ex1_question, research_bot, run_ex1


@app.cell
def ex1_run(ex1_citation_context, ex1_question, research_bot, run_ex1):
    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    response1 = run_research_turn(
        research_bot, ex1_question.value, ex1_citation_context
    )
    mo.md(format_messages_preview([response1]))
    return (response1,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Great! So let's ask it a follow-up.
    """)
    return


@app.cell
def ex1_followup_no_history(research_bot, run_ex1):
    # @spec MEM-COMP-001
    followup_question = "Who are the authors?"

    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    response2 = run_research_turn(research_bot, followup_question)
    mo.md(format_messages_preview([response2]))
    return (followup_question,)


@app.cell(hide_code=True)
def ex1_implementation_specs():
    mo.md(
        dedent("""
        So let's implement memory!

        Implement **`AppendOnlyMemory`** in `exercises/part2.py` — an immutable
        chat history you can pass into `run_research_turn(..., history=...)`.

        - **`append(message)`** — return a **new** memory with that turn added
          (don't mutate in place).
        - **`messages()`** — return the turns in order so the follow-up can see
          the prior Q&A.
        """)
    )
    return


@app.cell
def ex1_controls(ex1_citation_context, ex1_question, part2, response1):
    # @spec MEM-CHAT-010
    # @spec MEM-CHAT-012
    ex1_model_prompt = assemble_research_prompt(
        ex1_question.value, ex1_citation_context
    )
    memory = part2.AppendOnlyMemory()
    print(f"Memory on first initialization: {memory.messages()}")
    memory = memory.append(Message(role="user", content=ex1_model_prompt)).append(
        Message(role=response1.role, content=response1.content)
    )
    print("Memory after append:")
    for msg in memory.messages():
        print(msg)
    return (memory,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    If we have it implemented correctly, we should be able to pass this to our bot with history and get a better answer than before.
    """)
    return


@app.cell
def ex1_followup_with_history(
    followup_question,
    memory,
    research_bot,
    run_ex1,
):
    # @spec MEM-CHAT-011
    # @spec MEM-COMP-002
    # @spec MEM-COMP-003
    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    response3 = run_research_turn(
        research_bot, followup_question, history=memory.messages()
    )

    mo.md(format_messages_preview([response3]))
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent("""
        ## Exercise 2 — Citation memory

        Since our use case involves paper citations, it makes sense to design memory
        around that structure. Think of discussing two papers and then asking to
        compare them. An inventory of papers in the conversation can help more than
        raw chat history alone.

        Implement **`CitationMemory`** in `exercises/part2.py`:

        - **`add(citation, snippet)`** — store a citation plus a short snippet from
          when it was discussed; return a **new** instance.
        - **`as_context()`** — turn what's stored into a string you can pass as
          context text.

        Consider also that there may be multiple snippets per citation, and how to handle that on output. papers and how you'd want the model to use this block.
        """)
    )
    return


@app.cell
def ex2_paper1_seed():
    ex2_paper1 = fixtures[0]
    ex2_paper2 = fixtures[1]
    ex2_context1 = format_citations_for_context([ex2_paper1])
    ex2_context2 = format_citations_for_context([ex2_paper2])
    print(ex2_context1)
    print(ex2_context2)

    run_ex2 = mo.ui.run_button(label="Run Exercise 2")
    mo.vstack([run_ex2])
    return ex2_context1, ex2_context2, ex2_paper1, ex2_paper2, run_ex2


@app.cell
def ex2_run(
    ex2_context1,
    ex2_context2,
    ex2_paper1,
    ex2_paper2,
    part2,
    research_bot,
    run_ex2,
):
    # @spec MEM-CITE-010
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    # initialize citation memory
    citation_memory = part2.CitationMemory()

    ex2_paper1_response = run_research_turn(
        research_bot, "What is this paper about?", ex2_context1
    )
    citation_memory = citation_memory.add(
        citation=ex2_paper1, snippet=ex2_paper1_response.content
    )

    ex2_paper2_response = run_research_turn(
        research_bot, "What is this paper about?", ex2_context2
    )
    citation_memory = citation_memory.add(
        citation=ex2_paper2, snippet=ex2_paper2_response.content
    )

    mo.md(citation_memory.as_context())
    return (citation_memory,)


@app.cell
def ex2_compare(citation_memory, research_bot, run_ex2):
    # @spec MEM-CITE-011
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    response_w_citation_context = run_research_turn(
        research_bot,
        "Compare the papers.",
        citation_memory.as_context(),
    )

    mo.md(format_messages_preview([response_w_citation_context]))
    return


@app.cell(hide_code=True)
def why_these_sources_bridge():
    mo.vstack(
        [
            mo.md(
                dedent(
                    r"""
                    ## Why *these* sources? A bridge to Part 3

                    You may have used ChatGPT's "research mode" or similar tools that
                    retrieve papers automatically. If you watched it pull in 10 papers
                    and wondered **"why those 10?"** — you've hit a fundamental problem:

                    **Proprietary retrieval is a black box.** You can't see the ranking
                    algorithm, the source corpus, or the embedding model. You're trusting
                    a hidden pipeline to decide what your agent "knows."

                    That's exactly why we build our **own** retrieval pipeline in Part 3.
                    When you control the document store, the embedding model, and the
                    similarity search, you can answer "why these sources?" with evidence.
                    """
                )
            ),
            mo.callout(
                mo.md(
                    "**Check your understanding:** Name one risk of relying on a "
                    "proprietary tool's built-in paper retrieval for a literature review.\n\n"
                    "You can't audit **which** papers were excluded, **why** the top "
                    "results ranked above others, or whether the corpus has coverage "
                    "gaps in your subfield. A self-built pipeline makes each step "
                    "inspectable."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def vector_search_insight():
    mo.vstack(
        [
            mo.md(
                dedent(
                    r"""
                    ## The 1 RAG misconception: embeddings → text → prompt

                    Here's the key insight that will save you hours of confusion:

                    > **We don't stuff embeddings into the LLM. We stuff the *text*
                    > associated with an embedding *after retrieval*.**

                    An embedding is a vector of numbers — the LLM can't read vectors.
                    The pipeline is:

                    1. Embed every document, store the **vector + the original text** in a
                       vector database.
                    2. Embed the **query**, search the database for similar vectors.
                    3. **Fetch the original text** from the matched documents.
                    4. **Inject that text** into the LLM prompt as context.

                    <div style="background:#0f172a;border-radius:0.6rem;padding:1.2rem;margin-top:0.8rem;">
                    <svg width="100%" height="200" viewBox="0 0 620 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="10" y="15" width="80" height="36" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>
                      <text x="50" y="38" text-anchor="middle" fill="#e2e8f0" font-size="10" font-family="monospace">docs</text>
                      <path d="M90 33 L115 33" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <rect x="120" y="15" width="90" height="36" rx="6" fill="#1e293b" stroke="#fbbf24" stroke-width="2"/>
                      <text x="165" y="38" text-anchor="middle" fill="#fbbf24" font-size="10" font-family="monospace">embed</text>
                      <path d="M210 33 L235 33" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <rect x="240" y="10" width="110" height="46" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
                      <text x="295" y="30" text-anchor="middle" fill="#38bdf8" font-size="10" font-weight="700" font-family="monospace">Vector DB</text>
                      <text x="295" y="46" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="monospace">vectors + text</text>
                      <rect x="10" y="85" width="80" height="36" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>
                      <text x="50" y="108" text-anchor="middle" fill="#e2e8f0" font-size="10" font-family="monospace">query</text>
                      <path d="M90 103 L115 103" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <rect x="120" y="85" width="90" height="36" rx="6" fill="#1e293b" stroke="#fbbf24" stroke-width="2"/>
                      <text x="165" y="108" text-anchor="middle" fill="#fbbf24" font-size="10" font-family="monospace">embed</text>
                      <path d="M210 103 L250 103" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <text x="230" y="97" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="monospace">search</text>
                      <path d="M295 56 L295 130" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow2)"/>
                      <text x="320" y="97" fill="#cbd5e1" font-size="8" font-family="monospace">top-k</text>
                      <rect x="380" y="120" width="110" height="36" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="2"/>
                      <text x="435" y="143" text-anchor="middle" fill="#34d399" font-size="10" font-weight="700" font-family="monospace">fetch TEXT</text>
                      <path d="M350 103 L380 138" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <path d="M490 138 L515 138" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow2)"/>
                      <rect x="520" y="120" width="90" height="36" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
                      <text x="565" y="136" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="700" font-family="monospace">LLM</text>
                      <text x="565" y="149" text-anchor="middle" fill="#94a3b8" font-size="8" font-family="monospace">prompt ctx</text>
                      <rect x="380" y="15" width="100" height="36" rx="6" fill="#0f172a" stroke="#ef4444" stroke-width="2" stroke-dasharray="4 3"/>
                      <text x="430" y="38" text-anchor="middle" fill="#ef4444" font-size="9" font-family="monospace">embeddings?</text>
                      <path d="M350 33 L378 33" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 3"/>
                      <path d="M480 33 L518 33" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 3"/>
                      <path d="M525 20 L555 50 M555 20 L525 50" stroke="#ef4444" stroke-width="3"/>
                      <defs>
                        <marker id="arrow2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
                          <path d="M0,0 L8,4 L0,8" fill="#94a3b8"/>
                        </marker>
                      </defs>
                    </svg>
                    </div>

                    Part 3 will make this concrete with a **LanceDB** document store — you'll
                    see exactly how embeddings are stored, searched, and turned back into
                    text for the prompt.
                    """
                )
            ),
            mo.callout(
                mo.md(
                    "**Check your understanding:** After the vector database returns "
                    "the top-5 most similar documents, what do you feed into the LLM "
                    "— the embeddings or the original text?\n\n"
                    "The **original text**. The embeddings were only used to *find* "
                    "the right documents via similarity search. The LLM reads text, "
                    "not vectors."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def discussion():
    # @spec MEM-COMP-010
    mo.md(
        dedent("""
        ### Discussion prompts

        - When is chat history enough, and when does structured memory like `CitationMemory` pay off?
        - How might memory grow unbounded over a long research session, and what strategies could keep it in check?

        **Recap & handoff:** prompt (Part 1) + memory (Part 2) form the foundation of
        the agent. Part 3 builds on this by giving the agent **tools** to act, not just
        remember.
        """)
    )
    return


if __name__ == "__main__":
    app.run()
