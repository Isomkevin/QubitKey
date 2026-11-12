# QubitKey — Master Build Brief for Cursor and Google Antigravity

## 0. Mission

Build **QubitKey**, an open-source, locally runnable quantum entropy education and authentication prototype.

The product has one primary scientific deliverable and one practical application:

1. **Primary:** a Qiskit-based Quantum Random Number Generator (QRNG) experiment, with transparent source provenance and a rigorous comparison against classical random-number sources.
2. **Application:** an authenticator demonstration that provisions and verifies TOTP secrets. In the MVP, use the operating system's cryptographically secure random source for TOTP secrets. Do not claim that simulated Qiskit output is genuine quantum entropy or use unvalidated simulator output as cryptographic key material.
3. **Stretch:** an isolated ML-DSA challenge/signature demonstration using a vetted cryptographic implementation and its approved secure randomness interface. Clearly distinguish post-quantum signatures from QRNG and TOTP.

The goal is a polished hackathon prototype that can evolve into a responsible open-source product. Prioritize a working, understandable, reproducible demonstration over feature count.

## 1. Product statement

**Name:** QubitKey (working name; check naming/trademark/repository availability before public release)

**Tagline:** Quantum Entropy. Stronger Digital Identity.

**One-line description:** An open-source quantum entropy laboratory that demonstrates Qiskit measurement, compares quantum-simulator and classical random outputs, and connects the learning experience to a practical TOTP authenticator.

**Audience:** Qiskit Fall Fest judges, quantum-computing beginners, developers, and security-minded users.

**Product principles**
- Scientific honesty over marketing claims.
- Explicitly identify simulator, QPU and classical sources.
- Local-first, privacy-conscious, no account required for the MVP.
- Reproducible experiments with visible parameters and provenance.
- Explain concepts in beginner-friendly language.
- Use established cryptographic standards and libraries; never invent cryptography.
- Every feature must have tests and an observable acceptance criterion.

## 2. Non-negotiable technical truth

Do not conflate:
- Quantum randomness with post-quantum cryptography.
- Qiskit simulator samples with genuine physical quantum entropy.
- Statistical balance with cryptographic unpredictability.
- SHA-256 hashing with a universal entropy extractor.
- TOTP with quantum-resistant authentication.

**MVP security boundary**
- Qiskit simulator: educational simulation only; never label as hardware entropy.
- IBM QPU: hardware measurement source when configured and successfully executed; do not assume it is automatically suitable as a production entropy source.
- Classical cryptographic baseline: Python `secrets` / OS CSPRNG.
- Classical educational baseline: Python `random.Random`, with fixed seed available for reproducibility.
- TOTP secret generation: OS CSPRNG (`secrets.token_bytes`) in MVP.
- TOTP: RFC 6238-compatible implementation using a maintained library.
- ML-DSA: optional separate demo using a maintained, vetted library. The library must manage randomness through its supported secure interface. Do not inject arbitrary raw Qiskit bits into ML-DSA unless a reviewed, standards-aligned entropy integration is designed and validated.

## 3. User experience and core flows

### Flow A — Explore quantum randomness
1. User opens Quantum Lab.
2. Selects source: Simulator, IBM Quantum (if configured), or Classical comparison.
3. Selects qubit count / shots within safe bounds.
4. Sees the circuit diagram, Hadamard operations, measurement, counts, bitstream sample, and generated values.
5. Sees an explicit provenance label and run metadata.
6. Can download experiment data and a JSON report.

### Flow B — Compare sources
1. User chooses sample size.
2. App generates comparable datasets using:
   - Qiskit simulator output (educational simulation).
   - Python `random` PRNG (educational comparison).
   - Python `secrets` CSPRNG (cryptographic baseline).
   - IBM QPU only when credentials and backend are configured.
3. App compares frequency, distribution, run lengths, autocorrelation and selected statistical diagnostics.
4. Every chart includes sample size and source.
5. UI states that passing basic tests does not prove cryptographic security.

### Flow C — Authenticator demo
1. User creates a local demo account label/issuer.
2. Backend creates a TOTP secret using `secrets.token_bytes`.
3. UI displays a QR enrollment code and manual setup key, with a warning to keep it private.
4. User imports it into a standards-compatible authenticator app.
5. User enters the current OTP.
6. Backend verifies using a maintained TOTP library, with a narrow clock-skew window.
7. UI explains that this is QRNG-inspired educational context, not a quantum-resistant TOTP protocol.
8. Never log secrets, OTP values, provisioning URIs, or QR payloads.

