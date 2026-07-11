# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Experiments: what makes gemma4:12b reliably call respond_to_user?

Tests multiple configurations of the two-iteration AgentBot scenario:
  iter 1: search_corpus(query)  ← works fine
  iter 2: respond_to_user(summary)  ← THIS IS WHAT BREAKS

We simulate iteration 2 directly with litellm (bypassing AgentBot overhead)
to isolate what configuration makes the model choose respond_to_user.
"""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv

load_dotenv()

import litellm

# --- Config from .env ---
MODEL = os.getenv("LLM_MODEL", "openai/gemma4:12b")
API_BASE = os.getenv("TUTORIAL_LLM_BASE_URL", "")
API_KEY = os.getenv("TUTORIAL_LLM_API_KEY", "tutorial-no-auth")

# litellm registration (same as build_deep_research_agent.llm)
if MODEL.startswith("openai/"):
    litellm.register_model(
        {
            MODEL.split("/", 1)[1]: {
                "litellm_provider": "openai",
                "supports_response_schema": True,
                "mode": "chat",
            }
        }
    )

litellm.suppress_debug_info = True


# --- Tool schemas (matching what AgentBot sends) ---
SEARCH_CORPUS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_corpus",
        "description": "Semantic search over the ingested paper corpus.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": ""},
                "limit": {"type": "integer", "description": "", "default": 5},
            },
            "required": ["query"],
        },
    },
}

RESPOND_TO_USER_TOOL = {
    "type": "function",
    "function": {
        "name": "respond_to_user",
        "description": (
            "Respond to the user with a message.\n\n"
            "Use this tool when you don't think there's code to write "
            "(e.g., greetings, general questions, explanations, or when "
            "the user just needs a conversational response)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "description": "The message to send to the user",
                }
            },
            "required": ["response"],
        },
    },
}

TODAY_DATE_TOOL = {
    "type": "function",
    "function": {
        "name": "today_date",
        "description": "Get the current date.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}

RETURN_OBJECT_TOOL = {
    "type": "function",
    "function": {
        "name": "return_object_to_user",
        "description": (
            "Return an object from the calling context's globals to the user.\n\n"
            "Use this tool when you want to return a specific object (e.g. "
            "DataFrame, list, dict, etc.) from the calling context's globals() "
            "dictionary."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "variable_name": {
                    "type": "string",
                    "description": "The name of the variable in globals() to return",
                }
            },
            "required": ["variable_name"],
        },
    },
}

INSPECT_GLOBALS_TOOL = {
    "type": "function",
    "function": {
        "name": "inspect_globals",
        "description": "Inspect and return a summary of available objects in the globals dictionary.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}

ALL_TOOLS = [
    TODAY_DATE_TOOL,
    RESPOND_TO_USER_TOOL,
    RETURN_OBJECT_TOOL,
    INSPECT_GLOBALS_TOOL,
    SEARCH_CORPUS_TOOL,
]
MINIMAL_TOOLS = [RESPOND_TO_USER_TOOL, SEARCH_CORPUS_TOOL]

# --- Simulated search results (from a real run) ---
SEARCH_RESULTS = (
    "{'mode': 'corpus', 'items': ["
    "{'title': 'Protein 3D Graph Structure Learning for Robust Structure-based "
    "Protein Property Prediction', 'authors': ['Yufei Huang', 'Siyuan Li'], "
    "'year': 2023, 'url': 'http://arxiv.org/abs/2310.11466v2', "
    "'source': 'arxiv', 'domain': 'computational-biology'}, "
    "{'title': 'Mass Balance Approximation of Unfolding Improves Potential-Like "
    "Methods for Protein Stability Predictions', 'authors': ['Ivan Rossi'], "
    "'year': 2025, 'url': 'http://arxiv.org/abs/2504.06806v1', "
    "'source': 'arxiv', 'domain': 'computational-biology'}], "
    "'docstore_stats': {'table_name': 'corpus_papers', 'document_count': 40}}"
)


def call_model(
    label: str,
    messages: list[dict],
    tools: list[dict],
    tool_choice: str = "auto",
) -> dict | None:
    """Call the model and return a summary of the response."""
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT: {label}")
    print(f"  model={MODEL}  tools={len(tools)}  tool_choice={tool_choice}")
    print(f"{'=' * 60}")

    try:
        resp = litellm.completion(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            api_base=API_BASE,
            api_key=API_KEY,
            temperature=0.0,
        )
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

    msg = resp.choices[0].message
    finish = resp.choices[0].finish_reason
    tool_calls = msg.tool_calls
    content = (msg.content or "").strip()

    result = {
        "finish_reason": finish,
        "tool_calls": None,
        "content_preview": content[:120] if content else "",
    }

    if tool_calls:
        names = [tc.function.name for tc in tool_calls]
        result["tool_calls"] = names
        print(f"  finish_reason: {finish}")
        print(f"  tool_calls:    {names}  ✓")
        if content:
            print(f"  content:       {content[:80]}...")
    else:
        print(f"  finish_reason: {finish}")
        print("  tool_calls:    None  ✗ (model returned plain text!)")
        print(f"  content:       {content[:120]}")

    return result


def run_experiments():
    """Run all experiments testing iteration-2 termination behavior."""

    user_query = "What papers discuss protein structure prediction?"

    # ---- The iteration-2 state: search results are in memory, model must answer ----
    # This is the CRITICAL scenario where gemma4:12b fails.

    BASE_SYSTEM = (
        "You are a research assistant with access to a paper corpus. "
        "FIRST search for relevant papers using search_corpus. "
        "THEN, once you have results, call respond_to_user with a 2-3 sentence "
        "summary grounded in what the tool returned. "
        "You MUST use respond_to_user to deliver your final answer."
    )

    STRONG_SYSTEM = (
        "You are a research assistant with access to a paper corpus.\n\n"
        "RULES:\n"
        "1. If you need information, call search_corpus.\n"
        "2. If you already have search results, you MUST call respond_to_user "
        "with your answer. Do NOT write your answer as plain text.\n"
        "3. You MUST ALWAYS call a tool. Never respond without calling a tool.\n"
    )

    # How llamabot injects tool results (as HumanMessage, per the logs)
    llamabot_messages = [
        {"role": "system", "content": BASE_SYSTEM},
        {
            "role": "system",
            "content": f"Previously called tools:\n- search_corpus({{'query': '{user_query}'}}) -> {SEARCH_RESULTS}\n",
        },
        {"role": "user", "content": user_query},
        {"role": "user", "content": "Chosen Tool: search_corpus"},
        {"role": "user", "content": SEARCH_RESULTS},
    ]

    # Standard OpenAI format (tool response as a proper tool message)
    openai_messages = [
        {"role": "system", "content": BASE_SYSTEM},
        {"role": "user", "content": user_query},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "search_corpus",
                        "arguments": json.dumps({"query": user_query}),
                    },
                }
            ],
        },
        {"role": "tool", "tool_call_id": "call_1", "content": SEARCH_RESULTS},
    ]

    # ===== EXPERIMENT 1: Current AgentBot behavior (baseline reproduction) =====
    call_model(
        "1. Baseline: AgentBot format, all 5 tools, tool_choice=required",
        llamabot_messages,
        ALL_TOOLS,
        tool_choice="required",
    )

    # ===== EXPERIMENT 2: Same but tool_choice=auto =====
    call_model(
        "2. AgentBot format, all 5 tools, tool_choice=auto",
        llamabot_messages,
        ALL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 3: Minimal tools (just respond_to_user + search_corpus) =====
    call_model(
        "3. Minimal tools (2), tool_choice=auto",
        llamabot_messages,
        MINIMAL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 4: Strong system prompt =====
    strong_messages = [
        {"role": "system", "content": STRONG_SYSTEM},
        *llamabot_messages[1:],
    ]
    call_model(
        "4. Strong system prompt, minimal tools, tool_choice=auto",
        strong_messages,
        MINIMAL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 5: Standard OpenAI tool-response format =====
    call_model(
        "5. OpenAI tool-response format, minimal tools, tool_choice=auto",
        openai_messages,
        MINIMAL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 6: OpenAI format + strong prompt =====
    openai_strong = [{"role": "system", "content": STRONG_SYSTEM}, *openai_messages[1:]]
    call_model(
        "6. OpenAI format + strong prompt, minimal tools, tool_choice=auto",
        openai_strong,
        MINIMAL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 7: OpenAI format + strong prompt + all tools =====
    call_model(
        "7. OpenAI format + strong prompt, ALL tools, tool_choice=auto",
        openai_strong,
        ALL_TOOLS,
        tool_choice="auto",
    )

    # ===== EXPERIMENT 8: Ollama-style enhanced prompt (what llamabot appends) =====
    ollama_suffix = "\n\n**CRITICAL FOR OLLAMA MODELS**: You MUST ALWAYS select and call a tool. Never return a response without calling a tool. Every user request requires you to select one of the available tools and execute it. This is mandatory - you cannot skip tool selection."
    ollama_messages = [
        {"role": "system", "content": BASE_SYSTEM + ollama_suffix},
        *llamabot_messages[1:],
    ]
    call_model(
        "8. Ollama-enhanced prompt (llamabot suffix), all tools, tool_choice=auto",
        ollama_messages,
        ALL_TOOLS,
        tool_choice="auto",
    )

    print("\n" + "=" * 60)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_experiments()
