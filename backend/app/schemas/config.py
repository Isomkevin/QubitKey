"""Health and config response models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "qubitkey"
    time: datetime


class SourceAvailability(BaseModel):
    available: bool
    label: str
    educational: bool | None = None
    reason: str | None = None


class AppConfigResponse(BaseModel):
    limits: dict[str, int]
    sources: dict[str, SourceAvailability]
    features: dict[str, bool]
    disclaimers: list[str]
    software_versions: dict[str, str] = Field(default_factory=dict)
    extras: dict[str, Any] | None = None
