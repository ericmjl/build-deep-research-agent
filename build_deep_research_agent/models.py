"""Shared data models for the deep research agent tutorial."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["system", "user", "assistant", "tool"]


class Message(BaseModel):
    """A single chat message."""

    role: Role  # @spec TUT-MODEL-001
    content: str  # @spec TUT-MODEL-002


class CitationRecord(BaseModel):
    """Normalized bibliographic metadata for prompts and memory."""

    key: str  # @spec TUT-MODEL-010
    title: str  # @spec TUT-MODEL-010
    creators: list[str] = Field(default_factory=list)  # @spec TUT-MODEL-010
    year: int | None = None  # @spec TUT-MODEL-011
    abstract: str | None = None  # @spec TUT-MODEL-012
    url: str | None = None


class ResearchReport(BaseModel):
    """Final output from the multi-agent research pipeline."""

    query: str
    evidence: list[CitationRecord]
    report_markdown: str
