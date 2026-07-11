# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Reliability test: run the patched AgentBot N times to confirm the
auto-route behavior is deterministic and reliable across repeated runs.

Only change vs stock llamabot: when the model returns text without a tool
call, auto-route to respond_to_user instead of crashing.
"""

from __future__ import annotations

import logging
import time

from dotenv import load_dotenv

load_dotenv()

# ---- Patch: capture content + auto-route ----
import llamabot.bot.simplebot as _simplebot
import llamabot.bot.toolbot as _toolbot_mod
import llamabot.components.pocketflow.nodes as _nodes_mod
from llamabot.bot.simplebot import extract_tool_calls as _orig_extract

_last_model_content: str | None = None


def _capturing_extract(response):
    global _last_model_content
    try:
        _last_model_content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        _last_model_content = ""
    return _orig_extract(response)


_simplebot.extract_tool_calls = _capturing_extract
_toolbot_mod.extract_tool_calls = _capturing_extract

_orig_exec = _nodes_mod.DecideNode._exec_decision


def _auto_route_exec(self, prep_res, span_obj):
    global _last_model_content
    if prep_res.get("_force_terminate", False):
        return _orig_exec(self, prep_res, span_obj)

    import json

    from llamabot.bot.toolbot import ToolBot

    bot = ToolBot(
        model_name=self.model_name,
        tools=self.tools,
        system_prompt=self.system_prompt,
        **self.completion_kwargs,
    )
    # Don't force tool_choice — let the model decide (coding-agent pattern)
    bot.tool_choice = "auto"

    queued = prep_res.get("pending_tool_calls", [])
    if queued:
        tc = queued.pop(0)
        prep_res["pending_tool_calls"] = queued
        func_name = tc["name"]
        func_args_json = tc["arguments"]
    else:
        _last_model_content = None
        tool_calls = bot(
            prep_res["memory"], execution_history=prep_res.get("execution_history")
        )

        if not tool_calls:
            content = (_last_model_content or "").strip()
            if content:
                logging.info("  [auto-route] text -> respond_to_user")
                prep_res["func_call"] = {"response": content}
                return "respond_to_user"
            raise ValueError("No tool calls and no content")

        normalized = [
            {"name": tc.function.name, "arguments": tc.function.arguments}
            for tc in tool_calls
        ]
        nxt = normalized.pop(0)
        prep_res["pending_tool_calls"] = normalized
        func_name = nxt["name"]
        func_args_json = nxt["arguments"]

    logging.info(f"  [tool] {func_name}")
    try:
        func_args = json.loads(func_args_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Bad args: {e}")
    prep_res["func_call"] = func_args
    return func_name


_nodes_mod.DecideNode._exec_decision = _auto_route_exec

# ---- Run N trials ----
from llamabot import AgentBot, tool

from build_deep_research_agent.llm import get_completion_kwargs, get_model_name


@tool
def search_papers(query: str) -> dict:
    """Search for papers matching a query."""
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


N = 10
QUERIES = [
    "What papers discuss protein structure prediction?",
    "Find papers about graph neural networks.",
    "Which papers are about Bayesian methods?",
    "What papers discuss molecular dynamics?",
    "Are there papers about reinforcement learning?",
    "What papers discuss protein folding?",
    "Find papers about uncertainty quantification.",
    "Which papers use transformer architectures?",
    "What papers are about single-cell analysis?",
    "Find papers about active learning.",
]


def main():
    print(f"Running {N} trials with patched AgentBot")
    print(f"Model: {get_model_name()}")
    print("tool_choice: auto (coding-agent pattern)")
    print("=" * 60)

    results = []
    for i in range(N):
        query = QUERIES[i % len(QUERIES)]
        agent = AgentBot(
            tools=[search_papers],
            system_prompt="You are a research assistant. Search for papers using search_papers, then summarize what you found.",
            model_name=get_model_name(),
            max_iterations=5,
            **get_completion_kwargs(),
        )

        print(f"\n[Trial {i + 1}/{N}] {query}")
        t0 = time.time()
        try:
            result = agent(query)
            elapsed = time.time() - t0
            n_chars = len(str(result)) if result else 0
            print(f"  OK ({elapsed:.1f}s, {n_chars} chars)")
            print(f"  {str(result)[:100]}...")
            results.append(
                {"trial": i + 1, "ok": True, "time": elapsed, "chars": n_chars}
            )
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  FAILED ({elapsed:.1f}s): {type(e).__name__}: {e}")
            results.append(
                {
                    "trial": i + 1,
                    "ok": False,
                    "time": elapsed,
                    "chars": 0,
                    "error": str(e),
                }
            )

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    n_ok = sum(1 for r in results if r["ok"])
    n_fail = sum(1 for r in results if not r["ok"])
    avg_time = sum(r["time"] for r in results) / len(results)
    print(f"  Success: {n_ok}/{N}  ({100 * n_ok / N:.0f}%)")
    print(f"  Failed:  {n_fail}/{N}")
    print(f"  Avg time: {avg_time:.1f}s")
    if n_fail:
        print("  Failures:")
        for r in results:
            if not r["ok"]:
                print(f"    Trial {r['trial']}: {r.get('error', '?')}")

    print(
        f"\nVerdict: {'RELIABLE' if n_ok == N else 'UNRELIABLE — needs investigation'}"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
