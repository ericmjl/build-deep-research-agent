"""Tests for the ZoteroDocstore wrapper and MCP search JSON builder."""

# @spec EMCP-DOC-001

from __future__ import annotations

import json

import pytest

from build_deep_research_agent.fixtures.loader import load_citation_fixtures
from build_deep_research_agent.mcp.docstore import (
    DocstoreStats,
    ZoteroDocstore,
    build_search_json,
    build_zotero_research_server,
    compose_document_text,
)
from build_deep_research_agent.models import CitationRecord


def _sample_records() -> list[CitationRecord]:
    """Return two citation records spanning Bayesian and variational topics."""
    return [
        CitationRecord(
            key="BAYES01",
            title="Bayesian Workflow for Applied Research",
            creators=["Gelman, Andrew"],
            year=2020,
            abstract="A practical workflow for building and validating Bayesian models.",
        ),
        CitationRecord(
            key="VARINF02",
            title="Variational Inference with Stochastic Gradients",
            creators=["Blei, David"],
            year=2017,
            abstract="Approximating posteriors with optimization instead of sampling.",
        ),
    ]


def test_compose_document_text_uses_abstract_when_available() -> None:
    """The stored text contains title, authors, and abstract."""
    # @spec EMCP-DOC-012
    text = compose_document_text(_sample_records()[0])
    assert "Bayesian Workflow" in text
    assert "Gelman, Andrew" in text
    assert "validating Bayesian models" in text


def test_compose_document_text_falls_back_to_title_without_abstract() -> None:
    """When abstract is missing, the body falls back to the title."""
    record = CitationRecord(key="X1", title="Title Only", creators=["A"])
    text = compose_document_text(record)
    assert text.count("Title Only") == 2  # header + body fallback


def test_ingest_accepts_custom_composer() -> None:
    """A participant-supplied composer drives the stored text and side-table key."""
    # Exercise 1: compose_doc_text + make_docstore wiring.
    record = CitationRecord(
        key="C1", title="Custom", creators=["Eve"], abstract="Body text."
    )

    def my_composer(rec: CitationRecord) -> str:
        """Participant-style composer keyed off the record key and abstract."""
        return f"CUSTOM::{rec.key}::{rec.abstract}"

    store = ZoteroDocstore()
    store._backend = None
    store.ingest([record], composer=my_composer)
    # the participant's text is the side-table key, and search projects it back
    hits = store.search("Body text.", limit=3)
    assert hits
    assert hits[0].key == "C1"
    assert hits[0].snippet.startswith("CUSTOM::C1::")


@pytest.fixture
def keyword_store() -> ZoteroDocstore:
    """A ZoteroDocstore forced into keyword fallback mode for deterministic tests."""
    store = ZoteroDocstore()
    store._backend = None  # force keyword fallback
    store.ingest(_sample_records())
    return store


def test_ingest_records_populates_side_table(keyword_store: ZoteroDocstore) -> None:
    """Ingest records citation metadata keyed by the stored document text."""
    # @spec EMCP-DOC-010
    # @spec EMCP-DOC-013
    assert keyword_store.stats.document_count == 2
    assert set(keyword_store.all_keys()) == {"BAYES01", "VARINF02"}


def test_search_returns_hits_with_snippet(keyword_store: ZoteroDocstore) -> None:
    """Keyword search returns structured hits including a snippet."""
    # @spec EMCP-DOC-040
    # @spec EMCP-DOC-042
    hits = keyword_store.search("Bayesian models", limit=5)
    assert hits
    assert all(h.snippet for h in hits)
    assert hits[0].key == "BAYES01"
    assert hits[0].title == "Bayesian Workflow for Applied Research"
    assert hits[0].year == 2020


def test_search_empty_query_returns_empty(keyword_store: ZoteroDocstore) -> None:
    """An empty query returns no hits rather than erroring."""
    # @spec EMCP-SRV-041
    assert keyword_store.search("", limit=5) == []
    assert keyword_store.search("   ", limit=5) == []


def test_search_limit_clamped_to_one(keyword_store: ZoteroDocstore) -> None:
    """A limit below 1 is clamped to 1."""
    # @spec EMCP-SRV-042
    hits = keyword_store.search("Bayesian", limit=0)
    assert len(hits) == 1


