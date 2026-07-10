# Tutorial Delivery — Low-Level Design

**Created**: 2026-05-27

**Updated**: 2026-05-27

**HLD Link**: [../../high-level-design.md](../../high-level-design.md)

## Overview

Cross-cutting concerns for **how** the tutorial is delivered: Marimo conventions, instructor handoff, classroom infrastructure, shared package layout, shared data models, and llamabot + Modal LLM wiring used by every capability LLD.

Capability-specific notebooks and library code live in the five sibling LLDs (`prompting`, `memory`, `tools`, `planning`, `multi-agent`).

## Instructors & Timing

| Segment | Duration | Instructor | Notebooks |
|---------|----------|------------|-----------|
| Parts 1–2 | 80 min | Ben Batorsky | `01_intro_prompting.py`, `02_memory_state.py` |
| Parts 3–5 | 100 min | Eric Ma | `03_tools_mcp_zotero.py`, `04_workflows.py`, `05_multi_agent_demo.py` |

**Handoff (Part 2 → Part 3)**: Ben closes on why memory enables multi-turn research. Eric opens Part 3 with a brief recap of the agent stack (prompt + memory) and introduces tools (MCP) — without re-running Part 1–2 exercises.

Total session: ~3 hours. ~70% coding, ~30% discussion.

## Marimo Conventions

All five notebooks:

- **Format**: `.py` Marimo apps only — no Jupyter `.ipynb`.
- **Header**: PEP 723 inline script metadata where lesson-specific deps differ from Pixi.
- **Launch**: `uvx marimo edit --sandbox notebooks/` (or single notebook path).
- **Cell spine**: objectives → discussion callout → setup → exercises → comparison/reflection → summary.
- **Exercise code**: learner implementations live in `build_deep_research_agent/exercises/` as minimal stubs; **implementation specs** live in notebook markdown cells (Part 4: **ex1_implementation_specs**). Notebooks import directly (e.g. `from build_deep_research_agent.exercises import part4` in a single **part4_exercises** cell). Instructor reference solutions live in `exercises/solutions/` — swap imports via commented lines in that cell. **No `importlib.reload`** — participants restart the kernel after saving exercise files. **Part 3** diverges: exercise functions live as **in-cell scaffolds** that import reference answers from `exercises/solutions/part3.py` by default, so the notebook runs end-to-end green; learners override the scaffold body (TUT-MARIMO-014). Parts 2 & 4 keep the stub + comment-swap pattern (TUT-MARIMO-023).
- **Minimize wrappers**: participants implement named functions in the exercise module (e.g. `plan_research`, not a hidden `plan_fn` alias). Notebook cells hold visible orchestration (`@tool`, PocketFlow edges); library code provides stores and runners, not factories that hide tool construction (see [Planning LLD](../planning/LLD.md)).
- **App width**: `marimo.App(width="medium")` unless wide output requires `"full"`.

Remove `notebooks/example_notebook.py` when `01_intro_prompting.py` lands. (`05_multi_agent_demo.py` exists; stub remains.)

## Pixi / Python

- Pixi pins **Python 3.12** (required for `llamabot` dependency chain).
- PyPI deps in `pyproject.toml`: `llamabot`, `marimo`, `loguru`, `pydantic`, `python-dotenv`.

## Classroom Infrastructure

