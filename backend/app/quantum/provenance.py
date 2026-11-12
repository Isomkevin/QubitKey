"""Software version and provenance helpers."""

from __future__ import annotations


def software_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    try:
        import qiskit

        versions["qiskit"] = getattr(qiskit, "__version__", "unknown")
    except Exception:
        versions["qiskit"] = "unavailable"
    try:
        import qiskit_aer

        versions["qiskit_aer"] = getattr(qiskit_aer, "__version__", "unknown")
    except Exception:
        versions["qiskit_aer"] = "unavailable"
    try:
        import qiskit_ibm_runtime

        versions["qiskit_ibm_runtime"] = getattr(
            qiskit_ibm_runtime, "__version__", "unknown"
        )
    except Exception:
        pass
    return versions
