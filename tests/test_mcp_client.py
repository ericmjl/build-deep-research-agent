"""Tests for Zotero backend and MCP normalization."""

# @spec TOOLS-MCP-030

from __future__ import annotations

import json

import pytest

from build_deep_research_agent.mcp.client import (
    normalize_search_json,
    normalize_search_markdown,
    resolve_zotero_mcp_server_config,
    tutorial_zotero_mcp_server_config,
    zotero_mcp_server_config,
)
from build_deep_research_agent.mcp.zotero_backend import (
    records_to_search_json,
    search_zotero_items,
    zotero_item_to_citation,
)


def test_zotero_item_to_citation_parses_creators_and_year() -> None:
    """pyzotero item payloads map to CitationRecord with creators and year."""
    record = zotero_item_to_citation(
        {
            "data": {
                "key": "ABC12345",
                "title": "Bayesian Workflow",
                "creators": [
                    {"creatorType": "author", "lastName": "Ma", "firstName": "Eric"}
                ],
                "date": "2020-05-01",
                "abstractNote": "A practical workflow.",
                "url": "https://example.com/paper",
            }
        }
    )
    assert record.key == "ABC12345"
    assert record.title == "Bayesian Workflow"
    assert record.creators == ["Ma, Eric"]
    assert record.year == 2020
    assert record.abstract == "A practical workflow."


def test_search_zotero_items_fixture_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Search falls back to bundled fixtures when Zotero credentials are absent."""
    # @spec TOOLS-TUT-011
    # @spec TOOLS-TUT-040
    monkeypatch.delenv("ZOTERO_API_KEY", raising=False)
    monkeypatch.delenv("ZOTERO_LIBRARY_ID", raising=False)
    monkeypatch.delenv("ZOTERO_LOCAL", raising=False)
    records, mode = search_zotero_items("Bayesian", limit=3)
    assert mode == "fixtures"
    assert records
    assert any("Bayesian" in record.title for record in records)


def test_records_to_search_json_round_trip() -> None:
    """MCP JSON search output normalizes back to citation records."""
    # @spec TOOLS-SEARCH-030
    records, mode = search_zotero_items("Bayesian", limit=1)
    raw = records_to_search_json(records, mode=mode)
    parsed = normalize_search_json(raw, fallback_query="Bayesian")
    assert parsed
    assert parsed[0].title == records[0].title


def test_normalize_search_json_empty_items() -> None:
    """Empty items array in JSON payload returns an empty record list."""
    # @spec TOOLS-SEARCH-031
    assert normalize_search_json(json.dumps({"items": []}), fallback_query="x") == []


def test_normalize_search_markdown_empty() -> None:
    """Empty markdown search output returns an empty record list."""
    assert normalize_search_markdown("", fallback_query="x") == []


def test_tutorial_server_config_uses_current_python() -> None:
    """Tutorial MCP config launches the in-repo FastMCP server module."""
    # @spec TOOLS-MCP-002
    config = tutorial_zotero_mcp_server_config()
    assert config.command
    assert config.args == ["-m", "build_deep_research_agent.mcp.server"]


def test_resolve_zotero_mcp_server_config_defaults_to_tutorial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default MCP source selects the tutorial FastMCP server."""
    # @spec TOOLS-MCP-004
    # @spec TOOLS-TUT-020
    monkeypatch.delenv("ZOTERO_MCP_SOURCE", raising=False)
    config = resolve_zotero_mcp_server_config()
    assert config.args == ["-m", "build_deep_research_agent.mcp.server"]


def test_resolve_zotero_mcp_server_config_upstream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Upstream MCP source spawns the external zotero-mcp command."""
    # @spec TOOLS-TUT-021
    monkeypatch.setenv("ZOTERO_MCP_SOURCE", "upstream")
    config = resolve_zotero_mcp_server_config()
    assert config.command == zotero_mcp_server_config().command
