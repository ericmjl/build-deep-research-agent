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

    # --- Ollama ---
    OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
    OLLAMA_V1_URL = "http://localhost:11434/v1"

    # --- LM Studio ---
    LMSTUDIO_V1_URL = "http://localhost:1234/v1"
    LMSTUDIO_MODELS_URL = "http://localhost:1234/v1/models"

    # Ollama model tags (used with the ollama_chat/ litellm prefix).
    SMALL_MODEL_OLLAMA = "gemma2:2b"
    LARGE_MODEL_OLLAMA = "gemma4:12b"

    # LM Studio recommended models (HuggingFace-style identifiers).
    # Search for these in LM Studio's Discover tab, or run:
    #   lms get google/gemma-2-2b-it
    #   lms get google/gemma-3-12b-it
    SMALL_MODEL_LMSTUDIO = "google/gemma-2-2b-it"
    LARGE_MODEL_LMSTUDIO = "google/gemma-3-12b-it"

    # litellm model strings for .env.
    # Ollama: ollama_chat/ prefix → litellm's native adapter, reliable tool calling.
    LLM_MODEL_SMALL_OLLAMA = f"ollama_chat/{SMALL_MODEL_OLLAMA}"
    LLM_MODEL_LARGE_OLLAMA = f"ollama_chat/{LARGE_MODEL_OLLAMA}"
    OLLAMA_API_KEY = "ollama-no-auth"

    # LM Studio: openai/ prefix — LM Studio exposes an OpenAI-compatible API.
    # api_base is set via TUTORIAL_LLM_BASE_URL in .env; llm.py already handles this.
    LMSTUDIO_API_KEY = "lm-studio"

    # Remote: openai/ prefix — Modal endpoint exposes OpenAI-compatible API.
    REMOTE_BASE_URL_DEFAULT = (
        "https://nll-ai--ollama-service-ollamaservice-server.modal.run/v1"
    )
    LLM_MODEL_SMALL_REMOTE = f"openai/{SMALL_MODEL_OLLAMA}"
    LLM_MODEL_LARGE_REMOTE = f"openai/{LARGE_MODEL_OLLAMA}"

    # RAM threshold for the large model (gemma4:12b needs ~8 GB just for
    # weights; 32 GB total leaves headroom for the OS and context window).
    MIN_RAM_GB = 32
    return (
        LARGE_MODEL_LMSTUDIO,
        LARGE_MODEL_OLLAMA,
        LLM_MODEL_LARGE_OLLAMA,
        LLM_MODEL_LARGE_REMOTE,
        LLM_MODEL_SMALL_OLLAMA,
        LLM_MODEL_SMALL_REMOTE,
        LMSTUDIO_API_KEY,
        LMSTUDIO_MODELS_URL,
        LMSTUDIO_V1_URL,
        MIN_RAM_GB,
        OLLAMA_API_KEY,
        OLLAMA_TAGS_URL,
        OLLAMA_V1_URL,
        REMOTE_BASE_URL_DEFAULT,
        SMALL_MODEL_LMSTUDIO,
        SMALL_MODEL_OLLAMA,
    )


@app.cell(hide_code=True)
def title():
    mo.md("""
    # Environment check

    This notebook detects local LLM servers and writes `.env` with the right
    model configuration. It checks in **priority order**:

    1. **Ollama** (preferred) — native litellm adapter, reliable tool calling.
    2. **LM Studio** — OpenAI-compatible API, good GUI for model management.
    3. **Remote endpoint** — shared Modal server, always available as fallback.

    The tutorial uses **two models**:

    | Role | Ollama tag | LM Studio ID | Size | Parts |
    |------|-----------|--------------|------|-------|
    | Small | `gemma2:2b` | `google/gemma-2-2b-it` | ~1.6 GB | 1–2 |
    | Large | `gemma4:12b` | `google/gemma-3-12b-it` | ~8 GB | 3–5 |

    Once you see **Environment ready**, continue to `01_intro_prompting`.
    """)
    return


