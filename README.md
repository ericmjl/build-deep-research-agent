# build-deep-research-agent

SciPy 2026 Tutorial, Ben Batorsky x Eric Ma

Made with ❤️ by Eric Ma (@ericmjl).

## Get started for development

### Install Pixi

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

### Clone and set up the project

```bash
git clone git@github.com:ericmjl/build-deep-research-agent
cd build-deep-research-agent
pixi install
```

### Tutorial LLM endpoint

The notebooks call a shared Modal vLLM endpoint (no server-side auth). Create a `.env` file at the repo root with:

```bash
LLM_MODEL=openai/palmfuture/Qwen3.6-35B-A3B-GPTQ-Int4
TUTORIAL_LLM_BASE_URL=https://nll-ai--vllm-service-vllmserver-serve.modal.run/v1
```

`build_deep_research_agent.llm` loads these via `python-dotenv`. You do not need `TUTORIAL_LLM_API_KEY` for this endpoint.

**Bring your own provider:** set `OPENAI_API_KEY` instead (and omit `TUTORIAL_LLM_BASE_URL`) to use OpenAI or another compatible API.
