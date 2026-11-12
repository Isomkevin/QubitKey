"""TOTP enrollment and verification using OS CSPRNG + PyOTP.

Secrets are never logged. Demo store is in-memory and short-lived.
TOTP is not quantum-resistant.
"""

from __future__ import annotations

import base64
import io
import logging
import secrets as pysecrets
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import uuid4

import pyotp
import qrcode

from app.core.limits import (
    TOTP_RATE_LIMIT_PER_MINUTE,
    TOTP_TTL_SECONDS,
    TOTP_VALID_WINDOW,
)
from app.schemas.totp import (
    TotpEnrollRequest,
    TotpEnrollResponse,
    TotpVerifyRequest,
    TotpVerifyResponse,
)

logger = logging.getLogger(__name__)

WARNINGS = [
    "Keep this secret private. Do not share or commit it.",
    "TOTP is not quantum-resistant. Secret was generated with OS CSPRNG.",
    "Demo store is in-memory and short-lived; not production security.",
]


@dataclass
class _Enrollment:
    enrollment_id: str
    account_label: str
    issuer: str
    secret_base32: str
    expires_at: datetime
    verify_timestamps: list[float]


_lock = Lock()
_STORE: dict[str, _Enrollment] = {}


class TotpError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def _purge_expired(now: datetime) -> None:
    expired = [k for k, v in _STORE.items() if v.expires_at <= now]
    for k in expired:
        del _STORE[k]


def _os_csprng_base32_secret(num_bytes: int = 20) -> str:
    """Generate a base32 TOTP secret from OS CSPRNG (`secrets.token_bytes`)."""
    raw = pysecrets.token_bytes(num_bytes)
    return base64.b32encode(raw).decode("ascii").rstrip("=")


def enroll(request: TotpEnrollRequest) -> TotpEnrollResponse:
    secret_base32 = _os_csprng_base32_secret(20)
    totp = pyotp.TOTP(secret_base32)
    uri = totp.provisioning_uri(name=request.account_label, issuer_name=request.issuer)

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    enrollment_id = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=TOTP_TTL_SECONDS)
    record = _Enrollment(
        enrollment_id=enrollment_id,
        account_label=request.account_label,
        issuer=request.issuer,
        secret_base32=secret_base32,
        expires_at=expires_at,
        verify_timestamps=[],
    )
    with _lock:
        _purge_expired(datetime.now(timezone.utc))
        _STORE[enrollment_id] = record

    logger.info("TOTP enrollment created id=%s (secret redacted)", enrollment_id)

    return TotpEnrollResponse(
        enrollment_id=enrollment_id,
        account_label=request.account_label,
        issuer=request.issuer,
        secret_base32=secret_base32,
        otpauth_uri=uri,
        qr_png_base64=qr_b64,
        expires_at=expires_at,
        warnings=list(WARNINGS),
    )


def verify(request: TotpVerifyRequest) -> TotpVerifyResponse:
    now = datetime.now(timezone.utc)
    with _lock:
        _purge_expired(now)
        record = _STORE.get(request.enrollment_id)
        if record is None:
            return TotpVerifyResponse(valid=False)

        cutoff = time.time() - 60
        record.verify_timestamps = [t for t in record.verify_timestamps if t >= cutoff]
        if len(record.verify_timestamps) >= TOTP_RATE_LIMIT_PER_MINUTE:
            raise TotpError("Too many verification attempts", status_code=429)
        record.verify_timestamps.append(time.time())

        totp = pyotp.TOTP(record.secret_base32)
        ok = bool(totp.verify(request.otp, valid_window=TOTP_VALID_WINDOW))
        logger.info(
            "TOTP verify id=%s result=%s (otp redacted)",
            request.enrollment_id,
            ok,
        )
        return TotpVerifyResponse(valid=ok)


def clear_totp_store() -> None:
    with _lock:
        _STORE.clear()
