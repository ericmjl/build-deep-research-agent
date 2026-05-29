"""Tests for deterministic and ReAct planning workflows."""

from __future__ import annotations

from typing import Any

import pytest

from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.workflows import (
    DeterministicWorkflow,
    InvalidStateTransitionError,
    ReActDecision,
    ReActResult,
    ReActRunner,
    ReActStep,
    compare_workflow_results,
    validate_deterministic_transition,
)


@pytest.fixture
def sample_query() -> str:
    """Return a fixture search query used across workflow tests."""
    return "Bayesian workflow"


@pytest.fixture
def sample_citation() -> CitationRecord:
    """Return a minimal citation record for mocked search."""
    return CitationRecord(
        key="TEST0001",
        title="Bayesian workflow applied research",
        creators=["Ma, Eric"],
        year=2024,
        abstract="Tutorial fixture record.",
    )


def test_valid_deterministic_transitions_complete_in_order(sample_query: str) -> None:
    """Deterministic workflow visits plan, search, summarize, and done."""
    # @spec PLAN-DET-030
    states_seen: list[str] = []

    def search_fn(query: str, search_terms: str) -> list[CitationRecord]:
        """Return a single fixture citation for the search step."""
        _ = query
        return [
            CitationRecord(
                key="FIX001",
                title=search_terms,
                creators=["Demo"],
                year=2024,
            )
        ]

    def summarize_fn(query: str, evidence: list[CitationRecord]) -> str:
        """Return a deterministic summary string for tests."""
        return f"Summary for {query} with {len(evidence)} item(s)."

    workflow = DeterministicWorkflow(search_fn=search_fn, summarize_fn=summarize_fn)
    result = workflow.run(sample_query)

    for step in result.steps:
        states_seen.append(step.state)

    assert states_seen == ["plan", "search", "summarize", "done"]
    assert result.final_answer.startswith("Summary for")


def test_deterministic_step_methods_match_run(sample_query: str) -> None:
    """Explicit plan/search/summarize steps produce the same result as run()."""
    workflow = DeterministicWorkflow(
        search_fn=lambda q, terms: [
            CitationRecord(key="K1", title=terms, creators=[], year=2024)
        ],
        summarize_fn=lambda q, ev: f"answer: {q}",
    )
    stepped_terms, _ = workflow.plan(sample_query)
    stepped_evidence, _ = workflow.search(sample_query, stepped_terms)
    stepped_report, _ = workflow.summarize(
        sample_query, stepped_terms, stepped_evidence
    )
    bundled = workflow.run(sample_query)
    assert stepped_report == bundled.final_answer
    assert stepped_terms == bundled.steps[0].search_terms


def test_invalid_transition_raises(sample_query: str) -> None:
    """Invalid FSM transitions raise InvalidStateTransitionError."""
    # @spec PLAN-DET-031
    with pytest.raises(InvalidStateTransitionError) as exc_info:
        validate_deterministic_transition("plan", "done")

    assert exc_info.value.from_state == "plan"
    assert exc_info.value.to_state == "done"


def test_empty_search_still_summarizes(sample_query: str) -> None:
    """Empty search evidence still reaches summarize and done."""

    # @spec PLAN-DET-021
    def empty_search(query: str, search_terms: str) -> list[CitationRecord]:
        """Return no evidence to exercise the empty-search path."""
        _ = (query, search_terms)
        return []

    def summarize_fn(query: str, evidence: list[CitationRecord]) -> str:
        """Summarize even when evidence is empty."""
        assert evidence == []
        return f"No evidence for {query}."

    workflow = DeterministicWorkflow(
        search_fn=empty_search,
        summarize_fn=summarize_fn,
    )
    result = workflow.run(sample_query)

    assert result.steps[1].state == "search"
    assert result.steps[1].evidence == []
    assert result.final_answer == f"No evidence for {sample_query}."


def _scripted_react_steps(
    decisions: list[ReActDecision],
) -> Any:
    """Return a step_fn that pops scripted decisions in order."""

    def step_fn(
        query: str,
        trace: list[ReActStep],
        tools: dict[str, Any],
    ) -> ReActDecision:
        """Pop the next scripted decision for ReAct runner tests."""
        _ = (query, trace, tools)
        if not decisions:
            return ReActDecision(thought="fallback", final_answer="done")
        return decisions.pop(0)

    return step_fn


def test_react_stops_at_max_steps() -> None:
    """ReAct runner returns partial trace when max_steps is reached."""
    # @spec PLAN-REACT-030
    decisions = [
        ReActDecision(
            thought="search first",
            action="search_library",
            action_input={"query": "Bayesian"},
        )
    ] * 3

    runner = ReActRunner(
        tools={"search_library": lambda query, limit=5: f"found {query}"},
        step_fn=_scripted_react_steps(decisions),
        max_steps=2,
    )
    result = runner.run("Bayesian workflow")

    assert isinstance(result, ReActResult)
    assert len(result.trace) == 2
    assert result.stopped_reason == "max_steps"


def test_react_returns_complete_trace_on_final_answer() -> None:
    """ReAct runner stops when the model answers without another tool call."""
    # @spec PLAN-REACT-031
    decisions = [
        ReActDecision(
            thought="need evidence",
            action="search_library",
            action_input={"query": "Bayesian"},
        ),
        ReActDecision(
            thought="enough evidence",
            final_answer="Final markdown answer.",
        ),
    ]

    runner = ReActRunner(
        tools={"search_library": lambda query, limit=5: f"found {query}"},
        step_fn=_scripted_react_steps(decisions),
        max_steps=8,
    )
    result = runner.run("Bayesian workflow")

    assert len(result.trace) == 2
    assert result.trace[0].observation == "found Bayesian"
    assert result.final_answer == "Final markdown answer."
    assert result.stopped_reason == "answer"


def test_react_records_tool_errors_in_observation() -> None:
    """Tool failures become observations so the loop can continue."""
    # @spec PLAN-REACT-012
    decisions = [
        ReActDecision(
            thought="call missing tool",
            action="missing_tool",
            action_input={},
        ),
        ReActDecision(thought="recover", final_answer="Recovered."),
    ]

    runner = ReActRunner(
        tools={},
        step_fn=_scripted_react_steps(decisions),
        max_steps=4,
    )
    result = runner.run("test")

    assert "Tool error" in (result.trace[0].observation or "")
    assert result.final_answer == "Recovered."


def test_compare_workflows_returns_non_empty_answers(sample_query: str) -> None:
    """Both workflow types yield answers for the same query under mocks."""
    # @spec PLAN-COMP-030
    det = DeterministicWorkflow(
        search_fn=lambda q, terms: [
            CitationRecord(key="K1", title=terms, creators=[], year=2024)
        ],
        summarize_fn=lambda q, ev: f"det answer: {q}",
    ).run(sample_query)

    react = ReActRunner(
        tools={"search_library": lambda query, limit=5: "evidence"},
        step_fn=_scripted_react_steps(
            [
                ReActDecision(
                    thought="done", final_answer=f"react answer: {sample_query}"
                )
            ]
        ),
    ).run(sample_query)

    comparison = compare_workflow_results(sample_query, det, react)

    assert comparison.deterministic_answer
    assert comparison.react_answer
    assert comparison.deterministic_step_count == 4
    assert comparison.react_trace_length == 1
