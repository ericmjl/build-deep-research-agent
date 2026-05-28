"""Tests for prompt helpers."""

from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.prompts import (
    build_messages,
    format_citations_for_context,
)


def test_format_citations_for_context() -> None:
    """Formatted context includes title and creators from sample records."""
    # @spec PROMPT-SUM-040
    records = [
        CitationRecord(
            key="ABC12345",
            title="Test Paper",
            creators=["Author, A."],
            year=2024,
            abstract="An abstract.",
        )
    ]
    text = format_citations_for_context(records)
    assert "Test Paper" in text
    assert "Author, A." in text


def test_build_messages_orders_roles() -> None:
    """build_messages returns system first and user last."""
    # @spec PROMPT-SYS-030
    messages = build_messages("system text", "user text")
    assert messages[0].role == "system"
    assert messages[-1].role == "user"
