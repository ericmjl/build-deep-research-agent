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

    # Two models: small for Parts 1-2 (Ben), large for Parts 3-5 (Eric).
    SMALL_MODEL = "gemma2:2b"
    LARGE_MODEL = "gemma4:12b"

    # Local: ollama_chat/ prefix so llamabot detects Ollama and sets
    # tool_choice="auto" (reliable tool calling).
    LLM_MODEL_SMALL_LOCAL = f"ollama_chat/{SMALL_MODEL}"
    LLM_MODEL_LARGE_LOCAL = f"ollama_chat/{LARGE_MODEL}"
    TUTORIAL_LLM_API_KEY_LOCAL = "ollama-no-auth"

    # Remote: openai/ prefix — the Modal endpoint exposes an
    # OpenAI-compatible API, not Ollama's native protocol.
    REMOTE_BASE_URL_DEFAULT = (
        "https://ericmjl--ollama-service-ollamaservice-server.modal.run/v1"
    )
    LLM_MODEL_SMALL_REMOTE = f"openai/{SMALL_MODEL}"
    LLM_MODEL_LARGE_REMOTE = f"openai/{LARGE_MODEL}"

    # RAM threshold for the large model (gemma4:12b needs ~8 GB just for
    # weights; 32 GB total leaves headroom for the OS and context window).
    MIN_RAM_GB = 32
    return (
        LLM_MODEL_LARGE_LOCAL,
        LLM_MODEL_LARGE_REMOTE,
        LLM_MODEL_SMALL_LOCAL,
        LLM_MODEL_SMALL_REMOTE,
        LARGE_MODEL,
        MIN_RAM_GB,
        OLLAMA_TAGS_URL,
        OLLAMA_V1_URL,
        REMOTE_BASE_URL_DEFAULT,
        SMALL_MODEL,
        TUTORIAL_LLM_API_KEY_LOCAL,
    )


@app.cell(hide_code=True)
def title():
    mo.md("""
    # Environment check

    This notebook detects whether **Ollama** is available locally with the two
    models this tutorial uses:

    | Model | Size | Used in | Env var |
    |-------|------|---------|---------|
    | **gemma2:2b** | ~1.6 GB | Parts 1–2 (prompting, memory) | `LLM_MODEL_SMALL` |
    | **gemma4:12b** | ~8 GB | Parts 3–5 (tools, workflows, multi-agent) | `LLM_MODEL_LARGE` |

    Pick **local** (preferred) or **remote Modal endpoint**, and this notebook
    writes `.env` with both model variables set. It then pings each model to
    verify the endpoint works.

    Once you see **Environment ready**, continue to `01_intro_prompting`.
    """)
    return


@app.cell(hide_code=True)
def detect_ollama(LARGE_MODEL, MIN_RAM_GB, OLLAMA_TAGS_URL, SMALL_MODEL):
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

    def _has_model(name: str, models: list[str]) -> bool:
        return any(m == name or m.startswith(name + ":") for m in models)

    has_small = _has_model(SMALL_MODEL, available_models)
    has_large = _has_model(LARGE_MODEL, available_models)

    # System RAM check (psutil can flake on macOS — fall back gracefully).
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        has_enough_ram = total_ram_gb >= MIN_RAM_GB
    except Exception:  # noqa: BLE001
        total_ram_gb = 0.0
        has_enough_ram = True  # assume sufficient if we can't measure

    # Recommend local only if Ollama is running and at least the small model is pulled.
    local_recommended = ollama_reachable and has_small

    # --- Detection summary UI ---
    if ollama_reachable:

        def _model_line(name: str, found: bool) -> str:
            if found:
                return f"Found **{name}**."
            return f"**{name} not found.** Pull it with `ollama pull {name}`."

        ram_line = (
            f"System RAM: **{total_ram_gb:.1f} GB** "
            f"({'sufficient for large model' if has_enough_ram else f'below {MIN_RAM_GB} GB — large model will be slow/unavailable locally'})."
            if total_ram_gb
            else "System RAM: unable to measure (psutil error)."
        )
        ollama_status = mo.callout(
            mo.md(
                f"**Ollama detected** at `{OLLAMA_TAGS_URL}`\n\n"
                f"{_model_line(SMALL_MODEL, has_small)}\n\n"
                f"{_model_line(LARGE_MODEL, has_large)}\n\n{ram_line}"
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
                f"2. Pull the small model: `ollama pull {SMALL_MODEL}`\n"
                f"3. (Optional) Pull the large model: `ollama pull {LARGE_MODEL}`\n\n"
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
            "local": "Local Ollama (gemma2:2b + gemma4:12b on this machine)",
            "remote": "Remote endpoint (shared Modal server — both models)",
        },
        value="local" if local_recommended else "remote",
        label="Where should the tutorial LLMs run?",
    )

    save_env = mo.ui.run_button(label="Write .env and test")

    mo.vstack([source, save_env])
    return save_env, source


