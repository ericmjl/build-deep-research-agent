# Build Deep Research Agent — High-Level Design

**Created**: 2026-05-27
**Updated**: 2026-05-27
**Event**: SciPy 2026 Tutorial — Eric Ma × Ben Batorsky

**Proposal**: This HLD implements the accepted SciPy tutorial proposal. When the proposal and this doc diverge, update this doc to match the proposal.

---

## What Participants Build

By the end of ~3 hours, participants will have constructed a **Deep Research Agent**: an LLM-powered system that can query a Zotero citation library, synthesize literature summaries, and hold multi-turn research conversations. They will also see how specialized agents (Searcher, Synthesizer) can collaborate on literature review — and discuss failure modes, limitations, and the role of such agents alongside coding assistants.

**Deliverable**: A working single-agent research stack in five Marimo notebooks, backed by a small Python library they can customize after the conference.

---

## Mental Model (Organizing Principle)

We teach agents as **LLM-backed systems with four capabilities**, built in this order:

```
                    ┌─────────────────────────┐
                    │   Deep Research Agent   │
                    └───────────┬─────────────┘
          ┌─────────┬─────────┼─────────┬─────────┐
          ▼         ▼         ▼         ▼         │
       Prompt    Memory     Tools    Planning      │
     (context)  (state)     (MCP)   (workflows)    │
          │         │         │         │         │
       Part 1    Part 2    Part 3    Part 4        │
                                              Part 5
                                         (multi-agent demo)
```

