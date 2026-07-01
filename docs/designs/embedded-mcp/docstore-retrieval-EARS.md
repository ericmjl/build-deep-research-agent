# Docstore & Retrieval — EARS

**Parent LLD**: [./LLD.md](./LLD.md)

## Docstore Initialization

- [x] **EMCP-DOC-001**: The system shall create a `ZoteroDocstore` wrapping a llamabot `LanceDBDocStore` instance with table name `"zotero_papers"`.
- [x] **EMCP-DOC-002**: The system shall configure the docstore with an embedding model (default: `minishlab/potion-base-8M`).
- [x] **EMCP-DOC-003**: The system shall persist the docstore collection on disk (via LanceDB `storage_path`) so it survives notebook restarts.

## Document Ingestion

- [x] **EMCP-DOC-010**: The system shall ingest papers from Zotero (pyzotero or fixtures) into the docstore.
- [x] **EMCP-DOC-011**: Each ingested paper's Zotero key shall be retrievable via the side-table (the record's `.key` is carried as the side-table value; the table is keyed by the composed document text, not by the key).
- [x] **EMCP-DOC-012**: The system shall store the paper's abstract (or title if abstract is unavailable) as the searchable text.
- [x] **EMCP-DOC-013**: The system shall record citation metadata (`CitationRecord`) in a side-table keyed by the stored document text, because llamabot docstores carry no native per-document metadata.

## Chunking & Embedding

- [x] **EMCP-DOC-020**: Chunking and embedding happen inside `LanceDBDocStore`; the wrapper does not implement its own chunking.
- [x] **EMCP-DOC-021**: Retrieved text maps back to the parent document's citation metadata via the side-table.

## Retrieval

- [x] **EMCP-DOC-040**: The system shall support semantic retrieval over the docstore via `ZoteroDocstore.search(query, limit)`.
- [x] **EMCP-DOC-041**: The `zotero_search_items` MCP tool shall use `search` to find relevant papers.
- [x] **EMCP-DOC-042**: Each search result shall include a `snippet` field containing the retrieved text excerpt.
- [x] **EMCP-DOC-043**: The search shall return at most `limit` results (default 5).

## Docstore Statistics

- [x] **EMCP-DOC-050**: The `zotero_search_items` tool output shall include `docstore_stats` with: `table_name`, `document_count`, `embedding_model`, and `backend`. *(Raw embedding dimension is not exposed by the llamabot docstore public API.)*

## Fallback Behavior

- [x] **EMCP-DOC-060**: If the embedding model cannot be downloaded or initialized, the system shall fall back to keyword search over the side-table records.
- [x] **EMCP-DOC-061**: If the docstore is empty (no papers ingested), the system shall return an empty `items` array with a descriptive message.

## Related Documents

- [Embedded MCP LLD](./LLD.md)
