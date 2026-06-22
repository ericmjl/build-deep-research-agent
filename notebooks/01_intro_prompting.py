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

    import marimo as mo
    from llamabot import SimpleBot, set_debug_mode

    from build_deep_research_agent.llm import (
        get_completion_kwargs,
        get_model_name,
    )
    from build_deep_research_agent.models import Message
    from build_deep_research_agent.prompts import build_messages
    from build_deep_research_agent.utils import format_messages_preview

    set_debug_mode(enabled=False)

    def assemble_user_message(
        instructions_text: str, examples_text: str, context_text: str
    ) -> str:
        parts: list[str] = []
        if instructions_text.strip():
            parts.append(f"Instructions:\n{instructions_text.strip()}")
        if examples_text.strip():
            parts.append(f"Examples:\n{examples_text.strip()}")
        if context_text.strip():
            parts.append(f"Context:\n{context_text.strip()}")
        return "\n\n".join(parts)

    def prepare_prompt(
        identity_text: str,
        instructions_text: str,
        examples_text: str,
        context_text: str,
    ) -> tuple[str, str, list[Message]]:
        system_text = identity_text.strip()
        user_message = assemble_user_message(
            instructions_text, examples_text, context_text
        )
        messages = build_messages(system_text, user_message)
        return system_text, user_message, messages

    def run_llm_prompt(system_text: str, user_message: str) -> str:
        bot = SimpleBot(
            system_prompt=system_text,
            model_name=get_model_name(),
            **get_completion_kwargs(),
            stream_target="none",
        )
        return bot(user_message)


@app.cell(hide_code=True)
def intro():
    mo.md(
        dedent("""
        # Part 1: In-context Learning

        One of the things that makes LLMs so versatile is they have the capacity to be "steered" in natural language.  Without changing the underlying weights of the model, you can drastically alter its responses.  This is called "in-context learning".

        In this notebook, we will experiment with prompt structure in order to create a response that includes information from a citation we've extracted from our Zotero database.

        ## Prompt setup
        As discussed in the slides, we'll set up the prompt components and see how edits to them impact the results
        """)
    )
    return


@app.cell(hide_code=True)
def learning_objectives():
    mo.md(
        dedent("""
        ## Learning objectives

        After Exercise 1, you should be able to:

        - Explain how in-context learning steers an LLM without changing model weights.
        - Compose a prompt from Identity, Instructions, Examples, and Context, and inspect the assembled messages sent to the model.
        """)
    )
    return


@app.cell(hide_code=True)
def how_this_notebook_works():
    mo.md(
        dedent("""
        ## How this notebook works

        - **Exercises 1–3** provide four prompt fields: **Identity**, **Instructions**, **Examples**, and **Context**. Edit them and experiment.
        - Exercise 2 uses **citation metadata** in Context; Exercise 3 uses a **fulltext snippet**.
        - The **message preview** updates as you edit — no button required.
        - Click **Run Exercise** to call the live LLM and see the model response.

        Requires `TUTORIAL_LLM_BASE_URL` and `TUTORIAL_LLM_API_KEY` (Modal path)
        or `OPENAI_API_KEY` (BYO path).
        """)
    )
    return


@app.cell(hide_code=True)
def setup_env_check():
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
    return


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent("""
        ## Exercise 1 — Prompt components

        As described in the discussion, we have our various prompt "components", roughly summarized from the guidance literature:

        **Identity**: Here this is the system message

        **Instructions**: We can use this as the "user message" - it is what is directing the model what to do.

        **Examples**: Any examples of how we want the model to answer.

        **Context**: Relevant context, more on that later.

        The preview cell shows the assembled messages the model receives.
        """)
    )
    return


@app.cell
def ex1_prompt_components():
    # @spec PROMPT-SYS-002
    # @spec PROMPT-SYS-011
    _DEFAULT_IDENTITY = "You are a helpful assistant."

    _DEFAULT_INSTRUCTIONS = "What time is it?"

    _DEFAULT_EXAMPLES = (
        "Example request: What time is it?.\nExample response: Party time!"
    )

    _DEFAULT_CONTEXT = ""

    identity = mo.ui.text_area(
        value=_DEFAULT_IDENTITY, label="Identity", full_width=True
    )
    instructions = mo.ui.text_area(
        value=_DEFAULT_INSTRUCTIONS, label="Instructions", full_width=True
    )
    examples = mo.ui.text_area(
        value=_DEFAULT_EXAMPLES, label="Examples", full_width=True
    )
    context = mo.ui.text_area(value=_DEFAULT_CONTEXT, label="Context", full_width=True)
    # @spec PROMPT-SYS-012
    run_ex1 = mo.ui.run_button(label="Run Exercise 1")
    mo.vstack([identity, instructions, examples, context, run_ex1])
    return context, examples, identity, instructions, run_ex1


@app.cell
def ex1_preview(context, examples, identity, instructions):
    system_text, user_message, messages = prepare_prompt(
        identity.value, instructions.value, examples.value, context.value
    )

    mo.md(format_messages_preview(messages))
    return system_text, user_message


@app.cell
def ex1_run(run_ex1, system_text, user_message):
    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    response = run_llm_prompt(system_text, user_message)
    mo.md(format_messages_preview([response]))
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent("""
        ## Exercise 2 — Research summarization with citation context

        Same four prompt fields as Exercise 1 — but now with **research-relevant defaults**:

        - **Identity** is a research-assistant system prompt (try editing the constraints).
        - **Instructions** ask the model to find themes across papers.
        - **Examples** a simple templated response
        - **Context** is pre-loaded with citation metadata from our library.

        Edit any field and watch the preview update. Click **Run Exercise 2** when ready.
        """)
    )
    return


