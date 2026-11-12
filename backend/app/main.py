"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import config as config_api
from app.api import experiments as experiments_api
from app.api import health as health_api
from app.api import qrng as qrng_api
from app.core.config import get_settings
from app.core.logging_utils import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title="QubitKey API",
        version="0.1.0",
        description=(
            "Educational QRNG and TOTP demonstration. "
            "Simulator output is not physical quantum entropy. "
            "TOTP is not quantum-resistant."
        ),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_api.router)
    app.include_router(config_api.router)
    app.include_router(qrng_api.router)
    app.include_router(experiments_api.router)

    from app.api import analysis as analysis_api
    from app.api import totp as totp_api

    app.include_router(analysis_api.router)
    app.include_router(totp_api.router)

    if settings.enable_pqc:
        from app.api import pqc as pqc_api

        app.include_router(pqc_api.router)

    return app


app = create_app()
