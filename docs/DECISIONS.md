# QubitKey Architecture Decision Records

## ADR-001: Repository layout

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** README sketched a flatter `backend/api/` and `authentication/` layout; MASTER_BUILD_PROMPT and ARCHITECTURE specify `backend/app/` with `security/`.
- **Decision:** Use `backend/app/` with packages `core`, `api`, `schemas`, `quantum`, `analysis`, `security`. Notebook name: `notebooks/qrng_experiments.ipynb`. ASGI entry: `backend.app.main:app`.
- **Consequences:** README quickstart must be updated (Milestone 7 or when scaffold lands). Agents follow MASTER layout.

## ADR-002: Local simulator primitive

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Need a supported local sampling path compatible with Qiskit 2.x.
- **Decision:** Use `qiskit_aer.primitives.SamplerV2` as the `qiskit_simulator` adapter. Pin `qiskit~=2.6.2` and `qiskit-aer~=0.18.2`.
- **Consequences:** Aer is a required MVP dependency. Aer is in reduced maintenance; pin known-good versions and prefer primitives over legacy backends.

## ADR-003: IBM hardware adapter isolation

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** IBM Quantum Runtime APIs evolved (client-side Sampler in `qiskit-ibm-runtime` 0.50+). Silent simulator fallback would falsify provenance.
- **Decision:** Optional extra `qiskit-ibm-runtime~=0.52.1`. Hardware path uses Runtime service + ISA transpile + Sampler. On failure or missing credentials: disable `ibm_qpu` in `/api/config` and return explicit errors. **Never** fall back to Aer while labelling the result as QPU.
- **Consequences:** Core demo works without IBM credentials. Milestone 5 may document non-execution if no real job is run.

## ADR-004: Bitstring endianness

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Qiskit displays bitstrings with qubit 0 as the rightmost bit; incorrect conversion biases integers.
- **Decision:** Standardize on little-endian qubit-0-rightmost. Expose `bit_order` on every experiment. Unit-test conversion. For non-power-of-two ranges (e.g. die), use rejection sampling — never biased modulo.
- **Consequences:** Frontend and analysis must not reinterpret bit order independently.

## ADR-005: Experiment and TOTP storage

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** MVP is local-first with no accounts; durable secret storage would imply false security.
- **Decision:** In-process memory stores for experiments and TOTP enrollments. TOTP TTL ≈ 30 minutes. Document loss on restart. Enrollment responses use `Cache-Control: no-store`.
- **Consequences:** Not multi-worker safe; not production. Acceptable for hackathon/education prototype.

## ADR-006: TOTP secret generation

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Product must not use unvalidated simulator bits as cryptographic key material.
- **Decision:** Generate TOTP secrets with OS CSPRNG (`secrets.token_bytes` / library-equivalent). Implement RFC 6238 via `pyotp`. QR via `qrcode[pil]`.
- **Consequences:** Authenticator is “QRNG-inspired educational context,” not quantum-derived secrets in MVP.

## ADR-007: ML-DSA library (stretch)

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Optional post-quantum demo needs a maintained implementation with secure randomness interface.
- **Decision:** Prefer `cryptography>=48` ML-DSA-65 (`MLDSA65PrivateKey.generate()`). Keep `/api/pqc/*` isolated. Do not inject Qiskit bits into signing APIs.
- **Consequences:** Clear messaging that PQC ≠ QRNG ≠ TOTP. Feature may be skipped if blocked.

## ADR-008: Frontend language

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** MASTER prefers JavaScript unless TypeScript is justified.
- **Decision:** React + Vite + JavaScript + Tailwind + Recharts. No TypeScript in MVP.
- **Consequences:** Agents must not introduce TS without a new ADR.

## ADR-009: Analysis honesty

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Statistical diagnostics are easily oversold as security proofs.
- **Decision:** Implement educational metrics only. Label empirical Shannon entropy as empirical. No NIST SP 800-90B min-entropy certification claims. Every compare response includes caveats.
- **Consequences:** UI and methodology docs must repeat limitations.

## ADR-010: Schema ownership

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Parallel agents need stable contracts.
- **Decision:** Coordinator owns `backend/app/schemas/` and `docs/INTEGRATION_CONTRACTS.md`. Domain agents import models; field changes require ADR + contract update before implementation.
- **Consequences:** Slight coordination overhead; fewer integration breakages.

## ADR-011: Hosted demo platforms

- **Status:** Accepted
- **Date:** 2026-11-13
- **Context:** Judges need a zero-install path; local-only demos risk environment friction during a timed review.
- **Decision:** Deploy the React SPA to **Vercel** (`https://qubitkey.vercel.app`, root `frontend`, `VITE_API_BASE` at build time) and the FastAPI service to **Render** (`https://qubitkey-backend.onrender.com`, free plan, Frankfurt). Document CORS, cold starts, and ops in `docs/DEPLOYMENT.md`. Keep in-memory demo stores; do not add paid datastores without an explicit product decision.
- **Consequences:** Public demo URLs become part of the README and demo script. Free Render cold starts must be called out. Hosting does not change scientific honesty requirements.
