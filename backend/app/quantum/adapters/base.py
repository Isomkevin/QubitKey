"""Adapter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.schemas.common import SourceType
from app.schemas.experiment import CircuitInfo


class AdapterError(Exception):
    """Raised when a source adapter cannot fulfill a request."""

    def __init__(self, message: str, *, status_code: int = 503):
        super().__init__(message)
        self.status_code = status_code


@dataclass
class AdapterResult:
    source_type: SourceType
    backend_name: str | None
    job_id: str | None
    shots: int
    qubits: int
    raw_counts: dict[str, int]
    bit_samples: list[str]
    integer_samples: list[int]
    warnings: list[str] = field(default_factory=list)
    circuit: CircuitInfo | None = None


class SourceAdapter(ABC):
    source_type: SourceType

    @abstractmethod
    def is_available(self) -> tuple[bool, str | None]:
        """Return (available, reason_if_not)."""

    @abstractmethod
    def run(
        self,
        *,
        qubits: int,
        shots: int,
        seed: int | None = None,
        backend_name: str | None = None,
    ) -> AdapterResult:
        ...