@app.cell(hide_code=True)
def env_check(
    LLM_MODEL_LARGE_LOCAL,
    LLM_MODEL_LARGE_REMOTE,
    LLM_MODEL_SMALL_LOCAL,
    LLM_MODEL_SMALL_REMOTE,
    OLLAMA_V1_URL,
    REMOTE_BASE_URL_DEFAULT,
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
                f"LLM_MODEL_SMALL={LLM_MODEL_SMALL_LOCAL}",
                f"LLM_MODEL_LARGE={LLM_MODEL_LARGE_LOCAL}",
                f"TUTORIAL_LLM_BASE_URL={OLLAMA_V1_URL}",
                f"TUTORIAL_LLM_API_KEY={TUTORIAL_LLM_API_KEY_LOCAL}",
            ]
        else:
            lines = [
                f"LLM_MODEL_SMALL={LLM_MODEL_SMALL_REMOTE}",
                f"LLM_MODEL_LARGE={LLM_MODEL_LARGE_REMOTE}",
                f"TUTORIAL_LLM_BASE_URL={REMOTE_BASE_URL_DEFAULT}",
            ]
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        load_dotenv(dotenv_path=env_path, override=True)

    # --- Read back from env ---
    active_small = os.getenv("LLM_MODEL_SMALL", "").strip()
    active_large = os.getenv("LLM_MODEL_LARGE", "").strip()
    active_base_url = os.getenv("TUTORIAL_LLM_BASE_URL", "").strip()

    has_env = env_path.exists() and bool(active_small) and bool(active_large)

    if not has_env:
        result = mo.callout(
            mo.md(
                "Pick **Local** or **Remote** above, then click "
                "**Write .env and test**."
            ),
            kind="danger",
        )
    else:
        # --- Full integration test: call SimpleBot for each model ---
        from llamabot import SimpleBot

        from build_deep_research_agent.llm import (
            get_completion_kwargs,
            get_large_model_name,
            get_small_model_name,
        )

        results = []
        all_ok = True
        for label, model_name in [
            ("small", get_small_model_name()),
            ("large", get_large_model_name()),
        ]:
            try:
                test_bot = SimpleBot(
                    system_prompt="Reply with READY and nothing else.",
                    model_name=model_name,
                    **get_completion_kwargs(),
                )
                response = test_bot("Reply with READY.")
                reply = (
                    response.content.strip()
                    if hasattr(response, "content")
                    else str(response).strip()
                )
                results.append(f"- **{label}** (`{model_name}`): `{reply[:60]}`")
            except Exception as exc:  # noqa: BLE001
                all_ok = False
                results.append(f"- **{label}** (`{model_name}`): **FAILED** — `{exc}`")

        kind = "success" if all_ok else "danger"
        header = "**Environment ready**" if all_ok else "**Some models failed**"
        result = mo.callout(
            mo.md(
                f"{header}\n\n"
                f"Small model: `{active_small}`\n\n"
                f"Large model: `{active_large}`\n\n"
                f"Endpoint: `{active_base_url}`\n\n" + "\n".join(results)
            ),
            kind=kind,
        )

    result
    return


if __name__ == "__main__":
    app.run()
