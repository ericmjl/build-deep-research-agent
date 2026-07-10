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

The notebooks call a shared Modal Ollama endpoint (no server-side auth). Create a `.env` file **at the repo root** (next to `pyproject.toml`):

```text
build-deep-research-agent/     ← repo root
├── .env                       ← HERE (not in a subdirectory)
├── pyproject.toml
├── notebooks/
│   ├── 01_intro_prompting.py
│   └── ...
└── build_deep_research_agent/
```


```bash
LLM_MODEL=openai/gemma4:12b
TUTORIAL_LLM_BASE_URL=https://nll-ai--ollama-service-ollamaservice-server.modal.run/v1
```

`build_deep_research_agent.llm` loads these via `python-dotenv`. You do not need `TUTORIAL_LLM_API_KEY` for this endpoint.

> **Notebook 01 has a startup validator** (Cell 0) that checks `.env` automatically. If it's missing or incomplete, the cell shows a pre-filled form — just click "Write .env" and you're set. The defaults come from this README.

**Bring your own provider:** set `OPENAI_API_KEY` instead (and omit `TUTORIAL_LLM_BASE_URL`) to use OpenAI or another compatible API.

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
