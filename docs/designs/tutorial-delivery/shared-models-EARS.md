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

## Two-Model Setup

- [x] **TUT-MODEL-040**: The `llm.py` module shall expose `get_small_model_name()` returning the model for Parts 1–2 (prompting, memory), defaulting to `ollama_chat/gemma2:2b` when `LLM_MODEL_SMALL` is unset.
- [x] **TUT-MODEL-041**: The `llm.py` module shall expose `get_large_model_name()` returning the model for Parts 3–5 (tools, workflows, multi-agent), defaulting to `ollama_chat/gemma4:12b` when `LLM_MODEL_LARGE` is unset.
- [x] **TUT-MODEL-042**: The `get_completion_kwargs()` function shall return empty kwargs when both models use the `ollama_chat/` prefix (local Ollama), and return `api_base`/`api_key` when either model uses the `openai/` prefix (remote Modal endpoint).
- [x] **TUT-MODEL-043**: The deprecated `get_model_name()` function shall remain as a backward-compatible alias for `get_large_model_name()`, emitting a `DeprecationWarning`.
- [x] **TUT-MODEL-044**: The `make_bot()` function in `utils.py` shall accept a `model` parameter (`"small"` or `"large"`, default `"small"`) selecting which tutorial model to use.

## Testing

- [x] **TUT-MODEL-040**: Unit tests shall verify `CitationRecord` construction from fixture JSON used in Parts 1–2.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [Fixtures EARS](../prompting/fixtures-EARS.md)
