# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Experiment: coding-agent-style AgentBot patch (fast version).

Uses a trivial mock tool (no docstore) so we can test the agent loop in seconds.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv

load_dotenv()

# ---- Patch llamabot BEFORE creating any AgentBot ----
import llamabot.bot.simplebot as _simplebot
import llamabot.bot.toolbot as _toolbot_mod
import llamabot.components.pocketflow.nodes as _nodes_mod
from llamabot.bot.simplebot import extract_tool_calls as _orig_extract

_last_model_content: str | None = None


def _capturing_extract_tool_calls(response):
    global _last_model_content
    try:
        _last_model_content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        _last_model_content = ""
    return _orig_extract(response)


_simplebot.extract_tool_calls = _capturing_extract_tool_calls
_toolbot_mod.extract_tool_calls = _capturing_extract_tool_calls

_orig_exec_decision = _nodes_mod.DecideNode._exec_decision


def _coding_agent_exec_decision(self, prep_res, span_obj):
    global _last_model_content

    if prep_res.get("_force_terminate", False):
        return _orig_exec_decision(self, prep_res, span_obj)

    import json

    from llamabot.bot.toolbot import ToolBot

    bot = ToolBot(
        model_name=self.model_name,
        tools=self.tools,
        system_prompt=self.system_prompt,
        **self.completion_kwargs,
    )
    # CODING AGENT: always 'auto', never 'required'
    bot.tool_choice = "auto"

    queued_tool_calls = prep_res.get("pending_tool_calls", [])
    if queued_tool_calls:
        next_tool_call = queued_tool_calls.pop(0)
        prep_res["pending_tool_calls"] = queued_tool_calls
        func_name = next_tool_call["name"]
        func_args_json = next_tool_call["arguments"]
    else:
        _last_model_content = None
        tool_calls = bot(
            prep_res["memory"],
            execution_history=prep_res.get("execution_history"),
        )

        if not tool_calls:
            # ============================================================
            # CODING AGENT BEHAVIOR: model returned text, not a tool call.
            # In Claude Code / opencode, this IS the final answer.
            # Auto-route to respond_to_user with the text content.
            # ============================================================
            content = (_last_model_content or "").strip()
            if content:
                logging.info(
                    ">>> Coding-agent termination: model returned text "
                    "(no tool call) -> auto-routing to respond_to_user"
                )
                if span_obj:
                    span_obj["auto_terminated"] = True
                prep_res["func_call"] = {"response": content}
                return "respond_to_user"
            raise ValueError(
                f"No tool calls and no content from model: {self.model_name}"
            )

        normalized_tool_calls = [
            {"name": tc.function.name, "arguments": tc.function.arguments}
            for tc in tool_calls
        ]
        next_tool_call = normalized_tool_calls.pop(0)
        prep_res["pending_tool_calls"] = normalized_tool_calls
        func_name = next_tool_call["name"]
        func_args_json = next_tool_call["arguments"]

    if span_obj:
        span_obj["chosen_tool"] = func_name

    iteration_count = prep_res.get("iteration_count", "unknown")
    logging.info(
        f">>> DecideNode chose tool: {func_name} "
        f"(iteration: {iteration_count}/{self.max_iterations or 'unlimited'})"
    )
    try:
        func_args = json.loads(func_args_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse tool call arguments: {e}")
    prep_res["func_call"] = func_args
    return func_name


_nodes_mod.DecideNode._exec_decision = _coding_agent_exec_decision

# ---- Now run the AgentBot with a simple mock tool ----
from llamabot import AgentBot, tool

from build_deep_research_agent.llm import get_completion_kwargs, get_model_name


@tool
def search_papers(query: str) -> dict:
    """Search for papers matching a query. Returns matching paper titles."""
    # Mock results — no docstore needed
    return {
        "query": query,
        "items": [
            {
                "title": "AlphaFold: Highly accurate protein structure prediction",
                "authors": ["Jumper et al."],
                "year": 2021,
            },
            {
                "title": "ESM-2: Language models for protein structure prediction",
                "authors": ["Lin et al."],
                "year": 2023,
            },
        ],
    }


def main():
    print("=" * 60)
    print("CODING-AGENT PATCHED AGENTBOT (fast mock tool)")
    print("=" * 60)

    agent = AgentBot(
        tools=[search_papers],
        system_prompt=(
            "You are a research assistant. Search for papers using search_papers, "
            "then summarize what you found."
        ),
        model_name=get_model_name(),
        max_iterations=5,
        **get_completion_kwargs(),
    )

    query = "What papers discuss protein structure prediction?"
    print(f"\nQuery: {query!r}")
    print("Running agent (watch for >>> markers)...\n")

    try:
        result = agent(query)
        print("\n" + "=" * 60)
        print("SUCCESS — Result:")
        print("=" * 60)
        print(result)
    except Exception as e:
        print(f"\nFAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
