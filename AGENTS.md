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
- **Notebooks**: **Marimo** — prefer Marimo (`.py` notebooks with reactive execution) over Jupyter for exploratory work. Always launch in **sandboxed mode**: `uvx marimo edit --sandbox <folder>` (use `.` for the current directory). This ensures a fresh isolated environment with the latest package versions resolved automatically via `uvx`.

When adding dependencies, prefer declaring them in **`pyproject.toml`** and syncing the Pixi environment as this repo already does, rather than ad hoc `pip install` in prose unless the user asks for a one-off experiment.

## Repository layout (expectations)

- **Package code**: `build_deep_research_agent/` — main library and CLI.
- **Tests**: `tests/` — mirror public behavior; prefer pytest functions over heavy class taxonomies unless the codebase already uses patterns.
- **Docs**: `docs/` — Markdown for MkDocs; keep navigation in `mkdocs.yaml` when adding pages.
- **Config**: `pyproject.toml` at repo root; avoid duplicating tool config in random dotfiles.

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
