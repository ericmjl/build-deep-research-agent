# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "python-dotenv",
#     "psutil",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import json
    import os
    from pathlib import Path
    from urllib.error import URLError
    from urllib.request import Request, urlopen

    import marimo as mo
    import psutil
    from dotenv import load_dotenv

    env_path = Path(".env")


@app.cell(hide_code=True)
def constants():
    # Constants for environment detection and endpoint configuration.
    OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
    OLLAMA_V1_URL = "http://localhost:11434/v1"
    GEMMA4_MODEL = "gemma4:12b"

    # Local: use ollama_chat/ prefix so llamabot detects Ollama and sets
    # tool_choice="auto" (reliable tool calling with gemma4:12b).
    LLM_MODEL_FOR_LOCAL = f"ollama_chat/{GEMMA4_MODEL}"
    TUTORIAL_LLM_API_KEY_LOCAL = "ollama-no-auth"

    # Remote: use openai/ prefix — the Modal endpoint exposes an
    # OpenAI-compatible API, not Ollama's native protocol.
    REMOTE_BASE_URL_DEFAULT = (
        "https://nll-ai--ollama-service-ollamaservice-server.modal.run/v1"
    )
    REMOTE_MODEL_DEFAULT = f"openai/{GEMMA4_MODEL}"

    MIN_RAM_GB = 8
    return (
        GEMMA4_MODEL,
        LLM_MODEL_FOR_LOCAL,
        MIN_RAM_GB,
        OLLAMA_TAGS_URL,
        OLLAMA_V1_URL,
        REMOTE_BASE_URL_DEFAULT,
        REMOTE_MODEL_DEFAULT,
        TUTORIAL_LLM_API_KEY_LOCAL,
    )


@app.cell(hide_code=True)
def title():
    mo.md("""
    # Environment check

    This notebook detects whether **Ollama + gemma4:12b** is available locally
    and helps you choose between **local** (preferred) and a **remote endpoint**
    (fallback). It writes `.env` based on your choice and pings the endpoint.

    Once you see **Environment ready**, continue to `01_intro_prompting`.
    """)
    return


@app.cell(hide_code=True)
def detect_ollama(GEMMA4_MODEL, MIN_RAM_GB, OLLAMA_TAGS_URL):
    # @spec TUT-INFRA-006
    # Probe the local Ollama server for available models.
    ollama_reachable = False
    available_models: list[str] = []
    detect_error = ""

    try:
        req = Request(OLLAMA_TAGS_URL, method="GET")
        with urlopen(req, timeout=3) as tag_resp:
            data = json.loads(tag_resp.read().decode("utf-8"))
        ollama_reachable = True
        available_models = [m["name"] for m in data.get("models", [])]
    except URLError:
        pass  # Ollama not running — normal on machines without it.
    except Exception as exc:  # noqa: BLE001
        detect_error = str(exc)

    has_gemma4 = any(
        m == GEMMA4_MODEL or m.startswith(GEMMA4_MODEL + ":") for m in available_models
    )

    # System RAM check (psutil can flake on macOS — fall back gracefully).
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        has_enough_ram = total_ram_gb >= MIN_RAM_GB
    except Exception:  # noqa: BLE001
        total_ram_gb = 0.0
        has_enough_ram = True  # assume sufficient if we can't measure

    # Recommend local only if Ollama is running and model is pulled.
    # (Skip RAM gate if psutil failed — Ollama won't serve what it can't fit.)
    local_recommended = ollama_reachable and has_gemma4 and has_enough_ram

    # --- Detection summary UI ---
    if ollama_reachable:
        model_line = (
            f"Found **{GEMMA4_MODEL}** among {len(available_models)} model(s)."
            if has_gemma4
            else f"**{GEMMA4_MODEL} not found.** Pull it with `ollama pull {GEMMA4_MODEL}`."
        )
        ram_line = (
            f"System RAM: **{total_ram_gb:.1f} GB** "
            f"({'sufficient' if has_enough_ram else f'below recommended {MIN_RAM_GB} GB — local serving may be slow'})."
            if total_ram_gb
            else "System RAM: unable to measure (psutil error)."
        )
        ollama_status = mo.callout(
            mo.md(
                f"**Ollama detected** at `{OLLAMA_TAGS_URL}`\n\n"
                f"{model_line}\n\n{ram_line}"
            ),
            kind="success" if local_recommended else "warn",
        )
    else:
        hint = detect_error or "No Ollama server at `localhost:11434`."
        ollama_status = mo.callout(
            mo.md(
                f"**Ollama not detected locally.**\n\n{hint}\n\n"
                "To run locally:\n"
                "1. Install Ollama — see [ollama.com](https://ollama.com)\n"
                f"2. Pull the model: `ollama pull {GEMMA4_MODEL}`\n\n"
                "Or use the remote endpoint below."
            ),
            kind="warn",
        )

    ollama_status
    return (local_recommended,)