### Flow D — Optional post-quantum demo
1. Generate an ML-DSA key pair using a maintained implementation.
2. Register/store public key in a local demo session.
3. Generate a fresh server challenge with a cryptographically secure random source.
4. Sign the challenge on client/demo side.
5. Verify with public key.
6. Show algorithm, public-key fingerprint, challenge status and verification result.
7. Clearly state ML-DSA is a post-quantum signature standard; it is separate from QRNG and TOTP.

## 4. Recommended architecture

Use a monorepo:

```text
qubitkey/
├── AGENTS.md
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── .env.example
├── docker-compose.yml
├── Makefile
├── docs/
│   ├── PRODUCT_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── THREAT_MODEL.md
│   ├── EXPERIMENT_METHODOLOGY.md
│   ├── DEMO_SCRIPT.md
│   └── DECISIONS.md
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── quantum/
│   │   ├── analysis/
│   │   ├── security/
│   │   └── schemas/
│   └── tests/
├── notebooks/
│   └── qrng_experiments.ipynb
├── scripts/
└── .github/workflows/
```

### Frontend
- React + Vite.
- JavaScript preferred; do not introduce TypeScript unless a dependency or compelling engineering reason requires it.
- Tailwind CSS.
- Recharts for charts.
- Accessible components, responsive desktop-first dashboard with mobile support.
- Use a clear API client layer; no direct cryptographic logic in the browser.

### Backend
- Python 3.11+ (confirm compatibility with the selected Qiskit release).
- FastAPI + Pydantic.
- Qiskit and Qiskit Aer where compatible with the current stable release.
- IBM Quantum Runtime integration behind an optional adapter; no credentials required for simulator mode.
- NumPy, SciPy, pandas, matplotlib (notebook/export).
- PyOTP or another maintained RFC 6238 implementation.
- `qrcode` for provisioning QR creation.
- `secrets` for cryptographic secrets.
- Optional ML-DSA via a maintained library only after compatibility and API review.

### API boundary
- `GET /api/health`
- `GET /api/config`
- `POST /api/qrng/run`
- `POST /api/analysis/compare`
- `GET /api/experiments/{experiment_id}`
- `GET /api/experiments/{experiment_id}/export`
- `POST /api/auth/totp/enroll`
- `POST /api/auth/totp/verify`
- Optional:
  - `POST /api/pqc/keygen`
  - `POST /api/pqc/challenge`
  - `POST /api/pqc/verify`

Do not expose secrets in API responses except the one-time enrollment response needed for the local demo. Mark enrollment response `Cache-Control: no-store`; do not persist secrets by default. For an MVP, keep TOTP enrollment in a short-lived in-memory demo store or encrypted local store with a documented key-management limitation. Do not pretend an unprotected local database is secure.

## 5. Quantum implementation requirements

### Circuit
- `n` qubits initialized to `|0>`.
- Apply Hadamard to each qubit.
- Measure each qubit into classical bits.
- Use explicit register/bit-order handling and unit tests.
- Document Qiskit's displayed bitstring ordering; convert to integers consistently.
- For an eight-bit sample, one shot yields a value 0–255.
- For a six-sided die, do not use modulo 6 on 3-bit outcomes; use rejection sampling (discard 6 and 7) to avoid modulo bias.

### Sampler / backend
- Use current stable Qiskit API and verify it against official documentation at implementation time.
- Prefer a supported local sampler for simulator mode.
- Implement hardware execution as an adapter with explicit credential checks and backend selection.
- Do not silently fall back from QPU to simulator.
- Record source type, backend name, job ID if available, timestamp, circuit parameters, shots, Qiskit version and status.
- If hardware is unavailable, clearly disable the hardware option and explain why.

### Output model
Every run should return:
- `experiment_id`
- `source_type`: `qiskit_simulator | ibm_qpu | python_prng | python_csprng`
- `backend_name` if applicable
- `job_id` if applicable
- `shots`
- `qubits`
- `raw_counts`
- `bit_samples` (bounded preview only)
- `integer_samples` (bounded preview only)
- `created_at`
- `software_versions`
- `warnings`
- `provenance_statement`

