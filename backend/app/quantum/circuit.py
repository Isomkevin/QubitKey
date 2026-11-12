"""Hadamard QRNG circuit builder."""

from __future__ import annotations

from qiskit import QuantumCircuit

from app.schemas.experiment import CircuitInfo, GateInfo


def build_hadamard_qrng_circuit(num_qubits: int) -> QuantumCircuit:
    """Build n-qubit Hadamard + measure_all circuit.

    Each qubit starts in |0>, receives H, then is measured into classical bits.
    ``measure_all`` creates a classical register named ``meas``.
    """
    if num_qubits < 1:
        raise ValueError("num_qubits must be >= 1")
    qc = QuantumCircuit(num_qubits, name="hadamard_qrng")
    for q in range(num_qubits):
        qc.h(q)
    qc.measure_all()
    return qc


def circuit_info(qc: QuantumCircuit) -> CircuitInfo:
    gates: list[GateInfo] = []
    for inst in qc.data:
        name = inst.operation.name
        if name in {"barrier", "measure"}:
            continue
        qubits = [qc.find_bit(q).index for q in inst.qubits]
        gates.append(GateInfo(name=name, qubits=qubits))
    drawing = None
    try:
        drawing = str(qc.draw(output="text"))
    except Exception:
        drawing = None
    return CircuitInfo(
        num_qubits=qc.num_qubits,
        gates=gates,
        measurements=True,
        drawing=drawing,
    )
