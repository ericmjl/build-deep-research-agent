# Failure Mode Demos — EARS

**Parent LLD**: [Multi-Agent LLD](./LLD.md)

## Demo Presets

- [x] **MULTI-FAIL-001**: Notebook `05_multi_agent_demo.py` shall include a preset that runs the Synthesizer with empty evidence to demonstrate hallucination risk.
- [x] **MULTI-FAIL-002**: Notebook `05_multi_agent_demo.py` shall include a preset that injects oversized context to demonstrate context exhaustion or truncation behavior.
- [D] **MULTI-FAIL-003**: Notebook `05_multi_agent_demo.py` shall include a preset with low `REACT_MAX_STEPS` to demonstrate incomplete ReAct loops. *(Deferred until Part 4 `ReActRunner` exists.)*

## Facilitator Guidance

- [x] **MULTI-FAIL-010**: Each failure preset shall be accompanied by markdown notes on mitigations (max steps, truncation, structured outputs, human review).

## Architecture Recap

- [ ] **MULTI-FAIL-020**: Notebook `05_multi_agent_demo.py` shall include a recap diagram linking prompt → memory → tools → planning → multi-agent.

## Testing

- [x] **MULTI-FAIL-030**: Tests or notebook smoke checks shall verify empty-evidence preset produces a Synthesizer call with zero citations.

## Related Documents

- [Multi-Agent LLD](./LLD.md)
- [ReAct Runner EARS](../planning/react-runner-EARS.md)
- [Discussion Prompts EARS](./discussion-prompts-EARS.md)
