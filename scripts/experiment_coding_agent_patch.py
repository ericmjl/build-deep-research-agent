# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Experiment: coding-agent-style AgentBot patch.

Coding agents (Claude Code, opencode) treat "model returns text with no tool
call" as THE FINAL ANSWER — they don't crash. This script patches llamabot's
DecideNode to do the same, then runs a full AgentBot end-to-end.

Two changes:
1. tool_choice='auto' (not 'required') — matches coding agents, avoids Ollama
   silently ignoring 'required'
2. When the model returns content without a tool call, auto-route to
   respond_to_user with that content (instead of raising ValueError)
"""

from __future__ import annotations

import json
import logging

from dotenv import load_dotenv

load_dotenv()

# ---- Patch llamabot BEFORE creating any AgentBot ----
# We patch at two levels:
#   (a) extract_tool_calls — to capture the model's text content as a side effect
#   (b) DecideNode._exec_decision — to auto-route when no tool calls come back

import llamabot.bot.simplebot as _simplebot
import llamabot.bot.toolbot as _toolbot_mod
import llamabot.components.pocketflow.nodes as _nodes_mod
from llamabot.bot.simplebot import extract_tool_calls as _orig_extract

# Module-level capture of the last model response content
_last_model_content: str | None = None


def _capturing_extract_tool_calls(response):
    """Wrap extract_tool_calls to also capture the model's text content."""
    global _last_model_content
    try:
        _last_model_content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        _last_model_content = ""
    return _orig_extract(response)


# Patch in both modules (toolbot imports it from simplebot)
_simplebot.extract_tool_calls = _capturing_extract_tool_calls
_toolbot_mod.extract_tool_calls = _capturing_extract_tool_calls


# --- Patch DecideNode._exec_decision ---
_orig_exec_decision = _nodes_mod.DecideNode._exec_decision


def _coding_agent_exec_decision(self, prep_res, span_obj):
    """DecideNode._exec_decision with coding-agent termination behavior.

    Changes vs original:
    1. Always uses tool_choice='auto' (coding agents never force 'required')
    2. When the model returns no tool calls, treats the text content as the
       final answer → auto-routes to respond_to_user (instead of ValueError)
    """
    global _last_model_content

    # --- Force-termination check (unchanged from original) ---
    if prep_res.get("_force_terminate", False):
        return _orig_exec_decision(self, prep_res, span_obj)

    from llamabot.bot.toolbot import ToolBot

    # --- Build the ToolBot (same as original, but tool_choice='auto') ---
    enhanced_system_prompt = self.system_prompt
    bot = ToolBot(
        model_name=self.model_name,
        tools=self.tools,
        system_prompt=enhanced_system_prompt,
        **self.completion_kwargs,
    )
    # CODING AGENT BEHAVIOR: always 'auto', never 'required'
    bot.tool_choice = "auto"

    # --- Drain queued tool calls or call the LLM (same logic) ---
    queued_tool_calls = prep_res.get("pending_tool_calls", [])
    if queued_tool_calls:
        next_tool_call = queued_tool_calls.pop(0)
        prep_res["pending_tool_calls"] = queued_tool_calls
        func_name = next_tool_call["name"]
        func_args_json = next_tool_call["arguments"]
    else:
        _last_model_content = None  # reset before the LLM call
        tool_calls = bot(
            prep_res["memory"],
            execution_history=prep_res.get("execution_history"),
        )

        if not tool_calls:
            # ============================================================
            # CODING AGENT BEHAVIOR: model returned text, not a tool call.
            # In Claude Code / opencode, this IS the final answer.
            # We auto-route to respond_to_user with the text content.
            # ============================================================
            content = (_last_model_content or "").strip()
            if content:
                logging.info(
                    "Coding-agent termination: model returned text "
                    "(no tool call) → auto-routing to respond_to_user"
                )
                if span_obj:
                    span_obj["auto_terminated"] = True
                    span_obj.log(
                        "auto_terminated",
                        reason="model_returned_text_without_tool_call",
                    )
                prep_res["func_call"] = {"response": content}
                return "respond_to_user"
            # Truly broken: no tool calls AND no content
            raise ValueError(
                f"No tool calls and no content from model: {self.model_name}"
            )

        normalized_tool_calls = [
            {
                "name": tc.function.name,
                "arguments": tc.function.arguments,
            }
            for tc in tool_calls
        ]
        next_tool_call = normalized_tool_calls.pop(0)
        prep_res["pending_tool_calls"] = normalized_tool_calls
        func_name = next_tool_call["name"]
        func_args_json = next_tool_call["arguments"]

    # --- Log + parse args (same as original) ---
    if span_obj:
        span_obj["chosen_tool"] = func_name
        span_obj.log("tool_selected", tool_name=func_name)

    iteration_count = prep_res.get("iteration_count", "unknown")
    logging.info(
        f"DecideNode chose tool: {func_name} "
        f"(iteration: {iteration_count}/{self.max_iterations or 'unlimited'})"
    )
    try:
        func_args = json.loads(func_args_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse tool call arguments: {e}")
    prep_res["func_call"] = func_args
    return func_name


# Apply the patch
_nodes_mod.DecideNode._exec_decision = _coding_agent_exec_decision

# ---- Now set up and run the AgentBot ----
from llamabot import AgentBot, tool

from build_deep_research_agent.exercises.solutions import part3
from build_deep_research_agent.fixtures.loader import load_corpus_papers
from build_deep_research_agent.llm import get_completion_kwargs, get_model_name


def main():
    print("=" * 60)
    print("CODING-AGENT PATCHED AGENTBOT EXPERIMENT")
    print("=" * 60)

    # Build the docstore + search tool (same as Part 4 Exercise 1)
    print("\n[1] Building docstore...")
    papers = load_corpus_papers()
    docstore, side_table = part3.build_corpus_docstore(papers)
    print(f"    {len(papers)} papers, {len(side_table)} chunks")

    @tool
    def search_corpus(query: str, limit: int = 5) -> dict:
        """Semantic search over the ingested paper corpus."""
        return part3.search_corpus(docstore, side_table, query, limit)

    # Create the patched AgentBot
    print("\n[2] Creating AgentBot (coding-agent patched)...")
    agent = AgentBot(
        tools=[search_corpus],
        system_prompt=(
            "You are a research assistant with access to a paper corpus. "
            "FIRST search for relevant papers using search_corpus. "
            "THEN, once you have results, call respond_to_user with a 2-3 sentence "
            "summary grounded in what the tool returned. "
            "You MUST use respond_to_user to deliver your final answer."
        ),
        model_name=get_model_name(),
        max_iterations=5,
        **get_completion_kwargs(),
    )

    # Run it — this should work reliably now
    query = "What papers discuss protein structure prediction?"
    print(f"\n[3] Running agent: {query!r}")
    print("    (watch for 'Coding-agent termination' in logs)")
    print()

    try:
        result = agent(query)
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result)
    except Exception as e:
        print(f"\nFAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
