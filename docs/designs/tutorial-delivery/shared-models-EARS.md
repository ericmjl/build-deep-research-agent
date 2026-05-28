# Shared Models — EARS

**Parent LLD**: [Tutorial Delivery LLD](./LLD.md)

## Message Model

- [x] **TUT-MODEL-001**: The `Message` model in `models.py` shall include a `role` field with values `system`, `user`, `assistant`, or `tool`.
- [x] **TUT-MODEL-002**: The `Message` model shall include a `content` field of type string.

## CitationRecord Model

- [x] **TUT-MODEL-010**: The `CitationRecord` model shall include fields `key`, `title`, `creators`, `year`, and `abstract`.
- [x] **TUT-MODEL-011**: The `CitationRecord.year` field shall accept an integer or `None`.
- [x] **TUT-MODEL-012**: The `CitationRecord.abstract` field shall accept a string or `None`.

## Package Layout

- [x] **TUT-MODEL-020**: The repository shall expose shared models from `build_deep_research_agent/models.py`.
- [x] **TUT-MODEL-021**: The repository shall expose LLM integration from `build_deep_research_agent/llm.py`.

## LLM Module

- [ ] **TUT-MODEL-030**: The `llm.py` module shall expose a callable interface for text completion from a list of `Message` objects (or equivalent llamabot pattern). *(Partial: `get_completion_kwargs()` only; `complete()` wrapper planned.)*
- [x] **TUT-MODEL-031**: The tutorial shall not use LangChain for LLM orchestration.

## Testing

- [x] **TUT-MODEL-040**: Unit tests shall verify `CitationRecord` construction from fixture JSON used in Parts 1–2.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [Fixtures EARS](../prompting/fixtures-EARS.md)
