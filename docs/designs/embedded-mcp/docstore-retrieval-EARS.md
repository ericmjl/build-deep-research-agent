# Docstore & Retrieval — EARS

**Parent LLD**: [./LLD.md](./LLD.md)

## Docstore Initialization

- [ ] **EMCP-DOC-001**: The system shall create a llamabot TurboQuantDocstore instance named `"zotero_papers"`.
- [ ] **EMCP-DOC-002**: The system shall configure the docstore with an embedding model (default: `all-MiniLM-L6-v2`).
- [ ] **EMCP-DOC-003**: The system shall persist the docstore collection on disk so it survives notebook restarts.

## Document Ingestion

- [ ] **EMCP-DOC-010**: The system shall ingest papers from Zotero (pyzotero or fixtures) into the docstore.
- [ ] **EMCP-DOC-011**: Each ingested paper shall be assigned a unique `doc_id` from the Zotero item key.
- [ ] **EMCP-DOC-012**: The system shall store the paper's abstract (or title if abstract is unavailable) as the searchable text.
- [ ] **EMCP-DOC-013**: The system shall store citation metadata (title, creators, date, tags) as docstore metadata.

## Chunking

- [ ] **EMCP-DOC-020**: The system shall use TurboQuant's automatic chunking to split documents into overlapping chunks.
- [ ] **EMCP-DOC-021**: Each chunk shall retain the parent document's metadata for context.

## Embedding

- [ ] **EMCP-DOC-030**: The system shall generate embeddings for each chunk using the configured embedding model.
- [ ] **EMCP-DOC-031**: The system shall store embeddings in a vector index for similarity search.

## Retrieval

- [ ] **EMCP-DOC-040**: The system shall support similarity search over the docstore via `docstore.similarity_search(query, k)`.
- [ ] **EMCP-DOC-041**: The `zotero_search_items` MCP tool shall use similarity search to find relevant chunks.
- [ ] **EMCP-DOC-042**: Each search result shall include a `snippet` field containing the chunk text excerpt.
- [ ] **EMCP-DOC-043**: The search shall return at most `limit` results (default 5).

## Docstore Statistics

- [ ] **EMCP-DOC-050**: The `zotero_search_items` tool output shall include `docstore_stats` with: total chunk count and embedding dimension.

## Fallback Behavior

- [ ] **EMCP-DOC-060**: If the embedding model cannot be downloaded or initialized, the system shall fall back to fixture-based keyword search.
- [ ] **EMCP-DOC-061**: If the docstore is empty (no papers ingested), the system shall return an empty `items` array with a descriptive message.

## Related Documents

- [Embedded MCP LLD](./LLD.md)
