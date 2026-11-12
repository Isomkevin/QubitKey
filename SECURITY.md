# Security Policy

## Reporting

If you discover a vulnerability in QubitKey, please open a private security advisory or email the maintainers. Do not include secrets in public issues.

## Hosted demo

| Surface | URL |
|---|---|
| App | https://qubitkey.vercel.app |
| API | https://qubitkey-backend.onrender.com |

The public deployment is an **educational demo**, not a hardened multi-tenant service. Demo state is in-memory and resets on backend restart / cold start. See `docs/DEPLOYMENT.md` and `docs/THREAT_MODEL.md`.

## Product posture

QubitKey is an **educational prototype**:

- Not a certified entropy source.
- Not a production authentication service.
- Simulator output is not physical quantum entropy.
- TOTP is not quantum-resistant.
- QRNG is not post-quantum cryptography.

## Hard requirements for contributors

- Never commit `.env`, API tokens, TOTP secrets, or private keys.
- Never log secrets, OTPs, provisioning URIs, or private keys.
- Never silently fall back from IBM QPU execution to the simulator.
- Do not invent cryptographic algorithms; use maintained libraries only.
- Do not feed unvalidated simulator bits into cryptographic key APIs.
- Keep production CORS and `VITE_API_BASE` aligned when changing hosts.
