"""Experiment retrieve and export."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.core.limits import PREVIEW_SAMPLE_LIMIT
from app.quantum.store import get_experiment
from app.schemas.experiment import ExperimentResult

router = APIRouter(tags=["experiments"])


@router.get("/api/experiments/{experiment_id}", response_model=ExperimentResult)
def get_experiment_endpoint(experiment_id: str) -> ExperimentResult:
    result = get_experiment(experiment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return result.preview(PREVIEW_SAMPLE_LIMIT)


@router.get("/api/experiments/{experiment_id}/export")
def export_experiment(experiment_id: str) -> Response:
    result = get_experiment(experiment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    payload = result.model_dump(mode="json")
    body = json.dumps(payload, indent=2)
    filename = f"qubitkey-{experiment_id}.json"
    return Response(
        content=body,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
