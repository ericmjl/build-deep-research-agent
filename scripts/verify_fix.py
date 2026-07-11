# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Verify llamabot 0.19.6 auto-route fix works with NO monkeypatch."""

from __future__ import annotations

import logging
import time

from dotenv import load_dotenv

load_dotenv()

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


def main():
    print(
        f"llamabot: {__import__('importlib.metadata', fromlist=['version']).version('llamabot')}"
    )
    print(f"model: {get_model_name()}")
    print("=" * 60)

    queries = [
        "What papers discuss protein structure prediction?",
        "Find papers about graph neural networks.",
        "Which papers are about Bayesian methods?",
    ]

    for i, query in enumerate(queries, 1):
        agent = AgentBot(
            tools=[search_papers],
            system_prompt="You are a research assistant. Search for papers using search_papers, then summarize what you found.",
            model_name=get_model_name(),
            max_iterations=5,
            **get_completion_kwargs(),
        )

        print(f"\n[Trial {i}/{len(queries)}] {query}")
        t0 = time.time()
        try:
            result = agent(query)
            elapsed = time.time() - t0
            print(f"  OK ({elapsed:.1f}s)")
            print(f"  {str(result)[:120]}...")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  FAILED ({elapsed:.1f}s): {type(e).__name__}: {e}")

    print(f"\n{'=' * 60}")
    print("Done — all 3 trials should show OK with no monkeypatch.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
