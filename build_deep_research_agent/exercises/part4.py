"""Part 4 planning exercises — learner stubs (edit this file)."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from build_deep_research_agent.deterministic_agent import DeterministicWorkflowStore
from build_deep_research_agent.workflows import ReActDecision, ReActStep


def plan_research(
    store: DeterministicWorkflowStore, *, use_live_llm: bool = True
) -> str:
    """PocketFlow tool body for the plan state.

    Implementation spec: Exercise 1a in ``notebooks/04_workflows.py``.

    :param store: Shared workflow store (query is already set).
    :param use_live_llm: When ``False``, use a simple offline fallback for terms.
    :returns: Status message for PocketFlow memory.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Implement plan_research in build_deep_research_agent/exercises/part4.py"
    )


def search_literature(store: DeterministicWorkflowStore) -> str:
    """PocketFlow tool body for the search state.

    Implementation spec: Exercise 1a in ``notebooks/04_workflows.py``.

    :param store: Shared workflow store with ``search_terms`` from the plan step.
    :returns: Status message listing retrieved titles.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Implement search_literature in build_deep_research_agent/exercises/part4.py"
    )


def summarize_evidence(
    store: DeterministicWorkflowStore,
    *,
    use_live_llm: bool = True,
) -> str:
    """PocketFlow tool body for the summarize state.

    Implementation spec: Exercise 1a in ``notebooks/04_workflows.py``.

    :param store: Shared workflow store with evidence from search.
    :param use_live_llm: Whether to call the live LLM summarizer.
    :returns: Markdown report text.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Implement summarize_evidence in build_deep_research_agent/exercises/part4.py"
    )


def react_step_fn(
    query: str,
    trace: Sequence[ReActStep],
    tools: Mapping[str, Callable[..., str]],
) -> ReActDecision:
    """Return the next ReAct decision for the runner.

    Hint: step 0 calls ``search_library``; step 1 returns ``final_answer``
    without a tool call. Use ``ReActDecision`` from ``workflows.py``.

    :param query: Research question.
    :param trace: Prior ``ReActStep`` records.
    :param tools: Tool mapping from ``make_fixture_react_tools``.
    :returns: Next ``ReActDecision``.
    :raises NotImplementedError: Until you implement this exercise.
    """
    raise NotImplementedError(
        "Implement react_step_fn in build_deep_research_agent/exercises/part4.py"
    )
