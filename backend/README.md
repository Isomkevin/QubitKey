# QubitKey Backend

FastAPI service for QRNG experiments, entropy analysis, and TOTP demonstration.

## Live API

| Surface | URL |
|---|---|
| Base | https://qubitkey-backend.onrender.com |
| Health | https://qubitkey-backend.onrender.com/api/health |
| OpenAPI | https://qubitkey-backend.onrender.com/docs |
| Frontend | https://qubitkey.vercel.app |

Ops notes: [`../docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md).

## Setup

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
# Optional IBM hardware:
# pip install -e ".[dev,ibm]"
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

From the repository root you may also run:

```bash
uvicorn backend.app.main:app --reload --app-dir .
```

Prefer installing the package editable from `backend/` so imports resolve as `app.*`.

## Production start (Render)

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

CORS is controlled by `QUBITKEY_CORS_ORIGINS` (must include the Vercel origin in production).

## Tests

```bash
pytest -q
```

## Honesty

Simulator output is educational simulation, not physical quantum entropy. TOTP is not quantum-resistant. Statistical tests are not cryptographic certification.
