# System Prompt — EARS

**Parent LLD**: [Prompting LLD](./LLD.md)

## Prompt Template

- [x] **PROMPT-SYS-001**: The `prompts.py` module shall export `RESEARCH_SYSTEM_PROMPT` as a plain-string template for research tasks.
- [ ] **PROMPT-SYS-002**: The `RESEARCH_SYSTEM_PROMPT` template shall be readable and editable in `notebooks/01_intro_prompting.py` without hidden indirection.
- [x] **PROMPT-SYS-003**: The `prompts.py` module shall export `build_messages(system, user, history=None)` returning a list of `Message` objects.

## Part 1 Notebook

- [ ] **PROMPT-SYS-010**: Notebook `01_intro_prompting.py` shall import `RESEARCH_SYSTEM_PROMPT` from `build_deep_research_agent.prompts`.
- [ ] **PROMPT-SYS-011**: Notebook `01_intro_prompting.py` shall allow participants to modify role, constraints, or output-format sections of the system prompt.
- [ ] **PROMPT-SYS-012**: When the participant runs Exercise 1, the notebook shall call the shared LLM module with the assembled messages.

## Discussion Content

- [ ] **PROMPT-SYS-020**: Notebook `01_intro_prompting.py` shall include facilitator prompts on research-agent use cases and limitations.

## Testing

- [x] **PROMPT-SYS-030**: `tests/test_prompts.py` shall verify `build_messages` produces correctly ordered roles.

## Related Documents

- [Prompting LLD](./LLD.md)
- [Static Summarization EARS](./static-summarization-EARS.md)