| Capability | What it means in this tutorial | Taught in |
|------------|----------------------------------|-----------|
| **Prompt / in-context learning** | System prompts and static citation metadata in context | Part 1 |
| **Memory** | Append-only chat history; citation context across turns | Part 2 |
| **Tools** | MCP connection to Zotero via [zotero-mcp](https://github.com/54yyyu/zotero-mcp) (teaching path) and an in-repo **tutorial FastMCP server** (cooking-show fallback) | Part 3 |
| **Planning** | Deterministic workflow vs. ReAct (*Re*ason + *Act*) loop | Part 4 |
| **Multi-agent** | Searcher + Synthesizer collaboration; failure-mode discussion | Part 5 |

Everything in the repo — notebooks, library modules, tests, design docs — should map cleanly to one of these capabilities. If it does not, it does not belong in v1.

---

## Abstract (Proposal)

Through the construction of a Deep Research Agent, tutorial participants will learn the fundamental building blocks of LLM-driven applications. Starting with in-context learning and prompt design, we will progress through memory management, tool integration via the Model Context Protocol (MCP), and planning workflows. Participants will build a working agent that can query a Zotero citation library, synthesize literature summaries, and engage in multi-turn research conversations. We will also discuss failure modes, limitations, and the role of such agents in an age of coding assistants.

---

## Teaching Philosophy

- **Learning by doing** — ~70% hands-on coding, ~30% discussion.
- **First principles** — Practical, working code; participants understand what happens under the hood. No black-box agent frameworks (no LangChain).
- **Ordered for productivity** — Progression reflects what the instructors wished they knew when starting; each part assumes the previous.
- **Single agent first, multi-agent last** — Parts 1–4 build one functional agent; Part 5 demos specialization and discussion.

---

## Instructors & Session Flow

| Segment | Duration | Instructor | Notebooks |
|---------|----------|------------|-----------|
| Parts 1–2 | 80 min | **Ben Batorsky** | `01_intro_prompting.py`, `02_memory_state.py` |
| Parts 3–5 | 100 min | **Eric Ma** | `03_tools_mcp_zotero.py`, `04_workflows.py`, `05_multi_agent_demo.py` |

**Handoff (Part 2 → Part 3)**: Ben closes on why memory enables multi-turn research. Eric opens Part 3 by connecting **tools** (MCP) to the agent stack built so far — without re-running Part 1–2 exercises.

---

## Curriculum (Proposal Outline)

### Part 1: Introduction & In-Context Learning (40 min) — Ben

- **Discussion**: What is a research agent? Use cases and limitations.
- **Hands-on**: Anatomy of a system prompt for research tasks.
- **Hands-on**: Summarization with static Zotero metadata in context.

### Part 2: Memory & State Management (40 min) — Ben

- **Discussion**: Why memory matters for multi-turn research.
- **Hands-on**: Implementing simple append-only chat history.
- **Hands-on**: Building memory with Zotero citation context.
- **Hands-on**: Comparing results with and without memory.

### Part 3: Tools — MCP and Zotero Integration (40 min) — Eric

- **Discussion**: The Model Context Protocol (MCP) standard.
- **Hands-on**: Setting up a Zotero MCP server connection.
- **Hands-on**: Building a Zotero search tool.
- **Hands-on**: Executing live queries and summarizing results.

### Part 4: Planning Workflows (30 min) — Eric

- **Discussion**: Deterministic vs. agentic workflows.
- **Hands-on**: Read implementation specs in `04_workflows.py`; implement PocketFlow tool bodies (`plan_research`, `search_literature`, `summarize_evidence`) in `exercises/part4.py` (reference answers in `exercises/solutions/part4.py`); wire `@tool` + linear graph in the notebook.
- **Hands-on**: Same pipeline via AgentBot (prompt-controlled routing) for contrast.
- **Hands-on**: Implementing a ReAct (*Reason* + *Act*) loop.
- **Hands-on**: Comparing workflow approaches for research tasks.

### Part 5: Multi-Agent Systems & Discussion (30 min) — Eric

- **Demo**: Specialized Searcher and Synthesizer agents.
- **Discussion**: Failure modes — hallucination, context exhaustion, deadlocks.
- **Discussion**: Expansions — web search, PDF parsing, why bother in an age of coding agents.
- **Demo-oriented Q&A** — participants are often tired of coding by this point.

---

## Classroom Infrastructure

These are **external services** the tutorial depends on — not code we implement in this repo.

| Resource | Role | Participant setup |
|----------|------|-------------------|
| **Modal-hosted LLM** | Open-source model via custom API endpoint, live for tutorial duration | **No API key required**; endpoint URL provided in materials |
| **[zotero-mcp](https://github.com/54yyyu/zotero-mcp)** | MCP server for Zotero search and retrieval | Install/configure per upstream docs; Zotero credentials as needed |
| **Optional BYO LLM keys** | Compare provider quality/behavior | Welcome but not required |

Bundled **static citation fixtures** in this repo support Parts 1–2 (before live MCP). They are not a substitute for Part 3 live queries — they are teaching data for in-context learning and memory exercises.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                 Marimo notebooks (Parts 1–5)                      │
│         narrative · exercises · comparisons · demos               │
└─────────────────────────────┬────────────────────────────────────┘
                              │ imports
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│            build_deep_research_agent/ (we build this)               │
│   prompts · memory · workflows · agents · fixtures · mcp client/server │
└──────────────┬──────────────────────────────┬────────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐    ┌──────────────────────────────────┐
│ llamabot (we integrate)  │    │ Zotero MCP (integrate + build)    │
│ summarization · ReAct    │    │ upstream zotero-mcp (Part 3 teach) │
│ MCP tool calling         │    │ tutorial FastMCP server (fallback) │
└──────────────┬───────────┘    └──────────────────┬───────────────┘
               │                                   │
               ▼                                   ▼
┌──────────────────────────┐    ┌──────────────────────────────────┐
│ Modal LLM API endpoint   │    │ Zotero library (participant)        │
│ (tutorial-provided)      │    │ live bibliographic data             │
└──────────────────────────┘    └──────────────────────────────────┘
```

### Build vs. integrate

| Component | We build | We integrate |
|-----------|----------|--------------|
| Marimo lesson notebooks | ✓ | |
| `build_deep_research_agent` library (prompts, memory, workflows, agents) | ✓ | |
| Static citation fixtures (Parts 1–2) | ✓ | |
| MCP client wiring in notebooks/library | ✓ | |
| Tutorial FastMCP Zotero server (`mcp/server.py`) | ✓ | |
| llamabot | | ✓ |
| upstream zotero-mcp server | | ✓ |
| Modal LLM endpoint | | ✓ (operational) |
| LangChain / other agent frameworks | | ✗ (non-goal) |

---

## Key Design Decisions

### Decision 1: Proposal-first scope

**Choice**: HLD tracks the SciPy proposal; design docs and code serve the five-part outline.

**Rationale**: Prevents repo drift toward infrastructure (custom MCP servers, deployment) that the tutorial does not teach.

### Decision 2: Marimo-only delivery

**Choice**: Five `.py` Marimo notebooks under `notebooks/`; no Jupyter `.ipynb`.

**Rationale**: Python-native, reactive cells, better git diffs for maintained tutorial materials.

### Decision 3: Notebook-thin, library-thick

**Choice**: Teachable logic in `build_deep_research_agent/`; notebooks orchestrate and explain.

**Rationale**: Two instructors, one handoff; Ben's Parts 1–2 code is stable foundation for Eric's Parts 3–5; pytest targets the library.

### Decision 4: llamabot, not LangChain

**Choice**: llamabot for LLM calls, tool use, and agent patterns.

**Rationale**: Instructor preference; keeps prompts and tool traces inspectable for teaching.

### Decision 5: Upstream zotero-mcp for teaching; tutorial FastMCP server as fallback

**Choice**: Part 3 teaches MCP integration with external [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp). This repo also ships a **tutorial FastMCP server** (`build_deep_research_agent/mcp/server.py`) that uses **pyzotero** when credentials are set and falls back to bundled fixtures — the cooking-show dish that's already in the oven while participants learn to install upstream zotero-mcp by hand.

**Rationale**: Matches proposal (integrate, don't reimplement the full upstream server) while keeping classroom demos reliable when upstream install or Zotero auth is not ready.

**Default**: `ZOTERO_MCP_SOURCE=tutorial` for demos; set `upstream` when using hand-installed zotero-mcp.

### Decision 6: Tutorial-provided LLM via Modal

**Choice**: Default exercises use Modal-hosted open-source LLM endpoint; BYO keys optional.

**Rationale**: Matches proposal; removes API-key friction in the classroom.

### Decision 7: Design-driven documentation

**Choice**: HLD → LLD → EARS under `docs/`; tutorial changes update design docs in the same change (see `AGENTS.md`).

**Rationale**: Materials prepared before the conference; intent must survive across sessions and agents.

---

## Participant Prerequisites

From the proposal:

- Comfortable with Python — functions, dictionaries, lists.
- Basic LLM literacy (e.g. has used ChatGPT or Claude).
- Helpful but not required: `async/await`, prior LLM API or agent framework experience (we teach these from scratch in context).
- Helpful but not required: API calls (e.g. `requests`).

---

## Non-Goals (v1)

- Jupyter notebooks for tutorial delivery
- Building a custom Zotero MCP server (use upstream zotero-mcp)
- LangChain or comparable opaque agent frameworks
- Production deployment, auth systems, or multi-tenant hosting
- Web UI (FastAPI/HTMX) — optional Typer CLI for instructor smoke tests only
- PDF parsing, web search — Part 5 **discussion** only
- Requiring participant LLM API keys

---

## Technology Stack

| Concern | Choice |
|---------|--------|
| Language | Python ≥3.10 |
| Environment | Pixi |
| Tutorial UI | Marimo |
| LLM access | Modal-hosted endpoint (default); llamabot as client |
| Agent / LLM library | llamabot |
| Zotero tools | [zotero-mcp](https://github.com/54yyyu/zotero-mcp) via MCP |
| Static teaching data | Bundled citation fixtures in repo |
| CLI | Typer (smoke checks only) |
| Tests | pytest |
| Design docs | design-driven-dev in `docs/` |

---

## Repository Layout

```
build_deep_research_agent/   # capability modules (see tutorial-delivery LLD)
notebooks/                   # five Marimo notebooks (one per part)
tests/                       # pytest per capability
docs/
  high-level-design.md       # this document
  designs/
    tutorial-delivery/       # Marimo, instructors, infra, shared models, llm.py
    prompting/               # Part 1
    memory/                  # Part 2
    tools/                   # Part 3 — zotero-mcp client
    planning/                # Part 4 — workflows, ReAct Runner
    multi-agent/             # Part 5
```

---

## Implementation Status

**Last updated**: 2026-05-27

Build order so far: **Part 5 multi-agent demo first** (reference implementation), then Parts 1–4 backward toward Ben's segment.

| Capability | Library modules | Notebook | Tests | Status |
|------------|-----------------|----------|-------|--------|
| **Tutorial delivery** | `models.py`, `llm.py`, `__init__.py` | — | partial | In progress |
| **Prompting** (Part 1) | `prompts.py`, `fixtures/` | `01_*` not started | `test_prompts`, `test_fixtures` | Library partial |
| **Memory** (Part 2) | — | `02_*` not started | — | Not started |
| **Tools** (Part 3) | `mcp/client.py`, `mcp/server.py`, `mcp/zotero_backend.py` | `03_*` not started | `test_mcp_client` | Client + tutorial server done |
| **Planning** (Part 4) | `workflows.py` | `04_workflows.py` | `test_workflows` | **Done** |
| **Multi-agent** (Part 5) | `agents.py`, `research_tools.py` | `05_multi_agent_demo.py` | `test_agents` | **Demo scaffold done** |

When landing tutorial code, update the matching LLD and mark EARS `[x]` in the same change (see `AGENTS.md`).

---

## Definition of Done (v1)

- [ ] Five Marimo notebooks match the proposal outline and run in order.
- [ ] Parts 1–2: summarization and memory work with static fixtures; Ben can teach standalone.
- [ ] Part 3: live connection to zotero-mcp; search → summarize pipeline works.
- [x] Part 4: deterministic workflow and ReAct loop both runnable; comparison exercise included.
- [x] Part 5: Searcher + Synthesizer **AgentBot** demo scaffold (`agents.py`, `05_multi_agent_demo.py`); failure presets (empty, oversized) in notebook.
- [ ] Part 5: failure preset for low ReAct max-steps; architecture recap diagram in notebook.
- [ ] Default LLM path uses Modal endpoint without participant API keys.
- [ ] Handoff Part 2 → Part 3 is smooth (Eric does not re-teach Parts 1–2).
- [ ] LLDs and EARS trace to this HLD; code uses `@spec` where applicable.
- [x] EARS spec files exist under `docs/designs/`.

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Modal endpoint unavailable | Document BYO key path; instructor rehearsal checklist |
| zotero-mcp or Zotero auth fails | Pre-flight setup doc; Eric carries troubleshooting; static fixtures still support Parts 1–2 |
| Network issues in room | Smaller live queries; instructor demo fallback cells in Part 3 |
| Notebook / library drift | Notebooks import library APIs; tests lock contracts |
| Part 5 fatigue | Demo-heavy, minimal new coding per proposal |

---

## Related Designs

LLDs follow the [mental model](#mental-model-organizing-principle): one folder per capability, plus cross-cutting delivery.

| LLD | HLD capability | Part | Notebook | Build status |
|-----|----------------|------|----------|--------------|
| [Tutorial Delivery](./designs/tutorial-delivery/LLD.md) | *(cross-cutting)* | — | Marimo, instructors, Modal LLM, shared models | Partial |
| [Prompting](./designs/prompting/LLD.md) | Prompt / in-context learning | 1 | `01_intro_prompting.py` | Library only |
| [Memory](./designs/memory/LLD.md) | Memory | 2 | `02_memory_state.py` | Not started |
| [Tools](./designs/tools/LLD.md) | Tools (MCP) | 3 | `03_tools_mcp_zotero.py` | Client + tutorial server |
| [Planning](./designs/planning/LLD.md) | Planning | 4 | `04_workflows.py` | **Done** |
| [Multi-Agent](./designs/multi-agent/LLD.md) | Multi-agent | 5 | `05_multi_agent_demo.py` | **Demo scaffold** |
