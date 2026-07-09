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


class CorpusPaper(BaseModel):
    """A full-text paper in the Part 3 search corpus (arXiv + JOSS)."""

    title: str  # @spec EMCP-DOC-003
    authors: list[str] = Field(default_factory=list)  # @spec EMCP-DOC-003
    year: int | None = None  # @spec EMCP-DOC-003
    abstract: str | None = None  # @spec EMCP-DOC-003
    full_text: str  # @spec EMCP-DOC-003
    source: str  # @spec EMCP-DOC-003  ("arxiv" | "joss")
    source_id: str  # @spec EMCP-DOC-003  (arXiv id or DOI)
    url: str  # @spec EMCP-DOC-003
    domain: str  # @spec EMCP-DOC-003


class ResearchReport(BaseModel):
    """Final output from the multi-agent research pipeline."""

    query: str
    evidence: list[CitationRecord]
    report_markdown: str
