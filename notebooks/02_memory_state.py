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