@app.cell
def ex2_prompt_components():
    # @spec PROMPT-SUM-010
    _DEFAULT_IDENTITY_2 = "You are a careful research assistant helping a scientist synthesize literature.\n\nConstraints:\n- Ground every claim in the provided citation metadata.\n- If evidence is insufficient, say so explicitly.\n- Prefer concise, structured markdown with short sections and bullet points.\n- Do not invent citations, DOIs, or findings not supported by the context."

    _DEFAULT_INSTRUCTIONS_2 = "What is this paper about?"

    _DEFAULT_EXAMPLES_2 = (
        "User: What is this paper about?\n"
        "Context: <citation>\n"
        "Assistant: The paper is about <summary>"
    )

    _DEFAULT_CONTEXT_2 = (
        "[1] key=ABC12345\n"
        "Title: The Python Tutorial\n"
        "Authors: Python Software Foundation\n"
        "Year: 2024\n"
        "Abstract: An introduction to Python, a high-level programming language "
        "emphasizing readability, dynamic typing, and a rich standard library."
    )

    identity2 = mo.ui.text_area(
        value=_DEFAULT_IDENTITY_2, label="Identity", full_width=True
    )
    instructions2 = mo.ui.text_area(
        value=_DEFAULT_INSTRUCTIONS_2, label="Instructions", full_width=True
    )
    examples2 = mo.ui.text_area(
        value=_DEFAULT_EXAMPLES_2, label="Examples", full_width=True
    )
    context2 = mo.ui.text_area(
        value=_DEFAULT_CONTEXT_2, label="Context", full_width=True
    )
    # @spec PROMPT-SUM-011
    run_ex2 = mo.ui.run_button(label="Run Exercise 2")
    mo.vstack([identity2, instructions2, examples2, context2, run_ex2])
    return context2, examples2, identity2, instructions2, run_ex2


@app.cell
def ex2_preview(context2, examples2, identity2, instructions2):
    system_text2, user_message2, messages2 = prepare_prompt(
        identity2.value, instructions2.value, examples2.value, context2.value
    )

    mo.md(format_messages_preview(messages2))
    return system_text2, user_message2


@app.cell
def ex2_run(run_ex2, system_text2, user_message2):
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    # @spec PROMPT-SUM-012
    response2 = run_llm_prompt(system_text2, user_message2)
    mo.md(format_messages_preview([response2]))
    return


@app.cell(hide_code=True)
def ex3_fullpaper_header():
    mo.md(
        dedent("""
        ## Context as a "full paper"

        Though we're using citation metadata in Exercise 2, the **Context** field can hold the full text of a paper (or a representative excerpt). You may get [strange behavior with long contexts](https://arxiv.org/abs/2307.03172), but most models can still extract useful insights from fulltext.
        """)
    )
    return


@app.cell
def ex3_prompt_components(examples2, identity2, instructions2):
    # @spec PROMPT-SUM-013
    _DEFAULT_CONTEXT_3 = (
        "Title: The Python Tutorial (excerpt)\n"
        "Source: Python Software Foundation\n\n"
        "Python is an easy to learn, powerful programming language. It has efficient "
        "high-level data structures and a simple but effective approach to "
        "object-oriented programming. Python's elegant syntax and dynamic typing, "
        "together with its interpreted nature, make it an ideal language for scripting "
        "and rapid application development on many platforms.\n\n"
        "The Python interpreter and the extensive standard library are available in "
        "source or binary form without charge for all major platforms, and can be "
        "freely distributed. The same site also contains distributions of and "
        "pointers to many free third party Python modules, programs and tools, and "
        "additional documentation."
    )

    context3 = mo.ui.text_area(
        value=_DEFAULT_CONTEXT_3, label="Context", full_width=True
    )
    run_ex3 = mo.ui.run_button(label="Run Exercise 3")
    mo.vstack([identity2, instructions2, examples2, context3, run_ex3])
    return context3, run_ex3


@app.cell
def ex3_preview(context3, examples2, identity2, instructions2):
    system_text3, user_message3, messages3 = prepare_prompt(
        identity2.value, instructions2.value, examples2.value, context3.value
    )

    # @spec PROMPT-SUM-014
    mo.md(format_messages_preview(messages3))
    return system_text3, user_message3


@app.cell
def ex3_run(run_ex3, system_text3, user_message3):
    mo.stop(
        not run_ex3.value,
        mo.md("_Click **Run Exercise 3** to call the LLM._"),
    )

    # @spec PROMPT-SUM-015
    response3 = run_llm_prompt(system_text3, user_message3)
    mo.md(format_messages_preview([response3]))
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        dedent("""
        ## A note on "message history"

        Teeing this up for Part 2, but notice how the `build_messages` function works.  It takes the input and creates a list of "Message" objects.  Think how we might want to include another "turn" in the conversation
        """)
    )
    return


@app.cell
def _():
    build_messages("system text", "user text")
    return


@app.cell
def discussion():
    # @spec PROMPT-SYS-020
    mo.md(
        dedent("""
        ### Discussion prompts

        - Is this an agent?
        - What are the limitations of in-context learning?
        - How do the four prompt components (Identity, Instructions, Examples, Context) each change the output?

        **Recap & handoff:** a well-structured prompt is the foundation. But each call
        here is stateless — the model forgets everything between turns. Part 2 adds
        **memory** so the agent can carry context across a conversation.
        """)
    )
    return


if __name__ == "__main__":
    app.run()
