"""Tests for Part 2 tutorial exercise modules."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from build_deep_research_agent.exercises import part2 as learner_part2
from build_deep_research_agent.exercises.solutions import part2 as solutions_part2
from build_deep_research_agent.models import CitationRecord, Message


def _sample_citation() -> CitationRecord:
    """Return a representative CitationRecord for exercising memory helpers."""
    return CitationRecord(
        key="ABC12345",
        title="Bayesian Workflow for Applied Research",
        creators=["Gelman, Andrew"],
        year=2020,
    )


def test_learner_append_raises_not_implemented() -> None:
    """Learner AppendOnlyMemory.append is a stub until the participant implements it."""
    # @spec MEM-EX-030
    memory = learner_part2.AppendOnlyMemory()
    with pytest.raises(NotImplementedError):
        memory.append(Message(role="user", content="hello"))


def test_learner_retrieve_raises_not_implemented() -> None:
    """Learner AppendOnlyMemory.retrieve is a stub until the participant implements it."""
    # @spec MEM-EX-030
    memory = learner_part2.AppendOnlyMemory()
    with pytest.raises(NotImplementedError):
        memory.retrieve(n_results=1)


def test_learner_add_raises_not_implemented() -> None:
    """Learner CitationMemory.add is a stub until the participant implements it."""
    # @spec MEM-EX-030
    memory = learner_part2.CitationMemory()
    with pytest.raises(NotImplementedError):
        memory.add(_sample_citation(), "summary")


def test_learner_summarize_paper_raises_not_implemented() -> None:
    """Learner summarize_paper is a stub until the participant implements it."""
    # @spec MEM-CITE-032
    # @spec MEM-EX-030
    with pytest.raises(NotImplementedError):
        learner_part2.summarize_paper(MagicMock(), "text")


def test_solutions_append_preserves_order() -> None:
    """Instructor AppendOnlyMemory preserves append order."""
    # @spec MEM-CHAT-030
    memory = solutions_part2.AppendOnlyMemory()
    updated = memory.append(Message(role="user", content="first")).append(
        Message(role="assistant", content="second")
    )
    assert [m.content for m in updated.messages()] == ["first", "second"]


def test_solutions_append_does_not_mutate_original() -> None:
    """append returns a new instance without mutating the original."""
    # @spec MEM-CHAT-031
    original = solutions_part2.AppendOnlyMemory()
    updated = original.append(Message(role="user", content="hello"))
    assert original.messages() == []
    assert [m.content for m in updated.messages()] == ["hello"]


def test_solutions_retrieve_returns_recent() -> None:
    """retrieve(n_results) returns the most recent N messages."""
    # @spec MEM-CHAT-032
    memory = (
        solutions_part2.AppendOnlyMemory()
        .append(Message(role="user", content="one"))
        .append(Message(role="assistant", content="two"))
        .append(Message(role="user", content="three"))
    )
    recent = memory.retrieve(n_results=2)
    assert [m.content for m in recent] == ["two", "three"]
    assert memory.retrieve(n_results=0) == []


def test_solutions_add_same_key_replaces_existing() -> None:
    """Adding a citation with an existing key replaces the prior entry in context."""
    # @spec MEM-CITE-004
    # @spec MEM-CITE-031
    citation = _sample_citation()
    memory = (
        solutions_part2.CitationMemory()
        .add(citation, "original summary")
        .add(citation, "updated summary")
    )
    context = memory.as_context()
    assert "updated summary" in context
    assert "original summary" not in context


def test_solutions_as_context_includes_title_and_summary() -> None:
    """as_context includes citation title and summary text."""
    # @spec MEM-CITE-030
    # @spec MEM-COMP-030
    citation = _sample_citation()
    empty = solutions_part2.CitationMemory().as_context()
    populated = solutions_part2.CitationMemory().add(
        citation, "A short summary of the paper."
    )
    context = populated.as_context()
    assert empty != context
    assert "Bayesian Workflow" in context
    assert "A short summary of the paper." in context
    assert "Summary:" in context


def test_solutions_summarize_paper_calls_bot() -> None:
    """summarize_paper returns the bot response content."""
    # @spec MEM-CITE-005
    # @spec MEM-CITE-032
    bot = MagicMock()
    bot.return_value = MagicMock(content="Two-sentence summary.")
    result = solutions_part2.summarize_paper(bot, "Long abstract text")
    assert result == "Two-sentence summary."
    bot.assert_called_once()
