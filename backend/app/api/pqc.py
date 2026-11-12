"""Optional ML-DSA demo endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.pqc import (
    PqcChallengeResponse,
    PqcKeygenResponse,
    PqcVerifyRequest,
    PqcVerifyResponse,
)
from app.security.pqc_service import PqcError, challenge, keygen, verify

router = APIRouter(tags=["pqc"])


@router.post("/api/pqc/keygen", response_model=PqcKeygenResponse)
def pqc_keygen() -> PqcKeygenResponse:
    try:
        return keygen()
    except PqcError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


class _ChallengeBody(BaseModel):
    session_id: str


@router.post("/api/pqc/challenge", response_model=PqcChallengeResponse)
def pqc_challenge(body: _ChallengeBody) -> PqcChallengeResponse:
    try:
        return challenge(body.session_id)
    except PqcError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.post("/api/pqc/verify", response_model=PqcVerifyResponse)
def pqc_verify(body: PqcVerifyRequest) -> PqcVerifyResponse:
    try:
        return verify(body)
    except PqcError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