Avoid returning huge payloads by default. Store full experiment data only when user explicitly requests export or local session retention.

## 6. Statistical analysis requirements

Implement and explain:
- Zero/one frequency.
- Frequency proportion and deviation from 0.5.
- Histogram of integer samples.
- Longest run of identical bits.
- Run-length distribution.
- Shannon entropy estimate (clearly labeled as empirical Shannon entropy).
- Lag-1 autocorrelation and optionally several lags.
- Chi-square goodness-of-fit only where assumptions and expected counts are appropriate.
- NIST SP 800-22 frequency test may be included as an educational diagnostic if implemented correctly; do not call it certification.
- Do not implement NIST SP 800-90B claims casually. Min-entropy estimation and source validation require careful methodology, sample sizes, and health tests.

For every statistic, document:
- Formula or method.
- Input sample.
- Limitations.
- Whether the statistic says anything about cryptographic security (usually not on its own).

Comparison fairness:
- Match the number of bits or samples across sources.
- Show sample size and source parameters.
- Seed `random.Random` only for repeatable educational demonstrations.
- Never seed `secrets`.
- Do not cherry-pick runs or hide unfavorable outcomes.
- Do not promise the QPU output will look statistically “better” than a CSPRNG.

## 7. Security, privacy and safety requirements

- Never log secret keys, TOTP secrets, OTP values, provisioning URIs or private keys.
- No telemetry, analytics or remote storage by default.
- Keep `.env` out of Git; include `.env.example`.
- Validate request sizes and cap shots/qubits to prevent resource exhaustion.
- Add request timeouts and clear error handling.
- Use constant-time comparison where custom secret comparison is unavoidable; prefer maintained libraries.
- Do not store TOTP secrets in browser localStorage.
- Add CSRF protections if cookie-based sessions are introduced.
- Add rate limiting to OTP verification.
- Use a narrow verification time window.
- Avoid exposing detailed verification errors that help attackers.
- Add dependency scanning and secret scanning in CI where practical.
- Include a threat model and a clear “not production certified” disclaimer.
- No custom cryptographic algorithms.

## 8. Visual and interaction design

Design language:
- Sophisticated quantum-security laboratory.
- Deep navy / near-black base, restrained electric blue and violet accents, subtle grid/particle motifs.
- Premium, clean, data-dense but readable.
- Avoid excessive gradients, neon clutter, generic AI landing-page tropes and fake terminal effects.
- Prioritize clarity and legibility.
- Responsive and keyboard accessible.

Navigation:
- Overview
- Quantum Lab
- Entropy Observatory
- Authenticator
- Post-Quantum Demo (clearly marked experimental)
- Documentation / About

Overview should show:
- Current source availability.
- Last experiment.
- Bit count.
- Source provenance.
- Key metrics.
- Clear CTA to run an experiment.

Quantum Lab should show:
- Circuit diagram (drawn from actual circuit representation, not a decorative fake).
- Parameters.
- Run controls.
- Counts / bitstream.
- Export.
- Source provenance.

Entropy Observatory should show:
- Side-by-side comparisons.
- Histograms.
- Frequency.
- Runs.
- Entropy estimates.
- Correlation.
- Caveats.

Authenticator should show:
- Enrollment form.
- QR code.
- Manual key (reveal/hide).
- OTP verification.
- Success/failure state.
- Clear note on TOTP limitations.

## 9. Notebook requirements

Create `notebooks/qrng_experiments.ipynb` with:
1. Learning objectives.
2. Install instructions.
3. Imports and environment/version display.
4. Explanation of qubits and Hadamard gate.
5. Circuit creation and visualization.
6. One-shot measurement.
7. Repeated sampling.
8. Bitstream and integer conversion.
9. Classical `random.Random` comparison.
10. `secrets` CSPRNG baseline.
11. Histograms and bit-frequency charts.
12. Longest run and empirical Shannon entropy.
13. Autocorrelation.
14. Interpretation and caveats.
15. Optional IBM QPU section that is skipped safely without credentials.
16. Reproducibility and provenance section.

The notebook must run top-to-bottom in a clean environment. It must not require IBM credentials for the default path.

## 10. Testing and acceptance criteria

