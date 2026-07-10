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
    from llamabot import set_debug_mode

    from build_deep_research_agent.models import Message
    from build_deep_research_agent.prompts import build_messages
    from build_deep_research_agent.utils import format_messages_preview, make_bot

    set_debug_mode(enabled=False)

    def assemble_model_prompt(
        instructions_text: str,
        examples_text: str,
        context_text: str,
        user_query: str,
    ) -> str:
        parts: list[str] = []
        if instructions_text.strip():
            parts.append(f"Instructions:\n{instructions_text.strip()}")
        if examples_text.strip():
            parts.append(f"Examples:\n{examples_text.strip()}")
        if context_text.strip():
            parts.append(f"Context:\n{context_text.strip()}")
        if user_query.strip():
            parts.append(f"User: {user_query.strip()}")
        return "\n\n".join(parts)

    def prepare_prompt(
        identity_text: str,
        instructions_text: str,
        examples_text: str,
        context_text: str,
        user_query: str,
    ) -> tuple[str, str, list[Message]]:
        system_prompt = identity_text.strip()
        model_prompt = assemble_model_prompt(
            instructions_text, examples_text, context_text, user_query
        )
        messages = build_messages(system_prompt, model_prompt)
        return system_prompt, model_prompt, messages


@app.cell(hide_code=True)
def hero():
    mo.md(
        dedent(
            r"""
            <div style="display:flex;align-items:center;gap:1.2rem;background:linear-gradient(120deg,#0f172a,#1e293b);color:#e2e8f0;padding:1.3rem 1.6rem;border-radius:0.6rem;border-left:6px solid #34d399;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 14 L44 14 Q50 14 50 20 L50 36 Q50 42 44 42 L26 42 L16 50 L18 42 L10 42 Q6 42 6 36 L6 20 Q6 14 10 14 Z" stroke="#34d399" stroke-width="2" fill="none"/>
                <circle cx="18" cy="28" r="2.5" fill="#34d399"/>
                <circle cx="28" cy="28" r="2.5" fill="#34d399"/>
                <circle cx="38" cy="28" r="2.5" fill="#34d399"/>
              </svg>
              <div>
                <div style="font-size:1.5rem;font-weight:700;letter-spacing:-0.01em;line-height:1.15;">Part 1 &middot; Prompting &mdash; the art of <span style="color:#34d399;">in-context learning</span></div>
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

        - **Cell 0** validates your LLM setup before you start the exercises. If `.env` is missing/incomplete, it shows a form pre-filled with README defaults and can write `.env` for you.
        - **Exercises 1–3** provide five prompt fields: **Identity**, **Instructions**, **Examples**, **Context**, and **User Query**. Edit them and experiment.
        - Exercise 2 uses **citation metadata** in Context; Exercise 3 uses a **fulltext snippet**.
        - The **message preview** updates as you edit — no button required.
        - Click **Run Exercise** to call the live LLM and see the model response.
        """)
    )
    return


