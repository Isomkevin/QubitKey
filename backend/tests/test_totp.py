"""TOTP enrollment and verification tests."""

import pyotp
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.security.totp_service import clear_totp_store


@pytest.fixture(autouse=True)
def _clear():
    clear_totp_store()
    yield
    clear_totp_store()


@pytest.fixture
def client():
    return TestClient(app)


def test_enroll_and_verify(client: TestClient):
    r = client.post(
        "/api/auth/totp/enroll",
        json={"account_label": "demo@local", "issuer": "QubitKey"},
    )
    assert r.status_code == 200
    assert r.headers.get("cache-control") == "no-store"
    body = r.json()
    assert "secret_base32" in body
    assert body["otpauth_uri"].startswith("otpauth://totp/")
    assert body["qr_png_base64"]
    assert any("not quantum-resistant" in w.lower() for w in body["warnings"])

    otp = pyotp.TOTP(body["secret_base32"]).now()
    v = client.post(
        "/api/auth/totp/verify",
        json={"enrollment_id": body["enrollment_id"], "otp": otp},
    )
    assert v.status_code == 200
    assert v.json()["valid"] is True


def test_invalid_otp(client: TestClient):
    r = client.post(
        "/api/auth/totp/enroll",
        json={"account_label": "demo@local", "issuer": "QubitKey"},
    )
    body = r.json()
    v = client.post(
        "/api/auth/totp/verify",
        json={"enrollment_id": body["enrollment_id"], "otp": "000000"},
    )
    assert v.status_code == 200
    # May rarely collide; accept False as expected for fixed wrong code
    assert v.json()["valid"] is False


def test_unknown_enrollment(client: TestClient):
    v = client.post(
        "/api/auth/totp/verify",
        json={"enrollment_id": "00000000-0000-0000-0000-000000000000", "otp": "123456"},
    )
    assert v.status_code == 200
    assert v.json()["valid"] is False