### Backend
- Unit tests for circuit construction and measurement conversion.
- Test bitstring ordering.
- Test integer conversion.
- Test simulator run schema.
- Test shot/qubit limits.
- Test analysis metrics with deterministic fixtures.
- Test no silent QPU-to-simulator fallback.
- Test TOTP enrollment and valid/invalid/expired codes.
- Test that secrets are not logged.
- Test rate limiting if implemented.
- Test optional PQC flow using known-good library vectors or documented library tests.

### Frontend
- Build succeeds.
- Main routes load.
- API loading/error/empty states work.
- Charts use real API data.
- Responsive layout.
- Keyboard navigation and accessible labels.
- Authenticator QR and verification flow works.
- No secrets or OTP values appear in browser console.

### End-to-end
- Fresh clone setup documented and tested.
- `docker compose up --build` works if Docker path is included.
- Notebook runs independently.
- Full demo can be completed without IBM credentials.
- Hardware mode is opt-in and never faked.
- GitHub Actions runs lint/tests/build.

### Definition of done
A feature is not done because code was written. It is done only when:
1. It runs.
2. Tests pass.
3. Acceptance criteria are met.
4. UI is visually inspected.
5. Documentation is updated.
6. Security caveats are explicit.
7. Agent reports changed files, commands run, test results and known limitations.

## 11. AI-agent operating protocol

All agents must:
- Read `AGENTS.md`, `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md` and relevant docs before coding.
- Inspect the existing repository before proposing changes.
- Work only in assigned paths.
- Avoid editing another agent's assigned files.
- Use a separate Git branch or worktree.
- Never commit secrets or generated credentials.
- Never delete or overwrite user work without approval.
- Ask before introducing paid services, cloud infrastructure or external data storage.
- Run targeted tests after each change.
- Report assumptions and blockers rather than inventing facts.
- Keep a decision log for architecture changes.
- Never claim hardware execution unless a real IBM job ID/backend result exists.

### Suggested agent workstreams
- Agent 0 — Architect / coordinator: requirements, task graph, interfaces, integration.
- Agent 1 — Quantum engine: Qiskit circuits, simulator, hardware adapter, notebook.
- Agent 2 — Analysis: metrics, tests, comparison datasets, report schema.
- Agent 3 — Frontend: UI shell, charts, quantum lab, observatory.
- Agent 4 — Security/auth: TOTP flow, secure secret handling, optional ML-DSA research/demo.
- Agent 5 — QA/release: test plan, CI, Docker, documentation, visual QA.

For a small team, combine Agents 1+2 and Agents 4+5.

## 12. Required implementation sequence

Do not attempt all work in one giant code generation pass.

**Milestone 0 — Reconnaissance and plan**
- Inspect repo.
- Verify current stable package versions and official APIs.
- Produce architecture decisions, task graph, risks and file ownership.
- No implementation until the plan is approved.

**Milestone 1 — Backend QRNG vertical slice**
- Implement simulator circuit, output model, API, tests.
- Prove it runs without IBM credentials.

**Milestone 2 — Analysis and notebook**
- Implement metrics and comparison.
- Build runnable notebook.
- Validate scientific explanations.

**Milestone 3 — Frontend lab**
- Connect real API data.
- Add visualizations and provenance.

**Milestone 4 — TOTP demo**
- Add secure secret generation and enrollment.
- Test interoperability with an external TOTP app.
- Ensure no secrets are logged or persisted insecurely.

**Milestone 5 — Hardware adapter**
- Implement opt-in IBM QPU execution using current official APIs.
- Verify actual job metadata.
- Do not block core demo if unavailable.

**Milestone 6 — Optional ML-DSA**
- Research package support and compatibility.
- Build isolated challenge/signature demo only if time and security review permit.

**Milestone 7 — Hardening and release**
- Run all tests, browser QA, accessibility check, security review.
- Produce README, demo script, screenshots, architecture diagram and eight-slide presentation.

## 13. First instruction to the coordinator agent

Start with Milestone 0 only. Do not immediately start writing code.

Return:
1. Repository reconnaissance.
2. Confirmed toolchain and version compatibility, citing official docs or package metadata.
3. Proposed architecture and API contracts.
4. Agent/file ownership matrix.
5. Dependency and integration risks.
6. Test and acceptance plan.
7. Exact build sequence.
8. Any questions that block implementation.

After approval, implement milestone by milestone. At every milestone, run the relevant tests and report evidence.
