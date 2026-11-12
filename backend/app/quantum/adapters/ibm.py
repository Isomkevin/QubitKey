"""Optional IBM Quantum Runtime hardware adapter.

Never falls back to the local simulator. Missing credentials or execution
failures raise AdapterError with an explicit message.
"""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.quantum.adapters.base import AdapterError, AdapterResult, SourceAdapter
from app.quantum.circuit import build_hadamard_qrng_circuit, circuit_info
from app.quantum.conversion import bitstring_to_int, normalize_counts
from app.schemas.common import SourceType


class IbmQpuAdapter(SourceAdapter):
    source_type = SourceType.IBM_QPU

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def is_available(self) -> tuple[bool, str | None]:
        if not self.settings.enable_ibm_qpu:
            return False, "IBM QPU disabled (set QUBITKEY_ENABLE_IBM_QPU=true to opt in)"
        if not self.settings.ibm_quantum_token:
            return False, "IBM_QUANTUM_TOKEN not configured"
        try:
            import qiskit_ibm_runtime  # noqa: F401
        except ImportError:
            return False, "qiskit-ibm-runtime not installed (pip install '.[ibm]')"
        return True, None

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
            # Explicit failure — callers must NOT substitute Aer and label as QPU.
            raise AdapterError(
                reason or "IBM QPU unavailable",
                status_code=503,
            )

        try:
            from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
            from qiskit_ibm_runtime import QiskitRuntimeService
        except ImportError as exc:
            raise AdapterError(
                f"IBM runtime import failed: {exc}",
                status_code=503,
            ) from exc

        # Prefer client-side Sampler (0.50+); fall back to top-level Sampler on 0.52.
        try:
            from qiskit_ibm_runtime.executor_sampler import Sampler
        except ImportError:
            try:
                from qiskit_ibm_runtime import Sampler
            except ImportError as exc:
                raise AdapterError(
                    f"IBM Sampler unavailable: {exc}",
                    status_code=503,
                ) from exc

        token = self.settings.ibm_quantum_token
        assert token is not None

        try:
            service = QiskitRuntimeService(
                channel=self.settings.ibm_quantum_channel,
                token=token,
                instance=self.settings.ibm_quantum_instance,
            )
            chosen = backend_name or self.settings.ibm_quantum_backend
            if chosen:
                backend = service.backend(chosen)
            else:
                backend = service.least_busy(operational=True, simulator=False)
            backend_label = getattr(backend, "name", str(backend))

            qc = build_hadamard_qrng_circuit(qubits)
            pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
            isa_circuit = pm.run(qc)

            sampler = Sampler(mode=backend)
            job = sampler.run([isa_circuit], shots=shots)
            job_id = job.job_id() if hasattr(job, "job_id") else None
            result = job.result()
            pub = result[0]
            data = pub.data
            if hasattr(data, "meas"):
                counts = dict(data.meas.get_counts())
            else:
                counts = None
                for name in dir(data):
                    if name.startswith("_"):
                        continue
                    attr = getattr(data, name)
                    if hasattr(attr, "get_counts"):
                        counts = dict(attr.get_counts())
                        break
                if counts is None:
                    raise AdapterError("IBM Sampler result missing measurement counts")

            counts = normalize_counts(counts, qubits)
            bit_samples: list[str] = []
            for bitstring, count in counts.items():
                bit_samples.extend([bitstring] * count)
            integers = [bitstring_to_int(b) for b in bit_samples]

            return AdapterResult(
                source_type=SourceType.IBM_QPU,
                backend_name=backend_label,
                job_id=str(job_id) if job_id else None,
                shots=shots,
                qubits=qubits,
                raw_counts=counts,
                bit_samples=bit_samples,
                integer_samples=integers,
                warnings=[
                    "Physical QPU measurements — not a certified production entropy source.",
                    "Queue times, noise, and calibration affect outcomes.",
                ],
                circuit=circuit_info(qc),
            )
        except AdapterError:
            raise
        except Exception as exc:
            # Do not fall back to simulator.
            raise AdapterError(
                f"IBM QPU execution failed: {exc}. "
                "No simulator fallback was performed.",
                status_code=503,
            ) from exc
