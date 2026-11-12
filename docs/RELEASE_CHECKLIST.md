# Release Checklist

## Fresh clone

- [ ] `cd backend && python -m venv .venv && pip install -e ".[dev]"`
- [ ] `uvicorn app.main:app --reload --port 8000`
- [ ] `cd frontend && npm install && npm run dev`
- [ ] Open `http://localhost:5173`

## Verification

- [ ] `cd backend && pytest -q` passes
- [ ] `cd frontend && npm run build` succeeds
- [ ] Quantum Lab simulator run shows provenance: not physical quantum entropy
- [ ] Observatory caveats visible
- [ ] TOTP enroll returns `Cache-Control: no-store`; verify works with authenticator app
- [ ] IBM QPU unavailable returns error (no fake success)
- [ ] Notebook `notebooks/qrng_experiment.ipynb` runs without IBM credentials

## Honesty QA

- [ ] No UI/copy labels Aer as physical quantum entropy
- [ ] TOTP not described as quantum-resistant
- [ ] Stats not described as cryptographic certification
- [ ] PQC page states ML-DSA is separate from QRNG/TOTP

## Packaging

- [ ] `.env.example` present; no secrets in git
- [ ] CI workflow green
- [ ] `docker compose up --build` optional path documented
