"""Part 4 planning exercises — instructor reference solutions."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from pydantic import BaseModel, Field

from build_deep_research_agent.deterministic_agent import DeterministicWorkflowStore
from build_deep_research_agent.fixtures.search import search_fixture_library
from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.prompts import format_citations_for_context
from build_deep_research_agent.workflows import (
    ReActDecision,
    ReActStep,
    WorkflowStepSnapshot,
    default_summarize_fn,
    validate_deterministic_transition,
)


class SearchPlan(BaseModel):
    """Structured output for the plan step."""

    search_terms: list[str] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Five distinct literature search queries",
    )


def _derive_search_terms(query: str, *, use_live_llm: bool) -> str:
    """Return comma-separated search terms for a research question.

    :param query: Research question.
    :param use_live_llm: When ``False``, return a simple offline fallback.
    :returns: Comma-separated search terms.
    """
    if not use_live_llm:
        return query.strip()

    from llamabot import StructuredBot

    from build_deep_research_agent.llm import (
        get_completion_kwargs,
        get_large_model_name,
    )

    planner = StructuredBot(
        system_prompt=(
            "You help scientists search literature. "
            "Return five short, distinct search queries that together cover the question."
        ),
        pydantic_model=SearchPlan,
        model_name=get_large_model_name(),
        **get_completion_kwargs(),
    )
    plan = planner(f"Research question: {query}")
    return ", ".join(plan.search_terms)


def plan_research(
    store: DeterministicWorkflowStore, *, use_live_llm: bool = True
) -> str:
    """PocketFlow tool: plan state — derive search terms and record a snapshot.

    :param store: Shared workflow store (query is already set).
    :param use_live_llm: When ``False``, use a simple offline fallback for terms.
    :returns: Status message for PocketFlow memory.
    """
    validate_deterministic_transition("plan", "search")
    store.search_terms = _derive_search_terms(store.query, use_live_llm=use_live_llm)
    store.steps.append(
        WorkflowStepSnapshot(state="plan", search_terms=store.search_terms)
    )
    return f"Planned search terms: {store.search_terms}"


def search_literature(store: DeterministicWorkflowStore) -> str:
    """PocketFlow tool: search state — retrieve evidence and record a snapshot.

    :param store: Shared workflow store with ``search_terms`` from the plan step.
    :returns: Status message listing retrieved titles.
    """
    validate_deterministic_transition("search", "summarize")
    terms = store.search_terms or store.query
    term_list = [term.strip() for term in terms.split(",") if term.strip()]
    if not term_list:
        term_list = [terms.strip()]

    records: list[CitationRecord] = []
    seen_keys: set[str] = set()
    for term in term_list:
        for record in search_fixture_library(term, limit=3):
            if record.key in seen_keys:
                continue
            seen_keys.add(record.key)
            records.append(record)

    store.evidence = records[:5]
    store.steps.append(
        WorkflowStepSnapshot(
            state="search",
            search_terms=terms,
            evidence=list(store.evidence),
        )
    )
    titles = ", ".join(record.title for record in store.evidence) or "(none)"
    return f"Retrieved {len(store.evidence)} record(s): {titles}"


def summarize_evidence(
    store: DeterministicWorkflowStore,
    *,
    use_live_llm: bool = True,
) -> str:
    """PocketFlow tool: summarize state — write markdown report and record a snapshot.

    :param store: Shared workflow store with evidence from search.
    :param use_live_llm: Whether to call the live LLM summarizer.
    :returns: Markdown report text.
    """
    validate_deterministic_transition("summarize", "done")
    if not store.evidence:
        store.report = f"_No evidence retrieved for:_ `{store.query}`"
    elif use_live_llm:
        store.report = default_summarize_fn(store.query, store.evidence)
    else:
        context = format_citations_for_context(store.evidence)
        store.report = (
            f"## Offline stub summary\n\n**Question:** {store.query}\n\n{context}"
        )

    store.steps.append(
        WorkflowStepSnapshot(
            state="summarize",
            search_terms=store.search_terms,
            evidence=list(store.evidence),
            report_markdown=store.report,
        )
    )
    return store.report


def react_step_fn(
    query: str,
    trace: Sequence[ReActStep],
    tools: Mapping[str, Callable[..., str]],
) -> ReActDecision:
    """Scripted two-step ReAct loop for classroom demos.

    :param query: Research question.
    :param trace: Prior ``ReActStep`` records.
    :param tools: Tool mapping (unused in scripted starter).
    :returns: Next ``ReActDecision``.
    """
    _ = tools
    if not trace:
        return ReActDecision(
            thought="Search the fixture library for relevant papers.",
            action="search_library",
            action_input={"query": query, "limit": 3},
        )
    return ReActDecision(
        thought="Evidence collected; answering without another tool call.",
        final_answer=(
            f"## Scripted ReAct answer\n\n"
            f"Question: {query}\n\n"
            f"(Swap to LLM mode in the controls when ready.)"
        ),
    )


def build_agent(search_tool: Callable[..., Any], *, max_iterations: int = 5) -> Any:
    """Wire an ``AgentBot`` over the corpus search tool (Part 4 Exercise 1 reference).

    :param search_tool: the ``search_corpus`` ``@tool`` from Part 3.
    :param max_iterations: cap on the iterate loop (Exercise 5 tunes this).
    :returns: a configured ``AgentBot`` ready to call.
    """
    from llamabot import AgentBot

    from build_deep_research_agent.llm import (
        get_completion_kwargs,
        get_large_model_name,
    )

    return AgentBot(
        tools=[search_tool],
        system_prompt=(
            "You are a research assistant with access to a paper corpus. "
            "FIRST search for relevant papers using search_corpus. "
            "THEN, once you have results, call respond_to_user with a 2-3 sentence "
            "summary grounded in what the tool returned. "
            "You MUST use respond_to_user to deliver your final answer."
        ),
        model_name=get_large_model_name(),
        max_iterations=max_iterations,
        **get_completion_kwargs(),
    )


def count_decisions(agent: Any) -> int:
    """Count how many decision steps an ``AgentBot`` took (Part 4 reference).

    :param agent: an ``AgentBot`` that has already been called.
    :returns: number of spans whose ``operation_name`` is ``"decision"``.
    """
    return len([s for s in agent.spans if s.operation_name == "decision"])


def deterministic_pipeline(search_tool: Callable[..., Any], query: str) -> str:
    """Fixed search → summarize pipeline (no loop, no LLM routing).

    One search call, one summary call — the LLM never decides what to do next.
    This is the deterministic counterpoint to ``AgentBot``'s iterate loop.

    :param search_tool: The ``search_corpus`` callable (``@tool``-wrapped or raw).
    :param query: Research question.
    :returns: Summary text from the summarizer.
    """
    import json

    from llamabot import SimpleBot

    from build_deep_research_agent.llm import (
        get_completion_kwargs,
        get_large_model_name,
    )

    hits = search_tool(query)
    summarizer = SimpleBot(
        system_prompt=(
            "You are a research assistant. "
            "Summarize the search results in 2-3 sentences, "
            "citing paper titles where relevant."
        ),
        model_name=get_large_model_name(),
        **get_completion_kwargs(),
    )
    return summarizer(
        f"Research question: {query}\n\n"
        f"Search results:\n{json.dumps(hits, ensure_ascii=False)}"
    ).content
