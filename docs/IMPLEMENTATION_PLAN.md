# QubitKey Implementation Plan

## Mission

Build a scientifically honest, secure-by-design, open-source QRNG education and TOTP demonstration. Simulator output is never presented as physical quantum entropy. TOTP is not quantum-resistant. Statistical tests are not cryptographic certification.

## Live platform

| Surface | URL |
|---|---|
| App | https://qubitkey.vercel.app |
| API | https://qubitkey-backend.onrender.com |
| Deployment guide | [`DEPLOYMENT.md`](DEPLOYMENT.md) |

## Repository status

Milestones 0–7 implemented in-repo: backend QRNG/analysis/TOTP/IBM adapter/PQC, React frontend, notebook, CI/Docker/docs, and hosted demo (Vercel + Render). See `docs/RELEASE_CHECKLIST.md` and `docs/DEMO_SCRIPT.md` for verification and judging walkthrough.

## Toolchain (pinned)

| Component | Version / choice |
|---|---|
| Python | 3.11+ (recommend 3.11–3.13) |
| `qiskit` | `~=2.6.2` |
| `qiskit-aer` | `~=0.18.2` |
| `qiskit-ibm-runtime` | `~=0.52.1` (optional extra) |
| FastAPI + Pydantic v2 | current stable |
| Frontend | React + Vite + JavaScript + Tailwind + Recharts |
| TOTP | `pyotp~=2.10` + `qrcode[pil]` |
| Analysis | NumPy, SciPy, pandas |
| ML-DSA (stretch) | `cryptography>=48` |

**Local simulator:** `qiskit_aer.primitives.SamplerV2`.

**Hardware (opt-in):** `QiskitRuntimeService` + ISA transpile + client-side Sampler. Never silently fall back to Aer.

## Target layout

```text
qubitkey/
├── AGENTS.md, README.md, LICENSE, SECURITY.md, CONTRIBUTING.md
├── .env.example, Makefile, docker-compose.yml
├── docs/
├── prompts/
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── schemas/
│   │   ├── quantum/
│   │   ├── analysis/
│   │   └── security/
│   └── tests/
├── frontend/
├── notebooks/qrng_experiments.ipynb
├── scripts/
└── .github/workflows/
```

## API surface

| Method | Path | Milestone |
|---|---|---|
| GET | `/api/health` | 1 |
| GET | `/api/config` | 1 |
| POST | `/api/qrng/run` | 1 |
| GET | `/api/experiments/{id}` | 1 |
| GET | `/api/experiments/{id}/export` | 1 |
| POST | `/api/analysis/compare` | 2 |
| POST | `/api/auth/totp/enroll` | 4 |
| POST | `/api/auth/totp/verify` | 4 |
| POST | `/api/pqc/*` | 6 (stretch) |

See [INTEGRATION_CONTRACTS.md](INTEGRATION_CONTRACTS.md) for schemas and limits.

## Milestone sequence

### Milestone 0 — Planning (this document set)

Deliverables: `IMPLEMENTATION_PLAN.md`, `AGENT_OWNERSHIP.md`, `INTEGRATION_CONTRACTS.md`, `DECISIONS.md`.

### Milestone 1 — Backend QRNG vertical slice

- Scaffold backend package, health/config, shared schemas.
- Hadamard circuit, Aer SamplerV2, conversion helpers, in-memory experiment store.
- Endpoints: `/api/qrng/run`, experiment get/export.
- Tests: circuit, bit order, integers, schema, limits, provenance.
- **Gate:** pytest green; simulator never labelled as hardware.

### Milestone 2 — Analysis and notebook

- Frequency, histogram, runs, empirical Shannon entropy, autocorrelation, caveated goodness-of-fit.
- `/api/analysis/compare` across simulator, `random.Random`, `secrets`.
- Runnable `notebooks/qrng_experiments.ipynb` without IBM credentials.
- **Gate:** fixture tests; notebook executes; caveats present.

### Milestone 3 — Frontend lab

- Overview, Quantum Lab, Entropy Observatory, Authenticator stub, About.
- Real API data, provenance badges, circuit from API, Recharts, loading/error/empty states.
- **Gate:** `npm run build`; visual inspection documented.

### Milestone 4 — TOTP demo

- OS CSPRNG secrets, PyOTP, QR, rate limit, `Cache-Control: no-store`.
- Frontend enroll/verify; no localStorage secrets.
- **Gate:** valid/invalid/window tests; external authenticator interoperability when feasible.

### Milestone 5 — IBM QPU adapter

- Optional dependency; explicit errors; job metadata; UI disables hardware when unavailable.
- **Gate:** verifiable job ID **or** documented non-execution with no-fallback tests.

### Milestone 6 — Optional ML-DSA

- Isolated challenge/sign/verify via `cryptography` ML-DSA-65.
- Clear separation from QRNG and TOTP.
- Skip if time or review blocks.

### Milestone 7 — Hardening and release

- CI, Docker Compose, README quickstart fix, threat model, methodology, demo script.
- **Gate:** fresh-clone path; full demo without IBM; honesty disclaimers present.

## Milestone operating protocol

At every milestone:

1. Run targeted tests and record commands + outcomes.
2. Inspect actual output.
3. Verify integration against contracts.
4. Update documentation.
5. Report changed files, outstanding issues, and limitations.

Never claim tests passed, hardware execution, or visual QA without evidence.

## Ownership and parallelism

See [AGENT_OWNERSHIP.md](AGENT_OWNERSHIP.md). One owner per file path. Shared schema changes require a decision record in [DECISIONS.md](DECISIONS.md).

## Risks (summary)

| Risk | Mitigation |
|---|---|
| Simulator marketed as hardware entropy | Forced provenance fields + UI badges |
| Silent QPU → simulator fallback | Explicit adapter errors + tests |
| Simulator bits as crypto key material | TOTP/PQC use OS CSPRNG / library RNG only |
| Secret leakage | Redacting logger, no-store, no localStorage |
| Overclaimed statistics | Methodology caveats; no NIST 800-90B claims |
| Resource exhaustion | Caps on qubits/shots/sample sizes |

## Definition of done (MVP)

- Clean install and documented startup.
- Notebook runs without IBM credentials.
- Simulator never presented as physical quantum entropy.
- TOTP uses OS CSPRNG and maintained RFC 6238 library.
- No secrets in browser localStorage or logs.
- Statistical limitations documented.
- Core paths tested; CI green.
- Flows A–C work without IBM; Flow D optional.
