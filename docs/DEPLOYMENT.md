# QubitKey Deployment

Hosted for AstraCode Qiskit Fall Fest 2026 judging. Educational prototype — not a production entropy or authentication service.

## Live URLs

| Role | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://qubitkey.vercel.app |
| Backend API | Render | https://qubitkey-backend.onrender.com |
| OpenAPI | Render | https://qubitkey-backend.onrender.com/docs |
| Health | Render | https://qubitkey-backend.onrender.com/api/health |
| Research notebook (latest) | Binder | https://mybinder.org/v2/gh/Isomkevin/QubitKey/main?labpath=notebooks%2Fqrng_experiments.ipynb |
| Research notebook (pinned) | Binder | https://mybinder.org/v2/gh/Isomkevin/QubitKey/ef87d4e1390975de631c5dfc7a69f4c00d1244c2?urlpath=lab%2Ftree%2Fnotebooks%2Fqrng_experiments.ipynb |
| Source | GitHub | https://github.com/Isomkevin/QubitKey |

Binder builds from `binder/` on the chosen Git ref. Share only `mybinder.org/v2/...` launch URLs (not ephemeral `hub.*.mybinder.org/user/...` session links). Prefer the pinned commit URL for judging reproducibility.

Do **not** import the repo (or the `binder/` folder) as a separate Vercel Python project. Vercel cannot host Jupyter/Binder; that path fails with `PYTHON_ENTRYPOINT_NOT_FOUND`. Use mybinder.org for notebooks and keep the existing `qubitkey` Vercel project rooted at `frontend`.

Dashboard shortcuts (maintainers):

- Render service: `qubitkey-backend` (Frankfurt, free plan)
- Vercel project: `qubitkey` (team `kisom-projects`), root directory `frontend`
- Vercel project `binder` (if present): delete it — leftover mistaken import; not part of the hosted stack

## Topology

```text
Browser ──HTTPS──► Vercel (static Vite build)
                      │
                      │  VITE_API_BASE
                      ▼
                 Render (FastAPI + Qiskit Aer)
                      │
                      └── optional IBM Quantum Runtime (opt-in, credentials required)
```

- Frontend is a static SPA; API calls go cross-origin to Render.
- Backend binds `0.0.0.0:$PORT` (Render injects `PORT`).
- CORS allowlist includes the Vercel production origins and local Vite ports.

## Environment variables

### Backend (Render)

| Variable | Required | Notes |
|---|---|---|
| `QUBITKEY_CORS_ORIGINS` | Yes (prod) | Comma-separated origins, e.g. `https://qubitkey.vercel.app,https://qubitkey-kisom-projects.vercel.app,http://localhost:5173` |
| `QUBITKEY_ENABLE_PQC` | No | Default `false` |
| `QUBITKEY_ENABLE_IBM_QPU` | No | Default `false`; never silently falls back to simulator |
| `IBM_QUANTUM_TOKEN` | If QPU | Secret — set only in the host dashboard |
| `IBM_QUANTUM_INSTANCE` | If QPU | Optional instance / CRN |
| `IBM_QUANTUM_CHANNEL` | If QPU | Default `ibm_quantum_platform` |
| `IBM_QUANTUM_BACKEND` | If QPU | Optional preferred backend name |
| `PYTHON_VERSION` | Recommended | e.g. `3.12.8` |

### Frontend (Vercel)

| Variable | Required | Notes |
|---|---|---|
| `VITE_API_BASE` | Yes (prod) | `https://qubitkey-backend.onrender.com` — **baked in at build time** |

After changing `VITE_API_BASE`, trigger a new Vercel production deploy so the static bundle picks it up.

## Render service settings

Current direct-create configuration (also sketched in root `render.yaml`):

- **Runtime:** Python  
- **Build:** `cd backend && pip install .`  
- **Start:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`  
- **Health path (recommended):** `/api/health`  
- **Region:** Frankfurt  
- **Plan:** Free  

Free-tier behaviour:

- Spins down after ~15 minutes of inactivity.
- First request after sleep may take 30–60+ seconds.
- Suitable for hackathon demos; not for SLA-backed production.

## Vercel project settings

- **Framework:** Vite  
- **Root directory:** `frontend`  
- **Install:** `npm ci`  
- **Build:** `npm run build`  
- **Output:** `dist`  
- **SPA rewrites:** `frontend/vercel.json` → all routes to `/index.html`

## Redeploy checklist

1. Confirm GitHub `main` contains the intended commit.
2. Render auto-deploys on push when auto-deploy is enabled; or trigger a manual deploy from the dashboard.
3. Ensure `QUBITKEY_CORS_ORIGINS` includes every frontend origin you use (production + preview if needed).
4. On Vercel, confirm `VITE_API_BASE`, then redeploy production.
5. Smoke test:
   - `GET https://qubitkey-backend.onrender.com/api/health`
   - Open https://qubitkey.vercel.app → Overview loads source availability
   - Run a short simulator experiment in Quantum Lab

## Security notes for hosted demos

- No secrets in the frontend bundle except the public API base URL.
- TOTP enrollment responses use `Cache-Control: no-store`; secrets are not written to `localStorage`.
- Demo stores are in-memory and reset on Render restart / cold start.
- Do not enable IBM QPU or PQC in public demos unless credentials and feature flags are intentionally configured.
- Hosted deployment does not change the scientific posture: Aer remains educational simulation.

## Local Docker (optional)

```bash
docker compose up --build
```

See root `docker-compose.yml`. Prefer the documented local Python/Node path for development.