| Resource | Role | Participant setup |
|----------|------|-------------------|
| **Modal-hosted LLM** | Default LLM for all parts | Endpoint URL (+ key if needed) in materials; **no BYO key required** |
| **[zotero-mcp](https://github.com/54yyyu/zotero-mcp)** | MCP server for Part 3+ | Install/configure per upstream docs |
| **Optional BYO LLM keys** | Compare provider behavior | Welcome, not required |

### Environment variables

| Variable | Purpose |
|----------|---------|
| `TUTORIAL_LLM_BASE_URL` | Modal endpoint (default path) |
| `TUTORIAL_LLM_API_KEY` | Auth for Modal endpoint if required |
| `LLM_MODEL` | Model name for exercises |
| `RESEARCH_SEARCH_MODE` | `fixture` (default) or `mcp` for Searcher AgentBot |
| `ZOTERO_MCP_SOURCE` | `tutorial` (default, in-repo FastMCP) or `upstream` (hand-installed zotero-mcp) |
| `ZOTERO_MCP_COMMAND` | Executable for upstream zotero-mcp (when `ZOTERO_MCP_SOURCE=upstream`) |
| `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID` | Optional — live Zotero via tutorial server's pyzotero backend |
| `ZOTERO_LOCAL` | Optional — local Zotero via pyzotero |
| Optional provider vars (e.g. `OPENAI_API_KEY`) | BYO comparison path |

Load from `.env` (gitignored) for local rehearsal. Document in `docs/index.md` and each notebook setup cell.

`notebooks/01_intro_prompting.py` starts with a hidden **Cell 0** startup validator that checks `.env` presence, verifies required `TUTORIAL_LLM_BASE_URL` / `LLM_MODEL` (and optional `TUTORIAL_LLM_API_KEY`), offers a guided textbox form that can write `.env` from README defaults, pings the configured model endpoint with a trivial request, and reports pass/fail with actionable fixes.

### Troubleshooting (instructor)

| Issue | Mitigation |
|-------|------------|
| Modal endpoint down | BYO key path; rehearsal checklist |
| zotero-mcp fails | Upstream docs; Parts 1–2 still run on fixtures |
| MCP won't connect | Verify install; optional demo cell with captured output |
| LLM rate limits | Smaller contexts in exercise presets |

## Package Layout (Shared)

```
build_deep_research_agent/
├── __init__.py           # exports orchestrator, agents, models
├── cli.py                # Typer (scaffold; smoke commands planned)
├── models.py             # Message, CitationRecord, ResearchReport
├── llm.py                # get_completion_kwargs(), get_model_name()
├── prompts.py            # research + AgentBot role prompts
├── research_tools.py     # Searcher @tool definitions (Part 5)
├── agents.py             # Searcher/Synthesizer AgentBots, orchestrator
├── mcp/
│   ├── client.py         # MCP client + source resolution (Part 3+)
│   ├── server.py         # tutorial FastMCP Zotero server (fallback)
│   └── zotero_backend.py # pyzotero + fixture search backend
├── fixtures/
│   ├── loader.py         # load_citation_fixtures()
│   ├── search.py         # search_fixture_library()
│   └── zotero_library.json
├── memory.py             # → memory LLD (not started)
└── workflows.py          # → planning LLD (not started)
```

Legacy scaffold files (`preprocessing.py`, cookiecutter `schemas.py`) remain until removed.

## Shared Data Models

Defined in `models.py`; used across capability LLDs.

### `Message`

| Field | Type | Description |
|-------|------|-------------|
| `role` | `Literal["system", "user", "assistant", "tool"]` | Chat role |
| `content` | `str` | Body |

### `CitationRecord`

| Field | Type | Description |
|-------|------|-------------|
| `key` | `str` | Zotero item key |
| `title` | `str` | Title |
| `creators` | `list[str]` | Authors |
| `year` | `int \| None` | Publication year |
| `abstract` | `str \| None` | Optional abstract |

### `ResearchReport`

| Field | Type | Description |
|-------|------|-------------|
| `query` | `str` | Original question |
| `evidence` | `list[CitationRecord]` | Searcher output |
| `report_markdown` | `str` | Synthesizer output |

## LLM Integration (`llm.py`)

Shared llamabot configuration for all AgentBots and future `SimpleBot` exercises:

- `get_model_name() -> str` — from `LLM_MODEL` env var
- `get_completion_kwargs() -> dict` — `api_base` / `api_key` from `TUTORIAL_LLM_*` or `OPENAI_API_KEY`
- Raises `MissingLLMConfigError` when no credentials are configured

Part 5 agents pass `**get_completion_kwargs()` into `AgentBot` constructors directly.

## CLI (Smoke Only)

Typer entrypoint for instructor validation, not participant workflow:

- `smoke-llm` — one completion against Modal endpoint *(planned)*
- `smoke-import` — verify package imports *(planned)*

## Testing Conventions

- pytest function style under `tests/`
- Mock LLM in unit tests; `@pytest.mark.integration` for live endpoint
- `@spec` comments link tests to EARS IDs in capability LLDs

## Related Documents

- [High-Level Design](../../high-level-design.md)
- [Prompting LLD](../prompting/LLD.md)
- [Memory LLD](../memory/LLD.md)
- [Tools LLD](../tools/LLD.md)
- [Planning LLD](../planning/LLD.md)
- [Multi-Agent LLD](../multi-agent/LLD.md)
- [Marimo Conventions EARS](./marimo-conventions-EARS.md)
- [Classroom Infrastructure EARS](./classroom-infrastructure-EARS.md)
- [Shared Models EARS](./shared-models-EARS.md)
