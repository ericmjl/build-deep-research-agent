# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///
# @spec TUT-MARIMO-021
# @spec EMCP-RUN-001
# @spec EMCP-SRV-051
# @spec EMCP-RUN-021

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    """Setup cell: imports available to all exercise wiring."""

    import json
    from textwrap import dedent


@app.cell(hide_code=True)
def intro():
    # @spec EMCP-RUN-010
    import marimo as mo

    mo.md(
        dedent("""
        # Part 3: Tools — MCP and Zotero

        You now have prompts and memory. Part 3 adds **tools**: a way for the
        agent to *act* on the world rather than only talk about it.

        You will build a **Zotero research server** that exposes citation
        retrieval over the **Model Context Protocol (MCP)** — the same standard
        your coding assistant uses to call tools. The same file is both the
        teaching notebook and a runnable server:

        - **Narrative mode** (you are here): `marimo serve notebooks/03_tools_mcp_zotero.py`
        - **Server mode**: `uv run notebooks/03_tools_mcp_zotero.py` starts a headless
          MCP server any client can connect to.

        You build it in three exercises:

        1. **Document pipeline** — ingest citation papers into a semantic docstore.
        2. **Retrieval** — search the docstore and format results as an MCP payload.
        3. **MCP anatomy** — register the search **tool** and a metadata **resource**.

        Edit **`build_deep_research_agent/exercises/part3.py`** for the exercise
        functions; re-run the cell after saving.
        """)
    )
    return (mo,)


@app.cell(hide_code=True)
def instructor_note(mo):
    mo.md(
        dedent("""
        ### Instructors

        Reference solutions: `build_deep_research_agent/exercises/solutions/part3.py`

        In **part3_exercises**, comment out the learner import and uncomment the
        solutions import:

        ```python
        # from build_deep_research_agent.exercises import part3
        from build_deep_research_agent.exercises.solutions import part3
        ```

        Participants keep the default learner import only.
        """)
    )
    return


@app.cell(hide_code=True)
def mcp_anatomy(mo):
    mo.md(
        dedent("""
        ## MCP server anatomy

        An MCP server exposes four primitive types an agent can use:

        | Primitive | Purpose | FastMCP decorator |
        |-----------|---------|-------------------|
        | **Tools** | Actions the agent calls (search, summarize) | `@mcp.tool` |
        | **Resources** | Read-only data the agent requests | `@mcp.resource` |
        | **Prompts** | Pre-built message templates | `@mcp.prompt` |
        | **Apps** | Interactive UI components | `@mcp.app` |

        This notebook focuses on **tools** and **resources** for the Zotero server.

        Under the hood, FastMCP turns your typed Python functions into a JSON
        schema the agent can discover and call — parameter validation and return
        contracts are automatic.
        """)
    )
    return


@app.cell(hide_code=True)
def ex1_header(mo):
    mo.md(
        dedent("""
        ## Exercise 1 — Document pipeline

        A **docstore** stores documents and retrieves the ones most relevant to a
        query by *meaning* (semantic search via embeddings), not just keyword
        matching.

        llamabot's docstores are **string-in / string-out**: they retrieve
        document *text* but carry no per-document metadata. So
        `ZoteroDocstore` wraps a `LanceDBDocStore` with a **metadata side-table**
        (`dict[stored_text -> CitationRecord]`) so retrieved text maps back to
        rich citation items.

        The key decision is **what text to store** — that text is both what the
        docstore embeds and the key into the side-table.

        ### Exercise 1a — `compose_doc_text`

        Implement **`compose_doc_text`** in `exercises/part3.py`:

        Return a single string that captures what you want search to match. A
        good starting point combines the title, the authors, and the abstract
        (fall back to the title when there is no abstract). The string must be a
        stable function of the record — the same record always produces the same
        text.

        ### Exercise 1b — `make_docstore`

        Implement **`make_docstore`** in `exercises/part3.py`:

        1. Create a `ZoteroDocstore(table_name=table_name)`.
        2. Call `store.ingest(records, composer=compose_doc_text)` — pass *your*
           composer so the docstore stores the text you designed in 1a.
        3. Return the store.
        """)
    )
    return


@app.cell
def part3_exercises():
    from build_deep_research_agent.exercises import part3

    # Instructors: swap imports to load reference solutions.
    # from build_deep_research_agent.exercises.solutions import part3

    return (part3,)


@app.cell
def records():
    from build_deep_research_agent.fixtures.loader import load_citation_fixtures

    citation_records = load_citation_fixtures()
    print(f"Loaded {len(citation_records)} fixture papers.")
    return (citation_records,)


@app.cell
def ex1_docstore(citation_records, part3):
    research_store = part3.make_docstore(citation_records)
    return (research_store,)


@app.cell
def ex1_inspect(mo, research_store):
    stats = research_store.stats
    # @spec EMCP-DOC-050
    mo.md(
        dedent(f"""
        ### Docstore ready

        | Stat | Value |
        |------|-------|
        | Table | `{stats.table_name}` |
        | Documents ingested | {stats.document_count} |
        | Embedding model | `{stats.embedding_model}` |
        | Backend | `{stats.backend}` |

        The `{stats.backend}` backend means semantic embedding search is active.
        If the embedding model can't load, it falls back to keyword search.
        """)
    )
    return


@app.cell(hide_code=True)
def ex2_header(mo):
    mo.md(
        dedent("""
        ## Exercise 2 — Retrieval as a tool body

        Now wrap retrieval in the body of the `zotero_search_items` MCP tool.

        Implement **`zotero_search_items_fn`** in `exercises/part3.py`:

        1. Import `build_search_json` from `build_deep_research_agent.mcp.docstore`.
        2. Call `store.search(query, limit=limit)` to get `DocstoreSearchHit`s.
        3. Return `build_search_json(hits, mode=mode, stats=store.stats)`.

        Each hit carries the citation fields plus a `snippet` — the retrieved
        text excerpt most relevant to the query.
        """)
    )
    return


