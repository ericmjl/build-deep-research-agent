---
description: Review one or more Marimo tutorial notebooks + their design docs for mechanical consistency — section numbering, stray/renamed headers, intro outline matching the cell sequence, dangling references to removed exercises/functions, prose-vs-code drift, and @spec EARS anchor coherence. Returns structured findings.
agent: notebook-consistency-reviewer
---

Review these notebook(s) (and their design docs under `docs/designs/`) for
mechanical consistency and return structured findings per the output format in
your agent definition:

$ARGUMENTS

If no path was provided, review `notebooks/03_tools_mcp_zotero.py` and the
`docs/designs/embedded-mcp/` design docs by default (the most-recently
restructured part). When a specific notebook is given, also read its parent LLD
and EARS files so prose/code/doc drift is caught together.
