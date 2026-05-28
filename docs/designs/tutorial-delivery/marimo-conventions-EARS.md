# Marimo Conventions — EARS

**Parent LLD**: [Tutorial Delivery LLD](./LLD.md)

## Notebook Format

- [ ] **TUT-MARIMO-001**: The tutorial shall deliver all five lesson notebooks as Marimo `.py` files under `notebooks/`. *(1 of 5: `05_multi_agent_demo.py`.)*
- [x] **TUT-MARIMO-002**: The tutorial shall not include Jupyter `.ipynb` files for lesson delivery.
- [ ] **TUT-MARIMO-003**: When `notebooks/01_intro_prompting.py` exists, the repository shall remove `notebooks/example_notebook.py`.

## Notebook Structure

- [ ] **TUT-MARIMO-010**: Each lesson notebook shall include a markdown cell stating learning objectives for its tutorial part.
- [x] **TUT-MARIMO-011**: Each lesson notebook shall include a facilitator discussion callout cell (markdown, non-executable). *(Part 5 only so far.)*
- [ ] **TUT-MARIMO-012**: Each lesson notebook shall include a setup cell for imports and environment checks.
- [ ] **TUT-MARIMO-013**: Each lesson notebook shall include a summary cell referencing the next notebook or session handoff where applicable.

## Marimo App Configuration

- [x] **TUT-MARIMO-020**: Each lesson notebook shall use `marimo.App(width="medium")` unless wide output requires `"full"`.
- [x] **TUT-MARIMO-021**: Where lesson-specific dependencies differ from Pixi, the notebook file shall include PEP 723 inline script metadata.

## Launch Documentation

- [ ] **TUT-MARIMO-030**: Instructor materials shall document launching notebooks with `uvx marimo edit --sandbox notebooks/` or a single notebook path.

## Related Documents

- [Tutorial Delivery LLD](./LLD.md)
- [High-Level Design](../../high-level-design.md)
