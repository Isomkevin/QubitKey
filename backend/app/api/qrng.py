"""QRNG run endpoint."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.quantum.adapters.base import AdapterError
from app.quantum.service import run_qrng
from app.schemas.experiment import ExperimentResult, QrngRunRequest

router = APIRouter(tags=["qrng"])


@router.post("/api/qrng/run", response_model=ExperimentResult)
def qrng_run(body: QrngRunRequest) -> ExperimentResult:
    try:
        return run_qrng(body)
    except AdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
