# Finding and Invoking marimo

Only servers started with `--no-token` register in the local server registry
and are auto-discoverable — starting without a token makes discovery easier.
If a server has a token, set the `MARIMO_TOKEN` environment variable before
calling the execute script (avoids leaking the token in process listings).

```sh
marimo edit notebook.py --no-token [--sandbox]
```

How you invoke `marimo` depends on context — find the right way to run it.

## Inside a Python project

If there's a `pyproject.toml` in cwd or a parent directory, check that marimo
is actually in the dependencies before using the project's runner. Look for
`marimo` in:

- `[project.dependencies]`
- `[project.optional-dependencies]` or `[dependency-groups]` (dev deps)
- `[tool.pixi.dependencies]`
- The project's `.venv` (`uv pip show marimo` or check `.venv/bin/marimo`)

If marimo is in a named dependency group (not the default), you need to
specify it:

```sh
# marimo is in [dependency-groups] → "notebooks" group
uv run --group notebooks marimo edit notebook.py --no-token
```

Once you know marimo is available, use whatever CLI runner the project uses:

```sh
# uv-managed project
uv run marimo edit notebook.py --no-token
# pixi-managed project
pixi run marimo edit notebook.py --no-token
```

Skip `--sandbox` here — the project already manages dependencies.

## Pixi-managed projects: three critical gotchas

Pixi projects (e.g. build-deep-research-agent) often define a `marimo` task
in `pyproject.toml` that already includes subcommands (e.g.
`marimo = "marimo edit notebooks/ --no-sandbox --no-token"`). This causes
three gotchas that have wasted multiple sessions:

### 1. Pixi task arg mangling

`pixi run marimo edit notebooks/ --no-token` **double-appends** args because
the task command string is prepended wholesale — the actual invocation becomes
`marimo edit notebooks/ --no-sandbox --no-token edit notebooks/ --no-token`.

**Fix:** bypass the task alias by invoking the module directly:

```sh
pixi run python -m marimo edit notebooks/ --no-sandbox --no-token
```

General rule: when a pixi task already includes subcommands, do **not** pass
the same subcommands as extra args. Either call the bare task (`pixi run
marimo`) or use `python -m` to bypass it.

### 2. Background process required (OpenCode)

Marimo is a **long-running server**. If you start it in the foreground, the
shell tool will block/die and you will never be able to connect to it.
**Always start marimo as a background process:**

```sh
# OpenCode: nohup + & (the shell tool would otherwise block forever)
nohup pixi run python -m marimo edit notebooks/ --no-sandbox --no-token   &>/tmp/marimo.log &
sleep 2  # let it bind
```

The SKILL.md mentions `run_in_background` — that is Claude Code API language.
In OpenCode, the equivalent is `nohup ... &` (shell backgrounding).

### 3. Single-file mode throws `file_not_found`

`marimo edit <file>.py` (single-file mode) starts the server but throws
`file_not_found` websocket errors when the browser or `execute-code.sh`
connects (marimo 0.23.x `_single.py` resolver quirk with relative paths).

**Fix:** use **directory mode** instead and open the file from the browser:

```sh
# directory mode (reliable) — then open the specific file in the browser
nohup pixi run python -m marimo edit notebooks/ --no-sandbox --no-token   &>/tmp/marimo.log &
# open http://localhost:<port> and click the file, or navigate to
# http://localhost:<port>/?file=<file>.py
```


If `pyproject.toml` exists but marimo is **not** in the deps, treat this as
"outside a project" (see below).

## Outside a Python project

Prefer `--sandbox`. Sandbox mode creates an isolated environment for the
notebook and writes dependencies into the script itself as inline PEP 723
metadata — so the notebook stays self-contained and reproducible.

```sh
# With uv available (preferred)
uvx marimo@latest edit notebook.py --no-token --sandbox

# With marimo installed globally
marimo edit notebook.py --no-token --sandbox
```

## Global marimo install

If marimo is installed globally, check the version — code mode shipped in
v0.21.1. If the installed version is older, prompt the user to upgrade before
proceeding.

## Nothing found

If no project marimo, no `uv`/`uvx`, and no global `marimo` on PATH, tell the
user to install `uv` (<https://docs.astral.sh/uv/getting-started/installation/>).
