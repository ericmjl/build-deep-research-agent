"""LLM configuration for llamabot (local Ollama, local LM Studio, remote, or BYO).

The tutorial uses **two models**:

- **Small** (``gemma2:2b`` / ``google/gemma-2-2b-it``) — Parts 1–2 (prompting,
  memory). Lightweight, runs on any laptop. Env var: ``LLM_MODEL_SMALL``.
- **Large** (``gemma4:12b`` / ``google/gemma-3-12b-it``) — Parts 3–5 (tools,
  workflows, multi-agent). Needs more RAM / VRAM. Env var: ``LLM_MODEL_LARGE``.

Model prefix matters:
- ``ollama_chat/`` — litellm's native Ollama adapter. Connects to
  ``localhost:11434`` automatically. llamabot detects Ollama and sets
  ``tool_choice="auto"`` (reliable tool calling). Use for **local Ollama**.
- ``openai/`` — litellm's OpenAI adapter. Requires ``api_base`` and
  ``api_key``. Use for **local LM Studio** (OpenAI-compatible API at
  ``localhost:1234/v1``) and the **remote Modal endpoint**.
"""

from __future__ import annotations

import os
import warnings
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DEFAULT_SMALL_MODEL = "ollama_chat/gemma2:2b"
DEFAULT_LARGE_MODEL = "ollama_chat/gemma4:12b"

# Backward-compatible alias (deprecated — use DEFAULT_LARGE_MODEL).
DEFAULT_LLM_MODEL = DEFAULT_LARGE_MODEL

LOCAL_OLLAMA_BASE_URL = "http://localhost:11434/v1"
LOCAL_OLLAMA_API_KEY = "ollama-no-auth"


def _register_openai_model(model: str) -> None:
    """Register an ``openai/``-prefixed model with litellm for structured output.

    litellm does not know whether a custom-endpoint model supports structured
    output, so llamabot's StructuredBot rejects it. Register it explicitly.

    :param model: Full model identifier (e.g. ``openai/gemma4:12b``).
    """
    if not model.startswith("openai/"):
        return
    import litellm

    litellm.register_model(
        {
            model.split("/", 1)[1]: {
                "litellm_provider": "openai",
                "supports_response_schema": True,
                "mode": "chat",
            }
        }
    )


# Register both models at import time so StructuredBot works with either.
for _model in (
    os.getenv("LLM_MODEL_SMALL", DEFAULT_SMALL_MODEL),
    os.getenv("LLM_MODEL_LARGE", DEFAULT_LARGE_MODEL),
):
    _register_openai_model(_model)


# @spec TUT-MODEL-021
class MissingLLMConfigError(RuntimeError):
    """Raised when no LLM endpoint or API key is configured."""


def get_small_model_name() -> str:
    """Return the small model name for Parts 1–2 (prompting, memory).

    Defaults to ``ollama_chat/gemma2:2b`` (local Ollama) when
    ``LLM_MODEL_SMALL`` is unset.

    :returns: Model identifier for llamabot / litellm.
    """
    # @spec TUT-MODEL-040
    return os.getenv("LLM_MODEL_SMALL", DEFAULT_SMALL_MODEL)


def get_large_model_name() -> str:
    """Return the large model name for Parts 3–5 (tools, workflows, multi-agent).

    Defaults to ``ollama_chat/gemma4:12b`` (local Ollama) when
    ``LLM_MODEL_LARGE`` is unset.

    :returns: Model identifier for llamabot / litellm.
    """
    # @spec TUT-MODEL-041
    return os.getenv("LLM_MODEL_LARGE", DEFAULT_LARGE_MODEL)


def get_model_name() -> str:
    """Return the large model name (backward-compatible alias).

    .. deprecated::
        Use :func:`get_small_model_name` or :func:`get_large_model_name`
        instead. This alias exists so legacy code that has not yet migrated
        to the two-model setup continues to work. It returns the **large**
        model because that was the original single-model default.
    """
    warnings.warn(
        "get_model_name() is deprecated; use get_small_model_name() "
        "or get_large_model_name() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_large_model_name()  # @spec TUT-MODEL-021  @spec TUT-MODEL-043


def get_completion_kwargs() -> dict[str, Any]:
    """Build llamabot ``completion_kwargs`` from environment variables.

    Shared by both small and large models — they use the same endpoint.

    For ``ollama_chat/`` models litellm connects to ``localhost:11434``
    natively — no ``api_base`` or ``api_key`` needed.

    For ``openai/`` models (remote Modal endpoint or BYO provider):
    1. ``TUTORIAL_LLM_BASE_URL`` + ``TUTORIAL_LLM_API_KEY`` — explicit endpoint.
    2. ``OPENAI_API_KEY`` — BYO provider.

    :returns: Keyword arguments for llamabot bot constructors.
    """
    small = get_small_model_name()
    large = get_large_model_name()
    needs_endpoint = small.startswith("openai/") or large.startswith("openai/")

    # ollama_chat/ prefix: litellm's native adapter handles connection.
    # No api_base or api_key needed — llamabot detects Ollama correctly.
    if not needs_endpoint:
        return {}  # @spec TUT-INFRA-005  @spec TUT-MODEL-042

    kwargs: dict[str, Any] = {}
    base_url = os.getenv("TUTORIAL_LLM_BASE_URL")  # @spec TUT-INFRA-004
    tutorial_key = os.getenv("TUTORIAL_LLM_API_KEY")  # @spec TUT-INFRA-004
    openai_key = os.getenv("OPENAI_API_KEY")  # @spec TUT-INFRA-010

    if base_url:
        kwargs["api_base"] = base_url
        kwargs["api_key"] = tutorial_key or LOCAL_OLLAMA_API_KEY
    elif openai_key:
        kwargs["api_key"] = openai_key
    else:
        # Fall back to local Ollama via OpenAI-compatible API.
        kwargs["api_base"] = LOCAL_OLLAMA_BASE_URL
        kwargs["api_key"] = LOCAL_OLLAMA_API_KEY

    return kwargs
