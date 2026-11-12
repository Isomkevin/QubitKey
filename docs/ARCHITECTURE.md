# QubitKey Architecture

## Live deployment

| Layer | Host | URL |
|---|---|---|
| Frontend SPA | Vercel | https://qubitkey.vercel.app |
| Backend API | Render (Frankfurt) | https://qubitkey-backend.onrender.com |

Details: [`DEPLOYMENT.md`](DEPLOYMENT.md).

```text
  User browser
       │
       ▼
  Vercel (React/Vite static build)
       │  HTTPS + CORS
       ▼
  Render (FastAPI)
       ├── Quantum adapters (Aer simulator; optional IBM QPU)
       ├── Analysis (NumPy / SciPy / pandas)
       ├── TOTP security module (OS CSPRNG + pyotp)
       └── Optional ML-DSA demo (feature-flagged)
```

## Components

- **React/Vite frontend:** presentation, experiment controls, charts, authenticator UI.
- **FastAPI backend:** orchestration, validation, analysis, and security endpoints.
- **Quantum adapters:** local Aer simulator and optional IBM QPU adapter (no silent fallback).
- **Analysis module:** frequency, run-length, empirical entropy, and correlation diagnostics.
- **Security module:** TOTP provisioning/verification; isolated optional ML-DSA demo.
- **Notebook:** standalone educational experiment (`notebooks/`), independent of the hosted API.

## Data flow

User → React UI → FastAPI → selected source adapter → measurement samples → analysis → experiment report → UI.

Authenticator flow is separate:

User → TOTP enrollment → Python `secrets` → TOTP library → QR provisioning → user authenticator → verification.

Optional PQC flow:

Verifier creates a fresh challenge with OS CSPRNG → client signs with ML-DSA → verifier checks the signature against the registered public key.

## Trust boundaries

- Browser is untrusted for secret persistence.
- Simulator is educational and not a physical entropy source.
- QPU data is physical measurement data but requires source characterisation before production entropy claims.
- OS CSPRNG is the MVP source for TOTP secrets.
- PQC library controls key-generation randomness through supported secure interfaces.
- Hosted demo stores are in-memory and ephemeral (lost on Render restart / cold start).

## API surface

- `GET /api/health`
- `GET /api/config`
- `POST /api/qrng/run`
- `POST /api/analysis/compare`
- `GET /api/experiments/{id}`
- `GET /api/experiments/{id}/export`
- `POST /api/auth/totp/enroll`
- `POST /api/auth/totp/verify`
- Optional `/api/pqc/*` when `QUBITKEY_ENABLE_PQC=true`

All endpoints validate input, cap resource use, and avoid secret logging. Full schemas: [`INTEGRATION_CONTRACTS.md`](INTEGRATION_CONTRACTS.md).
