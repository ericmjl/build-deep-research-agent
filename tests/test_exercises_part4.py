"""Tests for Part 4 tutorial exercise modules."""

from __future__ import annotations

import pytest

from build_deep_research_agent.deterministic_agent import DeterministicWorkflowStore
from build_deep_research_agent.exercises import part4 as learner_part4
from build_deep_research_agent.exercises.solutions import part4 as solutions_part4


def test_learner_plan_research_raises_not_implemented() -> None:
    """Learner plan_research is a stub until the participant implements it."""
    store = DeterministicWorkflowStore(query="Bayesian workflow")
    with pytest.raises(NotImplementedError):
        learner_part4.plan_research(store, use_live_llm=False)


def test_solutions_plan_research_runs_offline() -> None:
    """Instructor plan_research works without LLM when use_live_llm is false."""
    store = DeterministicWorkflowStore(query="Bayesian workflow")
    message = solutions_part4.plan_research(store, use_live_llm=False)
    assert store.search_terms == "Bayesian workflow"
    assert "Bayesian workflow" in message
