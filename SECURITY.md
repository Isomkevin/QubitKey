# Security Policy

## Reporting

If you discover a vulnerability in QubitKey, please open a private security advisory or email the maintainers. Do not include secrets in public issues.

## Product posture

QubitKey is an **educational prototype**:

- Not a certified entropy source.
- Not a production authentication service.
- Simulator output is not physical quantum entropy.
- TOTP is not quantum-resistant.

## Hard requirements for contributors

- Never commit `.env`, API tokens, TOTP secrets, or private keys.
- Never log secrets, OTPs, provisioning URIs, or private keys.
- Never silently fall back from IBM QPU execution to the simulator.
- Do not invent cryptographic algorithms; use maintained libraries only.
- Do not feed unvalidated simulator bits into cryptographic key APIs.

See `docs/THREAT_MODEL.md` for the full threat model.
