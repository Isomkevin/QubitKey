"""In-memory experiment store (process-local; lost on restart)."""

from __future__ import annotations

from threading import Lock
from typing import Dict

from app.schemas.experiment import ExperimentResult

_lock = Lock()
_STORE: Dict[str, ExperimentResult] = {}


def save_experiment(result: ExperimentResult) -> ExperimentResult:
    with _lock:
        _STORE[result.experiment_id] = result
    return result


def get_experiment(experiment_id: str) -> ExperimentResult | None:
    with _lock:
        return _STORE.get(experiment_id)


def clear_store() -> None:
    with _lock:
        _STORE.clear()
