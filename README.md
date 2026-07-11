# build-deep-research-agent

SciPy 2026 Tutorial, Ben Batorsky x Eric Ma

Made with ❤️ by Eric Ma (@ericmjl).

## Get started for the tutorial

### 1. Install Pixi

This project uses [Pixi](https://pixi.sh) for environment and task management. If you don't have it yet, install it:

**Linux & macOS:**

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Restart your terminal afterwards, then verify with `pixi --version`. See the [Pixi installation docs](https://pixi.sh/latest/installation/) for alternatives (Homebrew, `winget`, `cargo`, etc.).

### 2. Clone and set up the project

```bash
git clone git@github.com:ericmjl/build-deep-research-agent
cd build-deep-research-agent
pixi install
```

<details>
<summary><b>Pixi install failed or slow?</b> — click for fallbacks</summary>

If `pixi install` fails or is slow (corporate proxy, conda-forge mirror issues, etc.), use one of these fallbacks:

**Fallback A — `uv sync` (fast PyPI-only resolver):**

```bash
uv sync
uv run marimo edit notebooks/
```

**Fallback B — `pip install -e .` (standard pip):**

```bash
pip install -e .
marimo edit notebooks/
```

Both fallbacks install the same dependencies declared in `pyproject.toml`. They skip the conda-forge channel (which is what can be slow), so they are often faster on restricted networks.

</details>

### 3. Configure the tutorial LLM endpoint

The tutorial uses **gemma4:12b** via **Ollama**. The preferred setup is to run
it locally — the notebooks also work against a shared remote endpoint if your
machine can't serve the model.

**Option A — Local Ollama (recommended):**

1. Install Ollama from [ollama.com](https://ollama.com).
2. Pull the model: `ollama pull gemma4:12b`.
3. Open `notebooks/00_check.py` — it will auto-detect local Ollama, write
   `.env` for you, and verify the endpoint.

```bash
# .env (written automatically by 00_check.py, or create manually)
# ollama_chat/ prefix = litellm's native Ollama adapter (reliable tool calling)
LLM_MODEL=ollama_chat/gemma4:12b
TUTORIAL_LLM_BASE_URL=http://localhost:11434/v1
TUTORIAL_LLM_API_KEY=ollama-no-auth
```

**Option B — Remote endpoint (fallback):**

If your machine lacks the RAM (~8 GB) to serve gemma4:12b locally, use the
shared Modal Ollama endpoint. The `openai/` prefix is required here — the
Modal endpoint exposes an OpenAI-compatible API, not Ollama's native protocol:

```bash
LLM_MODEL=openai/gemma4:12b
TUTORIAL_LLM_BASE_URL=https://nll-ai--ollama-service-ollamaservice-server.modal.run/v1
```

`00_check.py` will suggest this automatically when local Ollama is not detected.

**Option C — Bring your own provider:**

Set `OPENAI_API_KEY` instead (and omit `TUTORIAL_LLM_*`) to use OpenAI or
another compatible API.

> **Zero-config default:** if no `.env` exists and no env vars are set,
> `build_deep_research_agent.llm` defaults to local Ollama
> (`ollama_chat/gemma4:12b`). Run `00_check.py` to configure everything
> interactively.

### 4. Launch the notebooks

**Preferred (sandboxed, isolated environment):**

```bash
uvx marimo edit --sandbox notebooks/
```

**Fallback (uses the Pixi environment you just built — no network needed):**

```bash
pixi run marimo
```

This launches `marimo edit notebooks/` using the pre-installed Pixi environment. Use this if `uvx marimo edit --sandbox` fails (common on corporate laptops with restricted network or package-install policies).

> **Tip:** If neither works, you can open a single notebook directly: `pixi run marimo edit notebooks/01_intro_prompting.py`.
