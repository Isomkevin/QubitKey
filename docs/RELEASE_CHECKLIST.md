# Release Checklist

Use this before judging, demos, or tagging a release.

## Hosted platform (primary for judges)

| Check | Expected |
|---|---|
| https://qubitkey.vercel.app | App loads |
| https://qubitkey-backend.onrender.com/api/health | `{"status":"ok",...}` |
| https://qubitkey-backend.onrender.com/docs | OpenAPI UI loads |
| Overview → source availability | Aer / PRNG / CSPRNG listed; disclaimers visible |
| Quantum Lab simulator run | Provenance: not physical quantum entropy |
| Observatory | Caveats visible |
| Authenticator enroll + verify | Works; no secret in `localStorage` |
| Cold start recovery | After idle wake, first request may take 30–60s |

## Fresh local clone

- [ ] `cd backend && python -m venv .venv && pip install -e ".[dev]"`
- [ ] `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- [ ] `cd frontend && npm install && npm run dev`
- [ ] Open `http://localhost:5173`

## Verification

- [ ] `cd backend && pytest -q` passes
- [ ] `cd frontend && npm run build` succeeds
- [ ] Quantum Lab simulator run shows provenance: not physical quantum entropy
- [ ] Observatory caveats visible
- [ ] TOTP enroll returns `Cache-Control: no-store`; verify works with authenticator app
- [ ] IBM QPU unavailable returns error (no fake success / no silent simulator fallback)
- [ ] Notebook `notebooks/qrng_experiments.ipynb` runs without IBM credentials

## Honesty QA

- [ ] No UI/copy labels Aer as physical quantum entropy
- [ ] TOTP not described as quantum-resistant
- [ ] Stats not described as cryptographic certification
- [ ] PQC page states ML-DSA is separate from QRNG/TOTP
- [ ] Live demo README / docs links match current Vercel + Render URLs

## Packaging & deploy

- [ ] `.env.example` present; no secrets in git
- [ ] CI workflow green
- [ ] `docs/DEPLOYMENT.md` matches live hosts
- [ ] `QUBITKEY_CORS_ORIGINS` includes production Vercel origins
- [ ] `VITE_API_BASE` set on Vercel and baked into the production build
- [ ] `docker compose up --build` optional path documented
