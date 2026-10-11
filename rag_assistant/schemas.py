from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=1000)


class Citation(BaseModel):
    source: str
    section: str
    citation: str
    excerpt: str


class AskResponse(BaseModel):
    status: Literal["supported", "insufficient_evidence", "refused"]
    answer: str
    citations: list[Citation]
