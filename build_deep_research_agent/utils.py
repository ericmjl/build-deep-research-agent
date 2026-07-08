"""Utilities for build-deep-research-agent."""

from __future__ import annotations

from typing import TYPE_CHECKING

from build_deep_research_agent.llm import get_completion_kwargs, get_model_name
from build_deep_research_agent.models import Message

if TYPE_CHECKING:
    from llamabot import SimpleBot


def make_bot(system_prompt: str) -> SimpleBot:
    """Create a llamabot SimpleBot configured for tutorial exercises.

    :param system_prompt: System message passed to the bot.
    :returns: Configured SimpleBot instance.
    """
    from llamabot import SimpleBot

    return SimpleBot(
        system_prompt=system_prompt,
        model_name=get_model_name(),
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
