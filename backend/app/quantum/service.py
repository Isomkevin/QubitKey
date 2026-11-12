"""QRNG orchestration service."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.core.limits import PREVIEW_SAMPLE_LIMIT
from app.quantum.adapters.base import AdapterError, SourceAdapter
from app.quantum.adapters.classical import ClassicalCsprngAdapter, ClassicalPrngAdapter
from app.quantum.adapters.ibm import IbmQpuAdapter
from app.quantum.adapters.simulator import AerSimulatorAdapter
from app.quantum.provenance import software_versions
from app.quantum.store import save_experiment
from app.schemas.common import SourceType, provenance_for
from app.schemas.experiment import ExperimentResult, QrngRunRequest


def get_adapter(source_type: SourceType) -> SourceAdapter:
    if source_type == SourceType.QISKIT_SIMULATOR:
        return AerSimulatorAdapter()
    if source_type == SourceType.PYTHON_PRNG:
        return ClassicalPrngAdapter()
    if source_type == SourceType.PYTHON_CSPRNG:
        return ClassicalCsprngAdapter()
    if source_type == SourceType.IBM_QPU:
        return IbmQpuAdapter()
    raise AdapterError(f"Unsupported source_type: {source_type}", status_code=422)


def source_availability() -> dict[str, dict]:
    adapters: list[SourceAdapter] = [
        AerSimulatorAdapter(),
        IbmQpuAdapter(),
        ClassicalPrngAdapter(),
        ClassicalCsprngAdapter(),
    ]
    labels = {
        SourceType.QISKIT_SIMULATOR: ("Qiskit Aer simulator", True),
        SourceType.IBM_QPU: ("IBM Quantum hardware", False),
        SourceType.PYTHON_PRNG: ("Python random.Random", True),
        SourceType.PYTHON_CSPRNG: ("Python secrets CSPRNG", False),
    }
    out: dict[str, dict] = {}
    for adapter in adapters:
        available, reason = adapter.is_available()
        label, educational = labels[adapter.source_type]
        entry: dict = {
            "available": available,
            "label": label,
            "educational": educational,
        }
        if not available and reason:
            entry["reason"] = reason
        out[adapter.source_type.value] = entry
    return out


def run_qrng(request: QrngRunRequest) -> ExperimentResult:
    adapter = get_adapter(request.source_type)
    available, reason = adapter.is_available()
    if not available:
        raise AdapterError(reason or "Source unavailable", status_code=503)

    result = adapter.run(
        qubits=request.qubits,
        shots=request.shots,
        seed=request.seed,
        backend_name=request.backend_name,
    )

    experiment = ExperimentResult(
        experiment_id=str(uuid4()),
        source_type=result.source_type,
        backend_name=result.backend_name,
        job_id=result.job_id,
        shots=result.shots,
        qubits=result.qubits,
        raw_counts=result.raw_counts,
        bit_samples=result.bit_samples[:PREVIEW_SAMPLE_LIMIT],
        integer_samples=result.integer_samples[:PREVIEW_SAMPLE_LIMIT],
        created_at=datetime.now(timezone.utc),
        software_versions=software_versions(),
        warnings=result.warnings,
        provenance_statement=provenance_for(result.source_type),
        circuit=result.circuit,
        full_bit_samples=result.bit_samples,
    )
    # Stash full samples on the stored object for export/analysis helpers
    stored = experiment.model_copy(
        update={
            "bit_samples": result.bit_samples,
            "integer_samples": result.integer_samples,
        }
    )
    save_experiment(stored)
    return experiment
