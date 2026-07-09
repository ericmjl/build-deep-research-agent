# Marimo Conventions — EARS

**Parent LLD**: [Tutorial Delivery LLD](./LLD.md)

## Notebook Format

- [ ] **TUT-MARIMO-001**: The tutorial shall deliver all five lesson notebooks as Marimo `.py` files under `notebooks/`. *(1 of 5: `05_multi_agent_demo.py`.)*
- [x] **TUT-MARIMO-002**: The tutorial shall not include Jupyter `.ipynb` files for lesson delivery.
- [ ] **TUT-MARIMO-003**: When `notebooks/01_intro_prompting.py` exists, the repository shall remove `notebooks/example_notebook.py`.

## Notebook Structure

- [ ] **TUT-MARIMO-010**: Each lesson notebook shall include a markdown cell stating learning objectives for its tutorial part.
- [x] **TUT-MARIMO-011**: Each lesson notebook shall include a facilitator discussion callout cell (markdown, non-executable). *(Part 5 only so far.)*
- [ ] **TUT-MARIMO-012**: Each lesson notebook shall include a setup cell for imports and environment checks. *(Part 4: `setup` cell.)*
- [ ] **TUT-MARIMO-013**: Each lesson notebook shall include a summary cell referencing the next notebook or session handoff where applicable.
- [x] **TUT-MARIMO-014**: Part 3 exercise functions (`compose_doc_text`, `make_docstore`, `zotero_search_items_fn`, `register_zotero_tools`) shall be implemented as **in-cell scaffolds** in `notebooks/03_tools_mcp_zotero.py`. Each scaffold runs green by default — logic functions (`compose_doc_text`, `zotero_search_items_fn`, `register_zotero_tools`) delegate to the reference answer in `exercises/solutions/part3.py`, while wiring functions (`make_docstore`) inline the wiring using the notebook's upstream functions so that learner overrides propagate (e.g. overriding `compose_doc_text` changes what `make_docstore` stores). Learners do the exercise by overriding the scaffold body (no separate stub module, no import comment-swap). *(Part 3. Parts 2 & 4 retain the legacy exercises-submodule pattern — see TUT-MARIMO-023 — pending migration.)*
- [x] **TUT-MARIMO-015**: Instructor materials for Parts 2 & 4 shall document comment-swapping the exercise import to load reference solutions. *(Parts 2 & 4; Part 3 loads reference answers by default — see TUT-MARIMO-014.)*
- [x] **TUT-MARIMO-023**: Parts 2 & 4 (pending migration to TUT-MARIMO-014) shall keep learner stubs in `exercises/partN.py` (`NotImplementedError`) with reference solutions in `exercises/solutions/partN.py`; notebooks import the stub directly and instructors comment-swap the import to load solutions. *(Parts 2 & 4.)*
- [x] **TUT-MARIMO-016**: Part 4 shall not use `importlib.reload` on exercise modules; materials shall instruct kernel restart after editing `exercises/part4.py`.
- [x] **TUT-MARIMO-017**: Part 4 Exercise 1a shall wire PocketFlow `@tool` nodes and graph edges in notebook cells; the library shall not provide a factory that hides linear tool construction (removed `make_deterministic_workflow_tools`).
- [x] **TUT-MARIMO-018**: Part 4 shall publish PocketFlow tool-body implementation specs in notebook markdown cells; learner exercise modules shall remain minimal stubs (pointing to the notebook), with full reference implementations in `exercises/solutions/part4.py`.
- [x] **TUT-MARIMO-022**: Part 2 shall not use `importlib.reload` on exercise modules; materials shall instruct kernel restart after editing `exercises/part2.py`. *(Part 2 `part2_exercises` cell.)*

## Marimo App Configuration

- [x] **TUT-MARIMO-020**: Each lesson notebook shall use `marimo.App(width="medium")` unless wide output requires `"full"`.
- [x] **TUT-MARIMO-021**: Where lesson-specific dependencies differ from Pixi, the notebook file shall include PEP 723 inline script metadata.

## Launch Documentation

- [ ] **TUT-MARIMO-030**: Instructor materials shall document launching notebooks with `uvx marimo edit --sandbox notebooks/` or a single notebook path.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [High-Level Design](../../high-level-design.md)
