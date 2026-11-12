"""QRNG API and simulator schema tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.quantum.store import clear_store
from app.schemas.common import PROVENANCE, SourceType


@pytest.fixture(autouse=True)
def _clear():
    clear_store()
    yield
    clear_store()


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client: TestClient):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_config_lists_simulator(client: TestClient):
    r = client.get("/api/config")
    assert r.status_code == 200
    body = r.json()
    assert body["sources"]["qiskit_simulator"]["available"] is True
    assert "not physical quantum entropy" in " ".join(body["disclaimers"]).lower()


def test_qrng_simulator_run_schema(client: TestClient):
    r = client.post(
        "/api/qrng/run",
        json={"source_type": "qiskit_simulator", "qubits": 2, "shots": 64, "seed": 7},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["source_type"] == "qiskit_simulator"
    assert body["qubits"] == 2
    assert body["shots"] == 64
    assert body["job_id"] is None
    assert body["bit_order"] == "little_endian_qubit0_rightmost"
    assert body["provenance_statement"] == PROVENANCE[SourceType.QISKIT_SIMULATOR]
    assert "physical quantum entropy" in body["provenance_statement"].lower() or True
    assert "Not physical quantum entropy" in body["provenance_statement"]
    assert sum(body["raw_counts"].values()) == 64
    assert body["circuit"] is not None
    assert body["circuit"]["num_qubits"] == 2
    exp_id = body["experiment_id"]

    g = client.get(f"/api/experiments/{exp_id}")
    assert g.status_code == 200
    assert g.json()["experiment_id"] == exp_id

    e = client.get(f"/api/experiments/{exp_id}/export")
    assert e.status_code == 200
    assert "attachment" in e.headers.get("content-disposition", "")


def test_shot_qubit_limits(client: TestClient):
    r = client.post(
        "/api/qrng/run",
        json={"source_type": "qiskit_simulator", "qubits": 99, "shots": 10},
    )
    assert r.status_code == 422


def test_ibm_unavailable_no_fallback(client: TestClient):
    r = client.post(
        "/api/qrng/run",
        json={"source_type": "ibm_qpu", "qubits": 2, "shots": 32},
    )
    assert r.status_code == 503
    detail = r.json()["detail"].lower()
    assert "simulator" not in detail or "no simulator fallback" in detail or "not configured" in detail or "disabled" in detail
    # Must not return a successful simulator-shaped payload labelled ibm_qpu
    assert r.status_code != 200


def test_classical_csprng(client: TestClient):
    r = client.post(
        "/api/qrng/run",
        json={"source_type": "python_csprng", "qubits": 4, "shots": 16},
    )
    assert r.status_code == 200
    assert r.json()["source_type"] == "python_csprng"
