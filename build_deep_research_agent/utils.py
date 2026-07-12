"""Utilities for build-deep-research-agent."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from build_deep_research_agent.llm import get_completion_kwargs
from build_deep_research_agent.models import Message

if TYPE_CHECKING:
    from llamabot import SimpleBot

ModelSize = Literal["small", "large"]


def make_bot(  # @spec TUT-MODEL-044
    system_prompt: str, *, model: ModelSize = "small"
) -> SimpleBot:
    """Create a llamabot SimpleBot configured for tutorial exercises.

    :param system_prompt: System message passed to the bot.
    :param model: Which tutorial model to use — ``"small"`` (gemma2:2b,
        Parts 1–2) or ``"large"`` (gemma4:12b, Parts 3–5). Defaults to
        ``"small"``.
    :returns: Configured SimpleBot instance.
    """
    from llamabot import SimpleBot

    from build_deep_research_agent.llm import get_large_model_name, get_small_model_name

    model_name = get_small_model_name() if model == "small" else get_large_model_name()

    return SimpleBot(
        system_prompt=system_prompt,
        model_name=model_name,
        **get_completion_kwargs(),
        stream_target="none",
    )


def format_messages_preview(messages: list[Message]) -> str:
    """Render a list of chat messages as a Markdown preview block.

    :param messages: Messages whose ``role`` and ``content`` should be shown.
    :returns: Markdown string with one fenced ``text`` block per message.
    """
    preview_lines = []
    for message in messages:
        preview_lines.append(f"**{message.role}**\n\n```text\n{message.content}\n```")
    return "\n\n".join(preview_lines)
