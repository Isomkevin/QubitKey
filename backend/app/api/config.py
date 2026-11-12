"""Public configuration and source availability."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.quantum.provenance import software_versions
from app.quantum.service import source_availability
from app.schemas.config import AppConfigResponse, SourceAvailability

router = APIRouter(tags=["config"])


@router.get("/api/config", response_model=AppConfigResponse)
def config() -> AppConfigResponse:
    settings = get_settings()
    raw = source_availability()
    sources = {k: SourceAvailability(**v) for k, v in raw.items()}
    return AppConfigResponse(
        limits=settings.limits_dict(),
        sources=sources,
        features={
            "totp": True,
            "pqc": settings.enable_pqc,
            "analysis": True,
        },
        disclaimers=[
            "Simulator output is not physical quantum entropy.",
            "TOTP is not quantum-resistant.",
            "Statistical tests do not prove cryptographic security.",
        ],
        software_versions=software_versions(),
    )
