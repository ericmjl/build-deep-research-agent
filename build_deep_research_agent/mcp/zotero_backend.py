"""Zotero search backend for the tutorial FastMCP server."""

# @spec TOOLS-TUT-010

from __future__ import annotations

import json
import os
import re
from typing import Literal

from build_deep_research_agent.fixtures.search import search_fixture_library
from build_deep_research_agent.models import CitationRecord

ZoteroSearchMode = Literal["zotero_web", "zotero_local", "fixtures"]


def _parse_year(date_value: str | None) -> int | None:
    """Extract a four-digit year from a Zotero date string.

    :param date_value: Raw date field from Zotero metadata.
    :returns: Parsed year or ``None``.
    """
    if not date_value:
        return None
    match = re.search(r"\d{4}", date_value)
    return int(match.group()) if match else None


def _format_creator(creator: dict[str, str]) -> str:
    """Format a Zotero creator dict as ``Last, First`` or institution name.

    :param creator: Creator object from Zotero item metadata.
    :returns: Display name for prompts and citations.
    """
    if creator.get("name"):
        return creator["name"]
    last = creator.get("lastName", "").strip()
    first = creator.get("firstName", "").strip()
    if last and first:
        return f"{last}, {first}"
    return last or first


def zotero_item_to_citation(item: dict) -> CitationRecord:
    """Convert a pyzotero item payload to :class:`CitationRecord`.

    :param item: Raw item dict from pyzotero.
    :returns: Normalized citation record.
    """
    data = item.get("data", item)
    creators = [_format_creator(c) for c in data.get("creators", []) if c]
    return CitationRecord(
        key=str(data.get("key") or "UNKNOWN"),
        title=str(data.get("title") or "Untitled"),
        creators=[c for c in creators if c],
        year=_parse_year(data.get("date")),
        abstract=data.get("abstractNote") or None,
        url=data.get("url") or None,
    )


def _search_with_pyzotero(query: str, limit: int) -> list[CitationRecord]:
    """Search a live Zotero library via pyzotero.

    :param query: Quick-search query string.
    :param limit: Maximum records to return.
    :returns: Matching citation records.
    :raises RuntimeError: If pyzotero is unavailable or credentials are invalid.
    """
    try:
        from pyzotero import zotero
    except ImportError as exc:
        raise RuntimeError(
            "pyzotero is required for live Zotero search. "
            "Install with `pixi add --pypi pyzotero` or use fixture fallback."
        ) from exc

    local_mode = os.getenv("ZOTERO_LOCAL", "").lower() in {"1", "true", "yes"}
    library_id = os.getenv("ZOTERO_LIBRARY_ID", "")
    library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.getenv("ZOTERO_API_KEY", "")

    if local_mode:
        # @spec TOOLS-TUT-012
        client = zotero.Zotero(
            library_id=library_id or "0",
            library_type=library_type,
            api_key=api_key or "",
            local=True,
        )
    else:
        if not library_id or not api_key:
            raise RuntimeError(
                "Set ZOTERO_LIBRARY_ID and ZOTERO_API_KEY for web API search, "
                "or ZOTERO_LOCAL=true for local Zotero."
            )
        client = zotero.Zotero(library_id, library_type, api_key)

    items = client.top(q=query, limit=limit)
    return [zotero_item_to_citation(item) for item in items]


def search_zotero_items(
    query: str, limit: int = 5
) -> tuple[list[CitationRecord], ZoteroSearchMode]:
    """Search Zotero when configured; otherwise use bundled fixtures.

    This is the cooking-show fallback: participants see a working MCP tool even
    before they finish installing upstream ``zotero-mcp``.

    :param query: Search terms.
    :param limit: Maximum records to return.
    :returns: Tuple of records and the backend mode used.
    """
    force_fixtures = os.getenv("TUTORIAL_ZOTERO_FORCE_FIXTURES", "").lower() in {
        "1",
        "true",
        "yes",
    }
    if force_fixtures:
        return search_fixture_library(query, limit=limit), "fixtures"

    has_web_creds = bool(os.getenv("ZOTERO_LIBRARY_ID") and os.getenv("ZOTERO_API_KEY"))
    has_local = os.getenv("ZOTERO_LOCAL", "").lower() in {"1", "true", "yes"}

    if has_web_creds or has_local:
        try:
            records = _search_with_pyzotero(query, limit=limit)
            mode: ZoteroSearchMode = "zotero_local" if has_local else "zotero_web"
            if records:
                return records, mode
        except Exception:
            pass

    # @spec TOOLS-TUT-011
    return search_fixture_library(query, limit=limit), "fixtures"


def records_to_search_json(
    records: list[CitationRecord], mode: ZoteroSearchMode
) -> str:
    """Serialize search results for MCP tool output.

    :param records: Citation records to return.
    :param mode: Backend mode used for the search.
    :returns: JSON string consumed by ``normalize_search_json``.
    """
    payload = {
        "mode": mode,
        "items": [record.model_dump() for record in records],
    }
    return json.dumps(payload, ensure_ascii=False)
