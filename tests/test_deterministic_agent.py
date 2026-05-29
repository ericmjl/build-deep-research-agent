"""Tests for linear deterministic PocketFlow wiring."""

from unittest.mock import patch

from llamabot.components.tools import tool
from pocketflow import Flow

from build_deep_research_agent.deterministic_agent import (
    DeterministicWorkflowStore,
    build_planning_agentbot,
    deterministic_result_from_store,
    make_agentbot_workflow_tools,
    run_deterministic_flow,
)
from build_deep_research_agent.exercises.solutions import part4 as solutions_part4
from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.workflows import WorkflowStepSnapshot


def _linear_tools(store: DeterministicWorkflowStore) -> list:
    """Wire @tool nodes the way the notebook does for Exercise 1a."""

    @tool(loopback_name="search_literature")
    def plan_research() -> str:
        """Mirror notebook plan @tool for offline linear flow tests."""
        return solutions_part4.plan_research(store, use_live_llm=False)

    @tool(loopback_name="summarize_evidence")
    def search_literature() -> str:
        """Mirror notebook search @tool for offline linear flow tests."""
        return solutions_part4.search_literature(store)

    @tool(loopback_name=None)
    def summarize_evidence() -> str:
        """Mirror notebook summarize @tool for offline linear flow tests."""
        return solutions_part4.summarize_evidence(store, use_live_llm=False)

    return [plan_research, search_literature, summarize_evidence]


def _linear_flow(store: DeterministicWorkflowStore) -> Flow:
    """Wire plan → search → summarize the way the notebook does."""
    plan_tool, search_tool, summarize_tool = _linear_tools(store)
    plan_tool - "search_literature" >> search_tool
    search_tool - "summarize_evidence" >> summarize_tool
    return Flow(start=plan_tool)


def test_deterministic_linear_flow_completes_offline() -> None:
    """Linear PocketFlow graph visits plan, search, summarize, and done."""
    store = DeterministicWorkflowStore()
    flow = _linear_flow(store)
    flow_run = run_deterministic_flow(flow, store, "Bayesian workflow")
    result = flow_run.result

    assert [step.state for step in result.steps] == [
        "plan",
        "search",
        "summarize",
        "done",
    ]
    assert result.final_answer


def test_linear_tool_loopback_names_match_notebook_wiring() -> None:
    """Notebook @tool wiring points at the next step; summarize is terminal."""
    store = DeterministicWorkflowStore()
    plan_tool, search_tool, summarize_tool = _linear_tools(store)
    assert plan_tool.loopback_name == "search_literature"
    assert search_tool.loopback_name == "summarize_evidence"
    assert summarize_tool.loopback_name is None


def test_agentbot_workflow_tools_loop_back_to_decide() -> None:
    """AgentBot tools use default decide loopback for LLM routing."""
    store = DeterministicWorkflowStore()
    plan_tool, search_tool, summarize_tool = make_agentbot_workflow_tools(
        store,
        solutions_part4.plan_research,
        solutions_part4.search_literature,
        solutions_part4.summarize_evidence,
        use_live_llm=False,
    )
    assert plan_tool.loopback_name == "decide"
    assert search_tool.loopback_name == "decide"
    assert summarize_tool.loopback_name == "decide"


def test_deterministic_result_from_store_adds_done_snapshot() -> None:
    """Store conversion appends the terminal done snapshot."""
    store = DeterministicWorkflowStore(
        query="Bayesian workflow",
        search_terms="Bayesian workflow",
        evidence=[CitationRecord(key="K1", title="Paper", creators=[], year=2024)],
        report="Final report",
        steps=[
            WorkflowStepSnapshot(state="plan", search_terms="Bayesian workflow"),
        ],
    )
    result = deterministic_result_from_store(store)
    assert result.steps[-1].state == "done"
    assert result.final_answer == "Final report"


@patch("build_deep_research_agent.deterministic_agent.AgentBot")
def test_build_planning_agentbot_uses_workflow_prompt(mock_agentbot) -> None:
    """Planning AgentBot is constructed with workflow tools and prompt."""
    store = DeterministicWorkflowStore()

    def _plan_research(
        _store: DeterministicWorkflowStore, *, use_live_llm: bool = True
    ) -> str:
        """Stub plan tool for AgentBot construction test."""
        return "term"

    def _search_literature(_store: DeterministicWorkflowStore) -> str:
        """Stub search tool for AgentBot construction test."""
        return "found"

    def _summarize_evidence(
        _store: DeterministicWorkflowStore, *, use_live_llm: bool = True
    ) -> str:
        """Stub summarize tool for AgentBot construction test."""
        return "report"

    build_planning_agentbot(
        store,
        _plan_research,
        _search_literature,
        _summarize_evidence,
        use_live_llm=False,
    )
    mock_agentbot.assert_called_once()
    kwargs = mock_agentbot.call_args.kwargs
    assert "plan_research" in kwargs["system_prompt"]
    assert len(kwargs["tools"]) == 3
