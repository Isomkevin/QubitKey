# QubitKey Product & Technical Specification

## Product goal

An open-source quantum entropy learning platform with a practical TOTP authenticator demonstration — runnable locally and hosted for hackathon judging.

## Live demo (judges)

| Surface | URL |
|---|---|
| App | https://qubitkey.vercel.app |
| API | https://qubitkey-backend.onrender.com |
| Docs index | [`README.md`](README.md) |
| Demo script | [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) |

## MVP scope

1. Qiskit Hadamard-based QRNG on local Aer simulator.
2. Quantum circuit visualisation and measurement counts.
3. Fair comparison against Python `random` and `secrets`.
4. Statistical observatory with honest caveats.
5. TOTP enrollment/verification using OS CSPRNG-generated secrets.
6. Runnable Jupyter notebook.
7. Responsive React dashboard and FastAPI backend.
8. Reproducible setup, tests, CI, documentation, and **hosted demo** (Vercel + Render).

## Out of scope for MVP

- Production QRNG certification.
- Production entropy service or multi-tenant cloud accounts.
- Custom cryptographic primitives.
- Claiming TOTP is post-quantum.
- Feeding simulator output directly into cryptographic key generation.
- Blockchain identity or tokenization.

## Key user stories

- As a beginner, I can see a Hadamard circuit and understand why measurement yields a bit.
- As a learner, I can run many shots and inspect counts.
- As an investigator, I can compare simulator, PRNG and CSPRNG outputs using equal sample sizes.
- As a user, I can enroll a TOTP account and verify an OTP.
- As a judge, I can use the **hosted demo** without IBM credentials (and without a local install).
- As a reviewer, I can verify source provenance and reproduce reported statistics locally.

## Acceptance

- Hosted app and API are reachable and documented with stable URLs.
- Clean local install and startup documented.
- Notebook executes top-to-bottom without hardware credentials.
- Simulator is never represented as physical quantum entropy.
- TOTP uses OS CSPRNG and a maintained RFC 6238 library.
- No secrets are logged or stored in browser `localStorage`.
- Statistical tests have documented limitations.
- All core paths have tests.
- Demo script fits an ~8 minute judging window.
