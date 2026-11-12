"""Shared enumerations and provenance helpers."""

from __future__ import annotations

from enum import Enum


class SourceType(str, Enum):
    QISKIT_SIMULATOR = "qiskit_simulator"
    IBM_QPU = "ibm_qpu"
    PYTHON_PRNG = "python_prng"
    PYTHON_CSPRNG = "python_csprng"


PROVENANCE: dict[SourceType, str] = {
    SourceType.QISKIT_SIMULATOR: (
        "Educational Qiskit/Aer simulation. Not physical quantum entropy."
    ),
    SourceType.IBM_QPU: (
        "Physical IBM Quantum measurement outcomes. "
        "Not a certified production entropy source."
    ),
    SourceType.PYTHON_PRNG: (
        "Educational Python random.Random PRNG. Not suitable for cryptography."
    ),
    SourceType.PYTHON_CSPRNG: (
        "Operating-system CSPRNG via Python secrets. Classical cryptographic baseline."
    ),
}

BIT_ORDER = "little_endian_qubit0_rightmost"


def provenance_for(source: SourceType) -> str:
    return PROVENANCE[source]
