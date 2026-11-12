# QubitKey Threat Model

## Scope

Local-first educational prototype: QRNG lab, entropy comparison, TOTP demo, optional ML-DSA demo. Not a production entropy service or production authenticator.

## Assets

| Asset | Sensitivity |
|---|---|
| TOTP secrets / otpauth URIs / OTP codes | High (demo) |
| ML-DSA private keys | High (demo) |
| IBM Quantum API token | High |
| Experiment bitstreams | Low–medium (educational) |
| Provenance metadata | Low |

## Trust boundaries

1. **Browser** — untrusted for secret persistence. Do not store secrets in `localStorage` / `sessionStorage`.
2. **Backend process memory** — short-lived demo store; lost on restart; not multi-tenant safe.
3. **Simulator** — educational only; not a physical entropy source.
4. **IBM QPU** — physical measurements when executed; not certified for production entropy without characterisation.
5. **OS CSPRNG** — trusted for MVP TOTP / challenge generation.

## Threats and mitigations

| Threat | Mitigation |
|---|---|
| Secret leakage via logs | Redacting logger; never log secrets/OTPs/URIs |
| Browser storage of secrets | UI and docs forbid localStorage persistence |
| OTP brute force | Rate limit + narrow time window + generic failures |
| Cache leakage of enrollment | `Cache-Control: no-store` on enroll response |
| Fake hardware results | No silent QPU→simulator fallback; require job metadata |
| Overclaimed security | Forced provenance statements and UI caveats |
| Resource exhaustion | Caps on qubits/shots/compare bits |
| Dependency compromise | Pin versions; CI scanning in release milestone |

## Explicit non-goals

- Production QRNG certification (NIST SP 800-90B)
- Multi-user accounts / durable encrypted secret storage
- Feeding simulator bits into cryptographic key APIs
- Claiming TOTP is quantum-resistant

## Residual risks

- In-memory stores are process-local and unprotected at rest.
- Demo TOTP secret is returned once to the browser (required for enrollment UX).
- Optional IBM credentials in `.env` must remain uncommitted.
