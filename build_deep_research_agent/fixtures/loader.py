"""Load bundled Zotero-like citation fixtures and the Part 3 full-text corpus."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from pyprojroot import here

from build_deep_research_agent.models import CitationRecord, CorpusPaper

FIXTURE_PATH = (
    here() / "build_deep_research_agent" / "fixtures" / "zotero_library.json"
)  # @spec PROMPT-FIX-001

CORPUS_DIR = (
    here() / "build_deep_research_agent" / "fixtures" / "corpus"
)  # @spec EMCP-DOC-001


@lru_cache(maxsize=1)
def load_citation_fixtures(path: Path | None = None) -> list[CitationRecord]:
    """Load citation records from the bundled JSON fixture.

    Parts 1–2 use these fixtures for in-context and memory exercises.

    :param path: Optional override path for tests.
    :returns: Parsed citation records.
    """
    # @spec PROMPT-FIX-003
    # @spec PROMPT-FIX-011
    # @spec PROMPT-FIX-020
    fixture_path = path or FIXTURE_PATH
    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    return [CitationRecord.model_validate(item) for item in raw]


@lru_cache(maxsize=1)
def load_corpus_papers(directory: Path | None = None) -> list[CorpusPaper]:
    """Load the bundled full-text corpus (arXiv + JOSS) with no network access.

    Each ``*.md`` file in the corpus directory is YAML-ish frontmatter
    (``---`` delimited) followed by the paper body. The frontmatter parser is
    hand-rolled (no pyyaml dependency).

    :param directory: Optional override directory for tests.
    :returns: Parsed corpus papers.
    """
    # @spec EMCP-DOC-004
    corpus_dir = directory or CORPUS_DIR
    papers: list[CorpusPaper] = []
    for path in sorted(corpus_dir.glob("*.md")):
        meta, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        if not body.strip():
            continue
        authors = [a.strip() for a in meta.get("authors", "").split(",") if a.strip()]
        year_raw = meta.get("year", "").strip()
        year = int(year_raw) if year_raw.isdigit() else None
        papers.append(
            CorpusPaper(
                title=meta.get("title", path.stem).strip().strip('"'),
                authors=authors,
                year=year,
                abstract=meta.get("abstract") or None,
                full_text=body.strip(),
                source=meta.get("source", "unknown").strip(),
                source_id=meta.get("source_id", "").strip().strip('"'),
                url=meta.get("url", "").strip().strip('"'),
                domain=meta.get("domain", "unknown").strip(),
            )
        )
    return papers


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split a ``---``-delimited frontmatter block from the body.

    :param text: Raw file text.
    :returns: Tuple of a metadata dict (key -> value string) and the body text.
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    body = parts[2].lstrip("\n")
    return meta, body
