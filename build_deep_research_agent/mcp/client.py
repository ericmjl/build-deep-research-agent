"""MCP client helpers for Zotero integration."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Literal

from llamabot.mcp.manager import MCPClientManager
from llamabot.mcp.specs import MCPIntegrationOptions, MCPServerConfig

from build_deep_research_agent.models import CitationRecord

# @spec TOOLS-MCP-001
ZOTERO_MCP_TOOL_NAME = "zotero__zotero_search_items"  # @spec TOOLS-SEARCH-003
ZoteroMCPSource = Literal["tutorial", "upstream"]


def zotero_mcp_server_config(
    command: str | None = None,
    args: list[str] | None = None,
) -> MCPServerConfig:
    """Build stdio MCP config for the upstream zotero-mcp server.

    :param command: Executable name or path (defaults to ``ZOTERO_MCP_COMMAND``).
    :param args: Optional command arguments.
    :returns: llamabot MCP server configuration.
    """
    # @spec TOOLS-MCP-003
    # @spec TUT-INFRA-020
    return MCPServerConfig(
        name="zotero",
        transport="stdio",
        command=command or os.getenv("ZOTERO_MCP_COMMAND", "zotero-mcp"),
        args=args or [],
    )


def tutorial_zotero_mcp_server_config() -> MCPServerConfig:
    """Build stdio MCP config for the in-repo tutorial FastMCP server.

    :returns: llamabot MCP server configuration for ``build_deep_research_agent.mcp.server``.
    """
    # @spec TOOLS-MCP-002
    # @spec TOOLS-TUT-002
    return MCPServerConfig(
        name="zotero",
        transport="stdio",
        command=sys.executable,
        args=["-m", "build_deep_research_agent.mcp.server"],
    )


def resolve_zotero_mcp_server_config() -> MCPServerConfig:
    """Pick upstream or tutorial Zotero MCP server from environment.

    ``ZOTERO_MCP_SOURCE`` defaults to ``tutorial`` so classroom demos work
    without installing upstream ``zotero-mcp``. Set to ``upstream`` for the
    hand-built server path taught in Part 3.

    :returns: MCP server configuration for the selected source.
    """
    source = os.getenv("ZOTERO_MCP_SOURCE", "tutorial").lower()
    if source == "upstream":
        # @spec TOOLS-TUT-021
        return zotero_mcp_server_config()
    # @spec TOOLS-MCP-004
    # @spec TOOLS-TUT-020
    return tutorial_zotero_mcp_server_config()


class ZoteroMCPClient:
    """Thin wrapper around llamabot's MCP client manager for zotero-mcp."""

    # @spec TOOLS-MCP-005

    def __init__(
        self,
        server_config: MCPServerConfig | None = None,
        options: MCPIntegrationOptions | None = None,
    ) -> None:
        self._config = server_config or resolve_zotero_mcp_server_config()
        self._options = options or MCPIntegrationOptions()
        self._manager = MCPClientManager([self._config], self._options)
        self._manager.start()
        self._tools = {tool.__name__: tool for tool in self._manager.llamabot_tools()}

    @property
    def failures(self) -> list[tuple[str, BaseException]]:
        """Return MCP startup failures under best-effort mode."""
        return self._manager.failures

    @property
    def tool_names(self) -> list[str]:
        """Return discovered MCP tool function names."""
        # @spec TOOLS-MCP-005
        return sorted(self._tools)

    def close(self) -> None:
        """Close MCP sessions."""
        self._manager.close()

    def search_items(self, query: str, limit: int = 5) -> str:
        """Call zotero-mcp search and return raw tool output.

        :param query: Search query string.
        :param limit: Maximum number of results.
        :returns: Raw markdown/text from zotero-mcp.
        :raises RuntimeError: If the search tool is unavailable.
        """
        # @spec TOOLS-SEARCH-001
        tool = self._pick_search_tool()
        if tool is None:
            available = ", ".join(self.tool_names) or "(none)"
            raise RuntimeError(
                f"zotero search tool not found. Available MCP tools: {available}"
            )
        return str(tool(query=query, limit=limit))

    def _pick_search_tool(self) -> Any | None:
        """Return the zotero search tool callable, if discovered."""
        if ZOTERO_MCP_TOOL_NAME in self._tools:
            return self._tools[ZOTERO_MCP_TOOL_NAME]
        for name, tool in self._tools.items():
            if "search_items" in name:
                return tool
        return None


def normalize_search_markdown(raw: str, fallback_query: str) -> list[CitationRecord]:
    """Best-effort parse of zotero-mcp markdown search output.

    :param raw: Raw markdown returned by ``zotero_search_items``.
    :param fallback_query: Query string used when title extraction fails.
    :returns: Parsed citation records (may be a single aggregate record).
    """
    # @spec TOOLS-SEARCH-002
    if not raw.strip():
        return []  # @spec TOOLS-SEARCH-020

    records: list[CitationRecord] = []
    chunks = re.split(r"\n(?=#+\s|\[\d+\]|\*\*Title:\*\*)", raw)
    for index, chunk in enumerate(chunks, start=1):
        chunk = chunk.strip()
        if not chunk:
            continue
        title_match = re.search(
            r"(?:\*\*Title:\*\*|^#\s+)(.+)$", chunk, flags=re.MULTILINE
        )
        title = title_match.group(1).strip() if title_match else fallback_query
        year_match = re.search(r"(?:\*\*Year:\*\*|Year:)\s*(\d{4})", chunk)
        year = int(year_match.group(1)) if year_match else None
        creators_match = re.search(
            r"(?:\*\*Authors?:\*\*|Authors?:)\s*(.+)$", chunk, flags=re.MULTILINE
        )
        creators = (
            [
                part.strip()
                for part in creators_match.group(1).split(",")
                if part.strip()
            ]
            if creators_match
            else []
        )
        key_match = re.search(r"(?:key=|Item Key:)\s*([A-Z0-9]{8})", chunk)
        records.append(
            CitationRecord(
                key=key_match.group(1) if key_match else f"MCP{index:04d}",
                title=title,
                creators=creators,
                year=year,
                abstract=chunk,
            )
        )

    if records:
        return records

    return [
        CitationRecord(
            key="MCP0000",
            title=fallback_query,
            creators=[],
            year=None,
            abstract=raw,
        )
    ]


def normalize_search_json(raw: str, fallback_query: str) -> list[CitationRecord]:
    """Parse JSON-shaped tool output if zotero-mcp returns structured data.

    :param raw: Tool output string.
    :param fallback_query: Query used for fallback title.
    :returns: Parsed citation records.
    """
    # @spec TOOLS-SEARCH-002
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return normalize_search_markdown(raw, fallback_query=fallback_query)

    items = payload if isinstance(payload, list) else payload.get("items", [])
    if isinstance(items, list) and not items:
        return []  # @spec TOOLS-SEARCH-020
    records: list[CitationRecord] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        creators = item.get("creators") or item.get("authors") or []
        if isinstance(creators, str):
            creators = [creators]
        records.append(
            CitationRecord(
                key=str(item.get("key") or item.get("itemKey") or f"MCP{index:04d}"),
                title=str(item.get("title") or fallback_query),
                creators=[str(c) for c in creators],
                year=item.get("year"),
                abstract=item.get("abstract"),
            )
        )
    return records or normalize_search_markdown(raw, fallback_query=fallback_query)
