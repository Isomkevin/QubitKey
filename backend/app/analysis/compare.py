"""Fair multi-source comparison orchestration."""

from __future__ import annotations

from datetime import datetime, timezone

from app.analysis.metrics import compute_metrics
from app.quantum.adapters.base import AdapterError
from app.quantum.adapters.classical import csprng_bits, prng_bits
from app.quantum.adapters.ibm import IbmQpuAdapter
from app.quantum.adapters.simulator import simulate_counts_for_bits
from app.schemas.analysis import CompareRequest, CompareResponse, SourceMetrics
from app.schemas.common import SourceType, provenance_for


COMPARE_CAVEATS = [
    "Passing these diagnostics does not prove cryptographic security or sufficient min-entropy.",
    "Equal sample sizes are used for fairness; do not over-interpret single runs.",
    "Qiskit simulator output is educational simulation, not physical quantum entropy.",
]


def _bits_for_source(
    source: SourceType,
    sample_bits: int,
    *,
    qubits: int,
    seed: int | None,
) -> list[str]:
    if source == SourceType.QISKIT_SIMULATOR:
        return simulate_counts_for_bits(sample_bits, qubits=qubits, seed=seed)
    if source == SourceType.PYTHON_PRNG:
        return prng_bits(sample_bits, seed)
    if source == SourceType.PYTHON_CSPRNG:
        return csprng_bits(sample_bits)
    if source == SourceType.IBM_QPU:
        adapter = IbmQpuAdapter()
        available, reason = adapter.is_available()
        if not available:
            raise AdapterError(reason or "IBM QPU unavailable", status_code=503)
        shots = (sample_bits + qubits - 1) // qubits
        result = adapter.run(qubits=qubits, shots=shots, seed=None)
        bits: list[str] = []
        for sample in result.bit_samples:
            bits.extend(list(sample))
            if len(bits) >= sample_bits:
                break
        return bits[:sample_bits]
    raise AdapterError(f"Unsupported source: {source}", status_code=422)


def compare_sources(request: CompareRequest) -> CompareResponse:
    sources_out: list[SourceMetrics] = []
    for source in request.sources:
        bits = _bits_for_source(
            source,
            request.sample_bits,
            qubits=request.qubits,
            seed=request.seed,
        )
        # Build integer samples from qubit-sized chunks when possible
        integers: list[int] = []
        q = request.qubits
        from app.quantum.conversion import bitstring_to_int

        for i in range(0, len(bits) - q + 1, q):
            integers.append(bitstring_to_int("".join(bits[i : i + q])))

        metrics = compute_metrics(bits, integer_samples=integers)
        sources_out.append(
            SourceMetrics(
                source_type=source,
                provenance_statement=provenance_for(source),
                metrics=metrics,
            )
        )

    return CompareResponse(
        sample_bits=request.sample_bits,
        sources=sources_out,
        caveats=COMPARE_CAVEATS,
        created_at=datetime.now(timezone.utc),
    )
