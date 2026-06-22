"""Utilities for build-deep-research-agent."""

from build_deep_research_agent.models import Message


def format_messages_preview(messages: list[Message]) -> str:
    """Render a list of chat messages as a Markdown preview block.

    :param messages: Messages whose ``role`` and ``content`` should be shown.
    :returns: Markdown string with one fenced ``text`` block per message.
    """
    preview_lines = []
    for message in messages:
        preview_lines.append(f"**{message.role}**\n\n```text\n{message.content}\n```")
    return "\n\n".join(preview_lines)
