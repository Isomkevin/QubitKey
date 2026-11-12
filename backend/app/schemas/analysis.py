"""Analysis / compare schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.core.limits import DEFAULT_COMPARE_BITS, DEFAULT_QUBITS, MAX_COMPARE_BITS, MAX_QUBITS, MIN_QUBITS
from app.schemas.common import SourceType


class CompareRequest(BaseModel):
    sample_bits: int = Field(default=DEFAULT_COMPARE_BITS, ge=8, le=MAX_COMPARE_BITS)
    qubits: int = Field(default=DEFAULT_QUBITS, ge=MIN_QUBITS, le=MAX_QUBITS)
    sources: list[SourceType] = Field(
        default_factory=lambda: [
            SourceType.QISKIT_SIMULATOR,
            SourceType.PYTHON_PRNG,
            SourceType.PYTHON_CSPRNG,
        ]
    )
    seed: int | None = 42


class SourceMetrics(BaseModel):
    source_type: SourceType
    provenance_statement: str
    metrics: dict[str, Any]


class CompareResponse(BaseModel):
    sample_bits: int
    sources: list[SourceMetrics]
    caveats: list[str]
    created_at: datetime
