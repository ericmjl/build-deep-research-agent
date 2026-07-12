# Classroom Infrastructure — EARS

**Parent LLD**: [Tutorial Delivery LLD](./LLD.md)

## Modal LLM (Default Path)

- [x] **TUT-INFRA-001**: The default tutorial LLM path shall use a Modal-hosted open-source model via `TUTORIAL_LLM_BASE_URL`. *(Env var support in `llm.py`; Modal endpoint wired in `.env` → Gemma 4 12B IT (Ollama, `gemma4:12b`).)*
- [ ] **TUT-INFRA-002**: The tutorial materials shall not require participants to supply their own LLM API keys for default exercises.
- [ ] **TUT-INFRA-003**: When `TUTORIAL_LLM_API_KEY` is required for the Modal endpoint, instructor materials shall provide the value for tutorial duration.
- [x] **TUT-INFRA-004**: The `llm.py` module shall configure llamabot from `TUTORIAL_LLM_*` environment variables.
- [x] **TUT-INFRA-005**: If tutorial LLM configuration is missing, `llm.py` shall raise an error naming the required environment variables.
- [x] **TUT-INFRA-006**: A dedicated `00_check.py` notebook shall provide a startup validation that checks `.env`, verifies required tutorial LLM variables, offers guided `.env` setup when missing/incomplete, pings the model endpoint, and reports actionable pass/fail status. *(Moved out of `01_intro_prompting.py` into its own notebook; runnable via `pixi run checkenv`. The form cell creates the inputs; the check cell writes `.env` on click and pings, gating on a real `.env` file so stale process env never reports a false "ready".)*

## Optional BYO LLM

- [x] **TUT-INFRA-010**: Where a participant supplies an optional provider API key (e.g. `OPENAI_API_KEY`), `llm.py` shall support that path for comparison exercises.
- [ ] **TUT-INFRA-011**: Instructor materials shall document the optional BYO LLM path separately from the default Modal path.

## zotero-mcp (Part 3+) — SUPERSEDED

> Superseded 2026-07-06 by HLD Decision 8. Part 3 no longer teaches upstream `zotero-mcp`; it wraps pyzotero keyword search as a llamabot `@tool` and builds a self-contained corpus MCP server. Specs below retained for traceability.

- ~~**TUT-INFRA-020**~~: reference upstream zotero-mcp — superseded.
- ~~**TUT-INFRA-022**~~: tutorial FastMCP Zotero server fallback — superseded (retained as legacy code).
- ~~**TUT-INFRA-021**~~: pin zotero-mcp version — superseded.

## Instructor Handoff

- [ ] **TUT-INFRA-030**: Notebook `02_memory_state.py` shall include a handoff cell recapping prompt + memory before Part 3.
- [ ] **TUT-INFRA-031**: Notebook `03_tools_mcp_zotero.py` shall open with a brief recap of Parts 1–2 without re-running prior exercises.

## Troubleshooting Documentation

- [x] **TUT-INFRA-040**: `docs/index.md` shall document required environment variables and corpus/Zotero setup for the new Part 3 arc. *(Superseded by README setup section for participant-facing docs.)*
- [ ] **TUT-INFRA-041**: Instructor troubleshooting docs shall include mitigations for Modal endpoint unavailability.
- [ ] **TUT-INFRA-042**: Instructor troubleshooting docs shall include mitigations for Zotero-auth absence (phase-1 `@tool` fixture fallback) and MCP-client configuration failures.

## Setup Reliability (Issue #17)

- [x] **TUT-SETUP-010**: The README shall document the `.env` distribution path with the endpoint URL pre-populated so participants can copy values directly, and the notebook-01 startup validator shall read these defaults automatically.
- [x] **TUT-SETUP-011**: The README shall include a visual directory tree showing that `.env` goes at the repo root (next to `pyproject.toml`), not in a subdirectory.
- [x] **TUT-SETUP-012**: The project shall provide a non-sandbox marimo launch path via `pixi run marimo` (a Pixi task running `marimo edit notebooks/`) for corporate laptops where `uvx marimo edit --sandbox` fails. *(Pixi task in `pyproject.toml` under `[tool.pixi.feature.devtools.tasks]`.)*
- [x] **TUT-SETUP-013**: The README shall document fallbacks when `pixi install` fails or is slow: `uv sync` (PyPI-only resolver) and `pip install -e .` (standard pip).

## Bootstrap Command

- [x] **TUT-BOOT-001**: The Typer CLI shall expose a `bootstrap` command that installs Ollama, pulls the small model, auto-detects RAM for the large model, writes `.env`, and launches notebook 00. *(Implemented in `build_deep_research_agent/bootstrap.py`, wired into `cli.py`, pixi task `bootstrap` in `pyproject.toml`.)*
- [x] **TUT-BOOT-002**: The bootstrap command shall install Ollama via Homebrew (macOS), install script (Linux), or winget (Windows) when the `ollama` binary is not on PATH.
- [x] **TUT-BOOT-003**: The bootstrap command shall always pull `gemma2:2b` (small model for Parts 1–2).
- [x] **TUT-BOOT-004**: The bootstrap command shall check system RAM via `psutil` and pull `gemma4:12b` (large model for Parts 3–5) only when RAM >= 32 GB.
- [x] **TUT-BOOT-005**: The bootstrap command shall write `.env` with `LLM_MODEL_SMALL` and `LLM_MODEL_LARGE` set to `ollama_chat/` prefixed local Ollama defaults.
- [x] **TUT-BOOT-006**: The bootstrap command shall launch `notebooks/00_check.py` via `marimo edit --no-sandbox --no-token` for final env verification.
- [x] **TUT-BOOT-007**: The `00_check.py` notebook shall detect both `gemma2:2b` and `gemma4:12b` in the local Ollama instance and display their availability status.
- [x] **TUT-BOOT-008**: The `00_check.py` notebook shall write both `LLM_MODEL_SMALL` and `LLM_MODEL_LARGE` env vars to `.env` based on the local-vs-remote choice.
- [x] **TUT-BOOT-009**: The `00_check.py` notebook shall ping both models (small and large) via `SimpleBot` to verify the endpoint works for each.

## CLI Smoke Commands

- [ ] **TUT-INFRA-050**: The Typer CLI shall expose a `smoke-llm` command that performs one completion against the configured LLM endpoint.
- [ ] **TUT-INFRA-051**: The Typer CLI shall expose a `smoke-import` command that verifies core package imports.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [High-Level Design](../../high-level-design.md)
