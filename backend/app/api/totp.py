"""TOTP enroll/verify API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from app.schemas.totp import (
    TotpEnrollRequest,
    TotpEnrollResponse,
    TotpVerifyRequest,
    TotpVerifyResponse,
)
from app.security.totp_service import TotpError, enroll, verify

router = APIRouter(tags=["totp"])


@router.post("/api/auth/totp/enroll", response_model=TotpEnrollResponse)
def totp_enroll(body: TotpEnrollRequest, response: Response) -> TotpEnrollResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return enroll(body)
    except TotpError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.post("/api/auth/totp/verify", response_model=TotpVerifyResponse)
def totp_verify(body: TotpVerifyRequest) -> TotpVerifyResponse:
    try:
        return verify(body)
    except TotpError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
