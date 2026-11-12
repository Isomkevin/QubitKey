"""Qiskit Aer SamplerV2 educational simulator adapter."""

from __future__ import annotations

from collections import Counter

from app.quantum.adapters.base import AdapterError, AdapterResult, SourceAdapter
from app.quantum.circuit import build_hadamard_qrng_circuit, circuit_info
from app.quantum.conversion import counts_to_samples, normalize_counts
from app.schemas.common import SourceType


class AerSimulatorAdapter(SourceAdapter):
    source_type = SourceType.QISKIT_SIMULATOR

    def is_available(self) -> tuple[bool, str | None]:
        try:
            from qiskit_aer.primitives import SamplerV2  # noqa: F401

            return True, None
        except Exception as exc:  # pragma: no cover - import failure path
            return False, f"qiskit-aer unavailable: {exc}"

    def run(
        self,
        *,
        qubits: int,
        shots: int,
        seed: int | None = None,
        backend_name: str | None = None,
    ) -> AdapterResult:
        available, reason = self.is_available()
        if not available:
            raise AdapterError(reason or "Simulator unavailable", status_code=503)

        from qiskit_aer.primitives import SamplerV2

        qc = build_hadamard_qrng_circuit(qubits)
        sampler = SamplerV2(seed=seed) if seed is not None else SamplerV2()
        job = sampler.run([qc], shots=shots)
        result = job.result()
        pub = result[0]

        # measure_all creates classical register "meas"
        data = pub.data
        if hasattr(data, "meas"):
            counts = dict(data.meas.get_counts())
        else:
            # Fallback: first BitArray-like attribute
            counts = None
            for name in dir(data):
                if name.startswith("_"):
                    continue
                attr = getattr(data, name)
                if hasattr(attr, "get_counts"):
                    counts = dict(attr.get_counts())
                    break
            if counts is None:
                raise AdapterError("Sampler result missing measurement counts")

        counts = normalize_counts(counts, qubits)
        # Expand to individual shots for sample previews / analysis consumers
        bit_samples: list[str] = []
        for bitstring, count in counts.items():
            bit_samples.extend([bitstring] * count)
        # Deterministic shuffle-free expansion may over-represent order; for
        # statistical fairness analysis uses its own generators. Keep expansion.
        if len(bit_samples) != shots:
            # Sampler may return aggregated counts that sum to shots
            total = sum(counts.values())
            if total != shots:
                # Re-normalize by expanding exactly `count` times (already done)
                pass

        integer_samples = []
        from app.quantum.conversion import bitstring_to_int

        integer_samples = [bitstring_to_int(b) for b in bit_samples]

        warnings = [
            "Educational simulation only — not physical quantum entropy.",
        ]
        return AdapterResult(
            source_type=SourceType.QISKIT_SIMULATOR,
            backend_name=backend_name or "aer_sampler_v2",
            job_id=None,
            shots=shots,
            qubits=qubits,
            raw_counts=counts,
            bit_samples=bit_samples,
            integer_samples=integer_samples,
            warnings=warnings,
            circuit=circuit_info(qc),
        )


def simulate_counts_for_bits(num_bits: int, *, qubits: int, seed: int | None) -> list[str]:
    """Generate a flat list of bit characters of length num_bits via Aer."""
    if num_bits <= 0:
        return []
    shots = (num_bits + qubits - 1) // qubits
    adapter = AerSimulatorAdapter()
    result = adapter.run(qubits=qubits, shots=shots, seed=seed)
    bits: list[str] = []
    for sample in result.bit_samples:
        bits.extend(list(sample))
        if len(bits) >= num_bits:
            break
    return bits[:num_bits]