@app.cell
def ex2_try(part3, research_store):
    sample_payload = part3.zotero_search_items_fn(
        research_store, "Bayesian model checking", limit=3
    )
    sample = json.loads(sample_payload)
    print("mode:", sample["mode"], "| items:", len(sample["items"]))
    print("first title:", sample["items"][0]["title"])
    print("has snippet:", bool(sample["items"][0]["snippet"]))
    return (sample_payload,)


@app.cell(hide_code=True)
def ex3_header(mo):
    mo.md(
        dedent("""
        ## Exercise 3 — Register the MCP tool and resource

        FastMCP turns a decorated Python function into a discoverable MCP tool.
        Register the search tool plus a `zotero://metadata` resource on a server.

        Implement **`register_zotero_tools`** in `exercises/part3.py`:

        1. `@mcp.tool def zotero_search_items(query: str, limit: int = 5) -> str`
           — decorate a function with the same body as Exercise 2 (import
           `build_search_json` from `build_deep_research_agent.mcp.docstore`;
           use `store.search(...)` + `build_search_json(...)`).
        2. `@mcp.resource("zotero://metadata/{key}")` — return citation metadata
           JSON for a key (use `store.get_metadata(key)` and the stdlib `json`).
        3. `@mcp.resource("zotero://metadata")` — return `store.all_keys()` as JSON.

        These are the MCP **tool** and **resource** primitives from the table above.
        """)
    )
    return


@app.cell
def server_setup():
    from fastmcp import FastMCP

    # @spec EMCP-SRV-001
    # @spec EMCP-RUN-011
    mcp = FastMCP(
        name="zotero-research",
        instructions=(
            "Embedded Zotero MCP server for SciPy 2026 Part 3. "
            "Semantic search over an ingested citation docstore."
        ),
    )
    print("FastMCP server:", mcp.name)
    return FastMCP, mcp


@app.cell
def ex3_register(mcp, part3, research_store):
    # @spec EMCP-SRV-010
    # @spec EMCP-SRV-020
    part3.register_zotero_tools(mcp, research_store, mode="fixtures")
    return


@app.cell
async def ex3_inspect(mcp, mo):
    tools = await mcp.list_tools()
    templates = await mcp.list_resource_templates()
    mo.md(
        dedent(f"""
        ### Server assembled

        **Tools:** {", ".join(t.name for t in tools) or "_(none)_"}

        **Resource templates:** {", ".join(str(t.uri_template) for t in templates) or "_(none)_"}

        The tool schema (parameters, types, defaults) was generated automatically
        from your typed Python function — that is the MCP contract an agent calls.
        """)
    )
    return


@app.cell(hide_code=True)
def ex4_header(mo):
    mo.md(
        dedent("""
        ## Test it — call the tool over MCP

        This cell calls `zotero_search_items` **through FastMCP's protocol** (not
        the raw function) — the same path an external agent takes. Then it reads
        a `zotero://metadata/{key}` resource.

        In **server mode** (`uv run notebooks/03_tools_mcp_zotero.py`) the
        `__main__` block builds the reference server and any MCP client can do
        exactly this over stdio.
        """)
    )
    return


@app.cell
async def ex4_call_tool(json, mcp, mo):
    # @spec EMCP-SRV-013
    # @spec EMCP-RUN-012
    result = await mcp.call_tool(
        "zotero_search_items", {"query": "Bayesian", "limit": 3}
    )
    payload = json.loads(result.content[0].text)
    items = payload["items"]

    mo.stop(
        not items,
        mo.md(f"_No results. Message: {payload.get('message', '(none)')}_"),
    )

    item = items[0]
    meta_res = await mcp.read_resource(f"zotero://metadata/{item['key']}")
    meta = json.loads(meta_res.contents[0].content)

    mo.md(
        dedent(f"""
        ### Tool call result

        - **Items returned:** {len(items)}
        - **Backend mode:** `{payload["mode"]}`
        - **Top hit:** {item["title"]}
        - **Snippet:** _{item["snippet"][:120]}…_

        **Resource** `zotero://metadata/{item["key"]}` → found: `{meta["found"]}`
        """)
    )
    return


@app.cell(hide_code=True)
def recap(mo):
    mo.md(
        dedent("""
        ## Recap — docstore + MCP = extensible research backend

        - You built a **semantic docstore** (LanceDB embeddings + a metadata
          side-table) so retrieval returns structured citation items.
        - You exposed it as an **MCP tool** (`zotero_search_items`) and a
          **resource** (`zotero://metadata/{key}`) — the standard any agent client speaks.
        - The **same file** runs as a headless server (`uv run`) or an interactive
          notebook (`marimo serve`).

        **Next:** Part 4 wires tools like these into planning workflows
        (deterministic vs. ReAct), and Part 5 shows specialized agents
        collaborating over them.
        """)
    )
    return


if __name__ == "__main__":
    # Dual-mode server entry point.
    # @spec EMCP-SRV-050
    # @spec EMCP-RUN-020
    # @spec EMCP-RUN-003
    # `uv run notebooks/03_tools_mcp_zotero.py` starts a headless stdio MCP
    # server built from the reference implementation. Use `marimo serve` for
    # the interactive narrative above.
    from build_deep_research_agent.mcp.docstore import build_zotero_research_server

    # @spec EMCP-RUN-001
    # @spec EMCP-RUN-002
    # @spec EMCP-SRV-003
    build_zotero_research_server().run(transport="stdio", show_banner=False)
