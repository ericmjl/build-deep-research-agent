"""Load bundled Zotero-like citation fixtures."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from pyprojroot import here

from build_deep_research_agent.models import CitationRecord

FIXTURE_PATH = (
    here() / "build_deep_research_agent" / "fixtures" / "zotero_library.json"
)  # @spec PROMPT-FIX-001


@lru_cache(maxsize=1)
def load_citation_fixtures(path: Path | None = None) -> list[CitationRecord]:
    """Load citation records from the bundled JSON fixture.

    Parts 1–2 use these fixtures for in-context and memory exercises.
    Part 3 live Zotero queries use MCP — not fixtures as the default path.

    :param path: Optional override path for tests.
    :returns: Parsed citation records.
    """
    # @spec PROMPT-FIX-003
    # @spec PROMPT-FIX-011
    # @spec PROMPT-FIX-020
    fixture_path = path or FIXTURE_PATH
    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    return [CitationRecord.model_validate(item) for item in raw]
