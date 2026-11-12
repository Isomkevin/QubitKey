"""Optional ML-DSA challenge/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PqcKeygenResponse(BaseModel):
    session_id: str
    algorithm: str = "ML-DSA-65"
    public_key_b64: str
    public_key_fingerprint: str
    warnings: list[str]


class PqcChallengeResponse(BaseModel):
    session_id: str
    challenge_b64: str
    warnings: list[str]


class PqcVerifyRequest(BaseModel):
    session_id: str
    signature_b64: str = Field(min_length=1)
    # Demo may also accept server-side sign for local demo convenience:
    use_server_demo_sign: bool = False


class PqcVerifyResponse(BaseModel):
    valid: bool
    algorithm: str = "ML-DSA-65"
    detail: str | None = None
