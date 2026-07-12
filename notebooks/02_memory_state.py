# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///
# @spec TUT-MARIMO-021

import marimo

__generated_with = "0.23.14"
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

        - **Chat history** — prior user and assistant messages, plus
          ``retrieve(n_results)`` for a recent slice
        - **Citation memory** — paper metadata plus LLM **summaries** (tool-shaped
          evidence), not raw conversation snippets

        A research agent combines both: chat outputs *and* tool outputs. We'll build
        that composition by hand here; Parts 3–4 automate the tool side.
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
        - Append chat turns, retrieve a recent slice, and inject prior context into
          the next LLM call.
        - Summarize papers with a plain function, store them in `CitationMemory`, and
          combine chat + citation context in one query.
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

        1. **Exercise 1** — `AppendOnlyMemory.append` / `messages` / `retrieve` for
           chat history, and compare answers with and without populated memory.
        2. **Exercise 2** — `summarize_paper` + `CitationMemory.add` / `as_context`,
           then a combined chat + citation compare and an "add a paper, what changed?"
           beat.
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
def part2_exercises():
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
def fixtures_intro():
    mo.md(r"""
    Let's first take a look at some of the fixtures we'll be importing.

    We'll be using a pre-defined system prompt for these experiments.  Feel free to modify it!

    Our citations are predefined as `CitationRecord` objects.  It might be useful to get familiar with the attributes here, as we'll be using them throughout the rest of the workshop.
    """)
    return


@app.cell
def fixtures_preview():
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
def ex1_followup_prompt():
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
        - **`retrieve(n_results)`** — return only the most recent ``n_results``
          turns (drops the oldest).
        """)
    )
    return


@app.cell
def ex1_controls(ex1_citation_context, ex1_question, part2, response1):
    # @spec MEM-CHAT-010
    # @spec MEM-CHAT-012
    # @spec MEM-CHAT-013
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
    print(f"\nretrieve(n_results=1): {memory.retrieve(n_results=1)}")
    return (memory,)


@app.cell(hide_code=True)
def ex1_with_history_prompt():
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
        ## Exercise 2 — Summaries + citation memory

        Chat history alone doesn't record *what evidence* you gathered about each
        paper. In a research agent, a summarizer (later a `@tool`) produces that
        evidence — here we call a plain function and store the result.

        Implement in `exercises/part2.py`:

        1. **`summarize_paper(bot, text)`** — plain function (no `@tool`); return a
           short summary string.
        2. **`CitationMemory`**:
           - **`add(citation, summary)`** — store a citation plus its summary;
             return a **new** instance.
           - **`as_context()`** — format stored citations + summaries for prompt
             injection (later summary for a key wins).

        Then we'll **combine** chat history and citation memory in one compare
        query, add a third paper, and ask what changed.
        """)
    )
    return


@app.cell
def ex2_paper_seed():
    ex2_paper1 = fixtures[0]
    ex2_paper2 = fixtures[1]
    ex2_paper3 = fixtures[2]
    print(ex2_paper1.title)
    print(ex2_paper2.title)
    print(ex2_paper3.title)

    run_ex2 = mo.ui.run_button(label="Run Exercise 2")
    mo.vstack([run_ex2])
    return ex2_paper1, ex2_paper2, ex2_paper3, run_ex2


@app.cell
def ex2_summarize_two(ex2_paper1, ex2_paper2, part2, research_bot, run_ex2):
    # @spec MEM-CITE-010
    # @spec MEM-CITE-012
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    citation_memory = part2.CitationMemory()
    chat_memory = part2.AppendOnlyMemory()

    summary1 = part2.summarize_paper(
        research_bot, ex2_paper1.abstract or ex2_paper1.title
    )
    citation_memory = citation_memory.add(ex2_paper1, summary1)

    summary2 = part2.summarize_paper(
        research_bot, ex2_paper2.abstract or ex2_paper2.title
    )
    citation_memory = citation_memory.add(ex2_paper2, summary2)

    mo.md(citation_memory.as_context())
    return chat_memory, citation_memory


