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
def startup_validation():
    import json
    import os
    from pathlib import Path
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    from dotenv import load_dotenv

    # @spec TUT-INFRA-006
    env_path = Path(".env")

    readme_defaults = {
        "LLM_MODEL": "",
        "TUTORIAL_LLM_BASE_URL": "",
    }
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_lines = readme_path.read_text(encoding="utf-8").splitlines()
        for line in readme_lines:
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key in readme_defaults:
                readme_defaults[key] = value.strip()

    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

    required_vars = (
        "TUTORIAL_LLM_BASE_URL",
        "LLM_MODEL",
    )
    env_values = {name: os.getenv(name, "").strip() for name in required_vars}
    api_key = os.getenv("TUTORIAL_LLM_API_KEY", "").strip()
    missing_vars = [name for name, value in env_values.items() if not value]

    if not env_path.exists() or missing_vars:
        base_url_input = mo.ui.text(
            value=env_values["TUTORIAL_LLM_BASE_URL"]
            or readme_defaults["TUTORIAL_LLM_BASE_URL"],
            label="TUTORIAL_LLM_BASE_URL",
            full_width=True,
        )
        model_input = mo.ui.text(
            value=env_values["LLM_MODEL"] or readme_defaults["LLM_MODEL"],
            label="LLM_MODEL",
            full_width=True,
        )
        api_key_input = mo.ui.text(
            value=api_key,
            label="TUTORIAL_LLM_API_KEY (optional for shared tutorial endpoint)",
            kind="password",
            full_width=True,
        )
        save_env = mo.ui.run_button(label="Write .env from these values")

        issues: list[str] = []
        if not env_path.exists():
            issues.append("- `.env` was not found in the repository root.")
        if missing_vars:
            issues.append(
                "- Missing required environment variable(s):\n"
                + "\n".join(f"  - `{name}`" for name in missing_vars)
            )

        mo.callout(
            mo.md(
                "❌ **Environment not ready**\n\n" + "\n".join(issues) + "\n\n"
                "Paste values below (defaults are copied from the README), then click "
                "**Write .env from these values**."
            ),
            kind="warn",
        )
        mo.vstack([base_url_input, model_input, api_key_input, save_env])
        mo.stop(not save_env.value)

        lines = [
            f"LLM_MODEL={model_input.value.strip()}",
            f"TUTORIAL_LLM_BASE_URL={base_url_input.value.strip()}",
        ]
        if api_key_input.value.strip():
            lines.append(f"TUTORIAL_LLM_API_KEY={api_key_input.value.strip()}")

        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        load_dotenv(dotenv_path=env_path, override=True)
        mo.callout(
            mo.md("✅ Wrote `.env` and loaded it into this notebook session."),
            kind="success",
        )

        env_values = {name: os.getenv(name, "").strip() for name in required_vars}
        api_key = os.getenv("TUTORIAL_LLM_API_KEY", "").strip()

    model_name = env_values["LLM_MODEL"]
    base_url = env_values["TUTORIAL_LLM_BASE_URL"].rstrip("/")
    endpoint = f"{base_url}/chat/completions"

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "Reply with READY."}],
        "max_tokens": 8,
        "temperature": 0,
    }
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = "Bearer " + api_key

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    ENDPOINT_PING_TIMEOUT_SECONDS = 20

    try:
        with urlopen(request, timeout=ENDPOINT_PING_TIMEOUT_SECONDS) as _resp:
            status_code = _resp.status
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace").strip()
        error_detail = (
            f"\n\nEndpoint response snippet:\n```\n{error_body[:400]}\n```"
            if error_body
            else ""
        )
        mo.callout(
            mo.md(
                "❌ **Environment not ready**\n\n"
                f"LLM endpoint ping failed with HTTP status `{exc.code}`."
                f"{error_detail}\n\n"
                "**Fix:**\n"
                "- Verify `TUTORIAL_LLM_BASE_URL` points to a running OpenAI-compatible `/v1` endpoint.\n"
                "- Verify `LLM_MODEL` is available on that endpoint.\n"
                "- If your endpoint requires auth, set `TUTORIAL_LLM_API_KEY` and rerun this cell."
            ),
            kind="danger",
        )
    except URLError as exc:
        reason = str(exc.reason) if getattr(exc, "reason", None) else str(exc)
        mo.callout(
            mo.md(
                "❌ **Environment not ready**\n\n"
                f"Could not reach the configured LLM endpoint (`{reason}`).\n\n"
                "**Fix:** Verify `TUTORIAL_LLM_BASE_URL` and your network connection, then rerun this cell."
            ),
            kind="danger",
        )
    else:
        if 200 <= status_code < 300:
            mo.callout(mo.md("✓ Environment ready"), kind="success")
        else:
            mo.callout(
                mo.md(
                    "❌ **Environment not ready**\n\n"
                    f"LLM endpoint ping returned unexpected status `{status_code}`.\n\n"
                    "**Fix:** Confirm endpoint availability and credentials, then rerun this cell."
                ),
                kind="danger",
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
