"""LLM configuration for llamabot (Modal endpoint or BYO provider)."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


# @spec TUT-MODEL-021
class MissingLLMConfigError(RuntimeError):
    """Raised when no LLM endpoint or API key is configured."""


def get_model_name() -> str:
    """Return the model name used for tutorial exercises.

    :returns: Model identifier for llamabot / litellm.
    """
    return os.getenv("LLM_MODEL", "gpt-4o-mini")


def get_completion_kwargs() -> dict[str, Any]:
    """Build llamabot ``completion_kwargs`` from environment variables.

    Prefers ``TUTORIAL_LLM_*`` (Modal path). Falls back to ``OPENAI_API_KEY``.

    :returns: Keyword arguments for llamabot bot constructors.
    :raises MissingLLMConfigError: If neither tutorial nor BYO credentials exist.
    """
    kwargs: dict[str, Any] = {}
    base_url = os.getenv("TUTORIAL_LLM_BASE_URL")  # @spec TUT-INFRA-004
    tutorial_key = os.getenv("TUTORIAL_LLM_API_KEY")  # @spec TUT-INFRA-004
    openai_key = os.getenv("OPENAI_API_KEY")  # @spec TUT-INFRA-010

    if base_url:
        kwargs["api_base"] = base_url
    if tutorial_key:
        kwargs["api_key"] = tutorial_key
    elif openai_key:
        kwargs["api_key"] = openai_key

    if not kwargs.get("api_key") and not base_url:
        raise MissingLLMConfigError(  # @spec TUT-INFRA-005
            "Set TUTORIAL_LLM_BASE_URL and TUTORIAL_LLM_API_KEY (Modal path) "
            "or OPENAI_API_KEY (BYO path)."
        )
    return kwargs
