"""Isolated ML-DSA-65 challenge/signature demo using pyca/cryptography.

Separate from QRNG and TOTP. Library manages keygen randomness.
Do not inject Qiskit bits into this API.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import uuid4

from app.schemas.pqc import (
    PqcChallengeResponse,
    PqcKeygenResponse,
    PqcVerifyRequest,
    PqcVerifyResponse,
)

logger = logging.getLogger(__name__)

TTL_SECONDS = 30 * 60
WARNINGS = [
    "ML-DSA is a post-quantum signature scheme (FIPS 204). It is separate from QRNG and TOTP.",
    "Demo keys are held in short-lived process memory only — not production key management.",
]


class PqcError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


@dataclass
class _Session:
    session_id: str
    private_key: object
    public_key_bytes: bytes
    challenge: bytes | None = None
    challenge_consumed: bool = False
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=TTL_SECONDS)
    )


_lock = Lock()
_STORE: dict[str, _Session] = {}


def _import_mldsa():
    try:
        from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA65PrivateKey

        return MLDSA65PrivateKey
    except Exception as exc:  # pragma: no cover
        raise PqcError(
            f"ML-DSA unavailable (need cryptography>=48 with ML-DSA support): {exc}",
            status_code=503,
        ) from exc


def _fingerprint(public_bytes: bytes) -> str:
    return hashlib.sha256(public_bytes).hexdigest()[:16]


def keygen() -> PqcKeygenResponse:
    MLDSA65PrivateKey = _import_mldsa()
    private_key = MLDSA65PrivateKey.generate()
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes_raw()
    session_id = str(uuid4())
    with _lock:
        _STORE[session_id] = _Session(
            session_id=session_id,
            private_key=private_key,
            public_key_bytes=public_bytes,
        )
    logger.info("PQC keygen session=%s fp=%s", session_id, _fingerprint(public_bytes))
    return PqcKeygenResponse(
        session_id=session_id,
        algorithm="ML-DSA-65",
        public_key_b64=base64.b64encode(public_bytes).decode("ascii"),
        public_key_fingerprint=_fingerprint(public_bytes),
        warnings=list(WARNINGS),
    )


def challenge(session_id: str) -> PqcChallengeResponse:
    with _lock:
        session = _STORE.get(session_id)
        if session is None or session.expires_at <= datetime.now(timezone.utc):
            raise PqcError("Unknown or expired session", status_code=404)
        nonce = secrets.token_bytes(32)
        session.challenge = nonce
        session.challenge_consumed = False
    return PqcChallengeResponse(
        session_id=session_id,
        challenge_b64=base64.b64encode(nonce).decode("ascii"),
        warnings=list(WARNINGS),
    )


def verify(request: PqcVerifyRequest) -> PqcVerifyResponse:
    with _lock:
        session = _STORE.get(request.session_id)
        if session is None or session.expires_at <= datetime.now(timezone.utc):
            raise PqcError("Unknown or expired session", status_code=404)
        if session.challenge_consumed:
            return PqcVerifyResponse(
                valid=False,
                detail="Challenge already consumed (replay rejected)",
            )
        if session.challenge is None:
            raise PqcError("No active challenge", status_code=400)

        challenge_bytes = session.challenge
        private_key = session.private_key
        public_bytes = session.public_key_bytes

        if request.use_server_demo_sign:
            signature = private_key.sign(challenge_bytes)
        else:
            try:
                signature = base64.b64decode(request.signature_b64)
            except Exception as exc:
                raise PqcError("Invalid signature encoding", status_code=422) from exc

        from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA65PublicKey
        from cryptography.exceptions import InvalidSignature

        public_key = MLDSA65PublicKey.from_public_bytes(public_bytes)
        try:
            public_key.verify(signature, challenge_bytes)
            session.challenge_consumed = True
            session.challenge = None
            return PqcVerifyResponse(valid=True)
        except InvalidSignature:
            return PqcVerifyResponse(valid=False, detail="Invalid signature")


def clear_pqc_store() -> None:
    with _lock:
        _STORE.clear()
