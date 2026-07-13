# build-deep-research-agent

SciPy 2026 Tutorial, Ben Batorsky x Eric Ma

Made with ❤️ by Eric Ma (@ericmjl).

## Slides
Slides are available in pdf and markdown [here](https://github.com/bpben/research_agent_scipy_26)

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
<summary><b>Don't have Git or clone failed?</b> — click for a no-Git fallback</summary>

Download the project as a ZIP instead:

1. Go to <https://github.com/ericmjl/build-deep-research-agent/archive/refs/heads/main.zip> (or click **Code → Download ZIP** on the [repo page](https://github.com/ericmjl/build-deep-research-agent)).
2. Unzip and enter the folder:

   ```bash
   unzip build-deep-research-agent-main.zip
   cd build-deep-research-agent-main
   ```

3. Continue with `pixi install` below.

> **Note:** You won't be able to `git pull` updates with this method. If you install Git later, re-clone with the command above to get future updates.

</details>

<details>
<summary><b>Pixi install failed or slow?</b> — click for fallbacks</summary>

If `pixi install` fails or is slow (corporate proxy, conda-forge mirror issues, etc.), use one of these fallbacks:

**Fallback A — `uv sync` (fast PyPI-only resolver):**

```bash
uv sync
uv run marimo edit --no-sandbox notebooks/
```

**Fallback B — `pip install -e .` (standard pip):**

```bash
pip install -e .
marimo edit --no-sandbox notebooks/
```

Both fallbacks install the same dependencies declared in `pyproject.toml`. They skip the conda-forge channel (which is what can be slow), so they are often faster on restricted networks.

</details>

### 3. Configure the tutorial LLM endpoint

The tutorial uses **two models** via **Ollama**:

| Model | Size | Used in | Env var |
|-------|------|---------|---------|
| **gemma2:2b** | ~1.6 GB | Parts 1–2 (prompting, memory) | `LLM_MODEL_SMALL` |
| **gemma4:12b** | ~8 GB | Parts 3–5 (tools, workflows, multi-agent) | `LLM_MODEL_LARGE` |

#### Quick start — `pixi run bootstrap` (recommended)

The bootstrap command installs Ollama, pulls both models (auto-detects whether
your machine has enough RAM for the large model), writes `.env`, and launches
notebook 00 for verification:

```bash
pixi run bootstrap
```

If your machine has < 32 GB RAM, the large model is skipped — Parts 3–5 will
use the remote Modal endpoint instead (switch to "Remote" in notebook 00).

#### Option A — Local Ollama (recommended)

1. Install Ollama from [ollama.com](https://ollama.com) (or let `pixi run bootstrap` do it).
2. Pull the models:

   ```bash
   ollama pull gemma2:2b    # small — always
   ollama pull gemma4:12b   # large — needs >= 32 GB RAM
   ```

3. Open `notebooks/00_check.py` — it auto-detects local Ollama, writes `.env`
   with both model variables, and pings each model.

```bash
# .env (written automatically by bootstrap or 00_check.py)
LLM_MODEL_SMALL=ollama_chat/gemma2:2b
LLM_MODEL_LARGE=ollama_chat/gemma4:12b
TUTORIAL_LLM_BASE_URL=http://localhost:11434/v1
TUTORIAL_LLM_API_KEY=ollama-no-auth
```

#### Option B — Remote endpoint (fallback)

If your machine lacks the RAM (~32 GB) to serve gemma4:12b locally, use the
shared Modal Ollama endpoint (both models served from the same URL):

```bash
LLM_MODEL_SMALL=openai/gemma2:2b
LLM_MODEL_LARGE=openai/gemma4:12b
TUTORIAL_LLM_BASE_URL=https://nll-ai--ollama-service-ollamaservice-server.modal.run/v1
```

`00_check.py` will suggest this automatically when local Ollama is not detected.

#### Option C — Bring your own provider

Set `OPENAI_API_KEY` instead (and omit `TUTORIAL_LLM_*`) to use OpenAI or
another compatible API.

> **Zero-config default:** if no `.env` exists and no env vars are set,
> `build_deep_research_agent.llm` defaults to local Ollama
> (`ollama_chat/gemma2:2b` for small, `ollama_chat/gemma4:12b` for large).
> Run `pixi run bootstrap` or `pixi run checkenv` to configure everything
> interactively.

### 4. Launch the notebooks

```bash
pixi run marimo
```

This runs `marimo edit --no-sandbox --no-token notebooks/` using the Pixi
environment you just built. `--no-sandbox` is required because the lesson
notebooks import `build_deep_research_agent` (installed into the Pixi env via
editable install) — an isolated marimo sandbox would not see it.

**Open a single notebook** with `pixi run nbN`, where N is the notebook number:

| Task | Notebook | Title |
| ---- | -------- | ----- |
| `pixi run nb0` | `00_check.py` | Environment check (alias: `pixi run checkenv`) |
| `pixi run nb1` | `01_intro_prompting.py` | Part 1 — Prompting |
| `pixi run nb2` | `02_memory_state.py` | Part 2 — Memory & state |
| `pixi run nb3` | `03_tools_mcp_zotero.py` | Part 3 — Tools, MCP & Zotero |
| `pixi run nb4` | `04_workflows.py` | Part 4 — Agent workflows |
| `pixi run nb5` | `05_bonus_architectures.py` | Bonus — Architecture choices |

> **Tip:** `uvx marimo edit --sandbox notebooks/` is reserved for exploratory
> notebooks *outside* the curriculum — the sandbox isolates a fresh env, which
> can't see `build_deep_research_agent`. For the tutorial notebooks, always use
> `pixi run marimo` or `pixi run nb1`.

## Going further

### Evaluating your agent

You built a research agent — but how do you know if it's any good? Evaluating
LLM and retrieval systems is a discipline of its own, and the agent you just
built touches every layer it covers: retrieval quality (your Part 3 docstore),
tool use (your `@tool` and MCP server), and end-to-end generation (your Part 4
AgentBot loop).

Eric's [AI Evals course notes](https://gist.github.com/ericmjl/83b46da272b4ab7cce92fd56045341bf)
are a practical field guide: RAG pitfalls (corpus coverage, chunk quality,
retrieval sufficiency, hallucination), error-analysis methodology (open and
axial coding), building eval datasets, LLM-as-judge evaluators (with TPR/TNR
validation), retrieval metrics (recall@k), tool-calling evaluation, and CI/CD
for LLM systems. It maps directly onto the architecture you built in Parts 3–5.
