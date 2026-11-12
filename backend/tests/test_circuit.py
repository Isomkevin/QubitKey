"""Circuit construction tests."""

from app.quantum.circuit import build_hadamard_qrng_circuit, circuit_info


def test_hadamard_circuit_shape():
    qc = build_hadamard_qrng_circuit(4)
    assert qc.num_qubits == 4
    assert qc.num_clbits == 4
    h_count = sum(1 for inst in qc.data if inst.operation.name == "h")
    measure_count = sum(1 for inst in qc.data if inst.operation.name == "measure")
    assert h_count == 4
    assert measure_count == 4


def test_circuit_info_lists_h_gates():
    qc = build_hadamard_qrng_circuit(3)
    info = circuit_info(qc)
    assert info.num_qubits == 3
    assert info.measurements is True
    assert len(info.gates) == 3
    assert all(g.name == "h" for g in info.gates)
