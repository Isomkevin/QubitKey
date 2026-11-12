# QubitKey Demo Script (~8 minutes)

For AstraCode Qiskit Fall Fest 2026 judging.

## Live demo (preferred for judges)

| Surface | URL |
|---|---|
| App | https://qubitkey.vercel.app |
| API health | https://qubitkey-backend.onrender.com/api/health |
| OpenAPI | https://qubitkey-backend.onrender.com/docs |

**Cold start:** If the Overview page shows a temporary fetch error, wait ~30–60 seconds and refresh — the free Render API may be waking up. No IBM credentials are required for the core demo.

## Local fallback (optional)

```bash
# Terminal 1 — backend
cd backend && .venv/Scripts/activate   # or: source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend
cd frontend && npm install && npm run dev
```

Open http://localhost:5173

---

## Script

### 1. Overview (1 min)

Open https://qubitkey.vercel.app

- Show source availability (Aer / PRNG / CSPRNG; IBM QPU unavailable without credentials).
- Point at the scientific disclaimers.
- State clearly: **simulator ≠ physical quantum entropy**; **TOTP ≠ quantum-resistant**.

### 2. Quantum Lab (2 min)

- Source: `qiskit_simulator`
- Settings: **4 qubits**, **256 shots**, seed **7** (reproducible educational run)
- Run the experiment.
- Show: circuit drawing, measurement counts, provenance badge (**not physical quantum entropy**).

### 3. Entropy Observatory (2 min)

- Compare simulator / PRNG / CSPRNG at equal sample size.
- Highlight distribution / entropy / run visuals as educational diagnostics.
- Caveat aloud: **statistical tests ≠ cryptographic proof or entropy certification**.

### 4. Authenticator (2 min)

- Enroll `demo@local` (or similar).
- Show QR / manual key provisioning.
- Verify a live OTP from an authenticator app.
- Emphasize: secret from OS CSPRNG (`secrets`), maintained TOTP library, **no localStorage** of secrets.

### 5. Optional hardware / PQC (1 min)

- If IBM is configured: show availability and that failures do **not** fake QPU success.
- If PQC is enabled: open Post-Quantum page and stress **ML-DSA is separate from QRNG and TOTP**.

---

## Closing line

QubitKey is a scientifically honest educational lab: quantum measurement experiments, fair classical comparisons, and a practical TOTP demo — without overclaiming cryptographic certification or post-quantum security.

## Backup talking points (if network is slow)

- Architecture: React (Vercel) → FastAPI + Qiskit Aer (Render)
- Contracts and provenance rules: `docs/INTEGRATION_CONTRACTS.md`
- Threat model: `docs/THREAT_MODEL.md`
- Standalone notebook: `notebooks/qrng_experiments.ipynb`
