"""TOTP enroll/verify schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class TotpEnrollRequest(BaseModel):
    account_label: str = Field(min_length=1, max_length=128)
    issuer: str = Field(default="QubitKey", min_length=1, max_length=64)


class TotpEnrollResponse(BaseModel):
    enrollment_id: str
    account_label: str
    issuer: str
    secret_base32: str
    otpauth_uri: str
    qr_png_base64: str
    expires_at: datetime
    warnings: list[str]


class TotpVerifyRequest(BaseModel):
    enrollment_id: str
    otp: str = Field(min_length=6, max_length=8)


class TotpVerifyResponse(BaseModel):
    valid: bool
