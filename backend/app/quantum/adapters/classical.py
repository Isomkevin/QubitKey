"""Classical PRNG and CSPRNG adapters for fair comparison baselines."""

from __future__ import annotations

import random
import secrets
from collections import Counter

from app.quantum.adapters.base import AdapterResult, SourceAdapter
from app.quantum.conversion import bitstring_to_int
from app.schemas.common import SourceType


def _samples_from_bits(bit_chars: list[str], qubits: int) -> tuple[dict[str, int], list[str], list[int]]:
    bit_samples: list[str] = []
    for i in range(0, len(bit_chars) - qubits + 1, qubits):
        chunk = "".join(bit_chars[i : i + qubits])
        bit_samples.append(chunk)
    counts = dict(Counter(bit_samples))
    integers = [bitstring_to_int(b) for b in bit_samples]
    return counts, bit_samples, integers


class ClassicalPrngAdapter(SourceAdapter):
    source_type = SourceType.PYTHON_PRNG

    def is_available(self) -> tuple[bool, str | None]:
        return True, None

    def run(
        self,
        *,
        qubits: int,
        shots: int,
        seed: int | None = None,
        backend_name: str | None = None,
    ) -> AdapterResult:
        rng = random.Random(seed)
        bit_chars = [str(rng.randint(0, 1)) for _ in range(qubits * shots)]
        counts, bit_samples, integers = _samples_from_bits(bit_chars, qubits)
        return AdapterResult(
            source_type=SourceType.PYTHON_PRNG,
            backend_name=backend_name or "python_random",
            job_id=None,
            shots=shots,
            qubits=qubits,
            raw_counts=counts,
            bit_samples=bit_samples,
            integer_samples=integers,
            warnings=["Educational PRNG — not suitable for cryptography."],
            circuit=None,
        )


class ClassicalCsprngAdapter(SourceAdapter):
    source_type = SourceType.PYTHON_CSPRNG

    def is_available(self) -> tuple[bool, str | None]:
        return True, None

    def run(
        self,
        *,
        qubits: int,
        shots: int,
        seed: int | None = None,
        backend_name: str | None = None,
    ) -> AdapterResult:
        if seed is not None:
            from app.quantum.adapters.base import AdapterError

            raise AdapterError("seed is not allowed for python_csprng", status_code=422)
        bit_chars = [str(secrets.randbits(1)) for _ in range(qubits * shots)]
        counts, bit_samples, integers = _samples_from_bits(bit_chars, qubits)
        return AdapterResult(
            source_type=SourceType.PYTHON_CSPRNG,
            backend_name=backend_name or "python_secrets",
            job_id=None,
            shots=shots,
            qubits=qubits,
            raw_counts=counts,
            bit_samples=bit_samples,
            integer_samples=integers,
            warnings=["Classical OS CSPRNG baseline — not quantum entropy."],
            circuit=None,
        )


def prng_bits(num_bits: int, seed: int | None) -> list[str]:
    rng = random.Random(seed)
    return [str(rng.randint(0, 1)) for _ in range(num_bits)]


def csprng_bits(num_bits: int) -> list[str]:
    return [str(secrets.randbits(1)) for _ in range(num_bits)]