@app.cell(hide_code=True)
def text_in_text_out():
    mo.vstack(
        [
            mo.md(
                dedent(
                    r"""
                    ## Text in, text out

                    The most important mental model for working with LLMs: **an LLM is a
                    text-in, text-out machine.** It never executes code, calls functions,
                    or accesses databases directly. When we say "the model calls a tool,"
                    what actually happens is:

                    1. The model outputs **text** that *looks like* a function call.
                    2. A **wrapper** (our Python code) parses that text and runs the real function.
                    3. The result is converted back to **text** and fed into the next LLM call.

                    <div style="background:#0f172a;border-radius:0.6rem;padding:1.2rem;margin-top:0.8rem;">
                    <svg width="100%" height="170" viewBox="0 0 620 170" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="10" y="60" width="90" height="44" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>
                      <text x="55" y="87" text-anchor="middle" fill="#e2e8f0" font-size="11" font-family="monospace">text</text>
                      <path d="M100 82 L125 82" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow1)"/>
                      <rect x="130" y="50" width="80" height="64" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
                      <text x="170" y="87" text-anchor="middle" fill="#38bdf8" font-size="16" font-weight="700" font-family="monospace">LLM</text>
                      <path d="M210 82 L235 82" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow1)"/>
                      <rect x="240" y="60" width="90" height="44" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>
                      <text x="285" y="87" text-anchor="middle" fill="#e2e8f0" font-size="11" font-family="monospace">text</text>
                      <path d="M285 104 L285 125" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow1)"/>
                      <rect x="220" y="130" width="130" height="32" rx="6" fill="#0f172a" stroke="#fbbf24" stroke-width="2"/>
                      <text x="285" y="151" text-anchor="middle" fill="#fbbf24" font-size="11" font-family="monospace">Python wrapper</text>
                      <path d="M350 146 L380 146" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow1)"/>
                      <rect x="385" y="130" width="110" height="32" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="2"/>
                      <text x="440" y="151" text-anchor="middle" fill="#34d399" font-size="11" font-family="monospace">function()</text>
                      <path d="M440 130 L440 104" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow1)"/>
                      <rect x="395" y="60" width="90" height="44" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>
                      <text x="440" y="87" text-anchor="middle" fill="#e2e8f0" font-size="11" font-family="monospace">result</text>
                      <path d="M395 82 L370 82 Q360 82 360 72 L210 72" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>
                      <text x="285" y="52" text-anchor="middle" fill="#cbd5e1" font-size="9" font-family="monospace">model output</text>
                      <text x="440" y="52" text-anchor="middle" fill="#cbd5e1" font-size="9" font-family="monospace">fed back as text</text>
                      <defs>
                        <marker id="arrow1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
                          <path d="M0,0 L8,4 L0,8" fill="#94a3b8"/>
                        </marker>
                      </defs>
                    </svg>
                    </div>

                    Keep this in mind throughout the tutorial. Parts 3 and 4 will show how
                    the wrapper layer works — but the LLM itself is always just reading and
                    writing text.
                    """
                )
            ),
            mo.callout(
                mo.md(
                    "**Check your understanding:** If an LLM can't run code, how does "
                    'ChatGPT "browse the web" or "run Python"?\n\n'
                    "The chat interface has a **wrapper** that intercepts the model's "
                    'text output, detects commands like `browse("url")`, executes them, '
                    "and feeds the results back as text. The model never touches the "
                    "browser or the Python interpreter directly."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def ex1_header():
    mo.md(
        dedent("""
        ## Exercise 1 — Prompt components

        As described in the discussion, we have our various prompt "components", roughly summarized from the guidance literature:

        **Identity**: Gives the model its identity and constraints.

        **Instructions**: Directs the model on what to do.

        **Examples**: Any examples of how we want the model to answer.

        **Context**: Relevant context, more on that later.

        **User Query**: The user's query.  We may want to leave this a placeholder, and fill in on request.

        The preview cell shows the assembled messages the model receives.
        """)
    )
    return


@app.cell
def ex1_prompt_components():
    # @spec PROMPT-SYS-002
    # @spec PROMPT-SYS-011
    _DEFAULT_IDENTITY = "You are a helpful assistant."

    _DEFAULT_INSTRUCTIONS = "Answer the user's question directly."

    _DEFAULT_EXAMPLES = "User: Hello!\nResponse: Hi, how can I help you?"

    _DEFAULT_CONTEXT = "There's a world cup watch party tonight at 7pm"

    _DEFAULT_USER_QUERY = "What's going on tonight?"

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
    user_query = mo.ui.text_area(
        value=_DEFAULT_USER_QUERY, label="User Query:", full_width=True
    )
    # @spec PROMPT-SYS-012
    run_ex1 = mo.ui.run_button(label="Run Exercise 1")
    mo.vstack([identity, instructions, examples, context, user_query, run_ex1])
    return context, examples, identity, instructions, run_ex1, user_query


@app.cell
def ex1_preview(context, examples, identity, instructions, user_query):
    system_prompt, model_prompt, messages = prepare_prompt(
        identity.value,
        instructions.value,
        examples.value,
        context.value,
        user_query.value,
    )

    mo.md(format_messages_preview(messages))
    return model_prompt, system_prompt


@app.cell
def ex1_run(model_prompt, run_ex1, system_prompt):
    mo.stop(
        not run_ex1.value,
        mo.md("_Click **Run Exercise 1** to call the LLM._"),
    )

    bot = make_bot(system_prompt)
    response = bot(model_prompt)
    mo.md(format_messages_preview([response]))
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent("""
        ## Exercise 2 — Research summarization with citation context

        Same five prompt fields as Exercise 1 — but now with **research-relevant defaults**:

        - **Identity** is a research-assistant system prompt (try editing the constraints).
        - **Instructions** direct the model to summarize using only the citation metadata in Context.
        - **Examples** a simple templated response
        - **Context** is pre-loaded with citation metadata from our library.
        - **User Query** is the research question to answer (e.g. what the paper is about).

        Edit any field and watch the preview update. Click **Run Exercise 2** when ready.
        """)
    )
    return


@app.cell(hide_code=True)
def ex2_prompt_components():
    # @spec PROMPT-SUM-010
    _DEFAULT_IDENTITY_2 = "You are a careful research assistant helping a scientist synthesize literature.\n\nConstraints:\n- Ground every claim in the provided citation metadata.\n- If evidence is insufficient, say so explicitly.\n- Prefer concise, structured markdown with short sections and bullet points.\n- Do not invent citations, DOIs, or findings not supported by the context."

    _DEFAULT_INSTRUCTIONS_2 = (
        "Answer the user's question using only the citation metadata in Context."
    )

    _DEFAULT_EXAMPLES_2 = (
        "User: What is this paper about?\n"
        "Context: <citation>\n"
        "Assistant: The paper is about <summary>"
    )

    _DEFAULT_USER_QUERY_2 = "What is this paper about?"

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
    user_query2 = mo.ui.text_area(
        value=_DEFAULT_USER_QUERY_2, label="User Query:", full_width=True
    )
    # @spec PROMPT-SUM-011
    run_ex2 = mo.ui.run_button(label="Run Exercise 2")
    mo.vstack([identity2, instructions2, examples2, context2, user_query2, run_ex2])
    return context2, examples2, identity2, instructions2, run_ex2, user_query2


@app.cell
def ex2_preview(context2, examples2, identity2, instructions2, user_query2):
    system_prompt2, model_prompt2, messages2 = prepare_prompt(
        identity2.value,
        instructions2.value,
        examples2.value,
        context2.value,
        user_query2.value,
    )

    mo.md(format_messages_preview(messages2))
    return model_prompt2, system_prompt2


@app.cell
def ex2_run(model_prompt2, run_ex2, system_prompt2):
    mo.stop(
        not run_ex2.value,
        mo.md("_Click **Run Exercise 2** to call the LLM._"),
    )

    # @spec PROMPT-SUM-012
    bot2 = make_bot(system_prompt2)
    response2 = bot2(model_prompt2)
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


@app.cell(hide_code=True)
def ex3_prompt_components(examples2, identity2, instructions2, user_query2):
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
    mo.vstack([identity2, instructions2, examples2, context3, user_query2, run_ex3])
    return context3, run_ex3


@app.cell
def ex3_preview(context3, examples2, identity2, instructions2, user_query2):
    system_prompt3, model_prompt3, messages3 = prepare_prompt(
        identity2.value,
        instructions2.value,
        examples2.value,
        context3.value,
        user_query2.value,
    )

    # @spec PROMPT-SUM-014
    mo.md(format_messages_preview(messages3))
    return model_prompt3, system_prompt3


@app.cell
def ex3_run(model_prompt3, run_ex3, system_prompt3):
    mo.stop(
        not run_ex3.value,
        mo.md("_Click **Run Exercise 3** to call the LLM._"),
    )

    # @spec PROMPT-SUM-015
    bot3 = make_bot(system_prompt3)
    response3 = bot3(model_prompt3)
    mo.md(format_messages_preview([response3]))
    return


@app.cell(hide_code=True)
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
