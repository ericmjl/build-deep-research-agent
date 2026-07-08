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
    from textwrap import dedent


@app.cell(hide_code=True)
def intro():
    import marimo as mo

    mo.md(
        dedent("""
        # Part 2: Memory & state management

        Part 1 showed how to put citation metadata **in context** for a single turn.
        Part 2 adds **state** that persists across turns:

        - **Chat history** — prior user and assistant messages
        - **Citation memory** — paper metadata plus snippets from the conversation

        After this part you can explain why multi-turn research needs memory and inject
        prior context into the next LLM call.

        We'll be using some pre-populated citations and research prompts, but feel free
        to replace with your own. The fixture is a list of `CitationRecord` objects —
        see `models.py`.
        """)
    )
    return (mo,)


@app.cell(hide_code=True)
def how_this_notebook_works(mo):
    mo.md(
        dedent("""
        ## How this notebook works

        **Your code lives in** `build_deep_research_agent/exercises/part2.py`.
        Implement each method there, then **restart the kernel** (marimo: *Restart*
        in the menu) so Python reloads the module.

        1. **Exercise 1** — `AppendOnlyMemory.append` / `messages` for chat history,
           and compare answers with and without populated memory.
        2. **Exercise 2** — `CitationMemory.add` / `as_context` for citation context.
        """)
    )
    return


@app.cell
def research_setup():
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

    def run_research_turn(
        bot: SimpleBot,
        user_message: str,
        history: list[Message] | None = None,
    ) -> AIMessage:
        """Call the research bot with optional prior chat turns (roles preserved)."""
        turns = list(history or []) + [Message(role="user", content=user_message)]
        formatted_turns = "\n".join(
            [f"**{m.role}**\n\n```text\n{m.content}\n```" for m in turns]
        )
        return bot(formatted_turns)

    fixtures = load_citation_fixtures()
    return (
        Message,
        RESEARCH_SYSTEM_PROMPT,
        fixtures,
        format_citations_for_context,
        format_messages_preview,
        make_bot,
        run_research_turn,
    )


@app.cell
def _(RESEARCH_SYSTEM_PROMPT, fixtures):
    print(f"System prompt:\n{RESEARCH_SYSTEM_PROMPT}")

    print("Citations")
    for f in fixtures:
        print(type(f))
        print(f.title)
        print(f.abstract)
        print("---")
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
def ex1_header(mo):
    mo.md(
        dedent("""
        ## Exercise 1 — Append-only chat history

        Why do we need history? Let's see what happens if we continue the conversation about a paper
        """)
    )
    return


@app.cell
def ex1_seed(fixtures, format_citations_for_context, make_bot, mo, RESEARCH_SYSTEM_PROMPT):
    ex1_paper = fixtures[0]
    ex1_citation_context = format_citations_for_context([ex1_paper])
    research_bot = make_bot(RESEARCH_SYSTEM_PROMPT)

    question_w_context = f"What is this paper about?\n\nContext:{ex1_citation_context}"

    ex1_question = mo.ui.text_area(
        value=question_w_context,
        label="Initial question",
        full_width=True,
    )

    run_ex1 = mo.ui.run_button(label="Run Exercise 1")

    mo.vstack([ex1_question, run_ex1])
    return question_w_context, research_bot, run_ex1


@app.cell
def ex1_run(
    format_messages_preview,
    mo,
    question_w_context,
    research_bot,
    run_ex1,
    run_research_turn,
):
    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    response1 = run_research_turn(research_bot, question_w_context)
    mo.md(format_messages_preview([response1]))
    return (response1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Great! So let's ask it a follow-up.
    """)
    return


@app.cell
def ex1_followup_no_history(
    format_messages_preview,
    mo,
    research_bot,
    run_ex1,
    run_research_turn,
):
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
def ex1_memory_demo(mo):
    mo.md(
        dedent("""
        So let's implement memory!

        Review below, we want to be able to plug memory into our run_research_turn function.  Implement this memory store in `exercises/part2.py` by replacing the `AppendOnlyMemory` stub.
        """)
    )
    return


@app.cell
def ex1_controls(Message, part2, question_w_context, response1):
    # @spec MEM-CHAT-010
    # @spec MEM-CHAT-012
    memory = part2.AppendOnlyMemory()
    print(memory.messages())
    memory = memory.append(Message(role="user", content=question_w_context)).append(
        Message(role=response1.role, content=response1.content)
    )
    for msg in memory.messages():
        print(msg)
    return (memory,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we have it implemented correctly, we should be able to pass this to our bot with history and get a better answer than before.
    """)
    return


@app.cell
def ex1_followup_with_history(
    followup_question,
    format_messages_preview,
    memory,
    mo,
    research_bot,
    run_research_turn,
):
    # @spec MEM-CHAT-011
    # @spec MEM-COMP-002
    # @spec MEM-COMP-003
    response3 = run_research_turn(
        research_bot, followup_question, history=memory.messages()
    )
    mo.md(format_messages_preview([response3]))
    return


@app.cell(hide_code=True)
def ex2_header(mo):
    mo.md(
        dedent("""
        ## Exercise 2 — Citation memory

        Since we know our use-case involves paper citations, it makes sense to design our memory around this structure.  Think of the situation in which you have discussion about two papers and then want to compare them.  You might be better served by maintaining an inventory of the papers being included in the conversation.

        Implement `CitationMemory`.  We want to be able to add citations along with some context and also be able to plug that information into our LLM prompt.
        """)
    )
    return


@app.cell
def ex2_paper1_seed(fixtures, format_citations_for_context, mo):
    ex2_paper1 = fixtures[0]
    ex2_paper2 = fixtures[1]
    ex2_question1 = f"What is this paper about?\n\nContext:{format_citations_for_context([ex2_paper1])}"
    ex2_question2 = f"What is this paper about?\n\nContext:{format_citations_for_context([ex2_paper2])}"

    run_ex2 = mo.ui.run_button(label="Run exercise 2")
    mo.vstack([run_ex2])
    return ex2_paper1, ex2_paper2, ex2_question1, ex2_question2, run_ex2


@app.cell
def ex2_run(
    ex2_paper1,
    ex2_paper2,
    ex2_question1,
    ex2_question2,
    mo,
    part2,
    research_bot,
    run_ex2,
    run_research_turn,
):
    # @spec MEM-CITE-010
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run exercise 2** to call the LLM._"),
    )

    # initialize citation memory
    citation_memory = part2.CitationMemory()

    ex2_paper1_response = run_research_turn(research_bot, ex2_question1)
    citation_memory = citation_memory.add(
        citation=ex2_paper1, snippet=ex2_paper1_response.content
    )

    ex2_paper2_response = run_research_turn(research_bot, ex2_question2)
    citation_memory = citation_memory.add(
        citation=ex2_paper2, snippet=ex2_paper2_response.content
    )

    mo.md(citation_memory.as_context())
    return (citation_memory,)


@app.cell
def ex2_compare(citation_memory, mo, research_bot, run_ex2, run_research_turn):
    # @spec MEM-CITE-011
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run exercise 2** to call the LLM._"),
    )

    # if we inject citation context, we don't need the conversation memory in this case
    question_w_citation_context = (
        f"Compare the papers.\n\n{citation_memory.as_context()}"
    )

    response_w_citation_context = run_research_turn(
        research_bot, question_w_citation_context
    )

    mo.md(response_w_citation_context.content)
    return


@app.cell
def discussion(mo):
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
