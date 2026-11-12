"""Analysis compare endpoint."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.analysis.compare import compare_sources
from app.quantum.adapters.base import AdapterError
from app.schemas.analysis import CompareRequest, CompareResponse

router = APIRouter(tags=["analysis"])


@router.post("/api/analysis/compare", response_model=CompareResponse)
def analysis_compare(body: CompareRequest) -> CompareResponse:
    try:
        return compare_sources(body)
    except AdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
