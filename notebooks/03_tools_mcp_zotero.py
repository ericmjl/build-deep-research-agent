# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "build-deep-research-agent",
# ]
# ///
# @spec TUT-MARIMO-021

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")

with app.setup:
    """Imports available to every cell."""

    import json
    from collections import Counter
    from textwrap import dedent

    import marimo as mo
    from llamabot import tool


@app.cell(hide_code=True)
def walkthrough():
    # A guided, cell-by-cell walkthrough of Part 3. Click "Start tour" to be
    # talked through the exercises (plus the optional Zotero stretches).
    from wigglystuff import CellTour

    tour = mo.ui.anywidget(
        CellTour(
            steps=[
                {
                    "cell_name": "intro",
                    "title": "Part 3: Tools",
                    "description": "Part 3 adds tools - typed functions an agent can call to act on the world. We build a docstore, expose it as a @tool, then cross the process boundary with MCP.",
                },
                {
                    "cell_name": "corpus_header",
                    "title": "The data",
                    "description": "This free arXiv + JOSS corpus stands in for a reference library - no credentials needed.",
                },
                {
                    "cell_name": "ex1_header",
                    "title": "Exercise 1: docstore",
                    "description": "Build a docstore over the corpus with raw LanceDBDocStore, and keep a side-table mapping each chunk back to its paper.",
                },
                {
                    "cell_name": "ex2_header",
                    "title": "Exercise 2: @tool",
                    "description": "Wrap retrieval as a llamabot @tool called search_corpus - retrieve chunks, project to papers, return a dict.",
                },
                {
                    "cell_name": "ex3_header",
                    "title": "Exercise 3: MCP server",
                    "description": "Your @tool only works in-process. Now expose it as a standalone MCP server so any coding assistant can call it.",
                },
                {
                    "cell_name": "stretch_intro",
                    "title": "Stretch: your Zotero",
                    "description": "Finish early? These optional stretches point the same tools at your real Zotero library - keyword, then semantic over abstracts + PDF full text, then MCP. Needs credentials.",
                },
                {
                    "cell_name": "ex4_header",
                    "title": "Exercise 4 (stretch): keyword",
                    "description": "Keyword-search your Zotero library as a @tool via pyzotero - a warm-up before the docstore.",
                },
                {
                    "cell_name": "ex5_header",
                    "title": "Exercise 5 (stretch): semantic",
                    "description": "Build a docstore over your abstracts + extracted PDF full text, then retrieve by meaning as a @tool.",
                },
                {
                    "cell_name": "ex6_header",
                    "title": "Exercise 6 (stretch): MCP",
                    "description": "Serve your Zotero semantic search as a standalone FastMCP server.",
                },
                {
                    "cell_name": "recap",
                    "title": "Recap",
                    "description": "tool -> docstore + side-table -> @tool -> MCP server. Next: Part 4 planning workflows.",
                },
            ],
            auto_start=False,
        )
    )
    tour
    return


@app.cell(hide_code=True)
def hero():
    mo.md(
        dedent(
            r"""
            <div style="display:flex;align-items:center;gap:1.2rem;background:linear-gradient(120deg,#0f172a,#1e293b);color:#e2e8f0;padding:1.3rem 1.6rem;border-radius:0.6rem;border-left:6px solid #38bdf8;">
              <svg width="120" height="60" viewBox="0 0 120 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <line x1="14" y1="16" x2="14" y2="44" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 4"/>
                <circle cx="14" cy="12" r="6" fill="#38bdf8"/>
                <text x="26" y="15" fill="#cbd5e1" font-size="9" font-family="monospace">@tool</text>
                <circle cx="14" cy="30" r="5" fill="none" stroke="#38bdf8" stroke-width="2"/>
                <text x="26" y="33" fill="#cbd5e1" font-size="9" font-family="monospace">docstore</text>
                <circle cx="14" cy="48" r="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
                <text x="26" y="51" fill="#cbd5e1" font-size="9" font-family="monospace">MCP</text>
              </svg>
              <div>
                <div style="font-size:1.5rem;font-weight:700;letter-spacing:-0.01em;line-height:1.15;">Part 3 &middot; Tools &mdash; from <span style="color:#38bdf8;">@tool</span> to MCP</div>
                <div style="opacity:0.82;margin-top:0.25rem;font-size:0.95rem;">Build a Deep Research Agent &nbsp;&middot;&nbsp; SciPy 2026 &nbsp;&middot;&nbsp; Eric Ma</div>
              </div>
            </div>
            """
        )
    )
    return