@app.cell(hide_code=True)
def ex2_combine_prompt():
    mo.md(
        dedent("""
        ### Combined query — chat + citation memory

        A research turn often needs **both**: dialogue state (what we already asked)
        and evidence state (summaries of papers). Compose them inline — no third
        memory class.
        """)
    )
    return


@app.cell
def ex2_compare(chat_memory, citation_memory, research_bot, run_ex2):
    # @spec MEM-CITE-011
    # @spec MEM-COMP-003
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    compare_question = "Summarize the evidence in these papers"
    compare_response = run_research_turn(
        research_bot,
        compare_question,
        context_text=citation_memory.as_context(),
        history=chat_memory.messages(),
    )

    compare_prompt = assemble_research_prompt(
        compare_question, citation_memory.as_context()
    )
    chat_after_compare = chat_memory.append(
        Message(role="user", content=compare_prompt)
    ).append(Message(role=compare_response.role, content=compare_response.content))

    mo.md(format_messages_preview([compare_response]))
    return (chat_after_compare,)


@app.cell(hide_code=True)
def ex2_add_third_prompt():
    mo.md(
        dedent("""
        ### Add a paper — what changed?

        Summarize a third paper, add it to citation memory, and ask a follow-up that
        needs the prior compare turn (chat) **and** the full evidence inventory.
        """)
    )
    return


@app.cell
def ex2_add_third(
    chat_after_compare,
    citation_memory,
    ex2_paper3,
    part2,
    research_bot,
    run_ex2,
):
    # @spec MEM-CITE-013
    # @spec MEM-COMP-020
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    summary3 = part2.summarize_paper(
        research_bot, ex2_paper3.abstract or ex2_paper3.title
    )
    citation_after_third = citation_memory.add(ex2_paper3, summary3)

    change_question = "We just added another paper. What changes in your summary?"
    change_response = run_research_turn(
        research_bot,
        change_question,
        context_text=citation_after_third.as_context(),
        history=chat_after_compare.messages(),
    )

    mo.md(format_messages_preview([change_response]))
    return


@app.cell(hide_code=True)
def context_text_why():
    mo.md(
        dedent("""
        ### Why a special `context_text` keyword?

        The implementation above is pretty specific to this example. But why maintain
        two separate types of memory? One could think of the summarization being done
        as a **tool** and the summary as a **result** — that could just as easily
        become **part of** the chat memory.

        `Message` already allows `role="tool"`. Append those summary strings onto the
        existing `AppendOnlyMemory`, pass them as `history=...`, and the model still
        sees the evidence — no separate `context_text` / `CitationMemory.as_context()`
        path.
        """)
    )

    return


@app.cell
def tool_role_in_chat(chat_memory, citation_memory, research_bot, run_ex2):
    # @spec MEM-COMP-040
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** first so summaries exist._"),
    )

    # Same evidence as CitationMemory — appended onto the existing chat memory
    chat_with_tools = chat_memory
    for citation, summary in citation_memory.entries:
        chat_with_tools = chat_with_tools.append(
            Message(
                role="tool",
                content=f"summarize_paper result for {citation.key}:\n{summary}",
            )
        )

    print("Chat memory with tool turns (no context_text):")
    for turn in chat_with_tools.messages():
        print(turn)

    alt_response = run_research_turn(
        research_bot,
        "Summarize the evidence in these papers",
        history=chat_with_tools.messages(),
    )
    mo.md(format_messages_preview([alt_response]))

    return


@app.cell(hide_code=True)
def discussion():
    # @spec MEM-COMP-010
    mo.md(
        dedent("""
        ### Discussion prompts

            - Is this an agent?
            - What are the limitations of having append-based memory? How might you overcome them?

            **Recap & handoff:** prompt (Part 1) + memory (Part 2) form the foundation of
            the a workflow or agent.  Part 3 sets up a set of tools, which then get us closer to what might be considered an "agent".
        """)
    )

    return


if __name__ == "__main__":
    app.run()
