# QubitKey Architecture

## Components
- React/Vite frontend: presentation, experiment controls, charts and local authenticator UI.
- FastAPI backend: orchestration, validation, analysis and security endpoints.
- Quantum adapter: local simulator and optional IBM QPU adapter.
- Analysis module: frequency, run-length, empirical entropy and correlation diagnostics.
- Security module: TOTP provisioning/verification, plus isolated optional ML-DSA demo.
- Notebook: standalone educational experiment.

## Data flow
User → React UI → FastAPI → selected source adapter → measurement samples → analysis → experiment report → UI.

Authenticator flow is separate:
User → TOTP enrollment endpoint → Python `secrets` → TOTP library → QR provisioning → user authenticator → verification endpoint.

Optional PQC flow:
Verifier creates fresh challenge with OS CSPRNG → client signs using ML-DSA library → verifier checks signature using registered public key.

## Trust boundaries
- Browser is untrusted for secret persistence.
- Simulator is educational and not a physical entropy source.
- QPU data is physical measurement data but requires source characterization before production entropy claims.
- OS CSPRNG is the MVP source for TOTP secrets.
- PQC library controls key generation randomness through supported secure interfaces.

## Suggested API
- GET `/api/health`
- GET `/api/config`
- POST `/api/qrng/run`
- POST `/api/analysis/compare`
- GET `/api/experiments/{id}`
- GET `/api/experiments/{id}/export`
- POST `/api/auth/totp/enroll`
- POST `/api/auth/totp/verify`
- Optional `/api/pqc/*`

All endpoints must validate input, cap resource use and avoid secret logging.
