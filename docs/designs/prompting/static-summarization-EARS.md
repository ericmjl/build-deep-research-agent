# Static Summarization — EARS

**Parent LLD**: [Prompting LLD](./LLD.md)

## Citation Formatting

- [x] **PROMPT-SUM-001**: The `prompts.py` module shall export `format_citations_for_context(citations: list[CitationRecord]) -> str`.
- [x] **PROMPT-SUM-002**: When given a non-empty list of `CitationRecord` objects, `format_citations_for_context` shall return a non-empty string suitable for LLM context injection.

## Part 1 Exercise 2

- [x] **PROMPT-SUM-010**: Notebook `01_intro_prompting.py` shall load bundled citation fixtures for in-context summarization (no MCP, no memory module required).
- [x] **PROMPT-SUM-011**: When Exercise 2 runs, the notebook shall pass formatted citation context and a user question (e.g. theme synthesis) to the LLM.
- [x] **PROMPT-SUM-012**: Notebook `01_intro_prompting.py` shall display the model's summary output to the participant.

## Part 1 Exercise 3 (fulltext context)

- [x] **PROMPT-SUM-013**: Notebook `01_intro_prompting.py` shall provide Exercise 3 reusing Exercise 2's Identity, Instructions, and Examples, with **Context** defaulting to a fulltext snippet rather than bibliographic metadata.
- [x] **PROMPT-SUM-014**: When Exercise 3 preview runs, the notebook shall assemble and display messages using the fulltext context.
- [x] **PROMPT-SUM-015**: When Exercise 3 runs, the notebook shall pass the fulltext context and user question to the LLM and display the model's summary output.

## Scope Boundaries (Part 1)

- [x] **PROMPT-SUM-020**: Part 1 exercises shall not require MCP tool calls.
- [x] **PROMPT-SUM-021**: Part 1 exercises shall not require the memory module.

## Error Handling

- [ ] **PROMPT-SUM-030**: If LLM configuration is missing in Part 1 setup, the notebook shall surface an error naming required environment variables.
- [ ] **PROMPT-SUM-031**: If fixture loading fails, the notebook shall fail with a message indicating the fixture path.

## Testing

- [x] **PROMPT-SUM-040**: `tests/test_prompts.py` shall verify citation formatting includes title and creators for sample records.

## Related Documents

- [Prompting LLD](./LLD.md)
- [Fixtures EARS](./fixtures-EARS.md)
- [System Prompt EARS](./system-prompt-EARS.md)