def test_search_respects_limit(keyword_store: ZoteroDocstore) -> None:
    """At most ``limit`` hits are returned."""
    # @spec EMCP-DOC-043
    hits = keyword_store.search("inference models", limit=1)
    assert len(hits) == 1


def test_get_metadata_round_trip(keyword_store: ZoteroDocstore) -> None:
    """get_metadata resolves a key back to its citation record."""
    record = keyword_store.get_metadata("VARINF02")
    assert record is not None
    assert record.title == "Variational Inference with Stochastic Gradients"
    assert keyword_store.get_metadata("NOPE") is None


def test_stats_reports_backend_and_count(keyword_store: ZoteroDocstore) -> None:
    """stats exposes table name, document count, model, and backend."""
    # @spec EMCP-DOC-050
    stats = keyword_store.stats
    assert isinstance(stats, DocstoreStats)
    assert stats.document_count == 2
    assert stats.backend == "keyword"
    assert stats.embedding_model


def test_build_search_json_structure(keyword_store: ZoteroDocstore) -> None:
    """The MCP JSON output carries mode, items, and docstore_stats."""
    # @spec EMCP-SRV-013
    hits = keyword_store.search("Bayesian", limit=2)
    raw = build_search_json(hits, mode="fixtures", stats=keyword_store.stats)
    payload = json.loads(raw)
    assert payload["mode"] == "fixtures"
    assert payload["items"]
    item = payload["items"][0]
    for field in ("key", "title", "creators", "year", "abstract", "url", "snippet"):
        assert field in item  # @spec EMCP-SRV-014
    assert "docstore_stats" in payload


def test_search_empty_store_returns_empty() -> None:
    """Searching a store with no ingested papers returns no hits."""
    # @spec EMCP-DOC-061
    store = ZoteroDocstore()
    store._backend = None
    assert store.search("anything", limit=5) == []


def test_build_search_json_empty_message() -> None:
    """An empty result includes a descriptive message field."""
    # @spec EMCP-DOC-061
    store = ZoteroDocstore()
    store._backend = None  # empty store, keyword backend
    raw = build_search_json([], mode="fixtures", stats=store.stats)
    payload = json.loads(raw)
    assert payload["items"] == []
    assert "message" in payload
    assert "empty" in payload["message"].lower()


def test_semantic_backend_initializes_with_fixtures(tmp_path) -> None:
    """The LanceDB backend ingests and semantically retrieves fixture papers.

    Skipped when the embedding model cannot initialize (offline CI).
    """
    store = ZoteroDocstore(storage_path=tmp_path / "lancedb")
    if store._backend is None:  # model unavailable in this environment
        pytest.skip("LanceDB backend unavailable (embedding model not downloadable)")
    store.ingest(load_citation_fixtures())
    assert store.backend_name == "lancedb"
    hits = store.search("Bayesian", limit=3)
    assert hits
    assert any("Bayesian" in h.title for h in hits)


def test_build_zotero_research_server_tool_and_resource() -> None:
    """The reference server exposes a working search tool and metadata resource."""
    # @spec EMCP-SRV-001
    # @spec EMCP-SRV-010
    import asyncio

    async def _check() -> None:
        """Assert the reference server's tool, payload, and resource contracts."""
        mcp = build_zotero_research_server()
        assert mcp.name == "zotero-research"

        tools = await mcp.list_tools()
        assert "zotero_search_items" in [t.name for t in tools]

        result = await mcp.call_tool(
            "zotero_search_items", {"query": "Bayesian", "limit": 3}
        )
        payload = json.loads(result.content[0].text)
        # @spec EMCP-SRV-013
        assert payload["mode"] == "fixtures"
        assert payload["items"]
        assert payload["docstore_stats"]["document_count"] >= 1

        templates = await mcp.list_resource_templates()
        assert any("metadata/{key}" in str(t.uri_template) for t in templates)

        key = payload["items"][0]["key"]
        res = await mcp.read_resource(f"zotero://metadata/{key}")
        meta = json.loads(res.contents[0].content)  # @spec EMCP-SRV-021
        assert meta["found"] is True
        assert meta["key"] == key

    asyncio.run(_check())
