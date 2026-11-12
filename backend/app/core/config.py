"""Application settings."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.limits import (
    MAX_COMPARE_BITS,
    MAX_QUBITS,
    MAX_SHOTS,
    MIN_QUBITS,
    MIN_SHOTS,
    PREVIEW_SAMPLE_LIMIT,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "qubitkey"
    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="QUBITKEY_CORS_ORIGINS",
    )
    enable_pqc: bool = Field(default=False, alias="QUBITKEY_ENABLE_PQC")
    enable_ibm_qpu: bool = Field(default=False, alias="QUBITKEY_ENABLE_IBM_QPU")
    ibm_quantum_token: str | None = Field(default=None, alias="IBM_QUANTUM_TOKEN")
    ibm_quantum_instance: str | None = Field(default=None, alias="IBM_QUANTUM_INSTANCE")
    ibm_quantum_channel: str = Field(
        default="ibm_quantum_platform", alias="IBM_QUANTUM_CHANNEL"
    )
    ibm_quantum_backend: str | None = Field(default=None, alias="IBM_QUANTUM_BACKEND")

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def limits_dict(self) -> dict:
        return {
            "min_qubits": MIN_QUBITS,
            "max_qubits": MAX_QUBITS,
            "min_shots": MIN_SHOTS,
            "max_shots": MAX_SHOTS,
            "max_compare_bits": MAX_COMPARE_BITS,
            "preview_sample_limit": PREVIEW_SAMPLE_LIMIT,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