@app.cell(hide_code=True)
def intro():
    mo.md(
        dedent(
            """
            You now have prompts and memory. Part 3 adds **tools**: a way for the
            agent — the LLM + prompt + memory loop you've been building — to *act*
            on the world (search a library, query a docstore) rather than only talk
            about it. When we mean your *editor's* agent (Cursor, Claude, opencode)
            we'll say **coding assistant**, to keep the two distinct.

            We build one real capability across **three beats**, then cross the wall
            that **MCP (Model Context Protocol)** — a standard for exposing
            capabilities to any LLM client — was built for:

            1. **A free corpus** — ≥30 arXiv + JOSS full texts bundled in the repo,
               standing in for a reference library so nothing needs credentials.
            2. **A docstore** (a store that indexes text so you can retrieve it by
               *meaning*) over the corpus, wired with raw llamabot `LanceDBDocStore`
               (Exercise 1).
            3. **A `@tool`** exposing docstore query to an in-process agent
               (Exercise 2) — then the wall: only *this* process can call it.

            Crossing the wall:

            4. **A standalone MCP server** (Exercise 3) — expose the same capability
               over MCP so your coding assistant can call it.

            Exercises 1 and 2 live in the **scaffold cell** below each spec; Exercise
            3's scaffold is a source file you edit
            (`scripts/serve_corpus_mcp_starter.py`). Every scaffold runs green by
            default — it delegates to the reference answer
            (`exercises/solutions/part3.py`) — so the notebook works end-to-end out
            of the box. Replace a scaffold body to do the exercise yourself.
            """
        )
    )
    return


@app.cell(hide_code=True)
def instructors():
    mo.md(
        dedent(
            """
            ### Instructors

            Reference answers: `build_deep_research_agent/exercises/solutions/part3.py`
            (which delegates to `build_deep_research_agent/tools/`). Every scaffold
            delegates to it by default, so the notebook runs green with no comment-swap.
            Doing the exercise means replacing a scaffold body with a real implementation.
            """
        )
    )
    return


@app.cell(hide_code=True)
def tools_intro():
    mo.md(
        dedent(
            """
            ## What is a tool?

            A **tool** is a typed Python function with a describable contract: a name,
            parameters, a docstring, and a return value. llamabot's `@tool` decorator
            turns such a function into something an in-process agent can discover and
            call — the signature becomes a JSON schema the agent reads to decide when
            to use it.

            ```python
            from llamabot import tool

            @tool
            def search_corpus(query: str, limit: int = 5) -> dict:
                \"\"\"Semantic search over the ingested paper corpus.\"\"\"
                ...
            ```

            You'll build this tool over the corpus below, then hit the wall that
            motivates MCP.
            """
        )
    )
    return


@app.cell
def part3_import():
    # Reference answers, imported by default so the notebook runs end-to-end.
    from build_deep_research_agent.exercises.solutions import part3

    return (part3,)


@app.cell(hide_code=True)
def corpus_header():
    mo.md(
        dedent(
            """
            ## A free corpus that stands in for a reference library

            A real Zotero library needs credentials and setup. To keep Part 3
            self-contained, we bundle a **free corpus** that needs no setup: ≥30
            full-text papers fetched from arXiv and the Journal of Open Source
            Software, spanning AI, astrophysics, computational biology, and
            scientific computing. The papers live under
            `build_deep_research_agent/fixtures/corpus/` (extracted text only).

            Treat this corpus as your reference library for the rest of Part 3 —
            it is the substrate for the docstore you build next.
            """
        )
    )
    return


@app.cell
def corpus_load():
    from build_deep_research_agent.fixtures.loader import load_corpus_papers

    papers = load_corpus_papers()
    by_domain = Counter(p.domain for p in papers)
    print(f"{len(papers)} papers | domains: {dict(by_domain)}")
    return (papers,)


