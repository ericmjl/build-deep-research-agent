"""Tests for Part 2 tutorial exercise modules."""

from __future__ import annotations

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


def test_learner_add_raises_not_implemented() -> None:
    """Learner CitationMemory.add is a stub until the participant implements it."""
    # @spec MEM-EX-030
    memory = learner_part2.CitationMemory()
    with pytest.raises(NotImplementedError):
        memory.add(_sample_citation(), "snippet")


def test_solutions_append_preserves_order() -> None:
    """Instructor AppendOnlyMemory preserves append order."""
    memory = solutions_part2.AppendOnlyMemory()
    updated = memory.append(Message(role="user", content="first")).append(
        Message(role="assistant", content="second")
    )
    assert [m.content for m in updated.messages()] == ["first", "second"]


def test_solutions_add_same_key_replaces_existing() -> None:
    """Adding a citation with an existing key replaces the prior entry in context."""
    # @spec MEM-CITE-004
    citation = _sample_citation()
    memory = (
        solutions_part2.CitationMemory()
        .add(citation, "original snippet")
        .add(citation, "updated snippet")
    )
    context = memory.as_context()
    assert "updated snippet" in context
    assert "original snippet" not in context
