# Classroom Infrastructure — EARS

**Parent LLD**: [Tutorial Delivery LLD](./LLD.md)

## Modal LLM (Default Path)

- [x] **TUT-INFRA-001**: The default tutorial LLM path shall use a Modal-hosted open-source model via `TUTORIAL_LLM_BASE_URL`. *(Env var support in `llm.py`; Modal endpoint wired in `.env` → Qwen3.6-27B AWQ-INT4 vLLM on L40S.)*
- [ ] **TUT-INFRA-002**: The tutorial materials shall not require participants to supply their own LLM API keys for default exercises.
- [ ] **TUT-INFRA-003**: When `TUTORIAL_LLM_API_KEY` is required for the Modal endpoint, instructor materials shall provide the value for tutorial duration.
- [x] **TUT-INFRA-004**: The `llm.py` module shall configure llamabot from `TUTORIAL_LLM_*` environment variables.
- [x] **TUT-INFRA-005**: If tutorial LLM configuration is missing, `llm.py` shall raise an error naming the required environment variables.

## Optional BYO LLM

- [x] **TUT-INFRA-010**: Where a participant supplies an optional provider API key (e.g. `OPENAI_API_KEY`), `llm.py` shall support that path for comparison exercises.
- [ ] **TUT-INFRA-011**: Instructor materials shall document the optional BYO LLM path separately from the default Modal path.

## zotero-mcp (Part 3+)

- [x] **TUT-INFRA-020**: Part 3+ materials shall reference [zotero-mcp](https://github.com/54yyyu/zotero-mcp) for the upstream hand-install teaching path.
- [x] **TUT-INFRA-022**: The repository shall ship a tutorial FastMCP Zotero server as a cooking-show fallback when upstream install is not ready.
- [ ] **TUT-INFRA-021**: When implementation begins, instructor materials shall pin a minimum tested zotero-mcp version.

## Instructor Handoff

- [ ] **TUT-INFRA-030**: Notebook `02_memory_state.py` shall include a handoff cell recapping prompt + memory before Part 3.
- [ ] **TUT-INFRA-031**: Notebook `03_tools_mcp_zotero.py` shall open with a brief recap of Parts 1–2 without re-running prior exercises.

## Troubleshooting Documentation

- [ ] **TUT-INFRA-040**: `docs/index.md` shall document required environment variables and zotero-mcp setup.
- [ ] **TUT-INFRA-041**: Instructor troubleshooting docs shall include mitigations for Modal endpoint unavailability.
- [ ] **TUT-INFRA-042**: Instructor troubleshooting docs shall include mitigations for zotero-mcp connection failures.

## CLI Smoke Commands

- [ ] **TUT-INFRA-050**: The Typer CLI shall expose a `smoke-llm` command that performs one completion against the configured LLM endpoint.
- [ ] **TUT-INFRA-051**: The Typer CLI shall expose a `smoke-import` command that verifies core package imports.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [High-Level Design](../../high-level-design.md)