@app.cell(hide_code=True)
def corpus_show(papers):
    counts = Counter(p.domain for p in papers)
    mo.md(
        dedent(
            f"""
            ### Corpus loaded

            {len(papers)} papers across:
            {", ".join(f"`{d}` ({n})" for d, n in counts.most_common())}.

            Each `CorpusPaper` carries `title`, `authors`, `year`, `full_text`,
            `source` (`arxiv`/`joss`), `source_id`, `url`, and `domain`.
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex1_header():
    mo.md(r"""
    ## Exercise 1 — Build a docstore over the corpus (raw LanceDB)

    llamabot's `LanceDBDocStore` is **string-in / string-out**: it stores and
    retrieves document *text* but carries no per-document metadata. Under the hood
    it turns each stored chunk into a **vector embedding** — a numeric fingerprint
    of the chunk's meaning — and `retrieve(query)` ranks chunks by **cosine
    similarity** to the query's embedding, so matches are by *meaning* rather than
    keyword. You don't write the embedding step; `LanceDBDocStore` does it. Because
    the docstore hands back only text, you wire it directly and keep a
    **side-table** mapping each stored chunk back to its `CorpusPaper`:

    1. `from llamabot import LanceDBDocStore` and instantiate it.
    2. For each paper, split `full_text` into chunks; `docstore.append(chunk)`
       and record `side_table[chunk] = paper`.

    Implement **`build_corpus_docstore`** in the scaffold cell below. It returns
    `(docstore, side_table)`. The key teaching point: the side-table is *your*
    job — the docstore gives you text back, you project it to metadata.

    Example skeleton below — fill in the blanks:

    ```python
    from collections import defaultdict
    from llamabot import LanceDBDocStore
    from build_deep_research_agent.models import CorpusPaper
    from build_deep_research_agent.tools.corpus import chunk_text


    def build_corpus_docstore(papers: list[CorpusPaper]):
        # Instantiate a new LanceDBDocStore.
        docstore = LanceDBDocStore(
            table_name=______,            # give an informative table name
            embedding_model=_______,      # an embedding model, e.g. "minishlab/potion-base-8M"
            auto_create_fts_index=False,  # vector semantic search, not keyword FTS
        )
        try:
            docstore.reset()  # idempotent: clear any persisted data from a prior run
        except Exception:  # noqa: BLE001
            pass

        # Side-table: the docstore is string-in/string-out, so retrieve() returns
        # only chunk *text*. This maps each chunk text -> the CorpusPaper(s) it came
        # from, so a retrieved chunk can be projected back to its metadata (title,
        # authors, ...). Without it you'd get text with no way to know which paper
        # it belongs to.
        side_table: dict[str, list[CorpusPaper]] = defaultdict(list)

        # Loop over papers
        for _____ in ______:
            # Then loop over each chunk in paper.full_text using chunk_text
            for _____ in __________(_____._________):
                # Append the chunk to the docstore
                ________.append(_____)
                # Ensure side_table index mapping chunk to paper is also updated
                side_table[_____].append(_____)

        return docstore, side_table
    ```
    """)
    return


@app.cell
def _():
    return


@app.cell
def ex1_scaffold(papers, part3, sidetable):
    # @spec TUT-MARIMO-014
    # @spec EMCP-DOC-010
    # @spec EMCP-DOC-011
    # Exercise 1 — build_corpus_docstore (raw LanceDBDocStore + side-table).
    # Default: delegates to the reference (tools.corpus.build_corpus_docstore).
    # Override to wire the docstore + side-table yourself.
    def build_corpus_docstore(papers):
        # put your implementation here.
        return docstore, sidetable

    # Once you are done, delete `part3.` from the line below, keeping only build_corpus_docstore
    docstore, side_table = part3.build_corpus_docstore(papers)
    return docstore, side_table


@app.cell(hide_code=True)
def ex1_built(papers, side_table):
    mo.md(
        dedent(
            f"""
            ### Docstore ready

            - Papers ingested: **{len(papers)}**
            - Chunks stored: **{len(side_table)}**
            - Backend: raw `LanceDBDocStore` (vector semantic search)

            Each chunk is a key into `side_table`, so a retrieved chunk projects back to
            its paper. That projection is exactly what Exercise 2 wraps as a tool.
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex2_header():
    mo.md(
        dedent(
            """
            ## Exercise 2 — Expose docstore query as a `@tool`

            Now wrap retrieval as a `@tool`. The docstore hands back chunk **text**;
            your job is to project each chunk to its paper through `side_table` (so the
            caller gets metadata, not just a string), dedupe so each paper appears once,
            and return the result as a dict.

            1. Retrieve chunk texts from the docstore.
            2. Project each text to its paper via `side_table`, deduping by
               `source_id` so each paper appears at most once.
            3. Return a payload dict (`mode`, `items`, `docstore_stats`).

            Example skeleton below — fill in the blanks:

            ```python
            from llamabot import tool


            @tool
            def search_corpus(query: str, limit: int = 5) -> dict:
                \"\"\"Semantic search over the ingested corpus.\"\"\"
                # 1. Retrieve chunk *texts* from the docstore (string-out!).
                #    Ask for `limit` results.
                texts = docstore.________(query, n_results=______)

                # 2. Project each text to its paper via side_table; dedupe by
                #    source_id so each paper shows up at most once.
                hits = []
                seen = set()
                for _____ in ______:                              # loop over the retrieved texts
                    for _____ in side_table._______(_____, ()):   # papers that contain this chunk
                        if _____._____ in seen:                   # already returned this paper? skip it
                            continue
                        seen.add(_____._____)                     # remember the paper
                        hits.append(                              # build the hit record
                            {
                                "title": _____.title,
                                "authors": _____.authors,
                                "year": _____.year,
                                "url": _____.url,
                                "source": _____.source,
                                "domain": _____.domain,
                                "snippet": _______,               # the retrieved chunk text
                            }
                        )
                        break
                hits = hits[:______]                              # cap at `limit` results

                # 3. Return the payload dict. Don't json.dumps it — the llamabot
                #    @tool / FastMCP layer serializes the dict to JSON for you.
                payload = {
                    "mode": "corpus",
                    "items": hits,
                    "docstore_stats": {
                        "document_count": _______,               # distinct papers ingested
                        "backend": "lancedb",
                    },
                }
                return payload
            ```
            """
        )
    )
    return


@app.cell
def ex2_scaffold(docstore, part3, side_table):
    # @spec TUT-MARIMO-014
    # @spec EMCP-DOC-040
    # @spec EMCP-TOOL-003
    # Exercise 2 — search_corpus @tool.
    # Default: delegates to the reference. Replace the body to retrieve from
    # the raw docstore + side-table yourself.

    @tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested corpus; returns a dict {items, docstore_stats}."""
        # put your implementation here (retrieve from `docstore`, project via `side_table`, return a dict).
        # The line below delegates to the reference so the notebook runs green —
        # replace it with your own logic (see the skeleton in the cell above).
        return part3.search_corpus(docstore, side_table, query, limit)

    return (search_corpus,)


@app.cell
def ex2_try(search_corpus):
    corpus_payload = search_corpus("protein structure prediction", 3)
    print(
        "items:",
        len(corpus_payload["items"]),
        "| docs:",
        corpus_payload["docstore_stats"]["document_count"],
    )
    if corpus_payload["items"]:
        item = corpus_payload["items"][0]
        print("top:", item["title"][:50], "| domain:", item["domain"])
        print("snippet:", item["snippet"][:100])
    return


@app.cell(hide_code=True)
def limitation():
    mo.md(
        dedent(
            """
            ## The limitation — these tools live in-process

            `search_corpus` works, but only for an agent built **in this notebook's
            process**. Your coding agent — Cursor, Claude, opencode — cannot reach it.
            It has no way to call a Python function living in a marimo kernel on your
            machine.

            This is the gap **MCP** (Model Context Protocol) fills: a standard protocol
            so *any* client can invoke the capability you built, over stdio or HTTP.
            The next step turns `search_corpus` into a standalone MCP server your editor
            can talk to.
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex3_header():
    mo.md(
        dedent(
            """
            ## Exercise 3 — Build a standalone MCP server

            Your `search_corpus` tool works, but only an agent in *this* notebook
            kernel can call it. An **MCP server** exposes the same capability over a
            standard protocol so *any* client — your coding assistant — can reach it.

            Open **`scripts/serve_corpus_mcp_starter.py`**. It is a complete FastMCP
            server except the `search_corpus` tool body is a stub. Fill it in by
            reusing your Exercise 2 logic, then run the verify cell below. The
            reference answer is `scripts/serve_corpus_mcp.py`.

            The shape of the file (fill in the blanks):

            ```python
            from fastmcp import FastMCP
            from build_deep_research_agent.exercises.solutions import part3
            from build_deep_research_agent.fixtures.loader import load_corpus_papers

            # 1. Create the MCP server.
            mcp = FastMCP(_______)                       # give it a name

            # 2. Build the docstore over the corpus.
            papers = ___________()                        # load the bundled corpus
            docstore, side_table = part3.________________(papers)   # Exercise 1's builder

            # 3. Attach the search_corpus tool to the server. The @mcp.tool decorator
            #    is what binds the function to the server. Fill the body by reusing
            #    your Exercise 2 logic (retrieve -> project via side_table -> dict).
            @mcp.tool
            def search_corpus(query: str, limit: int = 5) -> dict:
                \"\"\"Semantic search over the ingested paper corpus.\"\"\"
                ...

            if __name__ == \"__main__\":
                mcp.run(transport=_______)               # stdio: requests on stdin/stdout
            ```

            FastMCP auto-serializes your dict return into the JSON that travels over
            MCP — no `json.dumps` needed.
            """
        )
    )
    return


@app.cell
async def ex3_verify():
    # @spec EMCP-SRV-001
    # Exercise 3 — verify your MCP server in-process via FastMCP's in-memory client.
    # Default: smoke-tests the REFERENCE server. Once you've filled in
    # scripts/serve_corpus_mcp_starter.py, switch `which` to "starter" to test yours.
    import importlib

    from fastmcp import Client

    which = "reference"  # or "starter" — your filled-in server

    # Each script builds its server at MODULE LEVEL — no build_server() wrapper.
    # Open the file and you see every step: FastMCP(...) is created, the corpus is
    # ingested into a docstore, and `search_corpus` is attached via @mcp.tool. We
    # import the resulting `mcp` here. `reload` re-runs the module so we pick up the
    # latest code (and your edits to the starter) and rebuild the docstore fresh —
    # the server's docstore uses its own table, so it never clashes with Exercise 1.
    if which == "starter":
        import scripts.serve_corpus_mcp_starter as _srv
    else:
        import scripts.serve_corpus_mcp as _srv
    importlib.reload(_srv)
    server = _srv.mcp

    # Hand the FastMCP instance straight to `Client` for an IN-MEMORY transport: the
    # full MCP protocol (tool discovery, calls) with no subprocess and no network —
    # the same calls your coding assistant makes over stdio, routed in-process.
    async with Client(server) as client:
        result = await client.call_tool(
            "search_corpus", {"query": "protein structure prediction", "limit": 3}
        )

    # MCP results come back as content blocks; FastMCP serialized the tool's dict
    # return into a TextContent. Pull its `.text` and parse the JSON back to a dict.
    text = next((c.text for c in result.content if hasattr(c, "text")), "")
    payload = json.loads(text)
    print("mode:", payload["mode"], "| items:", len(payload["items"]))
    if payload["items"]:
        print("top:", payload["items"][0]["title"][:55])
    return


@app.cell(hide_code=True)
def ex3_connect():
    mo.md(
        dedent(
            """
            ### Connect your coding assistant

            In a terminal, start your server (the one you filled in, or the reference):

            ```bash
            pixi run python scripts/serve_corpus_mcp_starter.py   # yours
            # or: pixi run python scripts/serve_corpus_mcp.py      # reference
            ```

            This starts a **stdio** server — your coding assistant spawns the script
            as a subprocess and talks to it over standard input/output. Then point
            your assistant at it. Either:

            - **Ask the assistant** to configure itself: *"Add an MCP server running
              `pixi run python scripts/serve_corpus_mcp_starter.py` and list its tools."*
            - **Hand-edit** the assistant's MCP config (e.g. opencode's `opencode.json`
              / Claude Desktop's config) with a stdio entry for the command above.

            Once connected, ask about the corpus — the assistant will call
            `search_corpus` over MCP and summarize the papers it finds. That is the
            payoff: the capability you built as an in-process `@tool` is now reachable
            by any client that speaks MCP.
            """
        )
    )
    return


@app.cell(hide_code=True)
def stretch_intro():
    mo.md(
        dedent(
            """
            ## Stretch goals — search *your* Zotero library, by meaning

            The exercises above run on a bundled corpus. These stretches point the
            same ideas at **your actual Zotero library** — a quick keyword warm-up,
            then semantic search over your abstracts **and extracted PDF full
            text**, then an MCP server. They need real credentials (no fixture
            fallback here — that is the whole point).

            > **Zotero API setup.** `pyzotero` is the Python client for Zotero's web
            > API. To search *your* library you need a Zotero account and two values
            > from https://www.zotero.org/settings/keys:
            >
            > - **`ZOTERO_LIBRARY_ID`** — your numeric user ID (shown on that page).
            > - **`ZOTERO_API_KEY`** — create a new private key (read access is enough).
            >
            > Export both in your shell. Using a shared lab library? Also set
            > `ZOTERO_LIBRARY_TYPE=group` (default is `user`).

            1. **Exercise 4** — keyword-search your library as a `@tool` (warm-up).
            2. **Exercise 5** — semantic search: build a docstore over your abstracts
               + extracted PDF full text, then retrieve by meaning.
            3. **Exercise 6** — serve it over MCP.
            """
        )
    )
    return


@app.cell(hide_code=True)
def ex4_header():
    mo.md(
        dedent(
            """
            ### Exercise 4 — Keyword-search your Zotero library (`@tool`, warm-up)

            A minimal pyzotero call to confirm you can reach your library: wrap
            `client.top(q=query)` as a `@tool`. No fixture fallback — it raises if
            your `ZOTERO_*` credentials are not set.

            Skeleton — fill in the blanks:

            ```python
            import os
            from llamabot import tool


            @tool
            def search_zotero(query: str, limit: int = 5) -> dict:
                \"\"\"Keyword-search my Zotero library.\"\"\"
                from pyzotero import zotero

                client = zotero.______(
                    os.getenv("ZOTERO_LIBRARY_ID"),
                    os.getenv("ZOTERO_LIBRARY_TYPE", "user"),
                    os.getenv("ZOTERO_API_KEY"),
                )
                items = client.____(q=______, ______=limit)
                return {
                    "mode": "zotero",
                    "items": [
                        {"title": i["data"]["title"], "creators": i["data"]["creators"], "abstract": i["data"].get("abstractNote")}
                        for i in items
                    ],
                }
            ```
            """
        )
    )
    return


@app.cell
def ex4_scaffold(part3):
    # @spec EMCP-TOOL-001
    # Exercise 4 — keyword search_zotero @tool (warm-up, stretch).
    # Requires ZOTERO_LIBRARY_ID + ZOTERO_API_KEY (no fixture fallback).
    # Default below delegates to the reference; replace the body with your own
    # pyzotero call (see the skeleton above).

    @tool
    def search_zotero(query: str, limit: int = 5) -> dict:
        """Keyword-search my Zotero library; returns a dict {mode, items}."""
        return part3.search_zotero(query, limit)

    return (search_zotero,)


@app.cell
def ex4_try(search_zotero):
    try:
        zotero_payload = search_zotero("bayesian", 5)
        print(
            "mode:",
            zotero_payload["mode"],
            "| items:",
            len(zotero_payload["items"]),
        )
        if zotero_payload["items"]:
            print("first:", zotero_payload["items"][0]["title"][:60])
    except Exception:  # noqa: BLE001
        print("Set ZOTERO_LIBRARY_ID + ZOTERO_API_KEY to run this stretch.")
    return


@app.cell(hide_code=True)
def ex5_header():
    mo.md(
        dedent(
            """
            ### Exercise 5 — Semantic search over your Zotero library (`@tool`)

            Keyword search only matches literal terms. Build a **docstore** over your
            library so you can retrieve by *meaning* — the same idea as Exercise 1,
            but over your abstracts **and the full text extracted from your PDFs**.
            Two cells: build the docstore, then wrap retrieval as a `@tool`.

            **Build the docstore** — index each item's abstract + extracted PDF text:

            ```python
            from llamabot import LanceDBDocStore
            from build_deep_research_agent.tools.corpus import chunk_text
            from build_deep_research_agent.tools.zotero import (
                fetch_zotero_items, zotero_client, zotero_item_full_text,
            )


            def build_zotero_docstore():
                docstore = LanceDBDocStore(
                    table_name=_______, embedding_model=_______, auto_create_fts_index=False
                )
                docstore.reset()
                items = _______________()
                client = ____________()
                side_table = {}
                for item in items:
                    text = item.______ or ""                        # abstract
                    full = ____________________(client, item.key)   # PDF full text ("" if none)
                    if full:
                        text = text + "\\n\\n" + full
                    if not text.strip():
                        continue
                    for chunk in __________(text):
                        docstore.append(chunk)
                        side_table.setdefault(chunk, []).append(item)
                return docstore, side_table
            ```

            **Wrap retrieval as a `@tool`** (same shape as `search_corpus` in Ex 2):

            ```python
            @tool
            def search_zotero_semantic(query: str, limit: int = 5) -> dict:
                \"\"\"Semantic search over my Zotero library.\"\"\"
                texts = docstore.________(query, n_results=______)
                hits, seen = [], set()
                for text in texts:
                    for item in side_table.get(text, ()):
                        if item.key in seen:
                            continue
                        seen.add(item.key)
                        hits.append({"title": item.title, "creators": item.creators,
                                     "year": item.year, "url": item.url,
                                     "abstract": item.abstract, "snippet": text})
                        break
                return {"mode": "zotero-semantic", "items": hits[:______]}
            ```
            """
        )
    )
    return


@app.cell
def ex5_build(part3):
    # Exercise 5 — build a docstore over your Zotero library (abstract + PDF text).
    # Requires ZOTERO_* credentials. Default delegates to the reference.

    def build_zotero_docstore():
        return part3.build_zotero_docstore()

    try:
        zotero_docstore, zotero_side_table = build_zotero_docstore()
        print("ingested", len(zotero_side_table), "chunks")
    except Exception:  # noqa: BLE001
        print("Set ZOTERO_LIBRARY_ID + ZOTERO_API_KEY to build the docstore.")
        zotero_docstore, zotero_side_table = None, {}
    return zotero_docstore, zotero_side_table


@app.cell
def ex5_search(part3, zotero_docstore, zotero_side_table):
    # Exercise 5 — semantic search @tool over the Zotero docstore.
    # Default delegates to the reference; replace with your own retrieve logic.

    @tool
    def search_zotero_semantic(query: str, limit: int = 5) -> dict:
        """Semantic search over my Zotero library; returns a dict {mode, items}."""
        return part3.search_zotero_semantic(
            zotero_docstore, zotero_side_table, query, limit
        )

    return (search_zotero_semantic,)


@app.cell
def ex5_try(search_zotero_semantic):
    try:
        zotero_semantic_payload = search_zotero_semantic("protein structure", 3)
        print(
            "mode:",
            zotero_semantic_payload["mode"],
            "| items:",
            len(zotero_semantic_payload["items"]),
        )
        if zotero_semantic_payload["items"]:
            print("top:", zotero_semantic_payload["items"][0]["title"][:60])
    except Exception:  # noqa: BLE001
        print("Build the docstore first (needs ZOTERO_* credentials).")
    return


@app.cell(hide_code=True)
def ex6_header():
    mo.md(
        dedent(
            """
            ### Exercise 6 — Serve your Zotero library over MCP (stretch)

            Expose `search_zotero_semantic` as a standalone MCP server — same shape
            as the corpus server in Exercise 3, but over your real Zotero library.
            Save the skeleton at the **repo root** as `serve_zotero_mcp.py` (so the
            import resolves), fill in the blanks, run it, and connect your coding
            assistant.

            ```python
            from fastmcp import FastMCP
            from build_deep_research_agent.exercises.solutions import part3

            # 1. Create the MCP server.
            mcp = FastMCP(_______)                       # give it a name
            # 2. Build the docstore once (abstract + PDF full text).
            docstore, side_table = part3.build_zotero_docstore()

            @mcp.tool
            def search_zotero_semantic(query: str, limit: int = 5) -> dict:
                \"\"\"Semantic search over my Zotero library.\"\"\"
                ...   # reuse your Exercise 5 logic

            if __name__ == \"__main__\":
                mcp.run(transport=_______)               # stdio
            ```

            Then run `pixi run python serve_zotero_mcp.py` and connect your coding
            assistant (same steps as Exercise 3's connect cell).
            """
        )
    )
    return


@app.cell(hide_code=True)
def recap():
    mo.md(
        dedent(
            """
            ## Recap

            - A **tool** is a typed function; llamabot's `@tool` turns its signature
              into a schema an in-process agent can call.
            - llamabot's `LanceDBDocStore` is **string-in / string-out**; you wired it
              raw and kept a **side-table** to project retrieved text back to papers.
            - In-process tools hit a wall — only agents in *this* process can call them.
            - **MCP** crosses that wall: you exposed the same `search_corpus` as a
              standalone FastMCP server any coding assistant can call (Exercise 3).
            - **Stretch:** search your *own* Zotero library — keyword (Ex 4), semantic
              over abstracts + PDF full text (Ex 5), and MCP (Ex 6).

            **Next:** Part 4 wires tools like these into planning workflows
            (deterministic vs. ReAct), and Part 5 shows specialized agents collaborating.
            """
        )
    )
    return


if __name__ == "__main__":
    app.run()
