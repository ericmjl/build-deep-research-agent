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
        MissingLLMConfigError,
        get_completion_kwargs,
        get_model_name,
    )
    from build_deep_research_agent.models import Message
    from build_deep_research_agent.prompts import build_messages

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


    def format_messages_preview(messages: list[Message]) -> str:
        preview_lines = []
        for message in messages:
            preview_lines.append(
                f"**{message.role}**\n\n```text\n{message.content}\n```"
            )
        return "\n\n".join(preview_lines)


    def run_llm_prompt(system_text: str, user_message: str) -> str:
        bot = SimpleBot(
            system_prompt=system_text,
            model_name=get_model_name(),
            **get_completion_kwargs(),
            stream_target="none"
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

        - **Exercise 1 & 2** provide four prompt fields: **Identity**, **Instructions**, **Examples**, and **Context**. Edit them and experiment.
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
        "Example request: What time is it?.\n"
        "Example response: Party time!"
    )

    _DEFAULT_CONTEXT = ""

    identity = mo.ui.text_area(value=_DEFAULT_IDENTITY, label="Identity", full_width=True)
    instructions = mo.ui.text_area(value=_DEFAULT_INSTRUCTIONS, label="Instructions", full_width=True)
    examples = mo.ui.text_area(value=_DEFAULT_EXAMPLES, label="Examples", full_width=True)
    context = mo.ui.text_area(value=_DEFAULT_CONTEXT, label="Context", full_width=True)
    run_ex1 = mo.ui.run_button(label="Run Exercise 1")
    mo.vstack([identity, instructions, examples, context, run_ex1])
    return context, examples, identity, instructions, run_ex1


@app.cell
def ex1_preview(context, examples, identity, instructions):
    system_text, user_message, messages = prepare_prompt(
        identity.value, instructions.value, examples.value, context.value
    )

    # @spec PROMPT-SYS-012
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
    _DEFAULT_IDENTITY_2 = 'You are a careful research assistant helping a scientist synthesize literature.\n\nConstraints:\n- Ground every claim in the provided citation metadata.\n- If evidence is insufficient, say so explicitly.\n- Prefer concise, structured markdown with short sections and bullet points.\n- Do not invent citations, DOIs, or findings not supported by the context.'

    _DEFAULT_INSTRUCTIONS_2 = "What is this paper about?"

    _DEFAULT_EXAMPLES_2 = (
        "User: What is this paper about?\n"
        "Context: <citation>\n"
        "Assistant: The paper is about <summary>"
    )

    _DEFAULT_CONTEXT_2 = '[1] key=ABC12345\nTitle: Bayesian Workflow for Applied Research\nAuthors: Gelman, Andrew, Ma, Eric\nYear: 2020\nAbstract: We describe a practical workflow for building, validating, and communicating Bayesian models in applied settings.'

    identity2 = mo.ui.text_area(value=_DEFAULT_IDENTITY_2, label="Identity", full_width=True)
    instructions2 = mo.ui.text_area(value=_DEFAULT_INSTRUCTIONS_2, label="Instructions", full_width=True)
    examples2 = mo.ui.text_area(value=_DEFAULT_EXAMPLES_2, label="Examples", full_width=True)
    context2 = mo.ui.text_area(value=_DEFAULT_CONTEXT_2, label="Context", full_width=True)
    run_ex2 = mo.ui.run_button(label="Run Exercise 2")
    mo.vstack([identity2, instructions2, examples2, context2, run_ex2])
    return context2, examples2, identity2, instructions2, run_ex2


@app.cell
def ex2_preview(context2, examples2, identity2, instructions2):
    system_text2, user_message2, messages2 = prepare_prompt(
        identity2.value, instructions2.value, examples2.value, context2.value
    )

    # @spec PROMPT-SUM-011
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


@app.cell
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
    build_messages('system text', 'user text')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