@app.cell(hide_code=True)
def choice_form(local_recommended):
    # Default selection: local if recommended, otherwise remote.
    source = mo.ui.radio(
        options={
            "local": "Local Ollama (gemma4:12b on this machine)",
            "remote": "Remote endpoint (shared Modal server)",
        },
        value="local" if local_recommended else "remote",
        label="Where should the tutorial LLM run?",
    )

    save_env = mo.ui.run_button(label="Write .env and test")

    mo.vstack([source, save_env])
    return save_env, source


@app.cell(hide_code=True)
def env_check(
    LLM_MODEL_FOR_LOCAL,
    OLLAMA_V1_URL,
    REMOTE_BASE_URL_DEFAULT,
    REMOTE_MODEL_DEFAULT,
    TUTORIAL_LLM_API_KEY_LOCAL,
    save_env,
    source,
):
    # --- Load existing .env if present ---
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)

    # --- Write .env when the user clicks the button ---
    if save_env.value:
        is_local = "local" in source.value.lower()
        if is_local:
            lines = [
                f"LLM_MODEL={LLM_MODEL_FOR_LOCAL}",
                f"TUTORIAL_LLM_BASE_URL={OLLAMA_V1_URL}",
                f"TUTORIAL_LLM_API_KEY={TUTORIAL_LLM_API_KEY_LOCAL}",
            ]
        else:
            lines = [
                f"LLM_MODEL={REMOTE_MODEL_DEFAULT}",
                f"TUTORIAL_LLM_BASE_URL={REMOTE_BASE_URL_DEFAULT}",
            ]
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        load_dotenv(dotenv_path=env_path, override=True)

    # --- Read back from env ---
    active_model = os.getenv("LLM_MODEL", "").strip()
    active_base_url = os.getenv("TUTORIAL_LLM_BASE_URL", "").strip()

    has_env = env_path.exists() and bool(active_model) and bool(active_base_url)

    if not has_env:
        result = mo.callout(
            mo.md(
                "Pick **Local** or **Remote** above, then click "
                "**Write .env and test**."
            ),
            kind="danger",
        )
    else:
        # --- Full integration test: call SimpleBot through llamabot/litellm ---
        # This verifies the model prefix (ollama_chat/ vs openai/), api_base,
        # api_key, and structured-output registration all work together.
        from llamabot import SimpleBot

        from build_deep_research_agent.llm import (
            get_completion_kwargs,
            get_model_name,
        )

        try:
            test_bot = SimpleBot(
                system_prompt="Reply with READY and nothing else.",
                model_name=get_model_name(),
                **get_completion_kwargs(),
            )
            response = test_bot("Reply with READY.")
            reply = (
                response.content.strip()
                if hasattr(response, "content")
                else str(response).strip()
            )
            result = mo.callout(
                mo.md(
                    f"**Environment ready**\n\n"
                    f"Model: `{active_model}`\n\n"
                    f"Endpoint: `{active_base_url}`\n\n"
                    f"LLM replied: `{reply[:80]}`"
                ),
                kind="success",
            )
        except Exception as exc:
            result = mo.callout(
                mo.md(
                    f"**LLM call failed.**\n\n"
                    f"Model: `{active_model}`\n"
                    f"Endpoint: `{active_base_url}`\n\n"
                    f"```\n{exc}\n```"
                ),
                kind="danger",
            )

    result
    return


if __name__ == "__main__":
    app.run()
