# Agent instructions (build-deep-research-agent)

This file is **repo-local guidance** for coding agents (Cursor, Claude Code, Copilot, and similar) working in this repository. It is the **canonical** place to record project-specific conventions and lessons learned. Prefer updating this file over one-off chat memory.

## Instruction hierarchy

1. **This file (`AGENTS.md`)** — durable rules for *this* repo (stack, layout, style, workflows).
2. **`pyproject.toml`** — tool configuration (Ruff, pytest, Pixi, Hatch, etc.); treat as source of truth for settings.
3. **User chat** — immediate task scope; if the user gives a rule that should persist, fold it into this file (see [Self-improvement](#self-improvement)).

If `CLAUDE.md` or `.claude/CLAUDE.md` appears later, consolidate duplicated guidance here and point those files at `AGENTS.md` (or replace them with a short stub) so instructions do not conflict.

## Stack (do not fight the template)

- **Python**: `>=3.10` (see `pyproject.toml`).
- **Env / tasks**: **Pixi** — use `pixi run …` or `pixi shell` as documented in `pyproject.toml` and the project README.
- **Packaging**: **Hatchling** (`[build-system]` in `pyproject.toml`).
- **Lint & format**: **Ruff** (`ruff check`, `ruff format`) and **pre-commit** (see `.pre-commit-config.yaml`).
- **Tests**: **pytest** (`pixi run test` or the task name defined for tests).
- **CLI**: **Typer** — entrypoint wired in `pyproject.toml` under `[project.scripts]`; implementation lives under `build_deep_research_agent/`.
- **Docs**: **MkDocs** (Material) when the docs workflow is used (`mkdocs.yaml`, `docs/`).
- **Design docs**: **design-driven-dev** workflow — `docs/high-level-design.md` (HLD), `docs/designs/<feature>/LLD.md`, and `docs/designs/<feature>/<subfeature>-EARS.md`. Follow the arrow of intent: **HLD → LLD → EARS → tests → code**.
- **Notebooks**: **Marimo only for this tutorial** — all lesson content lives in Marimo (`.py` notebooks with reactive execution) under `notebooks/`. **Do not add Jupyter notebooks** (`.ipynb`) for tutorial delivery. For exploratory work outside the curriculum, still prefer Marimo over Jupyter. Launch in **sandboxed mode**: `uvx marimo edit --sandbox <folder>` (use `.` for the current directory). This ensures a fresh isolated environment with the latest package versions resolved automatically via `uvx`. **When editing Marimo notebooks, use only the [marimo-pair](.agents/skills/marimo-pair/SKILL.md) skill** — mutate cells via `marimo._code_mode` (`ctx.create_cell`, `ctx.edit_cell`, `ctx.run_cell`), not direct file edits (see [Marimo notebook editing](#marimo-notebook-editing)).

When adding dependencies, prefer declaring them in **`pyproject.toml`** and syncing the Pixi environment as this repo already does, rather than ad hoc `pip install` in prose unless the user asks for a one-off experiment.

## Repository layout (expectations)

- **Package code**: `build_deep_research_agent/` — main library and CLI.
- **Tutorial notebooks**: `notebooks/` — Marimo `.py` notebooks only (see [Stack](#stack-do-not-fight-the-template)).
- **Tests**: `tests/` — mirror public behavior; prefer pytest functions over heavy class taxonomies unless the codebase already uses patterns.
- **Docs**: `docs/` — MkDocs pages plus design specs (`high-level-design.md`, `designs/`). Keep navigation in `mkdocs.yaml` when adding published pages.
- **Config**: `pyproject.toml` at repo root; avoid duplicating tool config in random dotfiles.

## Tutorial content and design docs

This repo is a **SciPy 2026 tutorial** (deep research agent). Tutorial content and design documentation must stay aligned.

**When changing tutorial content** — notebooks under `notebooks/`, lesson exercises, instructor runbooks, or shared library APIs used by lessons — **update the design docs in the same change** (or in a immediately preceding commit on the same branch):

1. **HLD** (`docs/high-level-design.md`) — scope, curriculum, architecture, or non-goal changes.
2. **LLD** (`docs/designs/<feature>/LLD.md`) — feature-level technical design for the affected area.
3. **EARS** (`docs/designs/<feature>/<subfeature>-EARS.md`) — testable requirements; mark `[x]` when implemented, delete obsolete specs.

**Before implementing** new tutorial features, check coherence: EARS → LLD → HLD. If drift exists, fix docs first.

**Code traceability (EARS)**: Every implemented EARS (marked `[x]` in `*-EARS.md`) must have a matching `# @spec EARS-ID` comment in **code or tests**. Requirements:

- Place the comment **immediately adjacent** to the implementing class, function, statement, or test — not only at the top of the file.
- One `@spec` per EARS ID at the narrowest site that satisfies the requirement (e.g. on `SearcherAgent.run`, not only on the module docstring).
- When marking an EARS `[x]`, add or verify the `@spec` anchor in the **same change**.
- Marimo notebook cells: put `# @spec EARS-ID` on the line directly above the cell logic that implements the spec.
- PEP 723 `# /// script` blocks must contain **only** valid script metadata (TOML). Put `@spec` comments **outside** the block (immediately after `# ///`), never inside it.
- Negative or repo-wide specs with no single code site (e.g. “shall not include Jupyter notebooks”) may stay doc-only until a concrete enforcement point exists.

Example:

```python
def load_citation_fixtures() -> list[CitationRecord]:
    # @spec PROMPT-FIX-020
    ...
```

**Do not** land notebook or curriculum changes without a corresponding design-doc update — agents and instructors rely on `docs/` as the source of truth across sessions.

### Marimo notebook editing

When a Marimo session is running (or when building lesson notebooks interactively), **only edit notebooks through the marimo-pair skill** — never `Write` / `StrReplace` / `Edit` on `notebooks/*.py` directly.

1. Read the skill: `.agents/skills/marimo-pair/SKILL.md` (or the user-attached copy).
2. Discover the running server (`discover-servers.sh` or `--url http://127.0.0.1:<port>`).
3. Connect with `execute-code.sh` and mutate the notebook via **`marimo._code_mode`**:

   ```python
   import marimo._code_mode as cm

   async with cm.get_context() as ctx:
       ctx.edit_cell(target, code="...")  # full new cell body
       ctx.run_cell(target)  # required — see below
   ```

4. **Always run cells after structural changes.** `create_cell` and `edit_cell` only update the notebook graph; they do **not** execute code or refresh downstream outputs. After every `create_cell` or `edit_cell`, call `ctx.run_cell(...)` on that cell (and on downstream dependents when the change affects variables they consume). Skipping `run_cell` leaves stale kernel state, hidden errors, and a broken reactive graph — the user will not see your changes until cells run.

5. Install notebook deps with `ctx.packages.add(...)`, not `pip` / `uv add` in cells.

6. **Preserve the cell shape the user chose.** Before `edit_cell`, read `ctx.cells[target].code` and match it. Part 4 exercise cells (e.g. `ex1_workflow_tools`, `ex1_pocketflow_graph`, `ex1_run`) are often **flat top-level code** — imports and logic at cell scope, not wrapped in `def cell_name(...):`. Do **not** re-introduce an outer function wrapper when adding docstrings, imports, or other edits; pass only the cell body the user already has.

Direct file edits are silently lost or clobbered when the kernel saves — the user will not see them. Disk reads are fine for inspection; prefer `ctx.cells[target].code` for live truth. Scaffolding a **new** notebook file on disk is OK only when no session is open yet; once marimo is running, switch to code mode for all further edits.

**Recovering from broken cells:** `code_mode` edits that omit `return` statements or land in `app._unparsable_cell(...)` break the reactive dependency graph (downstream `NameError`s). To fix:

1. **Read** all cells: iterate `ctx.cells.values()` and capture each cell's `name` and `code`.
2. **Delete** the broken cells with `ctx.delete_cell(name)`.
3. **Recreate** them with `ctx.create_cell(code=..., name=..., hide_code=...)` — or merge logic into an existing parsable `@app.cell` via `ctx.edit_cell`.
4. **Run** the edited cell and any downstream dependents in topological order with `ctx.run_cell(name)`.

If many cells are unparsable, dump live cell bodies, stop the session, rewrite `notebooks/*.py` with proper `@app.cell` function signatures (explicit dependency parameters), then reopen marimo — unparsable cells cannot be converted to parsable ones in-place via `edit_cell` alone.

Use **`pyprojroot.here()`** (or equivalent) for paths anchored at the project root when the project already uses `pyprojroot`; do not invent a new “find project root” helper.

## Code style (match existing code)

- **Type hints** on new functions and public APIs.
- **`pathlib.Path`** over `os.path` where practical.
- **Ruff** is the formatter and linter; run `ruff format` / `ruff check` or `pre-commit run --all-files` before claiming work is clean.
- **Docstrings**: Sphinx-style with `:param` / `:returns` where the project already does so; do not strip existing docstring depth.
- Prefer **small, reviewable diffs** — avoid drive-by refactors unrelated to the task.

If the user’s global preferences (e.g. logging library) differ from this repo, **follow this repo’s existing patterns** unless the user explicitly asks to migrate.

## Quality gates (before saying “done”)

- Run **tests** (`pixi run test` or the repo’s test task) after substantive Python changes.
- Run **Ruff** / **pre-commit** when edits touch Python or config hooks care about.
- Do not claim CI passes unless you actually ran the relevant commands and they succeeded.

## Self-improvement (how this file evolves)

When the user corrects the agent (“always do X”, “never do Y”, “use Z for this repo”), treat that as a candidate **permanent** rule:

1. **Propose** a concrete edit to `AGENTS.md` (section + wording), integrated into existing bullets — not a dated diary entry.
2. **Resolve conflicts** — if the new rule contradicts an older bullet, replace or narrow the old text so there is a single clear rule.
3. **Ask once** — “Should I add this to `AGENTS.md`?” — and apply after confirmation.

This keeps agent behavior stable across sessions and contributors.

## Scope and safety

- **Stay within the task** — no broad refactors or unrelated files unless the user expands scope.
- **Secrets** — never commit API keys, tokens, or machine-specific paths; use `.env` (gitignored) and documented env vars.
- **Generated or vendored trees** — do not “clean up” generated assets unless the user asked; some paths may be managed by Pixi, notebooks, or build tools.

## Optional: project glossary

Add a short subsection here once stable terms emerge (e.g. domain nouns, experiment IDs, dataset names) so agents use vocabulary consistently in code and docs.

---

*This repository was generated from [cookiecutter-python-project](https://github.com/ericmjl/cookiecutter-python-project). The [`pyds project init`](https://github.com/ericmjl/pyds-cli) command uses that template. Edit freely as the project grows.*
