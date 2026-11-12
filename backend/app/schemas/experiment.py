"""Experiment request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.core.limits import (
    DEFAULT_QUBITS,
    DEFAULT_SHOTS,
    MAX_QUBITS,
    MAX_SHOTS,
    MIN_QUBITS,
    MIN_SHOTS,
    PREVIEW_SAMPLE_LIMIT,
)
from app.schemas.common import BIT_ORDER, SourceType


class GateInfo(BaseModel):
    name: str
    qubits: list[int]


class CircuitInfo(BaseModel):
    num_qubits: int
    gates: list[GateInfo]
    measurements: bool = True
    drawing: str | None = None


class QrngRunRequest(BaseModel):
    source_type: SourceType = SourceType.QISKIT_SIMULATOR
    qubits: int = Field(default=DEFAULT_QUBITS, ge=MIN_QUBITS, le=MAX_QUBITS)
    shots: int = Field(default=DEFAULT_SHOTS, ge=MIN_SHOTS, le=MAX_SHOTS)
    seed: int | None = None
    backend_name: str | None = None

    @field_validator("seed")
    @classmethod
    def seed_not_for_csprng(cls, value: int | None, info):  # type: ignore[no-untyped-def]
        source = info.data.get("source_type")
        if value is not None and source == SourceType.PYTHON_CSPRNG:
            raise ValueError("seed is not allowed for python_csprng")
        return value


class ExperimentResult(BaseModel):
    experiment_id: str
    source_type: SourceType
    backend_name: str | None = None
    job_id: str | None = None
    shots: int
    qubits: int
    raw_counts: dict[str, int]
    bit_samples: list[str]
    integer_samples: list[int]
    created_at: datetime
    software_versions: dict[str, str]
    warnings: list[str] = Field(default_factory=list)
    provenance_statement: str
    circuit: CircuitInfo | None = None
    bit_order: str = BIT_ORDER
    # Internal-only fields excluded from default API when None
    full_bit_samples: list[str] | None = Field(default=None, exclude=True)
    metadata: dict[str, Any] | None = Field(default=None, exclude=True)

    def preview(self, limit: int = PREVIEW_SAMPLE_LIMIT) -> "ExperimentResult":
        data = self.model_dump()
        data["bit_samples"] = self.bit_samples[:limit]
        data["integer_samples"] = self.integer_samples[:limit]
        return ExperimentResult(**data)
