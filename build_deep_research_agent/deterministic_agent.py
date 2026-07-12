"""Deterministic and AgentBot planning workflows on PocketFlow."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from llamabot import AgentBot
from llamabot.components.tools import tool
from pocketflow import Flow

from build_deep_research_agent.llm import get_completion_kwargs, get_large_model_name
from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.prompts import WORKFLOW_AGENTBOT_PROMPT
from build_deep_research_agent.workflows import (
    DeterministicResult,
    DeterministicWorkflow,
    WorkflowStepSnapshot,
)

PlanResearchFn = Callable[..., str]
SearchLiteratureFn = Callable[..., str]
SummarizeEvidenceFn = Callable[..., str]


@dataclass
class DeterministicWorkflowStore:
    """Mutable state shared across deterministic workflow tools."""

    query: str = ""
    search_terms: str | None = None
    evidence: list[CitationRecord] = field(default_factory=list)
    report: str | None = None
    steps: list[WorkflowStepSnapshot] = field(default_factory=list)


def make_agentbot_workflow_tools(
    store: DeterministicWorkflowStore,
    plan_research_fn: PlanResearchFn,
    search_literature_fn: SearchLiteratureFn,
    summarize_evidence_fn: SummarizeEvidenceFn,
    *,
    use_live_llm: bool = True,
) -> list[Any]:
    """Wrap exercise PocketFlow tool bodies as AgentBot tools (decide-loop routing).

    Default ``@tool`` loopback goes to the LLM :class:`~llamabot.components.pocketflow.DecideNode`.
    The system prompt in :func:`build_planning_agentbot` steers plan → search → summarize → respond.

    :param store: Mutable workflow state updated by each tool body.
    :param plan_research_fn: ``plan_research`` from ``exercises/part4.py``.
    :param search_literature_fn: ``search_literature`` from ``exercises/part4.py``.
    :param summarize_evidence_fn: ``summarize_evidence`` from ``exercises/part4.py``.
    :param use_live_llm: Passed through to plan/summarize tool bodies.
    :returns: Tool list for :class:`~llamabot.AgentBot`.
    """

    @tool
    def plan_research() -> str:
        """Derive search terms from the research question (plan state)."""
        return plan_research_fn(store, use_live_llm=use_live_llm)

    @tool
    def search_literature() -> str:
        """Retrieve citation evidence for the planned terms (search state)."""
        return search_literature_fn(store)

    @tool
    def summarize_evidence() -> str:
        """Write a markdown summary from retrieved evidence (summarize state)."""
        return summarize_evidence_fn(store, use_live_llm=use_live_llm)

    return [plan_research, search_literature, summarize_evidence]


def build_planning_agentbot(
    store: DeterministicWorkflowStore,
    plan_research_fn: PlanResearchFn,
    search_literature_fn: SearchLiteratureFn,
    summarize_evidence_fn: SummarizeEvidenceFn,
    *,
    use_live_llm: bool = True,
    max_iterations: int = 8,
    system_prompt: str = WORKFLOW_AGENTBOT_PROMPT,
) -> AgentBot:
    """Construct an AgentBot for the same pipeline with prompt-controlled routing.

    AgentBot wires ``decide → tool → decide → …`` automatically. The LLM decide node
    picks the next tool; :data:`~build_deep_research_agent.prompts.WORKFLOW_AGENTBOT_PROMPT`
    describes the intended plan → search → summarize → respond order.

    :param store: Mutable workflow state shared by tools.
    :param plan_research_fn: ``plan_research`` from ``exercises/part4.py``.
    :param search_literature_fn: ``search_literature`` from ``exercises/part4.py``.
    :param summarize_evidence_fn: ``summarize_evidence`` from ``exercises/part4.py``.
    :param use_live_llm: Passed through to plan/summarize tool bodies.
    :param max_iterations: Safety cap on decide/tool loops.
    :param system_prompt: Decide-node prompt steering tool order.
    :returns: Configured :class:`~llamabot.AgentBot` (display in marimo for Mermaid).
    """
    workflow_tools = make_agentbot_workflow_tools(
        store,
        plan_research_fn,
        search_literature_fn,
        summarize_evidence_fn,
        use_live_llm=use_live_llm,
    )
    return AgentBot(
        tools=workflow_tools,
        system_prompt=system_prompt,
        model_name=get_large_model_name(),
        max_iterations=max_iterations,
        **get_completion_kwargs(),
    )


@dataclass
class DeterministicFlowRun:
    """Result of :func:`run_deterministic_flow` plus PocketFlow runtime state."""

    result: DeterministicResult
    shared: dict[str, Any]


def reset_workflow_store(store: DeterministicWorkflowStore, query: str) -> None:
    """Clear per-run fields on a workflow store.

    :param store: Store to reset.
    :param query: Research question for this run.
    """
    store.query = query
    store.search_terms = None
    store.evidence = []
    store.report = None
    store.steps = []


def deterministic_result_from_store(
    store: DeterministicWorkflowStore,
) -> DeterministicResult:
    """Convert workflow store snapshots into a :class:`DeterministicResult`.

    :param store: Populated store after a flow run.
    :returns: Result compatible with Exercise 3 comparison helpers.
    """
    report = store.report or ""
    terms = store.search_terms or ""
    done_snapshot = DeterministicWorkflow.done_snapshot(terms, store.evidence, report)
    return DeterministicResult(
        query=store.query,
        steps=[*store.steps, done_snapshot],
        final_answer=report,
    )


def run_deterministic_flow(
    flow: Flow,
    store: DeterministicWorkflowStore,
    query: str,
) -> DeterministicFlowRun:
    """Run a linear PocketFlow graph and return structured workflow output.

    :param flow: Flow starting at ``plan_research`` with search/summarize wired.
    :param store: Shared store bound to the workflow tools.
    :param query: Research question.
    :returns: Completed result and PocketFlow ``shared`` state (for marimo traces).
    """
    reset_workflow_store(store, query)

    shared: dict[str, Any] = {
        "memory": [query],
        "globals_dict": {},
        "func_call": {},
        "workflow_store": store,
        "execution_history": [],
    }
    flow.run(shared)
    if store.report is None and shared.get("result") is not None:
        store.report = str(shared["result"])
    return DeterministicFlowRun(
        result=deterministic_result_from_store(store),
        shared=shared,
    )


def run_planning_agentbot(
    agent: AgentBot,
    store: DeterministicWorkflowStore,
    query: str,
) -> DeterministicResult:
    """Run a planning AgentBot and return structured workflow output.

    :param agent: AgentBot from :func:`build_planning_agentbot`.
    :param store: Shared store bound to the agent's tools.
    :param query: Research question.
    :returns: Completed workflow result (same shape as the linear flow).
    """
    reset_workflow_store(store, query)
    agent.shared["workflow_store"] = store
    final_response = agent(query)
    if store.report is None:
        store.report = str(final_response)
    return deterministic_result_from_store(store)