@app.cell(hide_code=True)
def detect_local(
    LARGE_MODEL_OLLAMA,
    LMSTUDIO_MODELS_URL,
    LMSTUDIO_V1_URL,
    MIN_RAM_GB,
    OLLAMA_TAGS_URL,
    SMALL_MODEL_OLLAMA,
):
    # @spec TUT-INFRA-006
    # Probe local LLM servers in priority order: Ollama first, then LM Studio.

    # --- Ollama detection ---
    ollama_reachable = False
    ollama_models: list[str] = []
    ollama_error = ""

    try:
        req = Request(OLLAMA_TAGS_URL, method="GET")
        with urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        ollama_reachable = True
        ollama_models = [m["name"] for m in data.get("models", [])]
    except URLError:
        pass
    except Exception as exc:  # noqa: BLE001
        ollama_error = str(exc)

    def _has_model(name: str, models: list[str]) -> bool:
        return any(m == name or m.startswith(name + ":") for m in models)

    ollama_has_small = _has_model(SMALL_MODEL_OLLAMA, ollama_models)
    ollama_has_large = _has_model(LARGE_MODEL_OLLAMA, ollama_models)

    # --- LM Studio detection ---
    # LM Studio exposes an OpenAI-compatible API at localhost:1234.
    # GET /v1/models returns the currently loaded models.
    lmstudio_reachable = False
    lmstudio_model_ids: list[str] = []

    try:
        req2 = Request(LMSTUDIO_MODELS_URL, method="GET")
        with urlopen(req2, timeout=3) as resp2:
            lms_data = json.loads(resp2.read().decode("utf-8"))
        lmstudio_reachable = True
        # OpenAI-compatible /v1/models returns {"data": [{"id": "..."}, ...]}
        raw_models = (
            lms_data.get("data", []) if isinstance(lms_data, dict) else lms_data
        )
        lmstudio_model_ids = [m.get("id", str(m)) for m in raw_models]
    except URLError:
        pass
    except Exception:  # noqa: BLE001
        pass

    # --- RAM check (psutil can flake on macOS — fall back gracefully) ---
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        has_enough_ram = total_ram_gb >= MIN_RAM_GB
    except Exception:  # noqa: BLE001
        total_ram_gb = 0.0
        has_enough_ram = True

    # --- Priority: Ollama > LM Studio > Remote ---
    if ollama_reachable and ollama_has_small:
        local_default = "ollama"
    elif lmstudio_reachable and len(lmstudio_model_ids) > 0:
        local_default = "lmstudio"
    else:
        local_default = "remote"

    # --- Detection summary UI ---
    sections = []

    # Ollama section
    if ollama_reachable:

        def _model_line(name: str, found: bool) -> str:
            if found:
                return f"Found **{name}**."
            return f"**{name}** not found — pull it: `ollama pull {name}`"

        ram_line = (
            f"System RAM: **{total_ram_gb:.1f} GB** "
            f"({'sufficient for large model' if has_enough_ram else f'below {MIN_RAM_GB} GB — large model may be slow/unavailable locally'})"
            if total_ram_gb
            else "System RAM: unable to measure."
        )
        sections.append(
            mo.callout(
                mo.md(
                    f"**Ollama detected** at `{OLLAMA_TAGS_URL}`\n\n"
                    f"{_model_line(SMALL_MODEL_OLLAMA, ollama_has_small)}\n\n"
                    f"{_model_line(LARGE_MODEL_OLLAMA, ollama_has_large)}\n\n{ram_line}"
                ),
                kind="success" if ollama_has_small else "warn",
            )
        )
    else:
        hint = ollama_error or "No Ollama server at `localhost:11434`."
        sections.append(
            mo.callout(
                mo.md(
                    f"**Ollama not detected.**\n\n{hint}\n\n"
                    "Install Ollama: [ollama.com](https://ollama.com)\n"
                    f"Pull models: `ollama pull {SMALL_MODEL_OLLAMA}`"
                ),
                kind="neutral",
            )
        )

    # LM Studio section
    if lmstudio_reachable:
        if lmstudio_model_ids:
            model_list = "\n".join(f"- `{mid}`" for mid in lmstudio_model_ids)
        else:
            model_list = (
                "*(no models loaded — download and load a model in LM Studio's GUI)*"
            )
        sections.append(
            mo.callout(
                mo.md(
                    f"**LM Studio detected** at `{LMSTUDIO_V1_URL}`\n\n"
                    f"Loaded models:\n{model_list}"
                ),
                kind="success" if lmstudio_model_ids else "warn",
            )
        )
    else:
        sections.append(
            mo.callout(
                mo.md(
                    "**LM Studio not detected.**\n\n"
                    "No server at `localhost:1234`. "
                    "Install: [lmstudio.ai](https://lmstudio.ai)"
                ),
                kind="neutral",
            )
        )

    mo.vstack(sections)
    return (
        lmstudio_model_ids,
        lmstudio_reachable,
        local_default,
        ollama_reachable,
    )


@app.cell(hide_code=True)
def choice_form(
    LARGE_MODEL_OLLAMA,
    SMALL_MODEL_OLLAMA,
    lmstudio_reachable,
    local_default,
    ollama_reachable,
):
    # Build radio options based on what was detected.
    options = {}
    if ollama_reachable:
        options["ollama"] = (
            f"Local — Ollama ({SMALL_MODEL_OLLAMA} + {LARGE_MODEL_OLLAMA})"
        )
    if lmstudio_reachable:
        options["lmstudio"] = "Local — LM Studio"
    options["remote"] = "Remote endpoint (shared Modal server)"

    source = mo.ui.radio(
        options=options,
        value=local_default if local_default in options else "remote",
        label="Where should the tutorial LLMs run?",
    )

    save_env = mo.ui.run_button(label="Write .env and test")

    mo.vstack([source, save_env])
    return save_env, source


