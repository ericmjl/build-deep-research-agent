# Gotchas

## Private variables are cell-scoped

Variables with a `_` prefix are **private to the cell that defines them** in
marimo. They cannot be referenced from other cells — you'll get a `NameError`.

This matters when building notebooks programmatically. A common mistake:

```python
# Cell A
_df = pd.DataFrame(results)   # _df is private to this cell

# Cell B — FAILS
mo.ui.table(_df)               # NameError: name '_df' is not defined
```

**Fix:** Either merge both into one cell, or use a non-private name (`df`).

## Duplicate public imports across cells

marimo enforces single-definition: a public name (like `pd`) can only be
defined in one cell. If two cells both `import pandas as pd`, you get a
`Multiply-defined names` error at validation.

**Fix:** Use a `_` prefix on the second import (`import pandas as _pd`) or
consolidate imports into a shared cell.

## Silent `marimo-error` status hides the real exception

The "Duplicate public imports" rule above bites SILENTLY at runtime, not as a
loud validation error. Symptom: a downstream cell `NameError`s a variable you
EXPECT an upstream cell to define (e.g. `papers`, `Counter`). You then waste
many turns debugging the NameError directly — suspecting timing (probe ran
before the cell finished), CWD (`pyprojroot.here()` failing in the kernel),
import failures — when the real cause is that the defining cell ERRORED and
never committed its variable.

**Diagnostic order (do this BEFORE debugging the NameError):**

1. Check the upstream cell's status — `ctx.cells["corpus_load"].status`.
   A value of `marimo-error` means the cell raised but the exception is NOT
   shown as a normal traceback in the output stream; downstream just sees the
   missing variable.
2. If status is `marimo-error`, extract the real exception from the
   `CellOutput` (see next section). The common culprit is a
   `MultipleDefinitionError(name='Counter', cells=('Kclp',))` — the same name
   imported/defined in two cells (e.g. `from collections import Counter` in
   both `corpus_load` and `corpus_show`).
3. Remove the duplicate definition (import once in a shared/setup cell, or
   drop it from one cell and let marimo inject it as a parameter).

The tell: the scratch `execute-code` run of the same body in isolation WORKS,
but the cell version `marimo-error`s — because the conflict only exists in the
notebook's multi-cell graph, not in a standalone snippet.

## Extracting a cell's error from `CellOutput`

When a cell has `status == "marimo-error"`, the exception is buried in the
`CellOutput` struct, NOT printed to stdout/stderr. `CellOutput` is a struct
(not a namedtuple — `._fields` is not useful) with fields including
`channel, data, mimetype, errors, stderr, stdout`. Read the structured error
via `output.errors` (a list) or `output.data`. The mimetype for a cell
exception is `application/vnd.marimo+error`.

```python
# cell errored silently — extract the real exception
o = ctx.cells["corpus_load"].output
print(o.errors)   # -> [MultipleDefinitionError(name='Counter', cells=('Kclp',))]
print(o.data)     # structured error payload
```

Generalizes: any time a cell's variable is unexpectedly missing downstream,
check `ctx.cells[name].status` for `marimo-error` and read `.output.errors`
before hypothesizing about timing/CWD/imports. Discovered build-deep-research-
agent Part 4 corpus notebook (07-07): a `Counter` import duplicated across two
cells silently broke `papers` for ~5 diagnostic turns before the
`MultipleDefinitionError` was extracted from the CellOutput.

## `inspect.getsource()` on methods is indented

`inspect.getsource()` on a class method preserves the original indentation.
Passing this to `ast.parse()` fails with `IndentationError`.

```python
# FAILS
src = inspect.getsource(SomeClass.some_method)
tree = ast.parse(src)  # IndentationError: unexpected indent

# FIX
import textwrap
src = textwrap.dedent(inspect.getsource(SomeClass.some_method))
tree = ast.parse(src)
```

## Cached module availability

Some libraries cache optional-dependency availability at import time. Installing
a package mid-session via `ctx.packages.add()` won't update those caches.
The user may need to restart the kernel — but try known workarounds first.

### Polars + pyarrow

`df.to_pandas()` fails with `ModuleNotFoundError: pa.Table requires 'pyarrow'`.

**Workaround** — if this error occurs after installing pyarrow mid-session,
run the following via `execute-code` (scratchpad), NOT in a cell. The patch
mutates the cached module object in the running kernel, so it doesn't need to
persist in the notebook.

```python
import pyarrow as _pa
import polars.dataframe.frame as _frame_mod
_frame_mod.pa = _pa
```

Then re-run the failing cell.

## Bare anywidget object not rendering

If a custom anywidget subclass (e.g., a 3Dmol.js viewer) is returned as the
last expression in a cell and shows `<__main__.MolViewer object at 0x...>`
instead of rendering the widget UI, wrap it with `mo.ui.anywidget()`.

Marimo may not auto-detect all anywidget subclasses as renderable —
`mo.ui.anywidget(widget)` guarantees the widget UI is displayed.

```python
# FAILS — shows object repr instead of widget UI
viewer = MolViewer(pdb_id="7OG3")
viewer

# FIX — wraps for guaranteed rendering
viewer = MolViewer(pdb_id="7OG3")
mo.ui.anywidget(viewer)
```

## `ctx.cells` is subscript-only (no `.get()`)

`ctx.cells` is a `_CellsView` object. It supports subscript access
(`ctx.cells["my_cell"]`) and iteration (`for name, cell in ctx.cells.items()`),
but it does **NOT** support `.get()`. Calling `ctx.cells.get(name)` raises
`AttributeError: '_CellsView' object has no attribute 'get'`.

```python
# FAILS
cell = ctx.cells.get("my_cell")        # AttributeError

# FIX — subscript + KeyError guard, or iterate
try:
    cell = ctx.cells["my_cell"]
except KeyError:
    cell = None

for name, cell in list(ctx.cells.items()):
    ...
```

## `cell.code` is the body only (no `def` / `return` wrapper)

`ctx.cells[name].code` returns the cell's **inner body** — the statements
*inside* the `def cell_name():` function — WITHOUT the function signature
line or the final `return (...)` tuple. marimo regenerates those on save.

This is why the skill says `ctx.edit_cell(name, code=...)` takes "the full
new cell body": the body is exactly what `.code` gives back. When you
reconstruct a cell for editing (e.g. round-tripping through `inspect` or a
diff), pass the **body only** — never wrap it in `def cell_name():` and never
append a `return (...)`. marimo owns those.

## Direct `execute-code` is scratch; `run_cell` persists

The skill says "Nothing you define persists between calls," which seems to
contradict `ctx.run_cell(name)` clearly making a cell's variables stick. The
distinction is the execution path:

- **Direct `execute-code.sh` / `execute_code()`**: runs your snippet in a
  SCRATCH context inside the kernel. It SHARES the notebook's globals, so it
  CAN read variables defined by notebook cells — but anything it *defines*
  does NOT persist into notebook state. Each call is isolated.
- **`ctx.run_cell(name)`** (via `code_mode`): executes an actual NOTEBOOK
  cell. Its variables persist in the kernel globals and downstream cells react.

Verification pattern this enables: `run_cell` the cells you changed via
`code_mode`, then issue a SEPARATE direct `execute-code` call to print the
now-persistent variables (e.g. `print(len(research_store))`,
`print(tools[:3])`). The scratch call reads the notebook globals your
`run_cell` calls populated — no persistence needed on the scratch side.
