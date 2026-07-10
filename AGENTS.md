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
- **Notebooks**: **Marimo only for this tutorial** — all lesson content lives in Marimo (`.py` notebooks with reactive execution) under `notebooks/`. **Do not add Jupyter notebooks** (`.ipynb`) for tutorial delivery. For exploratory work outside the curriculum, still prefer Marimo over Jupyter. Launch in **sandboxed mode**: `uvx marimo edit --sandbox <folder>` (use `.` for the current directory). This ensures a fresh isolated environment with the latest package versions resolved automatically via `uvx`. For corporate laptops where `uvx --sandbox` fails, document the **non-sandbox fallback**: `pixi run marimo` (runs `marimo edit notebooks/` against the pre-built Pixi env, no network needed). **When editing Marimo notebooks, use only the [marimo-pair](.agents/skills/marimo-pair/SKILL.md) skill** — mutate cells via `marimo._code_mode` (`ctx.create_cell`, `ctx.edit_cell`, `ctx.run_cell`), not direct file edits (see [Marimo notebook editing](#marimo-notebook-editing)).

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

7. **All cells must have a name.** Every cell created or edited via `code_mode` must include an explicit `name` argument (e.g. `ctx.create_cell(code, name="my_cell")` or `ctx.edit_cell("my_cell", code=...)`). Never leave a cell unnamed — unnamed cells are hard to target, debug, and reason about across sessions.

8. **Full-rewrite vs targeted-edit workflow.** For a near-total notebook rewrite, the reliable path is: stop marimo → write the new `notebooks/*.py` on disk (correct `@app.cell` signatures + `return` tuples) → reopen. Once reopened, make ALL further targeted edits via `code_mode` (`edit_cell`/`create_cell`/`run_cell`) — do NOT repeat stop/restart cycles for each edit: the running kernel clobbers disk writes on save, and each restart loses marimo's live graph state. Stop/restart is for the initial rewrite only.

9. **One name, one cell (marimo's single-definition rule).** A name imported or assigned in two cells raises `MultipleDefinitionError`, which marks the defining cell `marimo-error` so its outputs never commit — and downstream cells then fail with `NameError` that *looks* like a broken dependency graph (but isn't). Centralize shared imports in the `with app.setup:` block (e.g. `Counter`, `tool`, `json`, `dedent`) and let cells reference them as params; never `from X import Y` the same `Y` in two cells, and never reuse a local variable name (e.g. `payload`) across two cells. **When a cell's `status` is `marimo-error`, read `cell.output.data` for the cause** (e.g. `MultipleDefinitionError(name='Counter', cells=('Kclp',))`) *before* assuming a graph-wiring bug and recreating cells.

Direct file edits are silently lost or clobbered when the kernel saves — the user will not see them. Disk reads are fine for inspection; prefer `ctx.cells[target].code` for live truth. Scaffolding a **new** notebook file on disk is OK only when no session is open yet; once marimo is running, switch to code mode for all further edits.

**Recovering from broken cells:** `code_mode` edits that omit `return` statements or land in `app._unparsable_cell(...)` break the reactive dependency graph (downstream `NameError`s). To fix:

1. **Read** all cells: iterate `ctx.cells.values()` and capture each cell's `name` and `code`.
2. **Delete** the broken cells with `ctx.delete_cell(name)`.
3. **Recreate** them with `ctx.create_cell(code=..., name=..., hide_code=...)` — or merge logic into an existing parsable `@app.cell` via `ctx.edit_cell`.
4. **Run** the edited cell and any downstream dependents in topological order with `ctx.run_cell(name)`.

If many cells are unparsable, dump live cell bodies, stop the session, rewrite `notebooks/*.py` with proper `@app.cell` function signatures (explicit dependency parameters), then reopen marimo — unparsable cells cannot be converted to parsable ones in-place via `edit_cell` alone.

Use **`pyprojroot.here()`** (or equivalent) for paths anchored at the project root when the project already uses `pyprojroot`; do not invent a new “find project root” helper.

### Exercise authoring standard

Each exercise is a **pair of cells** following a fixed shape (the Part 3 standard). The guiding principle: **minimize hand-built abstraction and expose how things work** — participants see the primitive (raw `LanceDBDocStore`, llamabot `@tool`, FastMCP) directly, and the scaffold makes them engage with the mechanism rather than wrapping it.

1. **Header cell** (`exN_header`, markdown, `hide_code=True`): prose explaining the mechanism and teaching point, then a fenced Python **skeleton with blanks** (`______`) outlining the solution — not the solution itself. Participants read the skeleton to know the shape; they fill the blanks in the scaffold.
2. **Scaffold cell** (`exN_scaffold`, code): a function **stub** to implement plus a **green reference call** so the notebook runs end-to-end out of the box, plus a **swap instruction**:
   - **Plain-function exercises**: the stub (`def <func>(...):` `# put your implementation here.` `pass`) and the green call (`<result> = part3.<func>(...)`) are separate lines. Instruction: *"Once you are done, delete `part3.` from the line below, keeping only `<func>`."*
   - **`@tool` exercises**: the decorator couples the definition to its invocation (the try-cell calls it directly), and the reference's signature differs from the local closure — so the `@tool` body defaults to the reference (`return part3.<func>(...)`) with a *"replace the body with your own logic"* instruction. Do **not** tell learners to "delete `part3.`" here — that would recurse.

Cell names track the exercise number: `exN_header`, `exN_scaffold`, `exN_built` (or `exN_try`). When exercises are reordered/renumbered, **rename the cells to match** via `code_mode` `edit_cell(target, code=<current>, name=<new>)` — the cell `def`-name must match the exercise number (no `ex2_*` cells under a `## Exercise 1` header). Rename in an order that frees names before reuse (rename `ex2_* → ex1_*` first, then `ex3_* → ex2_*`).

### Tutorial content review (pedagogy reviewer)

A read-only **`tutorial-pedagogy-reviewer`** subagent (`.opencode/agent/tutorial-pedagogy-reviewer.md`) reviews `notebooks/*.py` from a SciPy 2026 participant's lens — focusing on **language, vocabulary/jargon, and how new content is introduced** — and returns structured edit proposals (severity + location + rule + verbatim quote + concrete fix) that the main agent implements via marimo-pair. It applies an evidence-based checklist (vocabulary highest weight, then expertise calibration, cognitive load, pacing) drawn from `docs/research/adult-learning-pedagogy-for-technical-tutorials.md`. The audience is calibrated as **expert-in-domain, novice-in-topic**, so it flags both over-explanation of familiar Python (expertise reversal) and under-scaffolding of novel agent concepts.

- **Invoke**: `/review-pedagogy notebooks/01_intro_prompting.py` (single), or `/review-pedagogy` with no args to review all five in Part order (so earlier-part vocabulary isn't re-flagged).
- **The reviewer is read-only** (`edit: deny`, `bash: deny`) — it never edits; route its proposals through marimo-pair `code_mode` to apply, per [Marimo notebook editing](#marimo-notebook-editing).
- **Run it when** changing notebook prose, exercise framing, or introducing new technical vocabulary; keep the research doc's Section D (vocabulary/jargon) as the primary lens.

### Tutorial content review (consistency reviewer)

A read-only **`notebook-consistency-reviewer`** subagent (`.opencode/agent/notebook-consistency-reviewer.md`) catches the mechanical, nitty-gritty defects that slip past the build agent when restructuring: stray section numbers (e.g. a lone `Phase 6` among `Exercise 1/2`), an intro outline that no longer matches the cell sequence, recap/limitation cells naming a removed exercise or function, prose referencing a symbol the code no longer defines, and `# @spec` EARS anchors lost when logic is inlined.

- **Invoke**: `/review-consistency notebooks/03_tools_mcp_zotero.py` (single), or `/review-consistency` with no args to review Part 3 + its `docs/designs/mcp-tools/` docs.
- **The reviewer is read-only** (`edit: deny`, `bash: deny`) — route its findings through marimo-pair `code_mode` (notebooks) or direct edits (docs/code) to apply.
- **Dispatch after edits.** The main build agent **must** dispatch this reviewer (and the pedagogy reviewer, when prose changed) after any non-trivial notebook or design-doc edit — adding/removing/reordering exercises, renaming/inlining functions, or restructuring a notebook arc. Treat it as the mechanical backstop before declaring a restructure done.

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
- **Secrets** — never commit API keys, tokens, or machine-specific paths; use `.env` (gitignored) and documented env vars. **This extends to all public artifacts (PR descriptions, commit messages, issues, docs): never paste values read from `.env` — including endpoint URLs and hostnames, not just keys. Reference the variable name (`TUTORIAL_LLM_BASE_URL`), never its value.**
- **Generated or vendored trees** — do not “clean up” generated assets unless the user asked; some paths may be managed by Pixi, notebooks, or build tools.

## Optional: project glossary

Add a short subsection here once stable terms emerge (e.g. domain nouns, experiment IDs, dataset names) so agents use vocabulary consistently in code and docs.

---

*This repository was generated from [cookiecutter-python-project](https://github.com/ericmjl/cookiecutter-python-project). The [`pyds project init`](https://github.com/ericmjl/pyds-cli) command uses that template. Edit freely as the project grows.*
