"""Deterministic and ReAct planning workflows for Part 4."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from build_deep_research_agent.fixtures.search import search_fixture_library
from build_deep_research_agent.models import CitationRecord
from build_deep_research_agent.prompts import (
    RESEARCH_SYSTEM_PROMPT,
    format_citations_for_context,
)

# @spec PLAN-DET-001
DeterministicState = Literal["plan", "search", "summarize", "done"]
StoppedReason = Literal["answer", "max_steps"]


class InvalidStateTransitionError(ValueError):
    """Raised when a deterministic workflow transition is not allowed."""

    def __init__(self, from_state: str, to_state: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Invalid state transition: {from_state!r} -> {to_state!r}")


@dataclass
class WorkflowStepSnapshot:
    """State and evidence captured at one deterministic workflow step."""

    state: DeterministicState
    search_terms: str | None = None
    evidence: list[CitationRecord] = field(default_factory=list)
    report_markdown: str | None = None


@dataclass
class DeterministicResult:
    """Output from a completed deterministic workflow run."""

    query: str
    steps: list[WorkflowStepSnapshot]
    final_answer: str


SearchFn = Callable[[str, str], list[CitationRecord]]
SummarizeFn = Callable[[str, list[CitationRecord]], str]
PlanFn = Callable[[str], str]
ReActStepFn = Callable[
    [str, list["ReActStep"], Mapping[str, Callable[..., str]]], "ReActDecision"
]


@dataclass
class ReActStep:
    """One thought-action-observation turn in a ReAct loop."""

    thought: str  # @spec PLAN-REACT-003
    action: str | None = None  # @spec PLAN-REACT-003
    action_input: dict[str, Any] | None = None  # @spec PLAN-REACT-003
    observation: str | None = None  # @spec PLAN-REACT-003


@dataclass
class ReActDecision:
    """Model output for the next ReAct loop iteration."""

    thought: str
    action: str | None = None
    action_input: dict[str, Any] | None = None
    final_answer: str | None = None


@dataclass
class ReActResult:
    """Output from a ReAct runner."""

    query: str
    trace: list[ReActStep]  # @spec PLAN-REACT-002
    final_answer: str  # @spec PLAN-REACT-002
    stopped_reason: StoppedReason


@dataclass
class WorkflowComparison:
    """Side-by-side metrics for deterministic vs. ReAct runs."""

    query: str
    deterministic_step_count: int
    react_trace_length: int
    deterministic_output_kind: str
    react_output_kind: str
    deterministic_answer: str
    react_answer: str


# @spec PLAN-DET-002
DETERMINISTIC_TRANSITIONS: dict[DeterministicState, DeterministicState | None] = {
    "plan": "search",
    "search": "summarize",
    "summarize": "done",
    "done": None,
}


def validate_deterministic_transition(
    from_state: DeterministicState,
    to_state: DeterministicState,
) -> None:
    """Validate a deterministic workflow state transition.

    :param from_state: Current workflow state.
    :param to_state: Proposed next state.
    :raises InvalidStateTransitionError: If the transition is not allowed.
    """
    # @spec PLAN-DET-020
    expected = DETERMINISTIC_TRANSITIONS.get(from_state)
    if expected != to_state:
        raise InvalidStateTransitionError(from_state, to_state)


def default_plan_fn(query: str) -> str:
    """Use the full query as search terms for classroom demos.

    :param query: Research question.
    :returns: Search terms string.
    """
    return query.strip()


def default_fixture_search_fn(query: str, search_terms: str) -> list[CitationRecord]:
    """Search bundled fixtures using plan-step search terms.

    :param query: Original research question (unused; kept for injection symmetry).
    :param search_terms: Terms produced by the plan step.
    :returns: Matching citation records.
    """
    _ = query
    return search_fixture_library(search_terms, limit=5)


def default_summarize_fn(query: str, evidence: list[CitationRecord]) -> str:
    """Summarize evidence with llamabot SimpleBot when LLM credentials exist.

    :param query: Research question.
    :param evidence: Retrieved citation records.
    :returns: Markdown summary grounded in evidence.
    """
    from llamabot import SimpleBot

    from build_deep_research_agent.llm import get_completion_kwargs, get_model_name

    context = format_citations_for_context(evidence)
    prompt = (
        f"Research question:\n{query}\n\n"
        f"Evidence:\n{context}\n\n"
        "Write a concise markdown literature summary grounded in the evidence."
    )
    bot = SimpleBot(
        system_prompt=RESEARCH_SYSTEM_PROMPT,
        model_name=get_model_name(),
        **get_completion_kwargs(),
    )
    return str(bot(prompt))


class DeterministicWorkflow:
    """Fixed pipeline: plan -> search -> summarize -> done.

    Call :meth:`plan`, :meth:`search`, and :meth:`summarize` explicitly to
    walk the state machine step by step, or use :meth:`run` for a one-shot pass.

    :param search_fn: Callable invoked during the search state.
    :param summarize_fn: Callable invoked during the summarize state.
    :param plan_fn: Callable that derives search terms from the query.
    """

    # @spec PLAN-DET-001

    def __init__(
        self,
        search_fn: SearchFn | None = None,
        summarize_fn: SummarizeFn | None = None,
        plan_fn: PlanFn | None = None,
    ) -> None:
        # @spec PLAN-DET-003
        self._search_fn = search_fn or default_fixture_search_fn
        self._summarize_fn = summarize_fn or default_summarize_fn
        self._plan_fn = plan_fn or default_plan_fn

    def plan(self, query: str) -> tuple[str, WorkflowStepSnapshot]:
        """Run the ``plan`` state and validate ``plan`` → ``search``.

        :param query: Research question.
        :returns: Search terms and a snapshot for the plan step.
        """
        validate_deterministic_transition("plan", "search")
        search_terms = self._plan_fn(query)
        snapshot = WorkflowStepSnapshot(state="plan", search_terms=search_terms)
        return search_terms, snapshot

    def search(
        self, query: str, search_terms: str
    ) -> tuple[list[CitationRecord], WorkflowStepSnapshot]:
        """Run the ``search`` state and validate ``search`` → ``summarize``.

        :param query: Research question.
        :param search_terms: Comma-separated terms from :meth:`plan`.
        :returns: Retrieved evidence and a snapshot for the search step.
        """
        validate_deterministic_transition("search", "summarize")
        evidence = list(self._search_fn(query, search_terms))
        snapshot = WorkflowStepSnapshot(
            state="search",
            search_terms=search_terms,
            evidence=evidence,
        )
        return evidence, snapshot

    def summarize(
        self,
        query: str,
        search_terms: str,
        evidence: list[CitationRecord],
    ) -> tuple[str, WorkflowStepSnapshot]:
        """Run the ``summarize`` state and validate ``summarize`` → ``done``.

        :param query: Research question.
        :param search_terms: Terms produced during planning.
        :param evidence: Records retrieved during search.
        :returns: Markdown report and a snapshot for the summarize step.
        """
        validate_deterministic_transition("summarize", "done")
        report = self._summarize_fn(query, evidence)  # @spec PLAN-DET-021
        snapshot = WorkflowStepSnapshot(
            state="summarize",
            search_terms=search_terms,
            evidence=list(evidence),
            report_markdown=report,
        )
        return report, snapshot

    @staticmethod
    def done_snapshot(
        search_terms: str,
        evidence: list[CitationRecord],
        report: str,
    ) -> WorkflowStepSnapshot:
        """Build the terminal ``done`` snapshot (no transition to validate).

        :param search_terms: Terms produced during planning.
        :param evidence: Records retrieved during search.
        :param report: Final markdown answer from summarize.
        :returns: Snapshot marking the workflow complete.
        """
        return WorkflowStepSnapshot(
            state="done",
            search_terms=search_terms,
            evidence=list(evidence),
            report_markdown=report,
        )

    def run(self, query: str) -> DeterministicResult:
        """Execute all states in order and return step snapshots.

        :param query: Research question.
        :returns: Completed workflow result with per-step evidence.
        """
        search_terms, plan_snapshot = self.plan(query)
        evidence, search_snapshot = self.search(query, search_terms)
        report, summarize_snapshot = self.summarize(query, search_terms, evidence)
        done_snapshot = self.done_snapshot(search_terms, evidence, report)
        return DeterministicResult(
            query=query,
            steps=[plan_snapshot, search_snapshot, summarize_snapshot, done_snapshot],
            final_answer=report,
        )


def get_react_max_steps(explicit: int | None = None) -> int:
    """Resolve ReAct max steps from argument or ``REACT_MAX_STEPS`` env var.

    :param explicit: Override step limit when provided.
    :returns: Maximum ReAct iterations.
    """
    if explicit is not None:
        return explicit
    return int(os.getenv("REACT_MAX_STEPS", "8"))


def make_fixture_react_tools() -> dict[str, Callable[..., str]]:
    """Build offline ReAct tools backed by bundled citation fixtures.

    :returns: Tool name to callable mapping for :class:`ReActRunner`.
    """

    def search_library(query: str, limit: int = 5) -> str:
        """Search the bundled tutorial citation library.

        :param query: Case-insensitive substring query.
        :param limit: Maximum records to return.
        :returns: Formatted citation context.
        """
        records = search_fixture_library(query, limit=limit)
        return format_citations_for_context(records)

    return {"search_library": search_library}


def make_mcp_react_tools(client: Any) -> dict[str, Callable[..., str]]:
    """Wrap a :class:`~build_deep_research_agent.mcp.client.ZoteroMCPClient` for ReAct.

    :param client: Started MCP client with search available.
    :returns: Tool mapping suitable for :class:`ReActRunner`.
    """

    def zotero_search(query: str, limit: int = 5) -> str:
        """Search Zotero via MCP and return raw tool output.

        :param query: Search query string.
        :param limit: Maximum number of results.
        :returns: Raw search output from zotero-mcp.
        """
        return client.search_items(query=query, limit=limit)

    return {"zotero_search": zotero_search}


class ReActRunner:
    """Reason + Act loop with injectable step decisions for tests and demos.

    :param tools: Named callables the runner may invoke.
    :param step_fn: Callable returning the next :class:`ReActDecision`.
    :param max_steps: Step limit (defaults to ``REACT_MAX_STEPS`` env var).
    """

    # @spec PLAN-REACT-001

    def __init__(
        self,
        tools: Mapping[str, Callable[..., str]],
        step_fn: ReActStepFn,
        max_steps: int | None = None,
    ) -> None:
        self.tools = dict(tools)
        self.step_fn = step_fn
        self.max_steps = get_react_max_steps(max_steps)

    def run(self, query: str) -> ReActResult:
        """Execute the ReAct loop until a stop condition is met.

        :param query: Research question.
        :returns: Trace and final answer (possibly partial at max steps).
        """
        trace: list[ReActStep] = []
        final_answer = ""

        for _ in range(self.max_steps):
            decision = self.step_fn(query, trace, self.tools)
            step = ReActStep(
                thought=decision.thought,
                action=decision.action,
                action_input=decision.action_input,
            )

            if decision.final_answer and not decision.action:
                step.observation = None
                trace.append(step)
                final_answer = decision.final_answer
                return ReActResult(
                    query=query,
                    trace=trace,
                    final_answer=final_answer,
                    stopped_reason="answer",
                )  # @spec PLAN-REACT-010

            if decision.action:
                observation = self._invoke_tool(decision.action, decision.action_input)
                step.observation = observation
                trace.append(step)
                continue

            step.observation = "No action or final answer provided."
            trace.append(step)
            final_answer = decision.thought
            return ReActResult(
                query=query,
                trace=trace,
                final_answer=final_answer,
                stopped_reason="answer",
            )

        partial = trace[-1].thought if trace else "Max steps reached without an answer."
        return ReActResult(
            query=query,
            trace=trace,
            final_answer=partial,
            stopped_reason="max_steps",
        )  # @spec PLAN-REACT-011

    def _invoke_tool(self, action: str, action_input: dict[str, Any] | None) -> str:
        """Call a named tool and return its observation string.

        :param action: Tool name from the ReAct decision.
        :param action_input: Keyword arguments for the tool callable.
        :returns: Tool output or an error message recorded as observation.
        """
        # @spec PLAN-REACT-012
        tool = self.tools.get(action)
        if tool is None:
            return f"Tool error: unknown action {action!r}."
        kwargs = action_input or {}
        try:
            return str(tool(**kwargs))
        except Exception as exc:  # noqa: BLE001 — teaching moment in observations
            return f"Tool error: {exc}"


def make_llamabot_react_step_fn() -> ReActStepFn:
    """Build a ReAct step decider backed by llamabot SimpleBot JSON output.

    :returns: Callable suitable for :class:`ReActRunner`.
    """
    from llamabot import SimpleBot

    from build_deep_research_agent.llm import get_completion_kwargs, get_model_name

    system_prompt = """\
