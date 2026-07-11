"""LLM configuration for llamabot (local Ollama, remote endpoint, or BYO provider).

Model prefix matters:
- ``ollama_chat/`` — litellm's native Ollama adapter. Connects to
  ``localhost:11434`` automatically. llamabot detects Ollama and sets
  ``tool_choice="auto"`` (reliable tool calling). Use for **local Ollama**.
- ``openai/`` — litellm's OpenAI adapter. Requires ``api_base`` and
  ``api_key``. Use for the **remote Modal endpoint** (OpenAI-compatible API).
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM_MODEL = "ollama_chat/gemma4:12b"
LOCAL_OLLAMA_BASE_URL = "http://localhost:11434/v1"
LOCAL_OLLAMA_API_KEY = "ollama-no-auth"

# For openai/-prefixed models served on custom endpoints (e.g. Modal's
# Ollama-as-a-service), litellm does not know whether the model supports
# structured output, so llamabot's StructuredBot rejects it. Register it.
_configured_model = os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)
if _configured_model.startswith("openai/"):
    import litellm

    litellm.register_model(
        {
            _configured_model.split("/", 1)[1]: {
                "litellm_provider": "openai",
                "supports_response_schema": True,
                "mode": "chat",
            }
        }
    )


# @spec TUT-MODEL-021
class MissingLLMConfigError(RuntimeError):
    """Raised when no LLM endpoint or API key is configured."""


def get_model_name() -> str:
    """Return the model name used for tutorial exercises.

    Defaults to ``ollama_chat/gemma4:12b`` (local Ollama) when ``LLM_MODEL`` is unset.

    :returns: Model identifier for llamabot / litellm.
    """
    return os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)  # @spec TUT-MODEL-021


def get_completion_kwargs() -> dict[str, Any]:
    """Build llamabot ``completion_kwargs`` from environment variables.

    For ``ollama_chat/`` models litellm connects to ``localhost:11434``
    natively — no ``api_base`` or ``api_key`` needed.

    For ``openai/`` models (remote Modal endpoint or BYO provider):
    1. ``TUTORIAL_LLM_BASE_URL`` + ``TUTORIAL_LLM_API_KEY`` — explicit endpoint.
    2. ``OPENAI_API_KEY`` — BYO provider.

    :returns: Keyword arguments for llamabot bot constructors.
    """
    model = os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)

    # ollama_chat/ prefix: litellm's native adapter handles connection.
    # No api_base or api_key needed — llamabot detects Ollama correctly.
    if model.startswith("ollama_chat/"):
        return {}  # @spec TUT-INFRA-005

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
