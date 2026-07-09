# Docstore & Retrieval — EARS

**Parent LLD**: [./LLD.md](./LLD.md) · **HLD**: Decision 8

> Revised 2026-07-06: the corpus path teaches **raw** `LanceDBDocStore` + an explicit side-table, not the `ZoteroDocstore` wrapper (which remains for the legacy citation-fixtures path / Parts 1–2).

## Corpus (phase 2)

- [x] **EMCP-DOC-001**: The repo shall bundle ≥30 full-text papers (arXiv + JOSS) under `build_deep_research_agent/fixtures/corpus/` spanning AI, astrophysics, computational biology, and other domains. *(40 papers shipped.)*
- [x] **EMCP-DOC-002**: A fetcher script (`scripts/fetch_corpus.py`, PEP 723) shall reproduce the corpus from arXiv (PDF→text) and JOSS (markdown). Only extracted `.txt`/`.md` are committed — no PDFs.
- [x] **EMCP-DOC-003**: `CorpusPaper` shall carry `title`, `authors`, `abstract`, `full_text`, `source`, `source_id`, `url`, `domain`.
- [x] **EMCP-DOC-004**: `load_corpus_papers() -> list[CorpusPaper]` shall load the bundled corpus with no network access.

## Docstore over the corpus (phase 3 — raw LanceDB)

- [x] **EMCP-DOC-010**: The notebook shall wire a raw `llamabot.LanceDBDocStore` directly (no `ZoteroDocstore` wrapper): instantiate, chunk each paper's `full_text`, `append` each chunk.
- [x] **EMCP-DOC-011**: Because `LanceDBDocStore` is string-in/string-out, the notebook shall keep an explicit side-table mapping each stored chunk text → its `CorpusPaper`(s) (+ chunk locator).
- [x] **EMCP-DOC-012**: Retrieval shall call `docstore.retrieve(query, n_results=limit)` and project each returned text back to its paper via the side-table.
- [x] **EMCP-DOC-013**: The docstore shall be configured with embedding model `minishlab/potion-base-8M`.

## Retrieval `@tool` (phase 4)

- [x] **EMCP-DOC-040**: `search_corpus` shall return at most `limit` results (default 5), each carrying the paper metadata + the retrieved `snippet`.
- [x] **EMCP-DOC-041**: Empty/whitespace `query` shall yield an empty `items` array with a descriptive message.
- [x] **EMCP-DOC-050**: The `search_corpus` JSON output shall include `docstore_stats` (`table_name`, `document_count`, `embedding_model`, `backend`).

## Legacy (ZoteroDocstore / citation fixtures — Parts 1–2 path, retained)

- [x] **EMCP-DOC-060**: `ZoteroDocstore` (in `mcp/docstore.py`) shall remain available for the legacy citation-fixtures path and the `build_zotero_research_server` shim, with its keyword fallback intact. *(Not taught in the new Part 3 arc.)*

The retained `mcp/docstore.py` (`ZoteroDocstore`) still carries `@spec` anchors for the behaviors below; they describe that superseded implementation, not the new corpus arc:

- [x] **EMCP-DOC-020**: Chunking and embedding happen inside `LanceDBDocStore`; the wrapper implements no chunking of its own.
- [x] **EMCP-DOC-021**: Retrieved text maps back to the parent document's citation metadata via the side-table.
- [x] **EMCP-DOC-042**: Each search result includes a `snippet` field containing the retrieved text excerpt.
- [x] **EMCP-DOC-043**: The search returns at most `limit` results (default 5).
- [x] **EMCP-DOC-061**: If the docstore is empty, the system returns an empty `items` array with a descriptive message.

## Related documents

- [Embedded MCP LLD](./LLD.md)