You are a research agent using ReAct (Reason + Act).

Respond with JSON only:
{
  "thought": "your reasoning",
  "action": "tool_name or null",
  "action_input": {"query": "..."} or null,
  "final_answer": "markdown answer or null"
}

Rules:
- Use a tool when you need more evidence.
- When you have enough evidence, set action to null and provide final_answer.
- Do not invent tool names.
"""
    bot = SimpleBot(
        system_prompt=system_prompt,
        model_name=get_model_name(),
        **get_completion_kwargs(),
    )

    def step_fn(
        query: str,
        trace: list[ReActStep],
        tools: Mapping[str, Callable[..., str]],
    ) -> ReActDecision:
        """Propose the next ReAct step using the live LLM."""
        tool_list = ", ".join(sorted(tools)) or "(none)"
        history = "\n".join(
            f"Thought: {step.thought}\nAction: {step.action}\nObservation: {step.observation}"
            for step in trace
        )
        prompt = (
            f"Research question: {query}\n"
            f"Available tools: {tool_list}\n\n"
            f"Trace so far:\n{history or '(empty)'}\n\n"
            "Return the next JSON step."
        )
        raw = str(bot(prompt))
        return _parse_react_decision(raw)

    return step_fn


def _parse_react_decision(raw: str) -> ReActDecision:
    """Parse JSON ReAct output from an LLM response.

    :param raw: Model response text.
    :returns: Parsed decision with safe fallbacks.
    """
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return ReActDecision(thought=raw.strip(), final_answer=raw.strip())

    return ReActDecision(
        thought=str(payload.get("thought") or ""),
        action=payload.get("action"),
        action_input=payload.get("action_input"),
        final_answer=payload.get("final_answer"),
    )


def compare_workflow_results(
    query: str,
    deterministic: DeterministicResult,
    react: ReActResult,
) -> WorkflowComparison:
    """Build comparison metrics for Exercise 3.

    :param query: Shared research question.
    :param deterministic: Result from :class:`DeterministicWorkflow`.
    :param react: Result from :class:`ReActRunner`.
    :returns: Structured comparison for notebook rendering.
    """
    return WorkflowComparison(
        query=query,
        deterministic_step_count=len(deterministic.steps),
        react_trace_length=len(react.trace),
        deterministic_output_kind="structured report (markdown)",
        react_output_kind="trace + final answer",
        deterministic_answer=deterministic.final_answer,
        react_answer=react.final_answer,
    )
