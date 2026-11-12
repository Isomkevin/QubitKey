"""Optional ML-DSA demo tests."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app
from app.security.pqc_service import clear_pqc_store


@pytest.fixture(autouse=True)
def _clear():
    clear_pqc_store()
    get_settings.cache_clear()
    yield
    clear_pqc_store()
    get_settings.cache_clear()


def test_pqc_flow_server_demo_sign(monkeypatch):
    monkeypatch.setenv("QUBITKEY_ENABLE_PQC", "true")
    get_settings.cache_clear()
    client = TestClient(create_app())

    try:
        kg = client.post("/api/pqc/keygen")
    except Exception as exc:
        pytest.skip(f"ML-DSA unavailable: {exc}")

    if kg.status_code == 503:
        pytest.skip(kg.json().get("detail", "ML-DSA unavailable"))

    assert kg.status_code == 200
    session_id = kg.json()["session_id"]
    assert kg.json()["algorithm"] == "ML-DSA-65"
    assert any("separate from QRNG" in w for w in kg.json()["warnings"])

    ch = client.post("/api/pqc/challenge", json={"session_id": session_id})
    assert ch.status_code == 200

    v = client.post(
        "/api/pqc/verify",
        json={
            "session_id": session_id,
            "signature_b64": "AA==",
            "use_server_demo_sign": True,
        },
    )
    assert v.status_code == 200
    assert v.json()["valid"] is True

    # Replay should fail
    v2 = client.post(
        "/api/pqc/verify",
        json={
            "session_id": session_id,
            "signature_b64": "AA==",
            "use_server_demo_sign": True,
        },
    )
    assert v2.status_code == 200
    assert v2.json()["valid"] is False
