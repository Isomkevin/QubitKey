# Security and Authentication Agent Prompt

Implement only `backend/app/security/` and agreed security API endpoints. Read threat model and architecture first.

MVP:
- TOTP enrollment using OS CSPRNG (`secrets.token_bytes`).
- RFC 6238-compatible maintained library.
- QR provisioning URI and QR code.
- OTP verification with narrow time window and rate limiting.
- No secret/OTP/URI logging.
- `Cache-Control: no-store` on enrollment response.
- No insecure browser persistence.
- Clearly document demo storage limitations.

Stretch:
- Research a maintained ML-DSA implementation and supported API.
- Implement a separate challenge/signature/verify flow only if dependency compatibility and secure randomness are confirmed.
- Do not invent cryptography.
- Do not feed raw Qiskit simulator output into cryptographic APIs.
- Do not call TOTP quantum-resistant.
- Keep QRNG and PQC concepts separate in code and UI.

Add tests for valid, invalid, expired OTPs, rate limits, secret redaction and challenge replay prevention. Report any unresolved security risks plainly.