@app.cell(hide_code=True)
def lmstudio_setup_guide():
    mo.accordion(
        {
            "How to download models in LM Studio (optional)": mo.md(
                """
                LM Studio has a built-in model catalog. You can download models
                via the GUI or the `lms` CLI.

                **GUI:**

                1. Open LM Studio → **Discover** tab.
                2. Search for the model ID (e.g. `google/gemma-2-2b-it`).
                3. Click **Download**, pick a quantization (Q4_K_M is a good
                   speed/quality balance).
                4. Go to the **Chat** tab, select the model, and click **Load**.

                **CLI** (`lms` ships with LM Studio — run LM Studio at least once first):

                ```bash
                lms get google/gemma-2-2b-it      # small — Parts 1–2
                lms get google/gemma-3-12b-it      # large — Parts 3–5
                lms load google/gemma-2-2b-it      # load into memory
                ```

                > **Important:** a model must be **loaded** (not just downloaded)
                > before it appears in `GET /v1/models` and is usable by the
                > tutorial notebooks.
                """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def env_check(
    LLM_MODEL_LARGE_OLLAMA,
    LLM_MODEL_LARGE_REMOTE,
    LLM_MODEL_SMALL_OLLAMA,
    LLM_MODEL_SMALL_REMOTE,
    LMSTUDIO_API_KEY,
    LMSTUDIO_V1_URL,
    OLLAMA_API_KEY,
    OLLAMA_V1_URL,
    REMOTE_BASE_URL_DEFAULT,
    lmstudio_large,
    lmstudio_small,
    save_env,
    source,
):
    # --- Load existing .env if present ---
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)

    # --- Write .env when the user clicks the button ---
    if save_env.value:
        backend = source.value

        if backend == "ollama":
            lines = [
                f"LLM_MODEL_SMALL={LLM_MODEL_SMALL_OLLAMA}",
                f"LLM_MODEL_LARGE={LLM_MODEL_LARGE_OLLAMA}",
                f"TUTORIAL_LLM_BASE_URL={OLLAMA_V1_URL}",
                f"TUTORIAL_LLM_API_KEY={OLLAMA_API_KEY}",
            ]
        elif backend == "lmstudio":
            # openai/ prefix: LM Studio exposes an OpenAI-compatible API.
            # llm.py reads TUTORIAL_LLM_BASE_URL + TUTORIAL_LLM_API_KEY
            # for any openai/-prefixed model.
            small_id = lmstudio_small.value or "google/gemma-2-2b-it"
            large_id = lmstudio_large.value or "google/gemma-3-12b-it"
            lines = [
                f"LLM_MODEL_SMALL=openai/{small_id}",
                f"LLM_MODEL_LARGE=openai/{large_id}",
                f"TUTORIAL_LLM_BASE_URL={LMSTUDIO_V1_URL}",
                f"TUTORIAL_LLM_API_KEY={LMSTUDIO_API_KEY}",
            ]
        else:  # remote
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


@app.cell(hide_code=True)
def lms_model_picker(
    LARGE_MODEL_LMSTUDIO,
    SMALL_MODEL_LMSTUDIO,
    lmstudio_model_ids: list[str],
    source,
):
    # LM Studio model dropdowns — only shown when LM Studio is selected.
    # Populated from detected models + recommended defaults so participants
    # always have sensible options even if /v1/models returns nothing yet.
    _dropdown_opts = list(
        dict.fromkeys(lmstudio_model_ids + [SMALL_MODEL_LMSTUDIO, LARGE_MODEL_LMSTUDIO])
    )

    lmstudio_small = mo.ui.dropdown(
        options=_dropdown_opts,
        value=SMALL_MODEL_LMSTUDIO,
        label="Small model (Parts 1–2)",
        searchable=True,
    )

    lmstudio_large = mo.ui.dropdown(
        options=_dropdown_opts,
        value=LARGE_MODEL_LMSTUDIO,
        label="Large model (Parts 3–5)",
        searchable=True,
    )

    if source.value == "lmstudio":
        mo.vstack(
            [
                mo.md(
                    "**LM Studio model selection** — "
                    "pick the models you loaded in LM Studio:"
                ),
                mo.hstack([lmstudio_small, lmstudio_large]),
            ]
        )
    else:
        None
    return lmstudio_large, lmstudio_small


if __name__ == "__main__":
    app.run()
